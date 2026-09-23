// UnitConverter.kt
sealed class UnitCategory {
    object Length : UnitCategory()
    object Weight : UnitCategory()
    object Temperature : UnitCategory()
    // 可以继续添加更多类别
}

fun convert(category: UnitCategory, value: Double, from: String, to: String): Double {
    return when(category) {
        is UnitCategory.Length -> { /* 长度换算逻辑 */ }
        is UnitCategory.Weight -> { /* 重量换算逻辑 */ }
        is UnitCategory.Temperature -> { /* 温度换算逻辑 */ }
        // ... 每个类别的内部换算逻辑都能贡献不少代码
    }
}

fun main() {
    println("=== 单位换算器 ===")
    while (true) {
        // 打印菜单，读取用户输入
        // 调用 convert 函数并输出结果
    }
}