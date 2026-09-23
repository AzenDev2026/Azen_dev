package com.alre.core;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;

/**
 * 高性能文件搜索器
 */
public class FileSearcher {

    // 需要跳过的目录（可按需修改 / 留空则跳过所有）
    private static final Set<String> SKIP_DIRS = new HashSet<>(Arrays.asList(
            "node_modules", ".git", ".svn", ".idea", ".gradle",
            "__pycache__", ".cache", "$RECYCLE.BIN", "System Volume Information"
    ));

    private final ForkJoinPool pool;
    private volatile boolean cancelled = false;

    public FileSearcher() {
        // 并行度 = CPU 核心数
        this.pool = new ForkJoinPool(Math.max(2, Runtime.getRuntime().availableProcessors()));
    }

    /**
     * 异步搜索
     * @param keyword  文件名关键字（不区分大小写，支持包含匹配）
     * @param onFound  每找到一个文件回调
     * @param onDone   搜索完成回调（参数为找到的总数）
     */
    public void searchAsync(String keyword,
                            Consumer<Path> onFound,
                            Consumer<Integer> onDone) {
        cancelled = false;
        String lowerKey = keyword.toLowerCase();
        AtomicInteger count = new AtomicInteger(0);
        List<File> roots = PlatformUtil.getRoots();

        List<CompletableFuture<Void>> futures = new ArrayList<>();
        for (File root : roots) {
            futures.add(CompletableFuture.runAsync(
                    () -> scanRoot(root.toPath(), lowerKey, onFound, count),
                    pool));
        }

        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
                .whenComplete((v, ex) -> onDone.accept(count.get()));
    }

    public void cancel() {
        cancelled = true;
    }

    private void scanRoot(Path root, String lowerKey,
                          Consumer<Path> onFound, AtomicInteger count) {
        try {
            Files.walkFileTree(root, EnumSet.noneOf(FileVisitOption.class),
                    Integer.MAX_VALUE,
                    new SimpleFileVisitor<Path>() {

                        @Override
                        public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
                            if (cancelled) return FileVisitResult.TERMINATE;
                            String name = dir.getFileName() == null ? "" : dir.getFileName().toString();
                            if (SKIP_DIRS.contains(name)) {
                                return FileVisitResult.SKIP_SUBTREE;
                            }
                            // 跳过无权限目录
                            if (!dir.toFile().canRead()) {
                                return FileVisitResult.SKIP_SUBTREE;
                            }
                            return FileVisitResult.CONTINUE;
                        }

                        @Override
                        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                            if (cancelled) return FileVisitResult.TERMINATE;
                            if (!attrs.isRegularFile()) return FileVisitResult.CONTINUE;

                            String fileName = file.getFileName().toString().toLowerCase();
                            if (fileName.contains(lowerKey)) {
                                count.incrementAndGet();
                                onFound.accept(file);
                            }
                            return FileVisitResult.CONTINUE;
                        }

                        @Override
                        public FileVisitResult visitFileFailed(Path file, IOException exc) {
                            // 忽略权限错误、占用错误
                            return FileVisitResult.CONTINUE;
                        }
                    });
        } catch (IOException e) {
            // 忽略根目录不可访问
        }
    }

    public void shutdown() {
        cancelled = true;
        pool.shutdownNow();
    }
}