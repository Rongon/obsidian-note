# Agent = Model + Harness

---
## Claude Code 斜杠命令大全

### 一、会话管理

#### /clear

清空当前对话，开始一个全新的会话。

当你做完一个任务，**要切到下一个任务时**，用 /clear 可以把之前的上下文全部清掉，避免旧信息干扰新任务。

清空的对话不会丢失，后续还能通过 /resume 找回来。

![image.png](https://raw.githubusercontent.com/Rongon/obsidian-note/main/20260920090945261.png)

注意，如果你只是觉得上下文太长了、但还在做同一个任务，不要用 /clear，用接下来要讲的 /compact 更合适。

#### /compact

压缩当前对话，释放上下文空间。

Claude Code 的上下文窗口是有限的，聊着聊着就满了。一旦上下文接近上限，AI 的注意力会开始涣散，容易遗漏之前讨论过的细节，回答质量明显下降。

/compact 会把之前的对话浓缩成一份摘要，腾出空间继续工作，同时保留关键信息不丢失。压缩后的对话轮次更少了，后续每次请求发送的 token 也会减少，相当于间接帮你省钱。

![image.png](https://raw.githubusercontent.com/Rongon/obsidian-note/main/20260920091846984.png)

虽然 Claude Code 在上下文达到大约 95% 时会自动触发压缩，但我建议不要等到那时候才处理。自动压缩的时机不可控，可能正好在你实现关键逻辑的时候触发，导致一些重要细节被压缩掉。

更好的做法是在每完成一个阶段性任务后（比如调试完一个 Bug、开发完一个功能），主动执行一次 /compact，这样你可以控制保留哪些信息。

你还可以在后面加一段指令，告诉它压缩时重点保留什么。

比如你正在做 API 设计，可以这样：
```
/compact 重点保留 API 接口的设计决策和参数定义

```

![image.png](https://raw.githubusercontent.com/Rongon/obsidian-note/main/20260920091923132.png)

我的习惯是，当 /context 显示上下文用量超过 80% 时就执行一次 compact。

#### /resume

恢复之前的会话。

假如你昨天做到一半的任务今天想接着做，或者刚才 /clear 掉的对话需要回去看看，都可以用 /resume 来恢复。

直接输入后，会弹出一个会话选择器，列出你最近的所有会话，选一个就能恢复。