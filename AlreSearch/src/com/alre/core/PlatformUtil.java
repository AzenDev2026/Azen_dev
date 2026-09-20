package com.alre.core;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * 平台工具类：检测系统类型，返回可搜索的根路径
 */
public class PlatformUtil {

    public enum OS { WINDOWS, LINUX, MAC, UNKNOWN }

    public static OS detectOS() {
        String os = System.getProperty("os.name").toLowerCase();
        if (os.contains("win")) return OS.WINDOWS;
        if (os.contains("mac")) return OS.MAC;
        if (os.contains("nux") || os.contains("nix")) return OS.LINUX;
        return OS.UNKNOWN;
    }

    /**
     * 获取所有可搜索的根目录
     * - Windows: 遍历所有盘符 (C:\, D:\ ...)
     * - Linux/Mac: 从根目录 / 开始
     */
    public static List<File> getRoots() {
        List<File> roots = new ArrayList<>();
        OS os = detectOS();

        if (os == OS.WINDOWS) {
            File[] systemRoots = File.listRoots();
            if (systemRoots != null) {
                for (File f : systemRoots) {
                    if (f.canRead() && f.getTotalSpace() > 0) {
                        roots.add(f);
                    }
                }
            }
            // 兜底
            if (roots.isEmpty()) {
                roots.add(new File("C:\\"));
            }
        } else {
            // Linux / macOS / 其他类 Unix
            roots.add(new File("/"));
        }
        return roots;
    }

    public static String getOSName() {
        return System.getProperty("os.name") + " " + System.getProperty("os.version");
    }
}