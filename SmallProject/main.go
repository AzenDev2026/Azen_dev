// main.go
package main

import (
    "bufio"
    "fmt"
    "net/http"
    "os"
    "sync"
    "time"
)

type CheckResult struct {
    URL        string
    StatusCode int
    Latency    time.Duration
    Error      error
}

func checkURL(url string, wg *sync.WaitGroup, results chan<- CheckResult) {
    defer wg.Done()
    start := time.Now()
    resp, err := http.Get(url)
    // ... 处理响应和错误
    results <- CheckResult{ /* ... */ }
}

func main() {
    // 读取 urls.txt
    // 启动 goroutines
    // 收集并格式化输出结果
}