# 已安装 MCP 服务清单

本文件由 DSH 维护（Web 端 / 桌面端共用同一份 MCP 连接记录）。

- 本文件位置：`D:\FrontEnd\GitMd\MCP.md`
- 连接存储：`C:\Users\13035\.dsh\storages\mcp_connector.json`（挂在 `DSH_HOME` 下，**不在任何 profile 目录里**，所以 Web 端和桌面端看到的是同一批服务）
- 维护约定：每次新增或删除 MCP 服务后，同步更新本文件
- 最后核对：桌面端会话，共 6 条连接，健康检查 5/5 连接器正常

## MCP 服务列表

| MCP 服务            | 一句话功能                                                   |
| ----------------- | ------------------------------------------------------- |
| Firecrawl         | 网页抓取 / 爬取 / 站内地图 / 搜索 / 结构化抽取 / 论文检索，本机自装、用自己领的 API key |
| Web to MCP        | 把浏览器里正在看的页面（HTML + 截图）传给 agent 当参考，配合 Chrome 插件用        |
| Context7          | 按库名实时拉取框架 / 库的最新官方文档与代码示例，免 key 也能用（限流较低）               |
| Chrome DevTools   | 用 CDP 驱动 Chrome：看页面结构、点元素、填表、抓网络请求与性能轨迹                 |
| 腾讯云 EdgeOne Pages | 把一段 HTML / 静态页面直接部署到 EdgeOne Pages，返回公网可访问 URL          |
| GitHub            | 操作 GitHub：仓库与分支、Issue、PR、代码搜索、发起代码评审                    |

共 6 个 MCP 服务。
