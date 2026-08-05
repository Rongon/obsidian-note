# Vue Router

## 基础

### 入门

客户端路由的作用是在单页应用 (SPA) 中将浏览器的 URL 和用户看到的内容绑定起来。当用户在应用中浏览不同页面时，URL 会随之更新，但页面不需要从服务器重新加载。

Vue Router 基于 Vue 的组件系统构建，你可以通过配置**路由**来告诉 Vue Router 为每个 URL 路径显示哪些组件。

---

#### 示例

##### 创建路由器实例

路由器实例是通过调用 `createRouter()` 函数创建的:

```js
import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from './HomeView.vue'
import AboutView from './AboutView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/about', component: AboutView },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})
```

---

##### 注册路由器插件

一旦创建了我们的路由器实例，我们就需要将其注册为插件，这一步骤可以通过调用 `use()` 来完成。

```js
createApp(App).use(router).mount('#app')
```

```js
const app = createApp(App)
app.use(router)
app.mount('#app')
```

和大多数的 Vue 插件一样，`use()` 需要在 `mount()` 之前调用。

它的职责包括：

1. [全局注册](https://cn.vuejs.org/guide/components/registration.html#global-registration) `RouterView` 和 `RouterLink` 组件。
2. 添加全局 `$router` 和 `$route` 属性。
3. 启用 `useRouter()` 和 `useRoute()` 组合式函数。
4. 触发路由器解析初始路由。

---

##### 访问路由器和当前路由

选项式：this.$router` 和 `this.$route

组合式： `useRouter()` 和 `useRoute()` 

```vue
<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const search = computed({
  get() {
    return route.query.search ?? ''
  },
  set(search) {
    router.replace({ query: { search } })
  },
})
</script>
```

---

### 动态路由匹配

#### 带参数的动态路由匹配

 解决了什么问题：

如果没有动态路由，你只能为每个具体的 URL 配置一条路由。例如，要显示 100 个用户的信息，你可能需要定义 100 条路由规则，这根本无法维护。动态路由用**一个路由规则**匹配**无数个同类型的 URL**，并将变化的那个部分（比如用户 ID）提取出来，供组件使用。

```js
import User from './User.vue'

// 这些都会传递给 `createRouter`
const routes = [
  // 动态字段以冒号开始
  { path: '/users/:id', component: User },
]
```

 核心语法：

```js
const routes = [
  { path: '/users/:id', component: User }
]
```

多个动态参数可以同时存在：

```js
{ path: '/users/:username/posts/:postId', component: PostDetail }
```

| 匹配模式                       | 匹配路径                 | route.params                             |
| :----------------------------- | :----------------------- | :--------------------------------------- |
| /users/:username               | /users/eduardo           | `{ username: 'eduardo' }`                |
| /users/:username/posts/:postId | /users/eduardo/posts/123 | `{ username: 'eduardo', postId: '123' }` |

 在组件中获取参数：

**模板中**：

```vue
<template>
  <div>User {{ $route.params.id }}</div>
</template>
```

script setup 中：

```vue
<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
console.log(route.params.id)  // 获取动态参数
console.log(route.query)      // URL 查询参数 ?foo=bar
console.log(route.hash)       // URL hash #section
</script>
```

---

#### 响应路由参数的变化

当用户从 `/users/1` 导航到 `/users/2` 时，**同一个 `User` 组件会被复用**（不会销毁重建），因为两个路由都渲染同个组件，比起销毁再创建，复用则显得更加高效。**不过，这也意味着组件的生命周期钩子不会被调用**。

如果需要**响应路由参数的变化**（比如根据新 ID 重新请求数据），你需要使用 `watch`：

```vue
<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

watch(
  () => route.params.id,
  (newId, oldId) => {
    // 对路由变化做出响应...
  }
)
</script>
```

或者，使用 `beforeRouteUpdate` [导航守卫](https://router.vuejs.org/zh/guide/advanced/navigation-guards.html)，它还允许你取消导航：

```vue
<script setup>
import { onBeforeRouteUpdate } from 'vue-router'
// ...

onBeforeRouteUpdate(async (to, from) => {
  // 对路由变化做出响应...
  userData.value = await fetchUser(to.params.id)
})
</script>
```

---

#### 捕获所有路由或 404 Not found 路由

常规参数只匹配 url 片段之间的字符，用 `/` 分隔。如果我们想匹配**任意路径**，我们可以使用自定义的 *路径参数* 正则表达式，在 *路径参数* 后面的括号中加入 正则表达式 :

```js
const routes = [
  // 将匹配所有内容并将其放在 `route.params.pathMatch` 下
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  // 将匹配以 `/user-` 开头的所有内容，并将其放在 `route.params.afterUser` 下
  { path: '/user-:afterUser(.*)', component: UserGeneric },
]
```

可以通过将 `path` 拆分成一个数组，直接导航到路由：

```js
router.push({
  name: 'NotFound',
  // 保留当前路径并删除第一个字符，以避免目标 URL 以 `//` 开头。
  params: { pathMatch: this.$route.path.substring(1).split('/') },
  // 保留现有的查询和 hash 值，如果有的话
  query: route.query,
  hash: route.hash,
})
```

---

### 路由的匹配语法

大多数应用都会使用 `/about` 这样的静态路由和 `/users/:userId` 这样的动态路由，下面介绍其他方式。

#### 在参数中自定义正则

两个路由 `/:orderId` 和 `/:productName`，两者会匹配完全相同的 URL，所以我们需要一种方法来区分它们。

最简单的方法就是在路径中添加一个静态部分来区分它们：

```js
const routes = [
  // 匹配 /o/3549
  { path: '/o/:orderId' },
  // 匹配 /p/books
  { path: '/p/:productName' },
]
```

但在某些情况下，我们并不想添加静态的 `/o` `/p` 部分。由于，`orderId` 总是一个数字，而 `productName` 可以是任何东西，所以我们可以在括号中为参数指定一个自定义的正则：

```js
const routes = [
  // /:orderId -> 仅匹配数字
  { path: '/:orderId(\\d+)' },
  // /:productName -> 匹配其他任何内容
  { path: '/:productName' },
]
```

---

#### 可重复的参数

 核心问题：普通动态参数只能匹配“一段”：

普通动态参数 `:id` 只能匹配**两个斜杠之间的一个片段**：

| 路由         | 能匹配的 URL | 不能匹配的 URL               |
| :----------- | :----------- | :--------------------------- |
| `/:chapters` | `/one`       | `/one/two`，`/one/two/three` |

 解决方案：可重复参数 `+` 和 `*`：

| 修饰符 | 含义       | 是否允许空值 | 示例路由      | 匹配 `/` | 匹配 `/one` | 匹配 `/one/two/three` |
| :----- | :--------- | :----------- | :------------ | :------- | :---------- | :-------------------- |
| `+`    | 1 个或多个 | ❌ 不允许为空 | `/:chapters+` | ❌        | ✅           | ✅                     |
| `*`    | 0 个或多个 | ✅ 允许为空   | `/:chapters*` | ✅        | ✅           | ✅                     |

 获取参数：从字符串变成了数组：

```js
// URL: /one/two/three
// 路由: { path: '/:chapters+' }

