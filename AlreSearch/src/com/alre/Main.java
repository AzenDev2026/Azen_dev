package com.alre;

import com.alre.ui.SearchWindow;

import javax.swing.*;

public class Main {
    public static void main(String[] args) {
        // 使用系统外观
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {}

        SwingUtilities.invokeLater(() -> new SearchWindow().setVisible(true));
    }
}