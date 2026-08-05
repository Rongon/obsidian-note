NodeJs

# 三个重要知识点

## CommonJS (CJS) 与 ES Modules (ESM) 

- **CommonJS（旧规范）**：使用 `require()` 导入，`module.exports` 导出。它是**同步/运行时**加载的，常用于传统的 Node.js 环境（如早期的 Express 项目）。

- **ES Modules（新规范）**：使用 `import` 和 `export`。它是**异步/编译时静态解析**的，是现代浏览器和现代化构建工具（如 Vite）的基础。

- **痛点/考点**：为什么在 ESM 模块里不能直接使用 `__dirname` 和 `__filename`？

  - *标准答案*：因为 `__dirname` 是 CommonJS 注入的全局变量，而 ESM 采用的是全新的模块解析机制。在 ESM 中，必须通过 `import.meta.url` 结合 `fileURLToPath` 动态计算出来：

  ```js
  import { fileURLToPath } from 'url';
  import { dirname } from 'path';
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = dirname(__filename);
  ```

---

## Node.js 事件循环（Event Loop）与异步

- **顺序**：
  1. **同步代码**先执行。
  2. **微任务（Microtasks）**：`process.nextTick()` 拥有至高无上的特权（在 Node.js 中它比 `Promise.then` 还要快），然后是 `Promise.then` 的回调。
  3. **宏任务（Macrotasks）**：由事件循环的各个阶段执行，比如 `setTimeout`（Timers 阶段）、`setImmediate`（Check 阶段）。
- **核心细节**：理解 `setImmediate()` 和 `process.nextTick()` 的区别。`nextTick` 是在当前阶段结束、下一个阶段开始前立即执行（插队）；`setImmediate` 则是专门在 Poll 阶段之后的 Check 阶段执行（排队）。

---

## Node.js 原生支持运行 TypeScript

- **以前的痛点**：在 Node.js 里跑 TS，必须先用 `tsc` 编译成 JS，或者装 `ts-node` 等第三方臃肿包。
- **现在的红利**：最新的 Node.js 版本（v22/v23+）已经实验性支持或正式内置了无感运行 TypeScript（通过 `--experimental-strip-types` 标志）。这意味着 Node.js 正在全盘向现代高效的 DX（开发者体验）靠拢，不需要配置复杂的 `tsconfig` 也能直接跑 TS 脚本了。

---

# Node.js 事件循环（Event Loop）的 6 大阶段

```
┌───────────────────────────┐
│         1. Timers         │  <-- 执行 setTimeout 和 setInterval 的回调
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│    2. Pending Callbacks   │  <-- 执行延迟到下一个循环的 I/O 回调（如某些 TCP 错误）
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      3. Idle, Prepare     │  <-- 仅 Node.js 内部使用，可忽略
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│          4. Poll          │  <-- 核心：检索新的 I/O 事件；执行几乎所有 I/O 相关的回调
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│          5. Check         │  <-- 专门执行 setImmediate() 的回调
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│     6. Close Callbacks    │  <-- 执行关闭事件的回调（如 socket.on('close', ...)）
└─────────────┬─────────────┘
```

 重点记住这 3 个阶段：

1. **Timers 阶段**：只管 `setTimeout` 和 `setInterval`。
2. **Poll 阶段（轮询阶段）**：**事件循环的心脏**。用来处理文件读写（`fs`）、网络请求（`http`）等 I/O 回调。如果没有其他任务，事件循环会在这里**阻塞等待**新的 I/O 事件到来。
3. **Check 阶段**：只管 `setImmediate()` 的回调。

---