import { useRoute } from 'vue-router'
const route = useRoute()
console.log(route.params.chapters)  // ['one', 'two', 'three']  是一个数组！
```

在命名路由中传递时，也必须传数组：

```js
// ✅ 正确：传数组
router.push({ name: 'chapters', params: { chapters: ['a', 'b'] } })
// 生成 URL: /a/b

// ❌ 错误：传字符串（普通动态参数才传字符串）
router.push({ name: 'chapters', params: { chapters: 'a' } })
// 生成 URL: /a（a 被视为只有一个元素的数组，所以结果正确但语义不对）
```

---

#### Sensitive 与 strict 路由配置

默认情况下，所有路由是不区分大小写的，并且能匹配带有或不带有尾部斜线的路由。例如，路由 `/users` 将匹配 `/users`、`/users/`、甚至 `/Users/`。这种行为可以通过 `strict` 和 `sensitive` 选项来修改，它们既可以应用在整个全局路由上，又可以应用于当前路由上：

```js
const router = createRouter({
  history: createWebHistory(),
  routes: [
    // 将匹配 /users/posva 而非：
    // - /users/posva/ 当 strict: true
    // - /Users/posva 当 sensitive: true
    { path: '/users/:id', sensitive: true },
    // 将匹配 /users, /Users, 以及 /users/42 而非 /users/ 或 /users/42/
    { path: '/users/:id?' },
  ],
  strict: true, // applies to all routes
})
```

 `sensitive`：控制**大小写**敏感度；`strict`：控制**尾部斜线**的严格度

---

#### 可选参数

https://router.vuejs.org/zh/guide/essentials/route-matching-syntax.html#%E5%8F%AF%E9%80%89%E5%8F%82%E6%95%B0

---

### 嵌套路由

children：

```js
const routes = [
  {
    path: '/user/:id',
    component: User,
    children: [
      {
        // 当 /user/:id/profile 匹配成功
        // UserProfile 将被渲染到 User 的 <router-view> 内部
        path: 'profile',
        component: UserProfile,
      },
      {
        // 当 /user/:id/posts 匹配成功
        // UserPosts 将被渲染到 User 的 <router-view> 内部
        path: 'posts',
        component: UserPosts,
      },
    ],
  },
]
```

---

#### 嵌套的命名路由

```js
const routes = [
  {
    path: '/user/:id',
    component: User,
    // 请注意，只有子路由具有名称
    children: [{ path: '', name: 'user', component: UserHome }],
  },
]
```

```js
const routes = [
  {
    path: '/user/:id',
    name: 'user-parent',
    component: User,
    children: [{ path: '', name: 'user', component: UserHome }],
  },
]
```

| 配置方式           | 导航到 `/user/123` | 通过命名路由导航                                   |
| :----------------- | :----------------- | :------------------------------------------------- |
| **只给子路由命名** | 显示默认子路由     | 只能导航到子路由，必显示 `UserHome`                |
| **父子路由都命名** | 显示默认子路由     | 可导航到 `user-parent`，不显示子路由（刷新后恢复） |

**场景**：你想在父路由的 `User.vue` 中显示一个“欢迎页面”或“提示用户选择操作”的界面，而不是直接显示默认子路由。

**一句话总结**：给父路由命名，可以让你在客户端导航时“跳过”默认子路由，但页面刷新后 URL 匹配的默认行为会再次生效。

---

#### 忽略父组件

https://router.vuejs.org/zh/guide/essentials/nested-routes.html#%E5%BF%BD%E7%95%A5%E7%88%B6%E7%BB%84%E4%BB%B6-

---

### 命名路由

已经很简洁了：

https://router.vuejs.org/zh/guide/essentials/named-routes.html#%E5%91%BD%E5%90%8D%E8%B7%AF%E7%94%B1

```js
const routes = [
  {
    path: '/user/:username',
    name: 'profile', 
    component: User,
  },
]
```

---

### 编程式导航

https://router.vuejs.org/zh/guide/essentials/navigation.html#%E7%BC%96%E7%A8%8B%E5%BC%8F%E5%AF%BC%E8%88%AA

很简洁，知识点不多

| 声明式                    | 编程式             |
| :------------------------ | :----------------- |
| `<router-link :to="...">` | `router.push(...)` |

---

### 命名视图

一条路由可以同时渲染多个组件

https://router.vuejs.org/zh/guide/essentials/named-views.html#%E5%91%BD%E5%90%8D%E8%A7%86%E5%9B%BE

---

### 重定向和别名

https://router.vuejs.org/zh/guide/essentials/redirect-and-alias.html#%E9%87%8D%E5%AE%9A%E5%90%91%E5%92%8C%E5%88%AB%E5%90%8D

#### 别名

```js
const routes = [{ path: '/', component: Homepage, alias: '/home' }]
```

---

### 路由组件传参

#### 将 props 传递给路由组件

让路由组件从“主动去 URL 里拿数据”变成“被动接收数据”，数据来源从路由自动注入，组件本身不再依赖 Vue Router，变得更加纯粹和通用。

https://router.vuejs.org/zh/guide/essentials/passing-props.html#%E5%B0%86-props-%E4%BC%A0%E9%80%92%E7%BB%99%E8%B7%AF%E7%94%B1%E7%BB%84%E4%BB%B6

 问题：组件与路由紧耦合

传统的写法是组件内部直接读取 `$route.params.id`：

```vue
<!-- User.vue -->
<template>
  <div>User {{ $route.params.id }}</div>
