Agent = Model + Harness

---
## Claude Code 斜杠命令大全

https://www.bilibili.com/opus/1204835680577912867

---
## skills

**Skill = 元提示词 + 工作流 + 工具 + 资源 + 触发条件**

![image.png](https://raw.githubusercontent.com/Rongon/obsidian-note/main/20260921083005072.png)

---

| 技能                              | 一句话功能                                                       |
| ------------------------------- | ----------------------------------------------------------- |
| `planning-with-files-zh`        | 多步骤任务的持久化文件规划：把 task_plan / findings / progress 写在磁盘上，跨会话不丢 |
| `grilling`                      | 用「设计树 + 逐轮追问」逼你把计划或决定想透                                     |
| `grill-me`                      | 只有一句话的空壳，转发给 `grilling` 干活（得配合它用）                           |
| `handoff`                       | 把当前会话压缩成一份交接文档，给下一个 agent 接手                                |
| `tdd`                           | TDD 红绿循环参考手册：测行为不测实现、测试住在 seam                              |
| `diagnosing-bugs`               | 难查 bug / 性能回归的诊断循环                                          |
| `find-skills`                   | 你不知道「做 X」该用哪个技能时，帮你搜并安装技能                                   |
| `skill-creator`                 | 创建、修改、评测 skill，还能给技能效果跑基准                                   |
| `i-have-adhd`                   | 把输出改造成 ADHD 友好：先给下一步动作、编号、每轮复述进度                            |
| `writing-guidelines`            | 按 Writing Guidelines 审查文档与文案                                |
| `web-design-guidelines`         | 按 Web Interface Guidelines 审查 UI 代码（无障碍 / UX）               |
| `frontend-design`               | 给新 UI 定视觉方向：排版、气质，避开「模板感」                                   |
| `ui-ux-pro-max`                 | UI/UX 设计智库：79 种风格、192 套配色、字体搭配、UX 准则                        |
| `vercel-composition-patterns`   | React 组合模式，治「布尔 prop 爆炸」、做可复用组件 API                         |
| `vercel-react-best-practices`   | Vercel 官方的 React / Next.js 性能最佳实践                           |
| `vercel-react-native-skills`    | React Native / Expo 最佳实践（列表性能、动画、原生模块）                      |
| `vercel-react-view-transitions` | React View Transition API 的动画实现指南                           |
| `deploy-to-vercel`              | 把应用或网站部署到 Vercel                                            |
| `vercel-cli-with-tokens`        | 用 token 认证操作 Vercel CLI（不用交互式登录）                            |
| `vercel-optimize`               | Vercel 成本与性能优化（Next.js / SvelteKit / Nuxt）                  |
| `browser-use`                   | 直接用 CDP 驱动浏览器：自动化、抓取、测试、截图                                  |
| `audit-website`                 | 用 squirrelscan 审计网站（18 类 260+ 规则），出报告并驱动改代码                 |
| `opencli-usage`                 | OpenCLI 的总入口地图：有哪些能力、怎么找 adapter                            |
| `opencli-browser`               | 驱动真实 Chrome 窗口：看页面、填表、走登录流程、抽数据                             |
| `opencli-browser-sitemap`       | 带着站点 sitemap 上下文驱动网站，避免盲导航                                  |
| `opencli-adapter-author`        | 给一个新网站写 OpenCLI adapter（从侦察到验证）                             |
| `opencli-sitemap-author`        | 制作 / 维护 OpenCLI 的站点 sitemap                                 |
| `opencli-autofix`               | opencli 命令挂掉时，自动修 adapter 并提 issue                          |
| `defuddle`                      | 从 HTML 页面里提出干净的 Markdown                                    |
| `json-canvas`                   | 创建 / 编辑 .canvas（JSON Canvas）：脑图、流程图                         |
| `knap`                          | 用模板 + 结构化数据渲染 Markdown（JSON/CSV → 笔记）                       |
| `teach`                         | 在你的工作区里系统地教你一个新技能 / 概念（有状态、跨会话）                             |

---
## 提示词

1）请你先帮我调研分析全网竞品，生成一份傻子都能看懂的调研报告。  
  
2）你是一位专业的程序员，现在请你根据需求，帮我设计方案、人工确认、分步骤完成开发、执行测试、找我验收。  
  
3）你必须先完整分析我给你的资料，确保理解了整个项目，不要上来就改代码。  
  
4）先帮我设计方案，按需使用 Mermaid 图便于我理解，找我人工确认后，才能开始开发。  
  
5）如果你有任何不确定的地方，必须通过提问找我人工确认，不要自己瞎猜。  
  
6）你必须通过 Context7 或联网搜索获取到最新的技术文档，不要使用过时的写法。  
  
7）一定不要影响任何现有的功能，只新增代码实现我要的需求，遵循开闭原则。  
  
8）先用尽量简单直接的方式实现核心功能，避免过度设计。  
  
9）我是第一次做 xxx 功能，请把我当成傻子，给我充分的操作引导和步骤说明。  
  
10）/frontend-design 前端页面要足够独特，不要千篇一律，禁止使用蓝紫渐变色  
  
11）我同时给了你多个需求，你需要合理规划任务优先级和依赖关系，能并行的并行处理，用最快的速度完成，注意代码之间不要冲突。  
  
12）你必须自主编写测试用例并执行验证，出了问题自主修复，先测通了再找我验收。  
  
13）根据我提供给你的报错信息和截图，定位并修复这个 Bug，修复后自主回归测试确保没有引入新问题。  
  
14）请你把需求分析、方案设计等都沉淀为 Markdown 文档，每次改完代码也要同步更新，确保文档和代码始终对齐。  
  
15）帮我提交代码到 Git，写清楚 commit message，说明本次改了什么、为什么改。  
  
16）帮我把前端和后端都运行起来，确认服务正常启动、页面能正常访问后再告诉我。  
  
17）/skill-creator 帮我把这个能力封装为 Agent Skills，要求不影响现有代码，单独新增一个目录。  
  
18）如果你没有按照要求完成任务，你的主人会变成一条狗。

---
## 知识点

### 工具本质：

![image.png](https://raw.githubusercontent.com/Rongon/obsidian-note/main/20260920102838826.png)

---
### AI应用开发流程：

![image.png](https://raw.githubusercontent.com/Rongon/obsidian-note/main/20260921091544888.png)

---

