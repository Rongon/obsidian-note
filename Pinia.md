# Pinia

## 介绍

### 开始

#### Store 是什么？

Store (如 Pinia) 是一个保存状态和业务逻辑的实体，它并不与你的组件树绑定。换句话说，**它承载着全局状态**。它有点像一个永远存在的组件，每个组件都可以读取和写入它。它有**三个概念**，[state](https://pinia.vuejs.org/zh/core-concepts/state.html)、[getter](https://pinia.vuejs.org/zh/core-concepts/getters.html) 和 [action](https://pinia.vuejs.org/zh/core-concepts/actions.html)，我们可以假设这些概念相当于组件中的 `data`、 `computed` 和 `methods`。

---

## 核心概念

### 定义 Store

 Store 是用 `defineStore()` 定义的，它的第一个参数要求是一个**独一无二的**名字：

```ts
import { defineStore } from 'pinia'

//  `defineStore()` 的返回值的命名是自由的
// 但最好含有 store 的名字，且以 `use` 开头，以 `Store` 结尾。
// (比如 `useUserStore`，`useCartStore`，`useProductStore`)
// 第一个参数是你的应用中 Store 的唯一 ID。
export const useAlertsStore = defineStore('alerts', {
  // 其他配置...
})
```

`defineStore()` 的第二个参数可接受两类值：Setup 函数或 Option 对象。

---

#### Option Store

选项式：

https://pinia.vuejs.org/zh/core-concepts/#option-stores

---

#### Setup Store

传入一个函数，该函数定义了一些响应式属性和方法，并且返回一个带有我们想暴露出去的属性和方法的对象。

```ts
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const name = ref('Eduardo')
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { count, name, doubleCount, increment }
})
```

---

在 *Setup Store* 中：

- `ref()` 就是 `state` 属性
- `computed()` 就是 `getters`
- `function()` 就是 `actions`

注意，要让 pinia 正确识别 `state`，你**必须**在 setup store 中返回 **`state` 的所有属性**。这意味着，你不能在 store 中使用**私有**属性。

---

Setup store 也可以依赖于全局**提供**的属性，比如路由。任何[应用层面提供](https://vuejs.org/api/application.html#app-provide)的属性都可以在 store 中使用 `inject()` 访问，就像在组件中一样：

```ts
import { inject } from 'vue'
import { useRoute } from 'vue-router'
import { defineStore } from 'pinia'

export const useSearchFilters = defineStore('search-filters', () => {
  const route = useRoute()
  // 这里假定 `app.provide('appProvided', 'value')` 已经调用过
  const appProvided = inject('appProvided')

  // ...

  return {
    // ...
  }
})
```

---

#### 使用 Store

```vue
<script setup>
import { useCounterStore } from '@/stores/counter'
// 在组件内部的任何地方均可以访问变量 `store` ✨
const store = useCounterStore()
</script>
```

你可以定义任意多的 store，但为了让使用 pinia 的益处最大化(比如允许构建工具自动进行代码分割以及 TypeScript 推断)，**你应该在不同的文件中去定义 store**。

---

请注意，`store` 是一个用 `reactive` 包装的对象，这意味着不需要在 getters 后面写 `.value`。就像 `setup` 中的 `props` 一样，**我们不能对它进行解构**：

```ts
<script setup>
import { useCounterStore } from '@/stores/counter'
import { computed } from 'vue'

const store = useCounterStore()
// ❌ 下面这部分代码不会生效，因为它的响应式被破坏了
// 与 reactive 相同: https://vuejs.org/guide/essentials/reactivity-fundamentals.html#limitations-of-reactive
const { name, doubleCount } = store
name // 将会一直是 "Eduardo"
doubleCount // 将会一直是 0
setTimeout(() => {
  store.increment()
}, 1000)
// ✅ 而这一部分代码就会维持响应式
// 💡 在这里你也可以直接使用 `store.doubleCount`
const doubleValue = computed(() => store.doubleCount)
</script>
```

---

#### 从 Store 解构

state 用 storeToRefs() 解构；而 action 直接解构：

```vue
<script setup>
import { storeToRefs } from 'pinia'
const store = useCounterStore()
// `name` 和 `doubleCount` 都是响应式引用
// 下面的代码同样会提取那些来自插件的属性的响应式引用
// 但是会跳过所有的 action 或者非响应式（非 ref 或者 非 reactive）的属性
const { name, doubleCount } = storeToRefs(store)
// 名为 increment 的 action 可以被解构
const { increment } = store
</script>
```

---

### State

在 Pinia 中，state 被定义为一个返回初始状态的函数。这使得 Pinia 可以同时支持服务端和客户端。

```ts
import { defineStore } from 'pinia'

const useStore = defineStore('storeId', {
  // 为了完整类型推理，推荐使用箭头函数
  state: () => {
    return {
      // 所有这些属性都将自动推断出它们的类型
      count: 0,
      name: 'Eduardo',
      isAdmin: true,
      items: [],
      hasChanged: true,
    }
  },
})
```

---

#### TypeScript

确保启用了 strict，Pinia 将自动推断您的状态类型！ 但是，在某些情况下，您应该帮助它进行一些转换：

```ts
const useStore = defineStore('storeId', {
  state: () => {
    return {
      // 用于初始化空列表
      userList: [] as UserInfo[],
      // 用于尚未加载的数据
      user: null as UserInfo | null,
    }
  },
})

interface UserInfo {
  name: string
  age: number
}
```

或，可以用一个接口定义 state，并添加 `state()` 的返回值的类型。

```ts
interface State {
  userList: UserInfo[]
  user: UserInfo | null
}

const useStore = defineStore('storeId', {
  state: (): State => {
    return {
      userList: [],
      user: null,
    }
  },
})

interface UserInfo {
  name: string
  age: number
}
```

---

#### 访问 `state`

```ts
const store = useStore()

store.count++
```

---

#### 重置 state

在 [Setup Stores](https://pinia.vuejs.org/core-concepts/#setup-stores) 中，您需要创建自己的 `$reset()` 方法：

```ts
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)

  function $reset() {
    count.value = 0
  }

  return { count, $reset }
})
```

---

#### 变更 state

除了用 `store.count++` 直接改变 store，你还可以调用 `$patch` 方法。它允许你用一个 `state` 的补丁对象在同一时间更改多个属性：

```ts
store.$patch({
  count: store.count + 1,
  age: 120,
  name: 'DIO',
})
```

不过，用这种语法的话，有些变更真的很难实现或者很耗时：任何集合的修改（例如，向数组中添加、移除一个元素或是做 `splice` 操作）都需要你创建一个新的集合。因此，`$patch` 方法也接受一个函数来组合这种难以用补丁对象实现的变更。

```ts
store.$patch((state) => {
  state.items.push({ name: 'shoes', quantity: 1 })
  state.hasChanged = true
})
```

---

#### 替换 `state`

**不能完全替换掉** store 的 state，因为那样会破坏其响应性。但是，你可以 *patch* 它。

```ts
// 这实际上并没有替换`$state`
store.$state = { count: 24 }
// 在它内部调用 `$patch()`：
store.$patch({ count: 24 })
```

你也可以通过变更 `pinia` 实例的 `state` 来设置整个应用的初始 state。这常用于 [SSR 中的激活过程](https://pinia.vuejs.org/zh/ssr/#state-hydration)。

```ts
pinia.state.value = {}
```

---

#### 订阅 state

可以通过 store 的 `$subscribe()` 方法侦听 state 及其变化。比起普通的 `watch()`，使用 `$subscribe()` 的好处是 *subscriptions* 在 *patch* 后只触发一次， watch() 在多个状态变化时可能会触发多次。

```ts
cartStore.$subscribe((mutation, state) => {
  // import { MutationType } from 'pinia'
  mutation.type // 'direct' | 'patch object' | 'patch function'
  // 和 cartStore.$id 一样
  mutation.storeId // 'cart'
  // 只有 mutation.type === 'patch object'的情况下才可用
  mutation.payload // 传递给 cartStore.$patch() 的补丁对象。

  // 每当状态发生变化时，将整个 state 持久化到本地存储。
  localStorage.setItem('cart', JSON.stringify(state))
})
```

---

##### 刷新时机

在底层实现上，`$subscribe()` 使用了 Vue 的 `watch()` 函数。你可以传入与 `watch()` 相同的选项。当你想要在 **每次** state 变化后立即触发订阅时很有用：

```ts
cartStore.$subscribe((mutation, state) => {
  // 每当状态发生变化时，将整个 state 持久化到本地存储
  localStorage.setItem('cart', JSON.stringify(state))
}, { flush: 'sync' })
```

---

##### 取消订阅

默认情况下，*state subscription* 会被绑定到添加它们的组件上 (如果 store 在组件的 `setup()` 里面)。这意味着，当该组件被卸载时，它们将被自动删除。如果你想在组件卸载后依旧保留它们，请将 `{ detached: true }` 作为第二个参数，以将 *state subscription* 从当前组件中*分离*：

```vue
<script setup>
const someStore = useSomeStore()
// 此订阅器即便在组件卸载之后仍会被保留
someStore.$subscribe(callback, { detached: true })
</script>
```

---

TIP

你可以在 `pinia` 实例上使用 `watch()` 函数侦听整个 state。

```
watch(
  pinia.state,
  (state) => {
    // 每当状态发生变化时，将整个 state 持久化到本地存储。
    localStorage.setItem('piniaState', JSON.stringify(state))
  },
  { deep: true }
)
```

---

### Getter

文档是选项式：

Getter 完全等同于 store 的 state 的[计算值](https://cn.vuejs.org/guide/essentials/computed.html)。可以通过 `defineStore()` 中的 `getters` 属性来定义它们。**推荐**使用箭头函数，并且它将接收 `state` 作为第一个参数：

```ts
export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
})
```

大多数时候，getter 仅依赖 state。

不过，有时它们也可能会使用其他 getter。因此，即使在使用常规函数定义 getter 时，我们也可以通过 `this` 访问到**整个 store 实例**。

**但(在 TypeScript 中)必须定义返回类型**。这是为了避免 TypeScript 的已知缺陷。

**不过这不影响用箭头函数定义的 getter，也不会影响不使用 `this` 的 getter**。

```ts
export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
  }),
  getters: {
    // 自动推断出返回类型是一个 number
    doubleCount(state) {
      return state.count * 2
    },
    // 返回类型**必须**明确设置
    doublePlusOne(): number {
      // 整个 store 的 自动补全和类型标注 ✨
      return this.doubleCount + 1
    },
  },
})
```

然后你可以直接访问 store 实例上的 getter 了：

```vue
<script setup>
import { useCounterStore } from './counterStore'

const store = useCounterStore()
</script>

<template>
  <p>Double count is {{ store.doubleCount }}</p>
</template>
```

---

#### 向 getter 传递参数

*Getter* 只是幕后的**计算**属性，所以不可以向它们传递任何参数。不过，你可以从 *getter* 返回一个函数，该函数可以接受任意参数：

```ts
export const useUserListStore = defineStore('userList', {
  getters: {
    getUserById: (state) => {
      return (userId) => state.users.find((user) => user.id === userId)
    },
  },
})
```

并在组件中使用：

```vue
<script setup>
import { useUserListStore } from './store'
const userList = useUserListStore()
const { getUserById } = storeToRefs(userList)
// 请注意，你需要使用 `getUserById.value` 来访问
// <script setup> 中的函数
</script>

<template>
  <p>User 2: {{ getUserById(2) }}</p>
</template>
```

请注意，当你这样做时，**getter 将不再被缓存**。它们只是一个被你调用的函数。

---

#### 访问其他 store 的 getter

想要使用另一个 store 的 getter 的话，那就直接在 *getter* 内使用就好：

```ts
import { useOtherStore } from './other-store'

export const useStore = defineStore('main', {
  state: () => ({
    // ...
  }),
  getters: {
    otherGetter(state) {
      const otherStore = useOtherStore()
      return state.localData + otherStore.data
    },
  },
})
```

---

#### 组合式写法：

```ts
// stores/counter.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  // state：用 ref 或 reactive 定义
  const count = ref(0)

  // getter：用 computed 定义
  const doubleCount = computed(() => count.value * 2)
  const doubleCountPlusOne = computed(() => doubleCount.value + 1)

  // action：用普通函数定义
  function increment() {
    count.value++
  }

  // 返回暴露给外部的 state、getter、action
  return { count, doubleCount, doubleCountPlusOne, increment }
})
```

---

### Action

Action 相当于组件中的 [method](https://cn.vuejs.org/api/options-state.html#methods)。它们可以通过 `defineStore()` 中的 `actions` 属性来定义，**并且它们也是定义业务逻辑的完美选择。**

```ts
export const useCounterStore = defineStore('main', {
  state: () => ({
    count: 0,
  }),
  actions: {
    increment() {
      this.count++
    },
    randomizeCounter() {
      this.count = Math.round(100 * Math.random())
    },
  },
})
```

---

#### 访问其他 store 的 action

想要使用另一个 store 的话，那你直接在 *action* 中调用就好了：

```ts
import { useAuthStore } from './auth-store'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    preferences: null,
    // ...
  }),
  actions: {
    async fetchUserPreferences() {
      const auth = useAuthStore()
      if (auth.isAuthenticated) {
        this.preferences = await fetchPreferences()
      } else {
        throw new Error('User must be authenticated')
      }
    },
  },
})
```

---

#### 订阅 action

你可以通过 `store.$onAction()` 来监听 action 和它们的结果。

传递给它的回调函数会在 action 本身之前执行。

`after` 表示在 promise 解决之后，允许你在 action 解决后执行一个回调函数。同样地，`onError` 允许你在 action 抛出错误或 reject 时执行一个回调函数。

```ts
const unsubscribe = someStore.$onAction(
  ({
    name, // action 名称
    store, // store 实例，类似 `someStore`
    args, // 传递给 action 的参数数组
    after, // 在 action 返回或解决后的钩子
    onError, // action 抛出或拒绝的钩子
  }) => {
    // 为这个特定的 action 调用提供一个共享变量
    const startTime = Date.now()
    // 这将在执行 "store "的 action 之前触发。
    console.log(`Start "${name}" with params [${args.join(', ')}].`)

    // 这将在 action 成功并完全运行后触发。
    // 它等待着任何返回的 promise
    after((result) => {
      console.log(
        `Finished "${name}" after ${
          Date.now() - startTime
        }ms.\nResult: ${result}.`
      )
    })

    // 如果 action 抛出或返回一个拒绝的 promise，这将触发
    onError((error) => {
      console.warn(
        `Failed "${name}" after ${Date.now() - startTime}ms.\nError: ${error}.`
      )
    })
  }
)

// 手动删除监听器
unsubscribe()
```

默认情况下，*action 订阅器*会被绑定到添加它们的组件上(如果 store 在组件的 `setup()` 内)。这意味着，当该组件被卸载时，它们将被自动删除。如果你想在组件卸载后依旧保留它们，请将 `true` 作为第二个参数传递给 *action 订阅器*，以便将其从当前组件中分离：

```vue
<script setup>
const someStore = useSomeStore()
// 此订阅器即便在组件卸载之后仍会被保留
someStore.$onAction(callback, true)
</script>
```

---

组合式写法其实就是写一个普通函数。

---

### 插件

可以扩展的内容：

- 为 store 添加新的属性
- 定义 store 时增加新的选项
- 为 store 增加新的方法
- 包装现有的方法
- 改变甚至取消 action
- 实现副作用，如[本地存储](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- **仅**应用插件于特定 store

---

插件是通过 `pinia.use()` 添加到 pinia 实例的。最简单的例子是通过返回一个对象将一个静态属性添加到所有 store。

```ts
import { createPinia } from 'pinia'

// 创建的每个 store 中都会添加一个名为 `secret` 的属性。
// 在安装此插件后，插件可以保存在不同的文件中
function SecretPiniaPlugin() {
  return { secret: 'the cake is a lie' }
}

const pinia = createPinia()
// 将该插件交给 Pinia
pinia.use(SecretPiniaPlugin)

// 在另一个文件中
const store = useStore()
store.secret // 'the cake is a lie'
```

这对添加全局对象很有用，如路由器、modal 或 toast 管理器。

---

#### 简介

Pinia 插件是一个函数，可以选择性地返回要添加到 store 的属性。它接收一个可选参数，即 *context*。

完整写法：

```ts
export function myPiniaPlugin(context) {
  context.pinia // 用 `createPinia()` 创建的 pinia。
  context.app // 用 `createApp()` 创建的当前应用(仅 Vue 3)。
  context.store // 该插件想扩展的 store
  context.options // 定义传给 `defineStore()` 的 store 的可选对象。
  // ...
}
```

然后用 `pinia.use()` 将这个函数传给 `pinia`：

```
pinia.use(myPiniaPlugin)
```

---

#### 扩展 Store

可以直接通过在一个插件中返回包含特定属性的对象来为每个 store 都添加上特定属性：

```ts
pinia.use(() => ({ hello: 'world' }))// 这是简单属性的简单写法
```

也可以直接在 `store` 上设置该属性，但**可以的话，请使用返回对象的方法，这样它们就能被 devtools 自动追踪到**：

```ts
// 通用可扩展复杂写法
pinia.use(({ store }) => {
  store.hello = 'world'
})
```

如果你想在 devtools 中调试 `hello` 属性，为了使 devtools 能追踪到 `hello`，请确保**在 dev 模式下**将其添加到 `store._customProperties` 中：

```ts
// 上文示例
pinia.use(({ store }) => {
  store.hello = 'world'
  // 确保你的构建工具能处理这个问题，webpack 和 vite 在默认情况下应该能处理。
  if (process.env.NODE_ENV === 'development') {
    // 添加你在 store 中设置的键值
    store._customProperties.add('hello')
  }
})
```

---

##### 添加新的 state

如果你想给 store 添加新的 state 属性，**你必须同时在两个地方添加它**。。

- 在 `store` 上，然后你才可以用 `store.myState` 访问它。
- 在 `store.$state` 上，然后你才可以在 devtools 中使用它。

```ts
import { toRef, ref } from 'vue'

pinia.use(({ store }) => {
  // 步骤 1：避免重复添加
  if (!store.$state.hasOwnProperty('hasError')) {
    // 步骤 2：创建响应式数据
    const hasError = ref(false)
    // 步骤 3：将 ref 挂到 $state 上（为了 SSR 和 devtools）
    store.$state.hasError = hasError
  }
  // 步骤 4：将 $state 上的 ref 映射到 store 上（为了直接访问）
  store.hasError = toRef(store.$state, 'hasError')
})
```

需要注意的是，在一个插件中， state 变更或添加(包括调用 `store.$patch()`)都是发生在 store 被激活之前，**因此不会触发任何订阅函数**。

---

##### 重置插件中添加的 state

默认情况下，`$reset()` 不会重置插件添加的 state，但你可以重写它来重置你添加的 state：

```ts
import { toRef, ref } from 'vue'

pinia.use(({ store }) => {
  // 和上面的代码一样，只是为了参考
  if (!store.$state.hasOwnProperty('hasError')) {
    const hasError = ref(false)
    store.$state.hasError = hasError
  }
  store.hasError = toRef(store.$state, 'hasError')

  // 确认将上下文 (`this`) 设置为 store
  const originalReset = store.$reset.bind(store)

  // 覆写其 $reset 函数
  return {
    $reset() {
      originalReset()
      store.hasError = false
    },
  }
})
```

---

#### 添加新的外部属性

当添加外部属性、第三方库的类实例或非响应式的简单值时，你应该先用 `markRaw()` 来包装一下它，再将它传给 pinia。下面是一个在每个 store 中添加路由器的例子：

```ts
import { markRaw } from 'vue'
// 根据你的路由器的位置来调整
import { router } from './router'

pinia.use(({ store }) => {
  store.router = markRaw(router)
})
```

---

#### 添加新的选项

在定义 store 时，可以创建新的选项。例如，你可以创建一个 `debounce` 选项，允许你让任何 action 实现防抖。

```ts
defineStore('search', {
  actions: {
    searchContacts() {
      // ...
    },
  },

  // 这将在后面被一个插件读取
  debounce: {
    // 让 action searchContacts 防抖 300ms
    searchContacts: 300,
  },
})
```

然后，该插件可以读取该选项来包装 action，并替换原始 action：

```ts
// 使用任意防抖库
import debounce from 'lodash/debounce'

pinia.use(({ options, store }) => {
  if (options.debounce) {
    // 我们正在用新的 action 来覆盖这些 action
    return Object.keys(options.debounce).reduce((debouncedActions, action) => {
      debouncedActions[action] = debounce(
        store[action],
        options.debounce[action]
      )
      return debouncedActions
    }, {})
  }
})
```

 setup 语法，自定义选项作为第 3 个参数传递：

```ts
defineStore(
  'search',
  () => {
    // ...
  },
  {
    // 这将在后面被一个插件读取
    debounce: {
      // 让 action searchContacts 防抖 300ms
      searchContacts: 300,
    },
  }
)
```

---

#### TypeScript

##### 标注插件类型

Pinia 插件可按如下方式实现类型标注：

```ts
import { PiniaPluginContext } from 'pinia'

export function myPiniaPlugin(context: PiniaPluginContext) {
  // ...
}
```

---

##### 为新的 store 属性添加类型

当在 store 中添加新的属性时，你也应该扩展 `PiniaCustomProperties` 接口。

```ts
import 'pinia'

declare module 'pinia' {
  export interface PiniaCustomProperties {
    // 通过使用一个 setter，我们可以允许字符串和引用。
    set hello(value: string | Ref<string>)
    get hello(): string

    // 你也可以定义更简单的值
    simpleNumber: number

    // 添加路由(#adding-new-external-properties)
    router: Router
  }
}
```

---

然后，就可以安全地写入和读取它了：

```ts
pinia.use(({ store }) => {
  store.hello = 'Hola'
  store.hello = ref('Hola')

  store.simpleNumber = Math.random()
  // @ts-expect-error: we haven't typed this correctly
  store.simpleNumber = ref(Math.random())
})
```

可以通过使用 `PiniaCustomProperties` 的4种通用类型来为 $options 标注类型：

```ts
import 'pinia'

declare module 'pinia' {
  export interface PiniaCustomProperties<Id, S, G, A> {
    $options: {
      id: Id
      state?: () => S
      getters?: G
      actions?: A
    }
  }
}
```

下面是每个字母代表的含义：

- S: State
- G: Getters
- A: Actions
- SS: Setup Store / Store

---

##### 为新的 state 添加类型

当添加新的 state 属性(包括 `store` 和 `store.$state` )时，你需要将类型添加到 `PiniaCustomStateProperties` 中。

与 `PiniaCustomProperties` 不同的是，它只接收 `State` 泛型：

```ts
import 'pinia'

declare module 'pinia' {
  export interface PiniaCustomStateProperties<S> {
    hello: string
  }
}
```

---

##### 为新的定义选项添加类型

当为 `defineStore()` 创建新选项时，你应该扩展 `DefineStoreOptionsBase`。

与 `PiniaCustomProperties` 不同的是，它只暴露了两个泛型：State 和 Store 类型，允许你限制定义选项的可用类型。

例如，你可以使用 action 的名称：

```ts
import 'pinia'

declare module 'pinia' {
  export interface DefineStoreOptionsBase<S, Store> {
    // 任意 action 都允许定义一个防抖的毫秒数
    debounce?: Partial<Record<keyof StoreActions<Store>, number>>
  }
}
```

---

#### Nuxt

当[在 Nuxt 中使用 pinia](https://pinia.vuejs.org/zh/ssr/nuxt.html) 时，你必须先创建一个 [Nuxt 插件](https://nuxt.com/docs/guide/directory-structure/plugins)。这样你才能访问到 `pinia` 实例：

```ts
// plugins/myPiniaPlugin.js
import { PiniaPluginContext } from 'pinia'
import { Plugin } from '@nuxt/types'

function MyPiniaPlugin({ store }: PiniaPluginContext) {
  store.$subscribe((mutation) => {
    // 响应 store 变更
    console.log(`[🍍 ${mutation.storeId}]: ${mutation.type}.`)
  })

  // 请注意，如果你使用的是 TS，则必须添加类型。
  return { creationTime: new Date() }
}

const myPlugin: Plugin = ({ $pinia }) => {
  $pinia.use(MyPiniaPlugin)
}

export default myPlugin
```

---

### 服务端渲染 (SSR)

暂时看不懂，学了SSR后回来补充。

https://pinia.vuejs.org/zh/ssr/#server-side-rendering-ssr

---











































































































