</template>
```

**缺点**：

- **可复用性差**：这个 `User` 组件只能用于 Vue Router 环境中，且必须绑在 `/users/:id` 这样的路由上才能工作。
- **测试麻烦**：单元测试时，你必须模拟一个 `$route` 对象，或者用 `useRoute()` 的 mock，增加了测试复杂度。
- **组件不纯粹**：组件的输入来源有两处——props 和 URL，违反了“单一数据来源”原则。

---

 `props` 的三种模式：

| 模式         | 配置                                                         | 行为                                                         |
| :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **布尔模式** | `props: true`                                                | 把 `route.params` 全部作为 props 传给组件                    |
| **对象模式** | `props: { id: 'fixed' }`                                     | 静态地、固定地传 props，一般配合命名视图使用                 |
| **函数模式** | `props: (route) => ({ id: route.params.id, query: route.query.q })` | 完全自定义，可以从 `params`、`query`、`hash` 中组合出任意 props |

---

 布尔模式 (`props: true`)：

**数据来源**：纯URL路径参数
**适用场景**：URL里的动态参数（`:id`）直接就是组件需要的数据，无需加工。

```js
// ✅ URL: /user/42  → 组件 props: { id: '42' }
{ path: '/user/:id', component: User, props: true }
```

**什么时候用？**

- 组件用到的数据，完全来自 `params`，并且名字也对得上。
- 这是最推荐、最简洁的模式，能用它就尽量用。

---

 对象模式 (`props: { ... }`)：

**数据来源**：静态的、写死的配置
**适用场景**：你想给组件**传固定值**，这个值与 URL **完全无关**。

```js
// ✅ URL无论是什么，组件的 sidebar 始终是 true
{
  path: '/admin',
  components: { default: Admin, sidebar: Sidebar },
  props: { default: {}, sidebar: { isAdmin: true } }
}
```

**什么时候用？**

- 配合**命名视图**：不同视图需要不同配置。
- 多个路由复用同一组件，但需要传不同标识（比如页面标题）。
- **特殊提示**：对象模式下 `params` 的值**不会**自动传给组件。如果需要同时传 `params` 和静态值，要用下面的函数模式。

---

 函数模式 (`props: (route) => ({ ... })`)：

**数据来源**：需要组合、转换、或从非 `params` 来源提取的数据
**适用场景**：组件需要的 props 不纯是 `params`，需要从 `query`、`hash`、或元数据里取值，或者 `params` 名字与组件 props 名字不一致。

```js
// ✅ URL: /search?q=hello&page=1  → props: { keyword: 'hello', page: '1' }
{ 
  path: '/search', 
  component: Search, 
  props: (route) => ({ 
    keyword: route.query.q,   // 从 query 里拿
    page: parseInt(route.query.page) || 1  // 顺便做个类型转换
  })
}
```

**什么时候用？**

- 数据来自 `route.query`（问号后面的参数）。
- 数据名不匹配：URL参数叫 `:id`，但组件 props 声明叫 `userId`。
- 需要**类型转换**：把字符串 `"1"` 转成数字 `1`。
- 需要**组合数据**：同时从 `params` 和 `query` 里拿数据，甚至从 `meta` 里拿静态数据。

---

需要给组件传 props 吗？
  ├── 是
  │   ├── 数据来自 URL 的 params？
  │   │   ├── 是，且名字一致 → 用 布尔模式 (props: true)
  │   │   └── 是，但名字不一致/需要组合 query/需要转换 → 用 函数模式
  │   └── 数据是固定的，与 URL 无关 → 用 对象模式
  └── 否 → 继续用 $route 或 useRoute()

**能用布尔就用布尔**；参数名不匹配、要组合多个来源、要做类型转换时换函数；只传与URL无关的静态值时用对象。核心原则是**让组件通过 props 接收一切所需数据，不主动碰 `route`。**

---

### 不同的历史模式

https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E4%B8%8D%E5%90%8C%E7%9A%84%E5%8E%86%E5%8F%B2%E6%A8%A1%E5%BC%8F

它主要分为三种：Hash 模式、HTML5 模式和 Memory 模式。其中，HTML5 是官方推荐的默认模式，但需要服务器配合；Hash 模式兼容性好，无需服务器配置；Memory 模式则适用于 Node.js 或 SSR 等非浏览器环境。

---

## 进阶

### 导航守卫

#### 全局前置守卫

https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E5%85%A8%E5%B1%80%E5%89%8D%E7%BD%AE%E5%AE%88%E5%8D%AB

```js
const router = createRouter({ ... })

