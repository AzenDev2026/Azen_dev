package com.alre.ui;

import com.alre.core.FileSearcher;
import com.alre.core.PlatformUtil;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.nio.file.Path;
import java.text.SimpleDateFormat;
import java.util.Date;

public class SearchWindow extends JFrame {

    private final JTextField keywordField = new JTextField(28);
    private final JButton searchBtn = new JButton("搜索");
    private final JButton cancelBtn = new JButton("停止");
    private final JLabel statusLabel = new JLabel("就绪");
    private final DefaultTableModel tableModel;
    private final JTable resultTable;
    private final JProgressBar progressBar = new JProgressBar();

    private FileSearcher searcher;
    private int resultCount = 0;

    public SearchWindow() {
        super("AlreSearch - 文件搜索引擎");

        // ---- 顶部面板 ----
        JPanel topPanel = new JPanel(new BorderLayout(6, 6));
        topPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 6, 10));

        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 0));
        inputPanel.add(new JLabel("文件名："));
        inputPanel.add(keywordField);
        inputPanel.add(searchBtn);
        inputPanel.add(cancelBtn);

        JLabel osLabel = new JLabel("检测到系统: " + PlatformUtil.getOSName()
                + "  |  搜索根: " + PlatformUtil.getRoots());
        osLabel.setForeground(Color.GRAY);

        topPanel.add(inputPanel, BorderLayout.NORTH);
        topPanel.add(osLabel, BorderLayout.SOUTH);

        // ---- 结果表格 ----
        String[] columns = {"#", "文件名", "完整路径", "大小", "修改时间"};
        tableModel = new DefaultTableModel(columns, 0) {
            @Override public boolean isCellEditable(int r, int c) { return false; }
        };
        resultTable = new JTable(tableModel);
        resultTable.setAutoResizeMode(JTable.AUTO_RESIZE_LAST_COLUMN);
        resultTable.getColumnModel().getColumn(0).setPreferredWidth(45);
        resultTable.getColumnModel().getColumn(1).setPreferredWidth(200);
        resultTable.getColumnModel().getColumn(2).setPreferredWidth(420);
        resultTable.getColumnModel().getColumn(3).setPreferredWidth(90);
        resultTable.getColumnModel().getColumn(4).setPreferredWidth(150);

        JScrollPane scrollPane = new JScrollPane(resultTable);

        // 双击打开文件所在目录
        resultTable.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override public void mouseClicked(java.awt.event.MouseEvent e) {
                if (e.getClickCount() == 2) {
                    int row = resultTable.getSelectedRow();
                    if (row >= 0) {
                        String path = (String) tableModel.getValueAt(row, 2);
                        openInExplorer(path);
                    }
                }
            }
        });

        // ---- 底部状态栏 ----
        JPanel bottomPanel = new JPanel(new BorderLayout(6, 0));
        bottomPanel.setBorder(BorderFactory.createEmptyBorder(4, 10, 8, 10));
        progressBar.setIndeterminate(false);
        bottomPanel.add(statusLabel, BorderLayout.WEST);
        bottomPanel.add(progressBar, BorderLayout.CENTER);

        // ---- 布局 ----
        setLayout(new BorderLayout());
        add(topPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        // ---- 事件绑定 ----
        searchBtn.addActionListener(e -> startSearch());
        cancelBtn.addActionListener(e -> stopSearch());
        keywordField.addActionListener(e -> startSearch());  // 回车触发

        cancelBtn.setEnabled(false);

        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(1000, 640);
        setLocationRelativeTo(null);
    }

    private void startSearch() {
        String keyword = keywordField.getText().trim();
        if (keyword.isEmpty()) {
            JOptionPane.showMessageDialog(this, "请输入文件名关键字");
            return;
        }

        tableModel.setRowCount(0);
        resultCount = 0;
        statusLabel.setText("正在搜索: " + keyword + " ...");
        progressBar.setIndeterminate(true);
        searchBtn.setEnabled(false);
        cancelBtn.setEnabled(true);

        searcher = new FileSearcher();

        searcher.searchAsync(
                keyword,
                path -> SwingUtilities.invokeLater(() -> addResult(path)),
                total -> SwingUtilities.invokeLater(() -> {
                    progressBar.setIndeterminate(false);
                    statusLabel.setText("搜索完成，共找到 " + total + " 个文件");
                    searchBtn.setEnabled(true);
                    cancelBtn.setEnabled(false);
                })
        );
    }

    private void addResult(Path path) {
        resultCount++;
        String fileName = path.getFileName().toString();
        String fullPath = path.toAbsolutePath().toString();
        String size = "-";
        String mtime = "-";
        try {
            java.nio.file.attribute.BasicFileAttributes attrs =
                    java.nio.file.Files.readAttributes(path, java.nio.file.attribute.BasicFileAttributes.class);
            size = humanSize(attrs.size());
            mtime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
                    .format(new Date(attrs.lastModifiedTime().toMillis()));
        } catch (Exception ignored) {}

        tableModel.addRow(new Object[]{resultCount, fileName, fullPath, size, mtime});
    }

    private void stopSearch() {
        if (searcher != null) {
            searcher.cancel();
            statusLabel.setText("已停止搜索");
            progressBar.setIndeterminate(false);
            searchBtn.setEnabled(true);
            cancelBtn.setEnabled(false);
        }
    }

    private String humanSize(long bytes) {
        if (bytes < 1024) return bytes + " B";
        double kb = bytes / 1024.0;
        if (kb < 1024) return String.format("%.1f KB", kb);
        double mb = kb / 1024.0;
        if (mb < 1024) return String.format("%.1f MB", mb);
        return String.format("%.2f GB", mb / 1024.0);
    }

    private void openInExplorer(String filePath) {
        try {
            java.io.File file = new java.io.File(filePath);
            if (!file.exists()) return;
            if (Desktop.isDesktopSupported()) {
                Desktop.getDesktop().open(file.getParentFile());
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "无法打开: " + ex.getMessage());
        }
    }
}