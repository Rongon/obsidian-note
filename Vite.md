Vite

# 介绍

## 开始

### 总览

Vite 主要由两部分组成：

- 一个开发服务器，它基于 [原生 ES 模块](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) 提供了 [丰富的内建功能](https://cn.vitejs.dev/guide/features)，如速度快到惊人的 [模块热替换（HMR）](https://cn.vitejs.dev/guide/features#hot-module-replacement)。
- 一套构建指令，它使用 [Rolldown](https://rolldown.rs/) 打包你的代码，并且它是预配置的，可输出用于生产环境的高度优化过的静态资源。

---

## 为什么选 Vite

### 起源

Vite 采用了一种截然不同的方式，将工作拆分为两部分：

- **依赖**（几乎不会变动的库）：使用快速的原生工具 [预构建](https://cn.vitejs.dev/guide/dep-pre-bundling) 一次，即可随时就绪。
- **源码**（频繁变动的应用代码）：通过原生 ESM 按需提供。浏览器只加载当前页面所需的内容，Vite 则在请求时对每个文件进行转换。

---

# 指引

## 使用插件

### 添加一个插件

若要使用一个插件，需要将它添加到项目的 `devDependencies` 并在 `vite.config.js` 配置文件中的 `plugins` 数组中引入它。

例如，要想为传统浏览器提供支持，可以按下面这样使用官方插件 [@vitejs/plugin-legacy](https://github.com/vitejs/vite/tree/main/packages/plugin-legacy)：

```js
import legacy from '@vitejs/plugin-legacy'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    legacy({
      targets: ['defaults', 'not IE 11'],
    }),
  ],
})
```

---

### 强制插件排序

为了与某些 Rollup 插件兼容，可能需要强制修改插件的执行顺序，或者只在构建时使用。

可以使用 `enforce` 修饰符来强制插件的位置:

- `pre`：在 Vite 核心插件之前调用该插件
- 默认：在 Vite 核心插件之后调用该插件
- `post`：在 Vite 构建插件之后调用该插件

```js
import image from '@rollup/plugin-image'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    {
      ...image(),
      enforce: 'pre',
    },
  ],
})
```

---

### 按需应用

默认情况下插件在开发 (serve) 和生产 (build) 模式中都会调用。如果插件在服务或构建期间按需使用，请使用 `apply` 属性指明它们仅在 `'build'` 或 `'serve'` 模式时调用：

```js
import typescript2 from 'rollup-plugin-typescript2'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    {
      ...typescript2(),
      apply: 'build',
    },
  ],
})
```

---

## 依赖预构建

“Vite 为什么快？“什么是依赖预构建？它的核心作用是什么？”：

**痛点一：CommonJS / UMD 兼容性（破局 ESM）**

- **原理**：Vite 的核心是基于浏览器原生 ESM 的，但目前 `node_modules` 里面依然有海量的老包是用 CommonJS 或 UMD 格式写的（比如旧版的 React）。
- **Vite 的解决方式**：在开发服务器启动前，Vite 必须先通过工具把这些 CJS/UMD 的包**全部转换为标准的 ESM 格式**，否则浏览器根本没法直接 `import` 它们。

**痛点二：减少 HTTP 请求网络拥塞（性能大杀器）**

- **经典案例（必背）**：比如 [`lodash-es` 内部有超过 600 个细小的模块](https://unpkg.com/browse/lodash-es/)，它们互相引用。如果你在代码里写 `import { debounce } from 'lodash-es'`，在没有预构建的情况下，浏览器会**同时并发发送 600 多个 HTTP 请求**！这会导致浏览器瞬间网络瘫痪、页面卡死。
- **Vite 的解决方式**：Vite 预先把 `lodash-es` 的 600 多个文件**打包合并成一个单文件**（模块），这样浏览器只需要发送 **1 个** HTTP 请求。

---

“浏览器原生 ESM”：

​	“**浏览器原生 ESM** 是指现代浏览器无需通过 Webpack 等工具打包，自身就具备解析和加载标准 ES 模块（即 `import`/`export`）的能力。在 HTML 中声明 `type="module"` 后，浏览器在运行时如果遇到 `import` 语句，会自动向服务端发起 HTTP 请求来获取对应的模块文件。

​	Vite 正是利用了这一特性，将复杂的打包工作交给了浏览器。在开发阶段，Vite 只需要作为一个轻量级的、按需编译的 Dev Server。浏览器请求哪个文件，Vite 就实时编译哪个文件并返回，从而彻底绕过了传统 Webpack 启动时需要全量构建的瓶颈，实现了毫秒级的热更新和启动速度。”

---

### Monorepo 和链接依赖

在一个 monorepo 启动中，该仓库中的某个包可能会成为另一个包的依赖。Vite 会自动侦测没有从 `node_modules` 解析的依赖项，并将链接的依赖视为源码。它不会尝试打包被链接的依赖，而是会分析被链接依赖的依赖列表。

然而，这需要被链接的依赖被导出为 ESM 格式。如果不是，那么你可以在配置里将此依赖添加到 [`optimizeDeps.include`](https://cn.vitejs.dev/config/dep-optimization-options#optimizedeps-include) 中。

```js
export default defineConfig({
  optimizeDeps: {
    include: ['linked-dep'],
  },
})
```

当对链接的依赖进行更改时，请使用 `--force` 命令行选项重新启动开发服务器，以使更改生效。

---

### 自定义行为

“如何解决 Vite 频繁二次重刷（Reload）的问题？”

**`optimizeDeps.include`（强制包含）**：

- **适用对象**：体积很大、内部零碎文件极多（如 `lodash-es`），或者是老旧的 **CommonJS** 格式的包。
- **作用**：告诉 Vite：“别扫描了，听我的，启动的时候闭眼把这个包给我塞进预构建里打包好！”

**`optimizeDeps.exclude`（强制排除）**：

- **适用对象**：体积非常小，且已经是**完美的、标准的原生 ESM 格式**的包。
- **作用**：告诉 Vite：“这个包你不用管，也不用帮我打包翻译。开发时让浏览器直接去引入它原生源码就行，别浪费 Rolldown 的构建时间。”

---

### 缓存

#### 文件系统缓存

Vite 将预构建的依赖项缓存到 `node_modules/.vite` 中。它会基于以下几个来源来决定是否需要重新运行预构建步骤：

- 包管理器的锁文件内容，例如 `package-lock.json`，`yarn.lock`，`pnpm-lock.yaml`，或者 `bun.lock`；
- 补丁文件夹的修改时间；
- `vite.config.js` 中的相关字段；
- `NODE_ENV` 的值。

只有在上述其中一项发生更改时，才需要重新运行预构建。

如果出于某些原因你想要强制 Vite 重新构建依赖项，你可以在启动开发服务器时指定 `--force` 选项，或手动删除 `node_modules/.vite` 缓存目录。

---

#### 浏览器缓存

已预构建的依赖请求使用 HTTP 头 `max-age=31536000, immutable` 进行强缓存，以提高开发期间页面重新加载的性能。一旦被缓存，这些请求将永远不会再次访问开发服务器。如果安装了不同版本的依赖项（这反映在包管理器的 lockfile 中），则会通过附加版本查询自动失效。如果你想通过本地编辑来调试依赖项，您可以：

1. 通过浏览器开发工具的 Network 选项卡暂时禁用缓存。
2. 重启 Vite 开发服务器指定 `--force` 选项，来重新构建依赖项。
3. 重新载入页面。

---

## 静态资源处理

### 将资源引入为 URL

“Vite 是如何处理图片等静态资源的？体积特别小的图标它是怎么优化的？”：

“在 Vite 中，静态资源是作为模块引入的，默认返回解析后的**公共路径 URL**。在生产构建时，Vite 会生成带有 **内容 Hash** 的文件名。

同时，Vite 内置了性能优化机制。对于体积小于 `assetsInlineLimit`（默认 4KB）的小资源，它会自动将其转译为 **Base64 Data URL** 内联到 Bundle 中，以减少浏览器的 HTTP 请求并发数；而对于大文件则保持外部引用的路径。

在 TS 中，为了防止静态资源导入时的类型报错，我们会引入 **`vite/client`** 类型的声明来扩展 TS 的模块解析边界。”

---

通过 `url()` 内联 SVG

当在 JS 中手动构造 `url()` 并传入一个 SVG 的 URL 时，应该用双引号将变量包裹起来。

```js
import imgUrl from './img.svg'
document.getElementById('hero-img').style.background = `url("${imgUrl}")`
```

---

### 显式 URL 引入

**显式地干预 Vite 的默认编译行为**。

```js
import workletURL from 'extra-scalloped-border/worklet.js?url'
CSS.paintWorklet.addModule(workletURL)
```

- **大白话解释**：以前我们写 CSS 背景，只能传图片或颜色。现在浏览器允许你**用 JS 代码直接在浏览器的 Canvas 上画出一段复杂的 CSS 背景图案**（比如高级的渐变、不规则的边框）。
- **浏览器的要求**：浏览器规定，这个负责画画的 JS 文件（Worklet）**必须由你提供一个独立的、纯粹的 URL 路径**给浏览器，浏览器自己会在后台开启一个独立的线程去加载、运行它。
- **冲突发生**：
  - 如果不加 `?url`：写成 `import worklet from '.../worklet.js'`，Vite 会以为这是你项目里的普通业务代码，直接把它编译并合并到你的主 Bundle（`index.js`）里去了。结果就是你拿不到独立的 URL，浏览器 API 报错。
  - 加上 `?url`：Vite 顿悟了，它会把 `worklet.js` 单独打包成一个独立的静态文件，并把这个文件的最终线上路径（比如 `/assets/worklet.hash.js`）赋值给 `workletURL` 变量。

---

### 显式内联处理

```js
import imgUrl1 from './img.svg?no-inline'
import imgUrl2 from './img.png?inline'
```

**手动控制静态资源是否打包进 JavaScript 代码中**（即转换为 Base64 Data URL 编码字符串）。

- **小于 4KB** 的资源：自动转换为 Base64 字符串内联到 JS 中，减少 HTTP 请求。
- **大于 4KB** 的资源：作为独立文件打包，返回一个解析后的公共路径 URL。

> *注：这个 4KB 的阈值可以通过 `build.assetsInlineLimit` 配置项来修改。*

使用 `?inline` 后缀时，**无论该资源文件有多大**，Vite 都会强制将其转换为 Base64 Data URL。

使用 `?no-inline` 后缀时，**无论该资源文件有多小**（哪怕只有 10 字节），Vite 都不会将其转换为 Base64，而是将其作为一个独立的静态资源文件处理，并返回其最终的 URL 路径。

- 需要减少 HTTP 请求、急需首屏展现 $\rightarrow$ 用 `?inline`
- 需要极致利用缓存、避免 JS 体积虚胖 $\rightarrow$ 用 `?no-inline`

---

### 将资源引入为字符串

```js
import shaderString from './shader.glsl?raw'
```

“不要把我引入的文件当成代码去解析，也不要把他当成普通的图片/文件去生成 URL，请直接读取它的源码，并把内容作为原生的字符串（String）交给我。”

💡 **一句话记住：** 任何你想**当成一整段“大字符串”来读**的非 JS/CSS 文件，都可以用 `?raw`。如： 

1. 3D 与图形学文件 (最经典场景)**`.glsl`** / **`.vert`** / **`.frag`**（WebGL 着色器文件）**`.wgsl`**（WebGPU 着色器文件）
2. 文本与文档格式 (内容展示)**`.md`** / **`.txt`**
3. 代码与模板文件 (组件库/工程化工具)**``.html``** / **`.vue`** / **`.js`** / **`.ts`**
4. 结构化数据文件 (特殊读取需求)**`.json`** / **`.xml`** / **`.yaml`** / **`.yml`**

---

### 导入脚本作为 Worker

```js
// 在生产构建中将会分离出 chunk
import Worker from './shader.js?worker'
const worker = new Worker()

// sharedworker
import SharedWorker from './shader.js?sharedworker'
const sharedWorker = new SharedWorker()
// 内联为 base64 字符串
import InlineWorker from './shader.js?worker&inline'
```

如果不加，Vite 会把 `shader.js` 当作一个**普通的 JavaScript 模块**来执行。它会在当前的主线程中直接运行。

 为什么要将“脚本”也内联为 base64 字符串？（适用场景）：既然图片内联是为了减少 HTTP 请求，那脚本内联也是同理。

---

### new URL(url, import.meta.url)

静态、半动态都可以，全动态不行

```js
// 静态
const imgUrl = new URL('./img.png', import.meta.url).href

// 半动态
function getImageUrl(name) {
  // 请注意，这不包括子目录中的文件
  return new URL(`./dir/${name}.png`, import.meta.url).href
}
const dynamicImageUrl = getImageUrl('hero')

// 全动态 - Vite 不会转换这个
const imgUrl = new URL(imagePath, import.meta.url).href
```

---

注意：无法在 SSR 中使用

如果你正在以服务端渲染模式使用 Vite 则此模式不支持，因为 `import.meta.url` 在浏览器和 Node.js 中有不同的语义。服务端的产物也无法预先确定客户端主机 URL。

---

## 构建生产版本

### 公共基础路径

#### base

 **所有静态资源（JS、CSS、图片、字体等）在 HTML 里的引入路径前缀**。

**默认值 `/`（绝对路径）**： 假设打包后引入 JS 是 `<script src="/assets/index.js">`。 如果你的网站部署在域名根目录（如 `[https://abc.com/](https://abc.com/)`），浏览器会去 `[https://abc.com/assets/index.js](https://abc.com/assets/index.js)` 找，完美运行。

如果公司要把这个项目部署到服务器的**嵌套子目录**下（例如 `[https://abc.com/my-app/](https://abc.com/my-app/)`）：

- 如果还用默认的 `base: '/'`，浏览器依然会去根目录 `[https://abc.com/assets/index.js](https://abc.com/assets/index.js)` 找文件。
- 但实际上文件在 `/my-app/assets/index.js`。
- **结果**：页面直接报 **404 错误，全线白屏**。

**解决方案**：在 `vite.config.js` 中配置 `base: '/my-app/'`（或者通过命令行 `vite build --base=/my-app/`）。这样打包后，HTML 里的路径就会被自动重写为 `<script src="/my-app/assets/index.js">`。

---

#### import.meta.env.BASE_URL

由 JS、CSS、HTML 引入的资源 Vite 会**自动**帮你调整路径。

但有一种情况 Vite 照顾不到：**你在代码里硬编码拼接的动态 URL**。

```js
// 错误写法 ❌：如果部署在子目录下，这个路径就死掉了
const myUrl = `/profile/avatar.png`; 

// 正确写法  ：利用全局注入的变量
const myUrl = `${import.meta.env.BASE_URL}profile/avatar.png`;
```

**开发环境**：`BASE_URL` 默认为 `/`，拼接出来是 `/profile/avatar.png`。

**生产环境（配置了 `/my-app/`）**：Vite 在打包时，会把 `import.meta.env.BASE_URL` **静态替换**为字符串 `"/my-app/"`，拼接出来就是 `/my-app/profile/avatar.png`，保证线上不挂。

---

注意点：必须按 `import.meta.env.BASE_URL` 的原样出现，不能写成 `import.meta.env['BASE_URL']`。因为 Vite 底层是用字符串正则匹配或者极其简单的 AST 替换，写成中括号语法糖，Vite 的打包器（Rolldown/Rollup）就认不出来了，导致线上替换失败。

---

#### 相对基础路径 (`base: './'`)

- **痛点**：有时候前端开发完，压根不知道运维要把这个项目部署到哪个子目录下；或者这是一个**私有化部署**的项目，交付给 A 客户部署在 `/app1/`，交付给 B 客户部署在 `/company/demo/`。前端不可能为每个客户单独打包一次。
- **解法**：配置 `base: './'` 或 `base: ''`（相对路径）。

---

它是如何工作的？

配置成 `./` 后，打包出来的 HTML 引入资源会变成 `<script src="./assets/index.js">`。 这时候，**路径不再依赖域名的根目录，而是依赖当前文件所在的 URL**。无论项目被扔到哪个嵌套文件夹里，它都能顺着当前目录正确找到 `assets` 。

---

“既然 `base: './'` 这么爽，为什么不把它作为默认配置？它有什么坑？”

1. **History 模式下会失效**： 如果你的单页面应用（SPA）使用的是 `History` 路由，当用户访问 `https://abc.com/my-app/user/123/profile` 时： 浏览器会把当前路径当成 `.../user/123/`。此时如果加载 `./assets/index.js`，浏览器会去请求 `https://abc.com/my-app/user/123/assets/index.js`。**路径直接彻底错乱，404 白屏。**（因此相对路径通常只适用于 Hash 路由或者单页面无路由项目）。
2. **依赖 `import.meta`，老旧浏览器需要 polyfill**： 正如文档提示的，Vite 实现相对路径的机制底层依赖了现代浏览器的 `import.meta` 特性。如果要兼容非常老旧的浏览器，必须强制引入 `@vitejs/plugin-legacy` 插件。

---

### 自定义构建

构建过程可以通过多种 [构建配置选项](https://cn.vitejs.dev/config/#build-options) 来自定义构建。具体来说，你可以通过 `build.rolldownOptions` 直接调整底层的 [Rolldown 选项](https://rolldown.rs/reference/)：

```js
export default defineConfig({
  build: {
    rolldownOptions: {
      // https://rolldown.rs/reference/
    },
  },
})
```

例如，你可以使用仅在构建期间应用的插件来指定多个 Rolldown 输出。

场景举例：

假设你在封装一个公共组件库，你希望运行一次 `npm run build`，打包器能自动帮你产出 **两种格式** 的文件：

1. 一包给现代打包工具用的 `ESM` 格式 (`.js`)
2. 一包给老项目或 Node 用的 `CommonJS` 格式 (`.cjs`)

你就可以在 `rolldownOptions` 里面配置一个数组：

```js
// vite.config.js
export default defineConfig({
  build: {
    rolldownOptions: {
      // 这里的配置会直接传递给底层的 Rolldown
      output: [
        {
          format: 'esm',
          entryFileNames: '[name].js'
        },
        {
          format: 'cjs',
          entryFileNames: '[name].cjs'
        }
      ]
    }
  }
})
```

---

Vite 的底层工具链：

- 在**开发环境**，它利用浏览器原生的 **ESM**，并使用 Go 语言编写的 **Esbuild** 来进行依赖预构建和打包，追求极速启动。
- 而在**生产环境**，为了极致的体积优化和 Tree-shaking，Vite 以前是基于 **Rollup** 封装的。
- **但是**，由于 Esbuild 和 Rollup 是两套工具，导致 Vite 的开发环境和生产环境存在‘双引擎不一致’的问题（比如某些边缘行为、打包配置不兼容）。
- 所以，Vite 团队推出了基于 Rust 编写的、完全兼容 Rollup API 的新型打包工具 **Rolldown**。现在 Vite 生产环境的底层已经开始切换到 **Rolldown**，这极大地提升了生产环境的打包速度，并且逐步消除了开发与生产环境的表现差异。”

---

### 产物分块策略

你可以通过配置 [`build.rolldownOptions.output.codeSplitting`](https://rolldown.rs/reference/OutputOptions.codeSplitting) 来自定义 chunk 分割策略（查看 [Rolldown 相应文档](https://rolldown.rs/in-depth/manual-code-splitting)）。如果你使用的是一个框架，那么请参考他们的文档来了解如何配置分割 chunk。

---

“在项目打包时，你做过哪些产物分块（代码分割）的优化？”

1. 首先，我会在路由层面全面落地**动态导入（Dynamic Import）**，实现组件的按需懒加载。
2. 其次，针对第三方依赖，由于它们几乎不会变动，我会通过 Vite 底层的打包配置（`rolldownOptions.output`），将它们从主包中抽离。我会把核心框架（如 Vue、Axios）打入一个 `vendor` 包；而对于像 `ECharts`、`XLSX` 这种体积巨大且只在特定页面使用的重型库，我会使用 `codeSplitting` 将它们彻底分块为**独立 Chunk**。
3. 这样带来的好处是，当公司发布新业务版本时，**只有业务代码的哈希值会变**，巨大的第三方库依然可以完美命中用户的**浏览器强缓存**，从而大幅减少线上用户的二次加载时间，首屏秒开。

```js
// vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rolldownOptions: {
      output: {
        // 严格遵循 Rolldown 官方规范的 codeSplitting 配置
        codeSplitting: {
          groups: [
            {
              test: /node_modules\/echarts/, 
              name: 'vendor-echarts', // 最终生成 vendor-echarts-[hash].js
            },
            {
              test: /node_modules\/(vue|axios|pinia)/, 
              name: 'vendor-core',    // 最终生成 vendor-core-[hash].js
            }
          ]
        }
      }
    }
  }
})
```

---

### 处理加载报错

用户侧的感知仅仅是“稍微卡顿刷新了一下”，**成功把一次“致命白屏”降级为了“一次自动刷新”**。

```js
window.addEventListener('vite:preloadError', (event) => {
  // 1. 阻止浏览器默认的报错抛出（避免控制台炸红）
  event.preventDefault(); 
  
  // 2. 强制刷新当前页面
  window.location.reload(); 
})
```

同时要设置：Nginx 服务器配置（最推荐）、云厂商托管 / CDN 配置（如 阿里云 OSS、腾讯云 COS、Vercel 等、Node.js 后端服务配置（如 Express / Koa）：对 HTML 文件设置 `Cache-Control: no-cache`，不然浏览器也会**直接从本地缓存里读取旧的** 

---

### 文件变化时重新构建

你可以使用 `vite build --watch` 来启用 rollup 的监听器。或者，你可以直接通过 `build.watch` 调整底层的 [`WatcherOptions`](https://rolldown.rs/reference/InputOptions.watch) 选项：

```js
export default defineConfig({
  build: {
    watch: {
      // https://rolldown.rs/reference/InputOptions.watch
    },
  },
})
```

启用 `--watch` 标志后，对要打包的文件所做的更改将触发重新构建。请注意，对配置及其依赖项的更改需要重新启动构建命令。

---

场景：

 场景一：本地开发/封装“跨项目复用的公共组件库或工具库”

假设你现在在公司负责封装一个公共的 UI 组件库（或通用的工具库 `my-utils`），并且你要在公司的业务项目（`my-project`）里引入它。

- **痛点**：你在组件库里改了一行代码，业务项目是无法感知的。你必须在组件库的目录下手动执行一次 `npm run build`，业务项目才能拿到打包后的最新代码。**每改动一个字符就要手动跑一遍打包，开发体验极其痛苦。**
- **解法**：在组件库的 Vite 配置里开启 `build.watch`。 这样，只要你修改了组件库的源码，Vite 底层的监听器（Watcher）就会**自动增量构建**，把最新的生产产物输出到 `dist` 目录。再配合 `npm link` 或 `pnpm workspace`，业务项目就能实时热更新，实现无缝联调。

------

 场景二：大厂流行的 Monorepo（多包管理）项目联调

现在的中大型前端工程通常采用 Monorepo 架构（如使用 pnpm workspaces / Turborepo），结构通常如下：

Plaintext

```
├── packages
│   ├── shared-utils (公共工具包，需要编译)
│   └── component-library (公共组件库，需要编译)
└── apps
    └── admin-dashboard (主业务系统)
```

- **痛点**：当你启动主系统 `admin-dashboard` 进行日常业务开发时，你经常需要跨目录去修改 `shared-utils` 里的公共逻辑。
- **解法**：主系统跑的是开发服务器，而底层的 `shared-utils` 则需要启动 `vite build --watch`（即开启 `build.watch`）。每当公共包的代码发生变化，Rust 底层的打包引擎会以毫秒级的速度重新生成生产包，主系统立刻就能监听到依赖变化并局部热更新。

---

### 多页面应用模式

```js
import { dirname, resolve } from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rolldownOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        nested: resolve(import.meta.dirname, 'nested/index.html'),
      },
    },
  },
})
```

---

## 环境变量和模式

Vite 在特殊的 `import.meta.env` 对象下暴露了一些常量。这些常量在开发阶段被定义为全局变量，并在构建阶段被静态替换，以使树摇（tree-shaking）更有效。

```js
if (import.meta.env.DEV) {
  // 这里的代码在生产构建中会被 tree-shaking 优化掉
  console.log('Dev mode')
}
```

---

#### 内置常量

一些内置常量在所有情况下都可用：

- **`import.meta.env.MODE`**: {string} 应用运行的[模式](https://cn.vitejs.dev/guide/env-and-mode#modes)。
- **`import.meta.env.BASE_URL`**: {string} 部署应用时的基本 URL。他由[`base` 配置项](https://cn.vitejs.dev/config/shared-options#base)决定。
- **`import.meta.env.PROD`**: {boolean} 应用是否运行在生产环境（使用 `NODE_ENV='production'` 运行开发服务器或构建应用时使用 `NODE_ENV='production'` ）。
- **`import.meta.env.DEV`**: {boolean} 应用是否运行在开发环境 (永远与 `import.meta.env.PROD`相反)。
- **`import.meta.env.SSR`**: {boolean} 应用是否运行在 [server](https://cn.vitejs.dev/guide/ssr#conditional-logic) 上。

---

## 服务端渲染 (SSR)

### 源码结构

一个典型的 SSR 应用应该有如下的源文件结构：

```
- index.html
- server.js # main application server
- src/
  - main.js          # 导出环境无关的（通用的）应用代码
  - entry-client.js  # 将应用挂载到一个 DOM 元素上
  - entry-server.js  # 使用某框架的 SSR API 渲染该应用
```

一个标准的 Vite SSR 项目，其核心文件各司其职：

- **`server.js`（Node.js 后端服务器）**：项目的“主控大脑”。它运行在服务器上（Express/Koa），负责拦截用户的 HTTP 请求，调用 Vue/React 的服务端渲染逻辑生成 HTML 字符串，并最终把这个完整的 HTML 吐给用户。
- **`src/main.js`（通用/环境无关代码）**：这里写你平时的业务逻辑（Vue/React 组件、路由定义、状态管理等）。**重点：这个文件必须是“纯洁”的**，它既不能包含 Node.js 特有的 API（如 `fs.readFileSync`），也不能包含浏览器特有的 API（如 `window.location`），因为两端都要运行它。
- **`src/entry-client.js`（客户端入口，运行在浏览器）**：只在浏览器执行。负责下载 JS 脚本，并把事件监听器重新绑定到已经存在的 HTML 结构上（即 **水合/Hydration**）。
- **`src/entry-server.js`（服务端入口，运行在 Node.js）**：只在服务器执行。负责接收 `server.js` 传来的 URL，把 `main.js` 里的组件树转换成纯文本字符串。

---

`index.html` 将需要引用 `entry-client.js` 并包含一个占位标记供给服务端渲染时注入：

```html
<div id="app"><!--ssr-outlet--></div>
<script type="module" src="/src/entry-client.js"></script>
```

`<!--ssr-outlet-->` 为什么是一段注释？

1. **保证 SPA 回退体验**：如果由于某种极端原因（如 Node.js 服务器全面瘫痪），运维将项目临时紧急降级为传统的 **SPA（单页面应用）**。因为 `<!--ssr-outlet-->` 是一段纯 HTML 注释，浏览器渲染时会直接无视它，不会在页面上留下任何奇怪的乱码。随后底部的 `<script>` 脚本（`entry-client.js`）加载，会像往常一样在客户端全权接管并渲染页面。
2. **完美的字符串替换介质**：在 `server.js` 中，后端只需要执行一行 `template.replace('<!--ssr-outlet-->', appHtml)`，就能把成千上万行的 Vue/React 静态 HTML 文本精准、安全地塞进容器中。

---

为什么 HTML 里还要引入 `<script ... entry-client.js>`？

**此时发给浏览器的 HTML 只是一个“静态的空壳（脱水状态）”**。页面上的按钮虽然好看，但你用鼠标去点击它是没有任何反应的，因为绑定的 JavaScript 事件监听器（如 `@click` 或 `onClick`）还没生效。

底部的 `entry-client.js` 负责在后台静默下载、执行，然后**像胶水一样，把 JS 事件重新绑回现有的 HTML 节点上（水合状态）**。完成这一步后，页面才真正“活了过来”，变成了一个可以交互的动态应用。

---

### 条件逻辑

如果需要执行 SSR 和客户端间条件逻辑，可以使用：

```js
if (import.meta.env.SSR) {
  // ... 仅在服务端执行的逻辑
}
```

这是在构建过程中被静态替换的，因此它将允许对未使用的条件分支进行摇树优化。

---

### 设置开发服务器

在构建 SSR 应用程序时，你可能希望完全控制主服务器，并将 Vite 与生产环境脱钩。因此，建议以中间件模式使用 Vite。下面是一个关于 [express](https://expressjs.com/) 的例子：

https://cn.vitejs.dev/guide/ssr#setting-up-the-dev-server

```js
	// …………
	// 2. 应用 Vite HTML 转换。这将会注入 Vite HMR 客户端，
    //    同时也会从 Vite 插件应用 HTML 转换。
    //    例如：@vitejs/plugin-react 中的 global preambles
    template = await vite.transformIndexHtml(url, template)

	// 3. 加载服务器入口。vite.ssrLoadModule 将自动转换
    //    你的 ESM 源码使之可以在 Node.js 中运行！无需打包
    //    并提供了一种高效的模块失效机制，类似于模块热替换（HMR）。
    const { render } = await vite.ssrLoadModule('/src/entry-server.js')
	// …………
```

---

 “在本地开发 SSR 时，既然是 Node 服务器直出 HTML，那前端的 **HMR（代码热更新）** 怎么保持？每次改完代码都要手动刷新浏览器吗？”

“不需要，这全靠 **`vite.transformIndexHtml`** 这个核心方法。在本地开发时，Node 读取出来的 `index.html` 只是一个冰冷的纯文本。如果直接返回给浏览器，页面将失去热更新能力。只要调用了 `vite.transformIndexHtml(url, template)`，Vite 会在编译阶段对这个 HTML 字符串进行**动态转换**：它会在 HTML 的 `<head>` 顶部自动注入一段 **Vite 客户端 HMR 专属脚本（如 `/ @vite/client`）**。这样当浏览器加载该 HTML 后，就能在后台自动建立起与 Vite 编译器的 WebSocket 链接。后续开发者修改组件时，依然可以享受毫秒级的局部热替换（HMR）体验。”

---

### 生产环境构建

为了将 SSR 项目交付生产，我们需要：

1. 正常生成一个客户端构建；
2. 再生成一个 SSR 构建，使其通过 `import()` 直接加载，这样便无需再使用 Vite 的 `ssrLoadModule`；

`package.json` 中的脚本应该看起来像这样：

```json
{
  "scripts": {
    "dev": "node server",
    "build:client": "vite build --outDir dist/client",
    "build:server": "vite build --outDir dist/server --ssr src/entry-server.js"
  }
}
```

注意使用 `--ssr` 标志表明这将会是一个 SSR 构建。同时需要指定 SSR 的入口。

接着，在 `server.js` 中，通过 `process.env.NODE_ENV` 条件分支，需要添加一些用于生产环境的特定逻辑：

- 使用 `dist/client/index.html` 作为模板，而不是根目录的 `index.html`，因为前者包含了到客户端构建的正确资源链接。
- 使用 `import('./dist/server/entry-server.js')` （该文件是 SSR 构建产物），而不是使用 `await vite.ssrLoadModule('/src/entry-server.js')`。
- 将 `vite` 开发服务器的创建和所有使用都移到 dev-only 条件分支后面，然后添加静态文件服务中间件来服务 `dist/client` 中的文件。

---

### 生成预加载指令

在使用了SSR的情况下，有大量的动态路由懒加载的情况下就加--ssrManifest

`vite build` 支持使用 `--ssrManifest` 标志，这将会在构建输出目录中生成一份 `.vite/ssr-manifest.json`：

```
- "build:client": "vite build --outDir dist/client",
+ "build:client": "vite build --outDir dist/client --ssrManifest",
```

上面的脚本将会为客户端构建生成 `dist/client/.vite/ssr-manifest.json` 。清单包含模块 ID 到它们关联的 chunk 和资源文件的映射。

---

具体情景：

假设你的应用有 `/home` 和 `/about` 路由，它们都是用 `import()` 懒加载的。 当用户访问 `/about` 页面时，服务端（Node）确实把 `/about` 的 HTML 直出了。 但是！当 HTML 到了浏览器，执行客户端水合（Hydration）时，客户端 JS 突然发现：“糟糕，`/about` 路由对应的代码块（比如 `About.q8w9e0.js`）我还没下载呢！”此时浏览器只能**临时现发起网络请求**去下载这个动态分包。在下载完成前的这几百毫秒里，页面上的按钮**完全无法点击、无法交互，甚至可能出现短暂的页面局部白屏闪烁**。这就叫“水合阻碍”。

 解法：`ssrManifest`（资源预加载清单）

1. **生成清单**： 你打包客户端时加上 `--ssrManifest`，Vite 会生成一个 `ssr-manifest.json` 映射表。这个表记录得清清楚楚：**“哪个组件/路由对应哪个打包后的 JS 和 CSS 文件”**。
2. **服务端注入预加载链接**： 当用户请求 `/about` 时，Node 服务器在用 `renderToString` 渲染组件的同时，顺便看一眼这个 `json` 清单，发现渲染 `/about` 刚好要用到 `About.q8w9e0.js`。
3. **最终产物**： Node 服务器在吐出 HTML 时，直接在 `<head>` 里塞进一句：

```html
<link rel="preload" href="/assets/About.q8w9e0.js" as="script">
```

这样，浏览器在刚拿到 HTML 的第一个瞬间，还没等执行 Vue/React 的水合逻辑呢，就已经并行去下载 `/about` 路由的 JS 代码了。等到需要水合时，资源早已在本地缓存里准备就绪，消除了全网所有的网络空窗期！

---

## 后端集成

“**如果公司不用 Node.js 做 SSR，而是用传统的后端（如 Java、Go、PHP、Python），前端打包后那堆带 Hash 的 JS/CSS 文件，后端怎么正确引入到 HTML 模版里？**”

核心：**`manifest.json`（静态资源资产清单）**。

痛点：前端每次打包（`vite build`），为了解决浏览器缓存问题，生成的文件名都会带上哈希值（例如 `main.A8b9c2.js`）。 传统的后端（比如 Java Spring 里的 `.jsp`，或者 Go 里的 `.html` 模版）是**死代码**，它根本不知道这次打包出来的哈希值是什么，导致没办法写 `<script src="...">` 标签。

 🛠️ 解决方案（Vite 后端集成机制）：

1. **前端开启配置**：在 `vite.config.js` 中配置 `build.manifest: true`。
2. **生成“密码本”**：打包后，Vite 会额外生成一个 `.vite/manifest.json` 文件。
3. **“密码本”的内容**：它记录了“原始文件名”到“带哈希文件名”的映射关系。

```json
{
  "_shared-B7PI925R.js": {
    "file": "assets/shared-B7PI925R.js",
    "name": "shared",
    "css": ["assets/shared-ChJ_j-JJ.css"]
  },
  "_shared-ChJ_j-JJ.css": {
    "file": "assets/shared-ChJ_j-JJ.css",
    "src": "_shared-ChJ_j-JJ.css"
  },
  "logo.svg": {
    "file": "assets/logo-BuPIv-2h.svg",
    "src": "logo.svg"
  },
  "baz.js": {
    "file": "assets/baz-B2H3sXNv.js",
    "name": "baz",
    "src": "baz.js",
    "isDynamicEntry": true
  },
  "views/bar.js": {
    "file": "assets/bar-gkvgaI9m.js",
    "name": "bar",
    "src": "views/bar.js",
    "isEntry": true,
    "imports": ["_shared-B7PI925R.js"],
    "dynamicImports": ["baz.js"]
  },
  "views/foo.js": {
    "file": "assets/foo-BRBmoGS9.js",
    "name": "foo",
    "src": "views/foo.js",
    "isEntry": true,
    "imports": ["_shared-B7PI925R.js"],
    "css": ["assets/foo-5UjPuW-k.css"]
  }
}
```

4. **后端查表注入**：Java/Go 后端在渲染 HTML 时，先读取这个 JSON 清单，查出 `main.js` 现在的真名叫 `assets/main.A8b9c2.js`，然后动态拼进 HTML 里。

---

## 性能

常见的性能问题，例如：

- 服务器启动慢
- 页面加载慢
- 构建慢

---

### 减少解析操作

Vite 支持通过 [`resolve.extensions`](https://cn.vitejs.dev/config/shared-options#resolve-extensions) 选项“猜测”导入路径，该选项默认为 `['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json']`。

当您尝试使用 `import './Component'` 导入 `./Component.jsx` 时，Vite 将运行以下步骤来解析它：

1. 检查 `./Component` 是否存在，不存在。
2. 检查 `./Component.mjs` 是否存在，不存在。
3. 检查 `./Component.js` 是否存在，不存在。
4. 检查 `./Component.mts` 是否存在，不存在。
5. 检查 `./Component.ts` 是否存在，不存在。
6. 检查 `./Component.jsx` 是否存在，存在！

如上所示，解析一个导入路径需要进行 6 次文件系统检查。您的隐式导入越多，解析路径所需的时间就越多。

因此，通常最好明确您的导入路径，例如 `import './Component.jsx'`。也可以缩小 `resolve.extensions` 的列表以减少一般的文件系统检查，但必须确保它也适用于 `node_modules` 中的文件。

---

TypeScript

如果你正在使用 TypeScript，启用 `tsconfig.json` 中的 `compilerOptions` 的 `"moduleResolution": "bundler"` 和 `"allowImportingTsExtensions": true` 以直接在代码中使用 `.ts` 和 `.tsx` 扩展名。

---

1. 要显示引入

```tsx
// 显式扩展名：只需一次文件系统检查（更快）
import ComponentExplicit from './components/Component.tsx'
// 隐式导入：解析器会根据 resolve.extensions 进行多次检查
import ComponentImplicit from './components/Component'
```

2. **TypeScript 完美闭环（核心配置）**：以前在 TS 项目里写 `.ts` 后缀会报错。在最新版的 TS 中，需要在 `tsconfig.json` 中开启以下两个配置，即可完美支持在代码里手写后缀：

```json
"compilerOptions": {
  "moduleResolution": "bundler",
  "allowImportingTsExtensions": true
}
```

---

### 预热常用文件

```js
export default defineConfig({
  server: {
    warmup: {
      clientFiles: [
        './src/components/BigComponent.vue',
        './src/utils/big-utils.js',
      ],
    },
  },
})
```

使用 [`--open` 或 `server.open`](https://cn.vitejs.dev/config/server-options.html#server-open) 也可以提供性能提升，因为 Vite 将自动预热你的应用的入口起点或被提供的要打开的 URL。

---

### 使用更少或更原生化的工具链

保持 Vite 如此之快的关键在于减少源文件（JS/TS/CSS）的工作量。

精简工作的例子：

- 使用 CSS 而不是 Sass/Less/Stylus（可以由 PostCSS / Lightning CSS 处理嵌套）
- 不要将 SVG 转换为 UI 框架组件（例如 React、Vue 等）。请将其作为字符串或 URL 导入。

---

























































































































































































