router.beforeEach((to, from) => {
  // ...
  // 返回 false 以取消导航
  return false
})
```

`to` 和 `from` 是两个 **Route 对象**，分别代表**即将进入的目标路由**和**当前正要离开的路由**。它们包含了你需要的所有 URL 和路由信息。

---

#### 全局解析守卫

router.beforeResolve

解析守卫刚好会在导航被确认之前、**所有组件内守卫和异步路由组件被解析之后**调用。

`router.beforeResolve` 是获取数据或执行任何其他操作（如果用户无法进入页面时你希望避免执行的操作）的理想位置。

---

#### 全局后置钩子

```js
router.afterEach((to, from) => {
  sendToAnalytics(to.fullPath)
})
```

它们对于分析、更改页面标题、声明页面等辅助功能以及许多其他事情都很有用。

---

#### 在守卫内的全局注入

https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E5%9C%A8%E5%AE%88%E5%8D%AB%E5%86%85%E7%9A%84%E5%85%A8%E5%B1%80%E6%B3%A8%E5%85%A5

---

#### 路由独享的守卫

beforeEnter

https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E8%B7%AF%E7%94%B1%E7%8B%AC%E4%BA%AB%E7%9A%84%E5%AE%88%E5%8D%AB

---

#### 组件内的守卫

在路由组件内直接定义路由导航守卫(传递给路由配置的)

##### 可用的配置 API

可以为路由组件添加以下配置：

- `beforeRouteEnter`
- `beforeRouteUpdate`
- `beforeRouteLeave`

https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E5%8F%AF%E7%94%A8%E7%9A%84%E9%85%8D%E7%BD%AE-API

---

#### 完整的导航解析流程

https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E5%AE%8C%E6%95%B4%E7%9A%84%E5%AF%BC%E8%88%AA%E8%A7%A3%E6%9E%90%E6%B5%81%E7%A8%8B

----

### 路由元信息

文档有点乱，暂时看不太懂。但意思差不多，遇到再看再用上也行

- **meta 是什么？** —— 附加在路由上的自定义数据，用于携带路由所需的任意辅助信息。
- **合并机制** —— 父子路由的 meta 会自动合并，子路由相同属性会覆盖父路由。
- **与守卫配合** —— 在 `beforeEach` 里通过 `to.meta.xxx` 读取，实现统一的权限、标题等逻辑。

**一句话总结**：路由元信息就是给路由贴“标签”，让你在导航守卫中能统一读取，避免把权限、标题等逻辑分散到每个组件里。

https://router.vuejs.org/zh/guide/advanced/meta.html#%E8%B7%AF%E7%94%B1%E5%85%83%E4%BF%A1%E6%81%AF

---

### 数据获取

有时候，进入某个路由后，需要从服务器获取数据。例如，在渲染用户信息时，需要从服务器获取用户的数据。可以通过两种方式来实现：

- **导航完成之后获取**：先完成导航，然后在接下来的组件生命周期钩子中获取数据。在数据获取期间显示“加载中”之类的指示。
- **导航完成之前获取**：导航完成前，在路由进入的守卫中获取数据，在数据获取成功后执行导航。

从技术角度讲，两种方式都不错 —— 就看想要的用户体验是哪种。

---

 导航完成后获取数据/导航完成前获取数据

两种完整的例子：

https://router.vuejs.org/zh/guide/advanced/data-fetching.html#%E6%95%B0%E6%8D%AE%E8%8E%B7%E5%8F%96

---

### 组合式 API

#### Vue Router 和 组合式 API

##### 在 `setup` 中访问路由和当前路由

`route` 对象是一个响应式对象。在多数情况下，你应该**避免监听整个 `route`** 对象，同时直接监听你期望改变的参数。

在模板中仍然可以访问 `$router` 和 `$route`，所以如果只在模板中使用这些对象的话，是不需要 `useRouter` 或 `useRoute` 的。

---

##### 导航守卫

onBeforeRouteLeave/onBeforeRouteUpdate

---

##### `useLink`

https://router.vuejs.org/zh/guide/advanced/composition-api.html#useLink

---

### RouterView 插槽

 KeepAlive & Transition、模板引用

https://router.vuejs.org/zh/guide/advanced/router-view-slot.html

---

### 过渡动效

https://router.vuejs.org/zh/guide/advanced/transitions.html#%E8%BF%87%E6%B8%A1%E5%8A%A8%E6%95%88

#### 单个路由的过渡

​	想要在你的路径组件上使用转场，并对导航进行动画处理，你需要使用插槽。

---

#### 基于路由的动态过渡

​	也可以根据目标路由和当前路由之间的关系，动态地确定使用的过渡。

---

#### 强制在复用的视图之间进行过渡

​	Vue 可能会自动复用看起来相似的组件，从而忽略了任何过渡。幸运的是，可以[添加一个 `key` 属性](https://cn.vuejs.org/api/built-in-special-attributes.html#key)来强制过渡。这也允许在相同路由上使用不同的参数触发过渡：

---

### 滚动行为

使用前端路由，当切换到新路由时，想要页面滚到顶部，或者是保持原先的滚动位置，就像重新加载页面那样。

**注意: 这个功能只在支持 history.pushState 的浏览器中可用。**

https://router.vuejs.org/zh/guide/advanced/scroll-behavior.html#%E6%BB%9A%E5%8A%A8%E8%A1%8C%E4%B8%BA

---

#### 延迟滚动

有时候，我们需要在页面中滚动之前稍作等待。例如，当处理过渡时，我们希望等待过渡结束后再滚动。要做到这一点，你可以返回一个 Promise，它可以返回所需的位置描述符。

---

#### 高级偏移量

如果你的页面中有固定的导航栏或类似的元素，你可能需要设置偏移量，以确保目标元素不会被其他内容遮挡。 使用静态偏移值并不总是有效。在这种情况下，更好的做法是手动计算偏移量。一种简单的方法是结合 CSS 和 JavaScript 的 `getComputedStyle()`。

---

### 路由懒加载

```js
// 将
// import UserDetails from './views/UserDetails.vue'
// 替换成
const UserDetails = () => import('./views/UserDetails.vue')

const router = createRouter({
  // ...
  routes: [
    { path: '/users/:id', component: UserDetails }
    // 或在路由定义里直接使用它
    { path: '/users/:id', component: () => import('./views/UserDetails.vue') },
  ],
})
```

https://router.vuejs.org/zh/guide/advanced/lazy-loading.html#%E8%B7%AF%E7%94%B1%E6%87%92%E5%8A%A0%E8%BD%BD

---

### 类型化路由

即给路由也写ts，就能获得完整的类型检查和智能补全提示了。

可以为路由配置一个类型化的映射表。 虽然可以手动实现，但更推荐使用 [unplugin-vue-router](https://github.com/posva/unplugin-vue-router) 插件来自动生成路由及其类型。

https://router.vuejs.org/zh/guide/advanced/typed-routes.html#%E7%B1%BB%E5%9E%8B%E5%8C%96%E8%B7%AF%E7%94%B1-

---

#### 扩展 RouterLink

RouterLink 组件提供了足够的 `props` 来满足大多数基本应用程序的需求，但它并未尝试涵盖所有可能的用例，在某些高级情况下，你可能会发现自己使用了 `v-slot`。在大多数中型到大型应用程序中，值得创建一个（如果不是多个）自定义 RouterLink 组件，以在整个应用程序中重用它们。例如导航菜单中的链接，处理外部链接，添加 `inactive-class` 等。

https://router.vuejs.org/zh/guide/advanced/extending-router-link.html#%E6%89%A9%E5%B1%95-RouterLink

![image-20260603102750823](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260603102750823.png)

---

### 导航故障

#### 等待导航结果

需要一种方法来检测我们是否真的改变了页面。

https://router.vuejs.org/zh/guide/advanced/navigation-failures.html#%E7%AD%89%E5%BE%85%E5%AF%BC%E8%88%AA%E7%BB%93%E6%9E%9C

---

#### 检测导航故障

如果导航被阻止，导致用户停留在同一个页面上，由 `router.push` 返回的 `Promise` 的解析值将是 *Navigation Failure*。否则，它将是一个 *falsy* 值(通常是 `undefined`)。这样我们就可以区分我们导航是否离开了当前位置：

https://router.vuejs.org/zh/guide/advanced/navigation-failures.html#%E6%A3%80%E6%B5%8B%E5%AF%BC%E8%88%AA%E6%95%85%E9%9A%9C

---

#### 全局导航故障

https://router.vuejs.org/zh/guide/advanced/navigation-failures.html#%E5%85%A8%E5%B1%80%E5%AF%BC%E8%88%AA%E6%95%85%E9%9A%9C

---

#### 鉴别导航故障

正如我们在一开始所说的，有不同的情况会导致导航的中止，所有这些情况都会导致不同的 *Navigation Failure*。它们可以用 `isNavigationFailure` 和 `NavigationFailureType` 来区分。总共有三种不同的类型：

https://router.vuejs.org/zh/guide/advanced/navigation-failures.html#%E9%89%B4%E5%88%AB%E5%AF%BC%E8%88%AA%E6%95%85%E9%9A%9C

----

#### *导航故障*的属性

所有的导航失败都会暴露 `to` 和 `from` 属性，以反映失败导航的当前位置和目标位置：

https://router.vuejs.org/zh/guide/advanced/navigation-failures.html#%E5%AF%BC%E8%88%AA%E6%95%85%E9%9A%9C%E7%9A%84%E5%B1%9E%E6%80%A7

---

#### 检测重定向

当在导航守卫中返回一个新的位置时，我们会触发一个新的导航，覆盖正在进行的导航。与其他返回值不同的是，重定向不会阻止导航，**而是创建一个新的导航**。因此，通过读取路由地址中的 `redirectedFrom` 属性，对其进行不同的检查：

https://router.vuejs.org/zh/guide/advanced/navigation-failures.html#%E6%A3%80%E6%B5%8B%E9%87%8D%E5%AE%9A%E5%90%91

---

### 动态路由

#### 添加路由

动态路由主要通过两个函数实现。`router.addRoute()` 和 `router.removeRoute()`。它们**只**注册一个新的路由，也就是说，如果新增加的路由与当前位置相匹配，就需要你用 `router.push()` 或 `router.replace()` 来**手动导航**，才能显示该新路由。

```js
router.addRoute({ path: '/about', component: About })
// 我们也可以使用 this.$route 或 useRoute()
router.replace(router.currentRoute.value.fullPath)
```

如果需要等待新的路由显示，可以使用 `await router.replace()`。

---

#### 在导航守卫中添加路由

如果你决定在导航守卫内部添加或删除路由，你不应该调用 `router.replace()`，而是通过返回新的位置来触发重定向：

https://router.vuejs.org/zh/guide/advanced/dynamic-routing.html#%E5%9C%A8%E5%AF%BC%E8%88%AA%E5%AE%88%E5%8D%AB%E4%B8%AD%E6%B7%BB%E5%8A%A0%E8%B7%AF%E7%94%B1

---

#### 删除路由

有几个不同的方法来删除现有的路由：

https://router.vuejs.org/zh/guide/advanced/dynamic-routing.html#%E5%88%A0%E9%99%A4%E8%B7%AF%E7%94%B1

---

#### 添加嵌套路由

要将嵌套路由添加到现有的路由中，可以将路由的 *name* 作为第一个参数传递给 `router.addRoute()`，这将有效地添加路由，就像通过 `children` 添加的一样：

```js
router.addRoute({ name: 'admin', path: '/admin', component: Admin })
router.addRoute('admin', { path: 'settings', component: AdminSettings })
```

---

#### 查看现有路由

Vue Router 提供了两个功能来查看现有的路由：

- [`router.hasRoute()`](https://router.vuejs.org/zh/api/interfaces/Router.html#Methods-hasRoute)：检查路由是否存在。
- [`router.getRoutes()`](https://router.vuejs.org/zh/api/interfaces/Router.html#Methods-getRoutes)：获取一个包含所有路由记录的数组。

---

## 基于文件的路由

### 入门

**用文件目录结构自动生成路由配置，告别手动维护 `routes` 数组。**

```
src/pages/
├── index.vue          → 自动匹配 /
├── about.vue          → 自动匹配 /about
└── users/
    └── [id].vue       → 自动匹配 /users/:id
```

---

#### 设置

对vite、tsconfig.json、env.d.ts、进行一系列配置

https://router.vuejs.org/zh/file-based-routing/#%E8%AE%BE%E7%BD%AE

---

### 文件约定

https://router.vuejs.org/zh/file-based-routing/file-based-routing.html#%E6%96%87%E4%BB%B6%E7%BA%A6%E5%AE%9A

#### 路由文件夹结构

##### 嵌套路由

给定这个文件夹结构：

```
src/pages/
├── users/
│   └── index.vue
└── users.vue
```

将得到这个 `routes` 数组：

```js
const routes = [
  {
    path: '/users',
    component: () => import('src/pages/users.vue'),
    children: [
      { path: '', component: () => import('src/pages/users/index.vue') },
    ],
  },
]
```

而省略 `src/pages/users.vue` 组件将生成以下路由：

```js
const routes = [
  {
    path: '/users',
    // 注意这里没有 component
    children: [
      { path: '', component: () => import('src/pages/users/index.vue') },
    ],
  },
]
```

##### 没有嵌套布局的嵌套路由

```
src/pages/
├── users/
│   ├── [id].vue
│   └── index.vue
└── users.vue
```

如果想添加新路由 `/users/create`，可以添加新文件 `src/pages/users/create.vue` 但这会将 `create.vue` 组件嵌套在 `users.vue` 组件中。为避免这种情况，可以创建一个文件 `src/pages/users.create.vue`。`.` 在生成路由时将变成 `/`：

```js
const routes = [
  {
    path: '/users',
    component: () => import('src/pages/users.vue'),
    children: [
      { path: '', component: () => import('src/pages/users/index.vue') },
      { path: ':id', component: () => import('src/pages/users/[id].vue') },
    ],
  },
  {
    path: '/users/create',
    component: () => import('src/pages/users.create.vue'),
  },
]
```

---

#### 命名视图

https://router.vuejs.org/zh/file-based-routing/file-based-routing.html#%E5%91%BD%E5%90%8D%E8%A7%86%E5%9B%BE

---

#### 动态路由

你可以通过用括号包裹 *参数名称* 来添加 [路由参数](https://router.vuejs.org/guide/essentials/dynamic-matching.html)，例如 `src/pages/users/[id].vue` 将创建一个具有以下路径的路由：`/users/:id`。注意你可以在静态片段之间添加参数：`src/pages/users_[id].vue` -> `/users_:id`。你甚至可以添加多个参数：`src/pages/product_[skuId]_[seoDescription].vue`。

你可以通过用额外的一对括号包裹 *参数名称* 来创建 [**可选参数**](https://router.vuejs.org/guide/essentials/route-matching-syntax.html#optional-parameters)，例如 `src/pages/users/[[id]].vue` 将创建一个具有以下路径的路由：`/users/:id?`。

你可以通过在右括号后添加加号 (`+`) 来创建 [**可重复参数**](https://router.vuejs.org/guide/essentials/route-matching-syntax.html#repeatable-params)，例如 `src/pages/articles/[slugs]+.vue` 将创建一个具有以下路径的路由：`/articles/:slugs+`。

你可以将两者结合起来创建可选的可重复参数，例如 `src/pages/articles/[[slugs]]+.vue` 将创建一个具有以下路径的路由：`/articles/:slugs*`。

---

#### 通配符 / 404 Not found 路由

https://router.vuejs.org/zh/file-based-routing/file-based-routing.html#%E9%80%9A%E9%85%8D%E7%AC%A6-404-Not-found-%E8%B7%AF%E7%94%B1

---

#### 多个路由文件夹

可以通过将数组传递给 `routesFolder` 来提供多个路由文件夹：

```js
VueRouter({
  routesFolder: ['src/pages', 'src/admin/routes'],
})
```

---

### 配置

查看所有现有配置选项及其对应的**默认值**：

```js
import VueRouter from 'vue-router/vite'

VueRouter({
  // 如何以及扫描哪些文件夹以查找文件
  routesFolder: [
    {
      src: 'src/pages',
      path: '',
      // 覆盖全局设置
      exclude: excluded => excluded,
      filePatterns: filePatterns => filePatterns,
      extensions: extensions => extensions,
    },
  ],

  // 哪些类型的文件应被视为页面
  extensions: ['.vue'],

  // 要包含哪些文件
  filePatterns: ['**/*'],

  // 要排除的文件
  exclude: [],

  // 生成的 d.ts 文件路径
  dts: './typed-router.d.ts',

  // 如何生成路由名称
  getRouteName: routeNode => getFileBasedRouteName(routeNode),

  // <route> 自定义块的默认语言
  routeBlockLang: 'json5',

  // 如何导入路由，也可以是字符串
  importMode: 'async',

  // 根目录
  root: process.cwd(),

  // 路径解析器的选项
  pathParser: {
    // `users.[id]` 应该被解析为 `users/:id` 吗？
    dotNesting: true,
  },

  // 单独修改路由
  async extendRoute(route) {
    // ...
  },

  // 在写入文件之前修改路由
  async beforeWriteFiles(rootRoute) {
    // ...
  },
})
```

---

### 扩展路由

#### 在配置中扩展路由

基于文件的路由很方便，但完全依赖目录结构有时会不够灵活。比如：

- **场景一：给路由添加别名**
  你想让 `/about` 页面也能通过 `/company` 访问，但不想创建两个文件。这时就可以在构建时用 `extendRoute` 给这个路由加一个别名。
- **场景二：插入不符合文件命名规范的特殊路由**
  某些路由路径（如 `/from-root`）无法直接映射到 `src/pages` 的文件名上，或者你想指向一个不在 `src/pages` 目录下的组件。这时可以用 `beforeWriteFiles` 强制插入这条规则。
- **场景三：批量修改路由属性**
  比如你想给所有 `/admin` 开头的路由自动添加 `meta: { requiresAuth: true }`，可以在 `extendRoute` 里判断路径并统一添加。

---

 两个核心选项

| 选项                         | 作用                                     | 典型场景                               |
| :--------------------------- | :--------------------------------------- | :------------------------------------- |
| **`extendRoute(route)`**     | 遍历并修改**每一条**已生成的路由规则     | 添加别名、修改`meta`、调整路径优先级等 |
| **`beforeWriteFiles(root)`** | 在最终写入文件前，插入**额外的**路由规则 | 添加无法由文件结构直接映射的特殊路由   |

---

可以使用 `extendRoute` 或 `beforeWriteFiles` 选项在构建时扩展路由。两者都可以返回 Promise：

```js
import VueRouter from 'vue-router/vite'
import path from 'node:path'

VueRouter({
  extendRoute(route) {
    if (route.name === '/[name]') {
      route.addAlias('/hello-vite-:name')
    }
  },

  beforeWriteFiles(root) {
    root.insert('/from-root', path.join(__dirname, './src/pages/index.vue'))
  },
})
```

---

#### 组件内路由

可以直接在页面组件文件中覆盖路由配置。插件会拾取这些更改并反映在生成的 `typed-router.d.ts` 文件中。

---

##### `definePage()`

可以使用 `definePage()` 宏修改和扩展任何页面组件。这对于添加 meta 信息或修改路由对象很有用。它在 Vue 组件中全局可用，但如果需要，可以从 `vue-router` 导入它。

https://router.vuejs.org/zh/file-based-routing/extending-routes.html#definePage-

---

##### SFC `<route>` 自定义块

`<route>` 自定义块是一种扩展现有路由的方法。它可用于添加新的 `meta` 字段，覆盖 `path`、`name` 或路由中的任何其他内容。**它必须添加到 [路由文件夹](https://router.vuejs.org/zh/file-based-routing/file-based-routing.html#路由文件夹结构) 内的 `.vue` 组件中**。它类似于 [vite-plugin-pages 中的相同功能](https://github.com/hannoeru/vite-plugin-pages#sfc-custom-block-for-route-data) 以方便迁移。

https://router.vuejs.org/zh/file-based-routing/extending-routes.html#SFC-route-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9D%97

---

#### 在运行时扩展路由

作为一种权宜之计，可以在**运行时**通过简单地更改或克隆 `routes` 数组并将其传递给 `createRouter()` 之前扩展路由。由于这些更改是在运行时进行的，因此它们不会反映在生成的 `typed-router.d.ts` 文件中。

https://router.vuejs.org/zh/file-based-routing/extending-routes.html#%E5%9C%A8%E8%BF%90%E8%A1%8C%E6%97%B6%E6%89%A9%E5%B1%95%E8%B7%AF%E7%94%B1

---

### 热更新

当使用 `definePage()` 和 `<route>` 块时，可以为你的路由启用热更新 (HMR)，**在你对路由进行更改时避免重新加载页面或服务器**。

**强烈建议**启用 HMR，目前**仅适用于 Vite**。

```ts
import { createRouter, createWebHistory } from 'vue-router'
import {
  routes,
  handleHotUpdate, 
} from 'vue-router/auto-routes'

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 这将在运行时更新路由而无需重新加载页面
if (import.meta.hot) { 
  handleHotUpdate(router) 
} 
```

---

#### 运行时路由

如果你在运行时添加路由，你需要在回调中添加它们以确保它们在开发期间被添加。

```ts
import { createRouter, createWebHistory } from 'vue-router'
import { routes, handleHotUpdate } from 'vue-router/auto-routes'

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

function addRedirects() {
  router.addRoute({
    path: '/new-about',
    redirect: '/about?from=/new-about',
  })
}

if (import.meta.hot) {
  handleHotUpdate(router, (newRoutes) => { 
    addRedirects() 
  }) 
} else {
  // 生产环境
  addRedirects()
}
```

这是**可选的**，你也可以只是重新加载页面。

---

### ESLint

如果你不使用自动导入，你需要告诉 ESLint 关于 `vue-router/auto-routes` 的信息。将这些行添加到你的 eslint 配置中：

```ts
{
  "settings": {
    "import/core-modules": ["vue-router/auto-routes"]
  }
}
```

---

#### `definePage()`

由于 `definePage()` 是一个全局宏，你需要告诉 ESLint 关于它的信息。将这些行添加到你的 eslint 配置中

```ts
{
  "globals": {
    "definePage": "readonly"
  }
}
```































































































































































