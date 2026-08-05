# vue3

npm init vue@latest

优点：

![image-20231221025140113](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231221025140113.png)

## 组合式API(compositionAPI)

​	相同功能的所有内容封装在一起，不用滚上滚下，难以维护。

![image-20231221031335332](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231221031335332.png)

---

### 生命周期

![组件生命周期图示](https://cn.vuejs.org/assets/lifecycle_zh-CN.W0MNXI0C.png)

	1. setup直接写在script就是setup
	2. onMounted(() => {})以函数形式声明，可以写多个

---

### setup语法糖

	1. 执行时机：比beforeCreate还早
	2. setup函数内获取不到this（this是undefined）
		好处：不用再管this指向哪个实例，便于使用compositionAPI
	3. setup语法糖简化了return代码

---

### ref()响应式

​	数据本身不是响应式的，如果想要响应式，使用ref()

```vue
import { ref } from 'vue'
const count = ref(0)
const setCount = () => {
	count.value++
}

<div>{{count}}</div>
<button @click="setCount">+1</button>
```

	1. ref既可以接收简单类型，也可以接收复杂类型
	2. 本质上是在外层包了一层对象，再借助reactive实现响应式
	3. 在脚本中使用需要.value，在模板中使用不需要.value

---

### computed

​	语法不同：

```vue
import { computed } from 'vue'
const computedList = computed( () => {
	xxx
})
```

​	**计算属性应该是只读的，特殊情况需要配置get set**

---

### computed VS function

​	不经常变的用computed，经常变化的用function

---

### watch

​	侦听一个或多个数据变化，变化时执行回调函数。

1. 单个数据

```
import xxx
watch(count, (newValue, oldValue) => {
	log(${newValue}, ${oldValue})
})
```

2. 多个数据

```
import xxx
watch([ref1, ref2], (newArr, oldArr) => {
	log(${newArr}, ${oldArr})
})
```

3. immediate 立即执行

```
import xxx
watch(count, (newValue, oldValue) => {
	log(${newValue}, ${oldValue})
},{
	immediate: true
})
```

4. deep深度监视(复杂类型、对象)

```
watch(userInfo, (newValue) => {
	log(newValue)
},{
	deep: true
})
```

5. deep精确监视(固定写法)

```
watch(() => userInfo.value.age, (newValue, oldValue) => {
	log(xxx)
})
```

---

### 父子通信

1. 父传子（通过属性）

![image-20231224041443720](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224041443720.png)

2. 子传父（通过事件）

![image-20240512133605145](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240512133605145.png)

![image-20231224041522637](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224041522637.png)

---

### 模板引用

​	**通过ref获取dom或者组件**

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224042538420.png" alt="image-20231224042538420" style="zoom:50%;" />

​	**默认setup语法糖下组件内部的属性和方法是不开放的，若要开放，使用definedExpose()编译宏指定**

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224042756406.png" alt="image-20231224042756406" style="zoom: 67%;" />

---

### 透传 Attribute

https://cn.vuejs.org/guide/components/attrs.html

1. 如果你**不想要**一个组件自动地继承 attribute，你可以在组件选项中设置 `inheritAttrs: false`。

2. 这些透传进来的 attribute 可以在模板的表达式中直接用 `$attrs` 访问到。

3. 和 props 有所不同，透传 attributes 在 JavaScript 中保留了它们原始的大小写，所以像 `foo-bar` 这样的一个 attribute 需要通过 `$attrs['foo-bar']` 来访问。

4. 像 `@click` 这样的一个 `v-on` 事件监听器将在此对象下被暴露为一个函数 `$attrs.onClick`。

5. 多根节点的 Attributes 继承需要$attr显示绑定

6. 可以在 `<script setup>` 中使用 `useAttrs()` API 来访问一个组件的所有透传 attribute：

7. 

---

### 插槽slot

​	1. 通过使用插槽，`<FancyButton>` 仅负责渲染外层的 `<button>` (以及相应的样式)，而其内部的内容由父组件提供。

![插槽图示](https://cn.vuejs.org/assets/slots.CKcE8XYd.png)

2. 插槽内容可以访问到父组件的数据作用域，**无法访问**子组件的数据。

```vue
<span>{{ message }}</span>
<FancyButton>{{ message }}</FancyButton>
```

3. `v-slot` 有对应的简写 `#`，因此 `<template v-slot:header>` 可以简写为 `<template #header>`。
4. 可以结合使用 `$slots` 属性与 `v-if` 来实现**条件插槽**
5. 作用域插槽：父组件使用插槽传递过来的数据 `v-slot="slotProps"`

![scoped slots diagram](https://cn.vuejs.org/assets/scoped-slots.B67tIPc5.svg)

---

### provide/inject

1. 传递普通数据/响应式

顶：

```
provide('key', 数据)
```

底：

```
const message = inject('key')
```

2. 传递方法

```
const countAdd = () => {
	count.value++
}
provide('countAdd-btn', countAdd)
```

```
const setCount = inject('countAdd-btn')
```

3. 如果构建大型应用，包含非常多依赖提供，建议使用 Symbol 来作为注入名以避免潜在的冲突。

```
// keys.js
export const myInjectionKey = Symbol()
```

---

### defineOptions({}) /3.3.x

​	setup语法使得我们很难去定义和setup平级的属性(如：optionsAPI)，此时就可以用defineOptions({})

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224051156556.png" alt="image-20231224051156556" style="zoom:67%;" />

### 异步组件

​	在大型项目中，可能需要拆分应用为更小的块，并仅在需要时再从服务器加载相关组件。Vue 提供了 `defineAsyncComponent` 方法来实现此功能：

```js
import { defineAsyncComponent } from 'vue'

const AsyncComp = defineAsyncComponent(() => {
  return new Promise((resolve, reject) => {
    // ...从服务器获取组件
    resolve(/* 获取到的组件 */)
  })
})
// ... 像使用其他一般组件一样使用 `AsyncComp`
```

---

### 组合式函数（重点）

​	核心逻辑完全一致，只是把它移到一个外部函数中去，并返回需要暴露的状态。和在组件中一样，你也可以在组合式函数中使用所有的组合式 API。现在，`useMouse()` 的功能可以在任何组件中轻易复用了。

```javascript
// mouse.js
import { ref, onMounted, onUnmounted } from 'vue'

// 按照惯例，组合式函数名以“use”开头
export function useMouse() {
  // 被组合式函数封装和管理的状态
  const x = ref(0)
  const y = ref(0)

  // 组合式函数可以随时更改其状态。
  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  // 一个组合式函数也可以挂靠在所属组件的生命周期上
  // 来启动和卸载副作用
  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  // 通过返回值暴露所管理的状态
  return { x, y }
}
```

```vue
<script setup>
import { useMouse } from './mouse.js'

const { x, y } = useMouse()
</script>

<template>Mouse position is at: {{ x }}, {{ y }}</template>
```

1. 响应式参数

​	响应式对象用 `watchEffect()`/`watch()` 和 `toValue()`API 实践：

​	`toValue()` 可以将 ref 或 getter 规范化为值。如果参数是 ref，它会返回 ref 的值；如果参数是函数，它会调用函数并返回其返回值。否则，它会原样返回参数。

```
toValue(1) //       --> 1
toValue(ref(1)) //  --> 1
toValue(() => 1) // --> 1
```

​	 `watchEffect()` 立即运行一个函数，同时响应式地追踪其依赖，并在依赖更改时重新执行。

​	如果输入参数是 ref 或 getter 的情况下创建了响应式 effect，为了能够被正确追踪，要么使用 `watch()` 显式地监视 ref 或 getter，要么在 `watchEffect()` 中调用 `toValue()`。

---

### 自定义指令

1. 用法

```vue
<script setup>
// 在模板中启用 v-focus
const vFocus = {
  mounted: (el) => el.focus()
}
</script>

<template>
  <input v-focus />
</template>
```

2. 全局注册

```js
const app = createApp({})

// 使 v-focus 在所有组件中都可用
app.directive('focus', {
  /* ... */
})
```

3. 自定义指令也有钩子（生命周期）/没有beforeCreated

4. 钩子的参数

​	log(el)查看细节

​	https://cn.vuejs.org/guide/reusability/custom-directives.html#directive-hooks

5. 不推荐在组件上使用自定义指令

```vue
<MyComponent v-demo="test" />
```



---

# pinia

**相比于vuex，只有state，actions(支持异步)，getters**

**(比如 `useUserStore`，`useCartStore`，`useProductStore`)**

## 组合式基本语法

	1. state/数据/方法

​	选项式(优先)：

```js
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: {
    double: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
  },
})
```

​	组合式：

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224055146351.png" alt="image-20231224055146351" style="zoom:50%;" />

2. actions

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231224055848855.png" alt="image-20231224055848855" style="zoom:50%;" />

3. getter

---

### 解构

​	state其底层是用reactive实现的，如果解构会失去响应式，如果想保留响应式，使用storeToRefs()

```
const { name, doubleCount } = storeToRefs(store)
```

​	action可以直接解构

```
const { fn } = store
```

---

### 持久化

https://prazdevs.github.io/pinia-plugin-persistedstate/zh/guide/

---

# VueRouter

## 创建路由器实例

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

## 注册路由器插件

```js
createApp(App)
  .use(router)
  .mount('#app')
```

---

# 2026

## 基础

### 模板语法

#### 指令Directives

![image-20260415103523996](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260415103523996.png)

---

### 响应式基础

#### DOM更新时机

当你修改了响应式状态时，DOM 会被自动更新。但是需要注意的是，DOM 更新不是同步的。Vue 会在“next tick”更新周期中缓冲所有状态的修改，以确保不管你进行了多少次状态修改，每个组件都只会被更新一次。

要等待 DOM 更新完成后再执行额外的代码，可以使用 [nextTick()](https://cn.vuejs.org/api/general.html#nexttick) 全局 API：

```js
import { nextTick } from 'vue'

async function increment() {
  count.value++
  await nextTick()
  // 现在 DOM 已经更新了
}
```

---

### 计算属性

#### 基础

作用/使用场景：使用**计算属性**来描述依赖响应式状态的复杂逻辑。一个对象内部属性值复杂，有些地方又要引用这个值，导致代码臃肿时，用计算属性。

```vue
<script setup>
import { reactive, computed } from 'vue'

const author = reactive({
  name: 'John Doe',
  books: [
    'Vue 2 - Advanced Guide',
    'Vue 3 - Basic Guide',
    'Vue 4 - The Mystery'
  ]
})

// 一个计算属性 ref
const publishedBooksMessage = computed(() => {
  return author.books.length > 0 ? 'Yes' : 'No'
})
</script>

<template>
  <p>Has published books:</p>
  <span>{{ publishedBooksMessage }}</span>
</template>
```

---

#### 计算属性 vs 方法

计算属性会缓存，只要值不变，就不会执行，减少消耗；而方法每次都会执行

---

#### 可写计算属性

计算属性默认是只读的。特殊场景需要修改的话：

```vue
<script setup>
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')

const fullName = computed({
  // getter
  get() {
    return firstName.value + ' ' + lastName.value
  },
  // setter
  set(newValue) {
    // 注意：我们这里使用的是解构赋值语法
    [firstName.value, lastName.value] = newValue.split(' ')
  }
})
</script>
```

---

#### 获取上一个值（暂时不看）

https://cn.vuejs.org/guide/essentials/computed.html#previous

---

#### 最佳实践

Getter 不应有副作用

计算属性的 getter 应只做计算而没有任何其他的副作用，这一点非常重要，请务必牢记。举例来说，**不要改变其他状态、在 getter 中做异步请求或者更改 DOM**！一个计算属性的声明中描述的是如何根据其他值派生一个值。因此 getter 的职责应该仅为计算和返回该值。

---

### 类与样式绑定

#### 绑定HTML class

```vue
<div :class="{ active: isActive }"></div>
```

---

可以绑定一个返回对象的[计算属性](https://cn.vuejs.org/guide/essentials/computed.html)。这是一个常见且很有用的技巧：

```vue
const isActive = ref(true)
const error = ref(null)

const classObject = computed(() => ({
  active: isActive.value && !error.value,
  'text-danger': error.value && error.value.type === 'fatal'
}))

<div :class="classObject"></div>
```

---

#### 绑定内联样式

直接绑定一个样式对象通常是一个好主意，这样可以使模板更加简洁：

```vue
const styleObject = reactive({
  color: 'red',
  fontSize: '30px'
})

<div :style="styleObject"></div>

<div :style="{ color: activeColor, fontSize: fontSize + 'px' }"></div>
```

---

### 条件渲染

#### v-if vs v-show

`v-if` 有更高的切换开销，而 `v-show` 有更高的初始渲染开销。因此，如果需要频繁切换，则使用 `v-show` 较好；如果在运行时绑定条件很少改变，则 `v-if` 会更合适。

---

### 列表渲染

#### v-for

`v-for` 指令的值需要使用 `item in items` 形式的特殊语法

```vue
<li v-for="(item, index) in items">
  {{ parentMessage }} - {{ index }} - {{ item.message }}
</li>
```

也可以在定义 `v-for` 的变量别名时使用解构，和解构函数参数类似：

```vue
<li v-for="{ message } in items">
  {{ message }}
</li>

<!-- 有 index 索引时 -->
<li v-for="({ message }, index) in items">
  {{ message }} {{ index }}
</li>
```

---

### 事件处理

#### 在内联处理器中调用方法

```vue
function say(message) {
  alert(message)
}

<button @click="say('hello')">Say hello</button>
<button @click="say('bye')">Say bye</button>
```

---

#### 在内联事件处理器中访问事件参数

有时我们需要在内联事件处理器中访问原生 DOM 事件。

可以向该处理器方法传入一个特殊的 `$event` 变量，或者使用内联箭头函数：

```vue
<!-- 使用特殊的 $event 变量 -->
<button @click="warn('Form cannot be submitted yet.', $event)">
  Submit
</button>

<!-- 使用内联箭头函数 -->
<button @click="(event) => warn('Form cannot be submitted yet.', event)">
  Submit
</button>

function warn(message, event) {
  // 这里可以访问原生事件
  if (event) {
    event.preventDefault()
  }
  alert(message)
}
```

---

#### 事件修饰符

`.capture`、`.once` 和 `.passive` 修饰符与[原生 `addEventListener` 事件](https://developer.mozilla.org/zh-CN/docs/Web/API/EventTarget/addEventListener#options)相对应：

```vue
<!-- 添加事件监听器时，使用 `capture` 捕获模式 -->
<!-- 例如：指向内部元素的事件，在被内部元素处理前，先被外部处理 -->
<div @click.capture="doThis">...</div>

<!-- 点击事件最多被触发一次 -->
<a @click.once="doThis"></a>

<!-- 滚动事件的默认行为 (scrolling) 将立即发生而非等待 `onScroll` 完成 -->
<!-- 以防其中包含 `event.preventDefault()` -->
<div @scroll.passive="onScroll">...</div>
```

---

### 表单输入绑定

在前端处理表单时，我们常常需要将表单输入框的内容同步给 JavaScript 中相应的变量。手动连接值绑定和更改事件监听器可能会很麻烦：

```vue
<input
  :value="text"
  @input="event => text = event.target.value">
```

`v-model` 指令帮我们简化了这一步骤：

```vue
<input v-model="text">
```

---

#### 基本用法

- 文本

```vue
<p>Message is: {{ message }}</p>
<input v-model="message" placeholder="edit me" />
```
- 可以将多个复选框绑定到同一个数组或[集合](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)的值：

```vue
const checkedNames = ref([])

<div>Checked names: {{ checkedNames }}</div>

<input type="checkbox" id="jack" value="Jack" v-model="checkedNames" />
<label for="jack">Jack</label>

<input type="checkbox" id="john" value="John" v-model="checkedNames" />
<label for="john">John</label>

<input type="checkbox" id="mike" value="Mike" v-model="checkedNames" />
<label for="mike">Mike</label>
```

`checkedNames` 数组将始终包含所有当前被选中的框的值。

---

#### 值绑定

```vue
<input
  type="checkbox"
  v-model="toggle"
  true-value="yes"
  false-value="no" />
```

`true-value` 和 `false-value` 是 Vue 特有的 attributes，仅支持和 `v-model` 配套使用。这里 `toggle` 属性的值会在选中时被设为 `'yes'`，取消选择时设为 `'no'`。你同样可以通过 `v-bind` 将其绑定为其他动态值：

```vue
<input
  type="checkbox"
  v-model="toggle"
  :true-value="dynamicTrueValue"
  :false-value="dynamicFalseValue" />
```

---

### 侦听器 watch

#### 基础示例

需要在状态变化时执行一些“副作用”：例如更改 DOM，或是根据异步操作的结果去修改另一处的状态。

在组合式 API 中，我们可以使用 [`watch` 函数](https://cn.vuejs.org/api/reactivity-core.html#watch)在每次响应式状态发生变化时触发回调函数：

```vue
<script setup>
import { ref, watch } from 'vue'

const question = ref('')
const answer = ref('Questions usually contain a question mark. ;-)')
const loading = ref(false)

// 可以直接侦听一个 ref
watch(question, async (newQuestion, oldQuestion) => {
  if (newQuestion.includes('?')) {
    loading.value = true
    answer.value = 'Thinking...'
    try {
      const res = await fetch('https://yesno.wtf/api')
      answer.value = (await res.json()).answer
    } catch (error) {
      answer.value = 'Error! Could not reach the API. ' + error
    } finally {
      loading.value = false
    }
  }
})
</script>

<template>
  <p>
    Ask a yes/no question:
    <input v-model="question" :disabled="loading" />
  </p>
  <p>{{ answer }}</p>
</template>
```

`watch` 的第一个参数可以是不同形式的“数据源”：它可以是一个 ref (包括计算属性)、一个响应式对象、一个 [getter 函数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/get#description)、或多个数据源组成的数组：

注意，你不能直接侦听响应式对象的属性值，例如:

```js
const obj = reactive({ count: 0 })

// 错误，因为 watch() 得到的参数是一个 number
watch(obj.count, (count) => {
  console.log(`Count is: ${count}`)
})
```

这里需要用一个返回该属性的 getter 函数：

```js
// 提供一个 getter 函数
watch(
  () => obj.count,
  (count) => {
    console.log(`Count is: ${count}`)
  }
)
```

---

#### 深层侦听器

**传入响应式对象，自动深度监听；传入函数，默认只监听引用变化，加 `deep: true` 才能深度监听。**

---

#### 立即执行侦听器

`watch` 默认是懒执行的：仅当数据源变化时，才会执行回调。但在某些场景中，我们希望在创建侦听器时，立即执行一遍回调。举例来说，我们想请求一些初始数据，然后在相关状态更改时重新请求数据。

我们可以通过传入 `immediate: true` 选项来强制侦听器的回调立即执行：

```js
watch(
  source,
  (newValue, oldValue) => {
    // 立即执行，且当 `source` 改变时再次执行
  },
  { immediate: true }
)
```

---

#### 一次性侦听器

{ once: true }

---

#### `watchEffect()`

`watchEffect()` 允许我们自动跟踪回调的响应式依赖。上面的侦听器可以重写为：

```js
watchEffect(async () => {
  const response = await fetch(
    `https://jsonplaceholder.typicode.com/todos/${todoId.value}`
  )
  data.value = await response.json()
})
```

在执行期间，它会自动追踪 `todoId.value` 作为依赖(和计算属性类似)。每当 `todoId.value` 变化时，回调会再次执行。

对于这种只有一个依赖项的例子来说，`watchEffect()` 的好处相对较小。但是对于有多个依赖项的侦听器来说，使用 `watchEffect()` 可以消除手动维护依赖列表的负担。

此外，如果你需要侦听一个嵌套数据结构中的几个属性，`watchEffect()` 可能会比深度侦听器更有效，因为它将只跟踪回调中被使用到的属性，而不是递归地跟踪所有的属性。

---

#### `watch` vs. `watchEffect`

`watch` 和 `watchEffect` 都能响应式地执行有副作用的回调。它们之间的主要区别是追踪响应式依赖的方式：

- `watch` 只追踪明确侦听的数据源。它不会追踪任何在回调中访问到的东西。另外，仅在数据源确实改变时才会触发回调。`watch` 会避免在发生副作用时追踪依赖，因此，我们能更加精确地控制回调函数的触发时机。
- `watchEffect`，则会在副作用发生期间追踪依赖。它会在同步执行过程中，自动追踪所有能访问到的响应式属性。这更方便，而且代码往往更简洁，但有时其响应性依赖关系会不那么明确。

---

#### 副作用清理

情景：**“快速切换导致数据错乱”**	不用担心用户手快导致页面数据错乱	侦听的值变化频繁（搜索框联想、下拉选择加载详情、分页切换），并且伴随 API 请求	**这个异步操作的结果回来时，会不会因为数据已经过时而对页面造成负面影响？**	用户快速输入 "a" -> "ab" -> "abc"，三个请求发出。如果 "a" 的请求最慢返回，页面上最终显示的会是 "a" 的建议词，与当前输入框里的 "abc" 完全不匹配。	**调用 API 并更新页面数据**	**只有当你害怕“过时的数据回来污染现在的状态”时，才需要写清理函数。** 如果你写的异步操作即使晚回来也不会对界面造成任何可见错误，那就不用写。

```js
import { watch, onWatcherCleanup } from 'vue'

watch(id, (newId) => {
  // AbortController()是js的api，推荐使用。
  const controller = new AbortController()

  fetch(`/api/${newId}`, { signal: controller.signal }).then(() => {
    // 回调逻辑
  })

  onWatcherCleanup(() => {
    // 终止过期请求
    controller.abort()
  })
})
```

注意：在回调**一开始**就注册清理函数。等发完请求才注册，那就晚了。

```js
watch(id, async (newId) => {
  const controller = new AbortController()
  
  // ✅ 立即注册，还没发请求就先准备好刹车
  onWatcherCleanup(() => controller.abort())
  
  const res = await fetch(...)
})
```

```js
watch(id, async (newId) => {
  const res = await fetch(...)
  // ❌ 等数据回来了才注册，中间如果 id 变了根本来不及取消
  onWatcherCleanup(() => {})
})
```

3.5以下兼容：

```js
watch(id, (newId, oldId, onCleanup) => {
  // ...
  onCleanup(() => {
    // 清理逻辑
  })
})

watchEffect((onCleanup) => {
  // ...
  onCleanup(() => {
    // 清理逻辑
  })
})
```

---

#### 回调的触发时机

默认情况下，侦听器回调会在父组件更新 (如有) **之后**、所属组件的 DOM 更新**之前**被调用。

凡是需要在数据变化后**测量或操作 DOM** 的场景，一律用 `flush: 'post'`

---

Post Watchers：

如果想在侦听器回调中能访问被 Vue 更新**之后**的所属组件的 DOM，你需要指明 `flush: 'post'` 选项：

```js
watch(source, callback, {
  flush: 'post'
})

watchEffect(callback, {
  flush: 'post'
})
```

别名 `watchPostEffect()`：

```js
import { watchPostEffect } from 'vue'

watchPostEffect(() => {
  /* 在 Vue 更新后执行 */
})
```

同步侦听器（谨慎使用）：

flush: 'sync'	别名：`watchSyncEffect()`：

默认 `pre` 是“**攒一波再处理**”（性能好）；`sync` 是“**零延迟、单线程阻塞式处理**”（除了极特殊情况，**不要用**）。

---

#### 停止侦听器

在大多数情况下，你无需关心怎么停止一个侦听器。

侦听器必须用**同步**语句创建：如果用异步回调创建一个侦听器，那么它不会绑定到当前组件上，你必须手动停止它，以防内存泄漏。

```vue
<script setup>
import { watchEffect } from 'vue'

// 它会自动停止
watchEffect(() => {})

// ...这个则不会！
setTimeout(() => {
  watchEffect(() => {})
}, 100)
</script>
```

要手动停止一个侦听器，请调用 `watch` 或 `watchEffect` 返回的函数：

```js
const unwatch = watchEffect(() => {})

// ...当该侦听器不再需要时
unwatch()
```

注意，需要异步创建侦听器的情况很少，请尽可能选择同步创建。如果需要等待一些异步数据，你可以使用条件式的侦听逻辑：

```js
// 需要异步请求得到的数据
const data = ref(null)

watchEffect(() => {
  if (data.value) {
    // 数据加载后执行某些操作...
  }
})
```

---

### 模板引用：ref

#### 访问模板引用

在组合式 API 中获取引用，我们可以使用辅助函数 `useTemplateRef()`

```vue
<script setup>
import { useTemplateRef, onMounted } from 'vue'

// 第一个参数必须与模板中的 ref 值匹配
const input = useTemplateRef('my-input')

onMounted(() => {
  input.value.focus()
})
</script>

<template>
  <input ref="my-input" />
</template>
```

只可以**在组件挂载后**才能访问模板引用。如果你想在模板中的表达式上访问 `input`，在初次渲染时会是 `null`。

3.5前的兼容：

```vue
<script setup>
import { ref, onMounted } from 'vue'

// 声明一个 ref 来存放该元素的引用
// 必须和模板里的 ref 同名
const input = ref(null)

onMounted(() => {
  input.value.focus()
})
</script>

<template>
  <input ref="input" />
</template>
```

如果不使用 `<script setup>`，需确保从 `setup()` 返回 ref：

```js
export default {
  setup() {
    const input = ref(null)
    // ...
    return {
      input
    }
  }
}
```

如果你需要侦听一个模板引用 ref 的变化，确保考虑到其值为 `null` 的情况：

```js
watchEffect(() => {
  if (input.value) {
    input.value.focus()
  } else {
    // 此时还未挂载，或此元素已经被卸载(例如通过 v-if 控制)
  }
})
```

---

#### 组件上的ref

大多数情况下，你应该首先使用标准的 props 和 emit 接口来实现父子组件交互。

---

#### v-for 中的模板引用

当在 `v-for` 中使用模板引用时，对应的 ref 中包含的值是一个数组，它将在元素被挂载后包含对应整个列表的所有元素：

```vue
<script setup>
import { ref, useTemplateRef, onMounted } from 'vue'

const list = ref([
  /* ... */
])

const itemRefs = useTemplateRef('items')

onMounted(() => console.log(itemRefs.value))
</script>

<template>
  <ul>
    <li v-for="item in list" ref="items">
      {{ item }}
    </li>
  </ul>
</template>
```

兼容3.5 前的用法：

需要声明一个与模板引用 attribute 同名的 ref。该 ref 的值需要是一个数组。

```vue
<script setup>
import { ref, onMounted } from 'vue'

const list = ref([
  /* ... */
])

const itemRefs = ref([])

onMounted(() => console.log(itemRefs.value))
</script>

<template>
  <ul>
    <li v-for="item in list" ref="itemRefs">
      {{ item }}
    </li>
  </ul>
</template>
```

ref 数组**并不**保证与源数组相同的顺序。

---

#### 函数模板引用

`ref` attribute 还可以绑定为一个函数，会在每次组件更新时都被调用。该函数会收到元素引用作为其第一个参数：

```vue
<input :ref="(el) => { /* 将 el 赋值给一个数据属性或 ref 变量 */ }">
```

这里需要使用动态的 `:ref` 绑定才能够传入一个函数。当绑定的元素被卸载时，函数也会被调用一次，此时的 `el` 参数会是 `null`。

---

### 组件基础

#### 传递 props（父传子）

[`defineProps`](https://cn.vuejs.org/api/sfc-script-setup.html#defineprops-defineemits) 宏：

```vue
<script setup>
defineProps(['title'])
</script>

<BlogPost title="My journey with Vue" />
<BlogPost title="Blogging with Vue" />
<BlogPost title="Why Vue is so fun" />
```

如果没有使用 `<script setup>`，props 必须以 `props` 选项的方式声明，props 对象会作为 `setup()` 函数的第一个参数被传入：

```js
export default {
  props: ['title'],
  setup(props) {
    console.log(props.title)
  }
}
```

在实际应用中，我们可能在父组件中会有如下的一个博客文章数组，这种情况下，我们可以使用 `v-for` 来渲染它们：

```vue
const posts = ref([
  { id: 1, title: 'My journey with Vue' },
  { id: 2, title: 'Blogging with Vue' },
  { id: 3, title: 'Why Vue is so fun' }
])

<BlogPost
  v-for="post in posts"
  :key="post.id"
  :title="post.title"
 />
```

示例：

```vue
// 父组件
<template>
  <div>
    <h2>父组件</h2>
    <button @click="parentCount++">增加计数</button>
    <!-- 2. 通过属性向子组件传递数据 -->
    <Child :count="parentCount" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Child from './components/ChildComponent.vue'

const parentCount = ref(0)
</script>
```

```vue
// 子组件
<template>
  <div>
    <h4>子组件</h4>
    <p>接收到的数字：<strong>{{ count }}</strong></p>
  </div>
</template>

<script setup lang="ts">
// 1. 使用 defineProps 声明接收的属性
defineProps({
  count: {
    type: Number
  }
})
</script>
```



---

#### 监听事件（子传父）

$emit()

示例：

```vue
// 子组件
<template>
  <div>
    <h4>子组件</h4>
    <button @click="decrease">减少计数</button>
    <button @click="$emit('decrease')">减少计数</button>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(['decrease'])

const decrease = () => {
  emit('decrease')
}
</script>
```

```vue
// 父组件
<template>
  <div>
    <h2>父组件</h2>
    <p>当前数字：<strong>{{ count }}</strong></p>
    <Child @decrease="count--" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Child from './components/ChildComponent.vue'

const count = ref(0)
</script>
```

---

#### 插槽基础

像 HTML 元素一样向组件中传递内容：

```vue
<AlertBox>
  Something bad happened.
</AlertBox>
```

```vue
// AlertBox.vue
<template>
  <div class="alert-box">
    <strong>This is an Error for Demo Purposes</strong>
    <slot />
  </div>
</template>
```

---

#### 动态组件

`<component :is="...">` 的意思是：**Vue，请你看一下 `is` 这个变量里存的是哪个组件，然后把那个组件渲染到 `<component>` 这个位置上。**

使用场景：切换tab

```vue
<!-- currentTab 改变时组件也改变 -->
<component :is="tabs[currentTab]"></component>
```

在上面的例子中，被传给 `:is` 的值可以是以下几种：

- 被注册的组件名
- 导入的组件对象

当使用 `<component :is="...">` 来在多个组件间作切换时，被切换掉的组件会被卸载。我们可以通过 KeepAlive 组件强制被切换掉的组件仍然保持“存活”的状态。

---

#### DOM 内模板解析注意事项

https://cn.vuejs.org/guide/essentials/component-basics#in-dom-template-parsing-caveats

这是在 html 和 js 里写 vue，而不是单文件组件.vue 	一般情况很少用

---

### 生命周期

![组件生命周期图示](https://cn.vuejs.org/assets/lifecycle_zh-CN.W0MNXI0C.png)

---

## 深入组件

### props

一个组件需要显式声明它所接受的 props，这样 Vue 才能知道外部传入的哪些是 props，哪些是透传 attribute

---

#### 响应式 Props 解构

const { foo } = defineProps(['foo'])

在 Vue 3.5 及以后，`defineProps` 可以放心解构，编译器会自动帮你保持响应性，还能用原生默认值语法。

---

##### 将解构的 props 传递到函数中

`watch` 的第一个参数必须是**响应式源**（ref、reactive 对象）或**返回响应式数据的 getter 函数**。

而解构出来的 `foo` 虽然在使用时会被自动转换为 `props.foo`，但它本身**只是一个普通值**（字符串、数字等），不是 ref。直接传给 `watch`，Vue 拿不到依赖追踪的钩子。

正确做法：用 getter 函数包裹

```js
const { foo } = defineProps(['foo'])

// ✅ 用 () => foo 包装，编译器会自动处理为 () => props.foo
watch(() => foo, (newVal) => {
  console.log('foo 变成了：', newVal)
})
```

扩展到外部函数：

```js
// 假设你封装了一个组合式函数
function useFeature(getter) {
  watch(getter, (val) => {
    console.log('值变化了：', val)
  })
}

const { foo } = defineProps(['foo'])

// ✅ 传 getter，响应性持续存在
useFeature(() => foo)

// ❌ 直接传值，响应性丢失
useFeature(foo)
```

---

#### 传递 prop 的细节

##### Prop 名字格式

 prop 用 camelCase 形式；子组件传递 props 用 camelCase 形式；组件名用 PascalCase

```vue
defineProps({
  greetingMessage: String
})
<span>{{ greetingMessage }}</span>

<MyComponent greeting-message="hello" />
```

---

##### 静态 vs. 动态 Props

```vue
<BlogPost title="My journey with Vue" />

<!-- 根据一个变量的值动态传入 -->
<BlogPost :title="post.title" />
```

---

##### 使用一个对象绑定多个 prop

可以直接显式写 v-bind 简洁绑定多个prop

```vue
const post = {
  id: 1,
  title: 'My Journey with Vue'
}
<BlogPost v-bind="post" />

//上面等价于下面
<BlogPost :id="post.id" :title="post.title" />
```

---

##### 单向数据流

所有的 props 都遵循着**单向绑定**原则，props 因父组件的更新而变化，自然地将新的状态向下流往子组件，而不会逆向传递。

---

### v-model

#### 基本用法

默认的 `v-model` 绑定的是 `modelValue` 这个 prop 和 `update:modelValue`

使用 [`defineModel()`](https://cn.vuejs.org/api/sfc-script-setup.html#definemodel) 宏：

```vue
<script setup>
const model = defineModel()

function update() {
  model.value++
}
</script>

<template>
  <div>Parent bound v-model is: {{ model }}</div>
  <button @click="update">Increment</button>
</template>
```

父组件可以用 `v-model` 绑定一个值：

```vue
<Child v-model="countModel" />
```

---

##### 3.4 之前的用法

```vue
<script setup>
defineProps({
  firstName: String,
  lastName: String
})

defineEmits(['update:firstName', 'update:lastName'])
</script>

<template>
  <input
    type="text"
    :value="firstName"
    @input="$emit('update:firstName', $event.target.value)"
  />
  <input
    type="text"
    :value="lastName"
    @input="$emit('update:lastName', $event.target.value)"
  />
</template>
```

---

#### 处理 v-model 修饰符

在自定义组件中**识别并处理父组件通过 `v-model` 添加的自定义修饰符**

自定义修饰符可以做到一些 vue 内置组件没有的，比如将首字母改为大写

用set方法：

```vue
// 子组件
<script setup>
const [model, modifiers] = defineModel({
  set(value) {
    // 如果父组件使用了 .capitalize 修饰符
    if (modifiers.capitalize) {
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
    // 没使用修饰符就原样返回
    return value
  }
})
</script>

<template>
  <input type="text" v-model="model" />
</template>
```

----

##### 3.4 之前的用法

```vue
<script setup>
const props = defineProps({
  modelValue: String,
  modelModifiers: { default: () => ({}) }
})

const emit = defineEmits(['update:modelValue'])

function emitValue(e) {
  let value = e.target.value
  // ------------------------------
  if (props.modelModifiers.capitalize) {
    value = value.charAt(0).toUpperCase() + value.slice(1)
  }
  // ----------------------------------
  emit('update:modelValue', value)
}
</script>

<template>
  <input type="text" :value="props.modelValue" @input="emitValue" />
</template>
```

---

### 透传 Attributes

#### Attributes 继承

“透传 attribute”指的是传递一个没有被该组件声明为 [props](https://cn.vuejs.org/guide/components/props.html) 或 [emits](https://cn.vuejs.org/guide/components/events.html#defining-custom-events) 的 attribute 或者 `v-on` 事件监听器给组件。最常见的例子就是 `class`、`style` 和 `id`。

当一个组件以单个元素为根作渲染时，透传的 attribute 会自动被添加到根元素上。

---

#### 禁用 Attributes 继承

使用场景：最常见的需要禁用 attribute 继承的场景就是 attribute 需要应用在根节点以外的其他元素上。

inheritAttrs: false

```vue
<script setup>
defineOptions({
  inheritAttrs: false
})
// ...setup 逻辑
</script>
```

这些透传进来的 attribute 可以在模板的表达式中直接用 `$attrs` 访问到。

```vue
<span>Fallthrough attribute: {{ $attrs }}</span>
```

这个 `$attrs` 对象包含了除组件所声明的 `props` 和 `emits` 之外的所有其他 attribute，例如 `class`，`style`，`v-on` 监听器等等。

有时候我们可能为了样式，需要在 `<button>` 元素外包装一层 `<div>`：

```vue
<div class="btn-wrapper">
  <button class="btn">Click Me</button>
</div>
```

我们想要所有像 `class` 和 `v-on` 监听器这样的透传 attribute 都应用在内部的 `<button>` 上而不是外层的 `<div>` 上。我们可以通过设定 `inheritAttrs: false` 和使用 `v-bind="$attrs"` 来实现：

```vue
<div class="btn-wrapper">
  <button class="btn" v-bind="$attrs">Click Me</button>
</div>
```

---

#### 在 JavaScript 中访问透传 Attributes

如果需要，可以在 `<script setup>` 中使用 `useAttrs()` API 来访问一个组件的所有透传 attribute：

```vue
<script setup>
import { useAttrs } from 'vue'

const attrs = useAttrs()
</script>
```

---

### 插槽 Slots

#### 插槽内容与出口

组件能够接收任意类型的 JavaScript 值作为 props，组件要接收模板内容用插槽 Slots

![插槽图示](https://cn.vuejs.org/assets/slots.CKcE8XYd.png)

---

插槽内容可以是任意合法的模板内容，不局限于文本。例如我们可以传入多个元素，甚至是组件：

```vue
<FancyButton>
  <span style="color:red">Click me!</span>
  <AwesomeIcon name="plus" />
</FancyButton>
```

通过使用插槽，`<FancyButton>` 组件更加灵活和具有可复用性。现在组件可以用在不同的地方渲染各异的内容，但同时还保证都具有相同的样式。

---

#### 渲染作用域

插槽内容可以访问到父组件的数据作用域，**无法访问**子组件的数据，因为插槽内容本身是在父组件模板中定义的。举例来说：

```vue
<span>{{ message }}</span>
<FancyButton>{{ message }}</FancyButton>
```

这里的两个 `{{ message }}` 插值表达式渲染的内容都是一样的。

---

#### 默认内容

```vue
<button type="submit">
  <slot>
    Submit <!-- 默认内容 -->
  </slot>
</button>
```

---

#### 具名插槽

`v-slot` 有对应的简写 `#`，因此 `<template v-slot:header>` 可以简写为 `<template #header>`。其意思就是“将这部分模板片段传入子组件的 header 插槽中”。

![具名插槽图示](https://cn.vuejs.org/assets/named-slots.CCIb9Mo_.png)

```vue
<BaseLayout>
  <template #header>
    <h1>Here might be a page title</h1>
  </template>

  <template #default>
    <p>A paragraph for the main content.</p>
    <p>And another one.</p>
  </template>

  <template #footer>
    <p>Here's some contact info</p>
  </template>
</BaseLayout>
```

---

#### 条件插槽

有时你需要根据内容是否被传入了插槽来渲染某些内容。

```vue
<template>
  <div class="card">
    <div v-if="$slots.header" class="card-header">
      <slot name="header" />
    </div>
    
    <div v-if="$slots.default" class="card-content">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>
```

---

#### 动态插槽名

```vue
<base-layout>
  <template v-slot:[dynamicSlotName]>
    ...
  </template>

  <!-- 缩写为 -->
  <template #[dynamicSlotName]>
    ...
  </template>
</base-layout>
```

---

#### 作用域插槽

让子组件在渲染时将一部分数据提供给插槽

```vue
// 子组件
<!-- <MyComponent> 的模板 -->
<div>
  <slot :text="greetingMessage" :count="1"></slot>
</div>

// 父组件
<MyComponent v-slot="slotProps">
  {{ slotProps.text }} {{ slotProps.count }}
</MyComponent>

// 也可以解构
<MyComponent v-slot="{ text, count }">
  {{ text }} {{ count }}
</MyComponent>
```

![scoped slots diagram](https://cn.vuejs.org/assets/scoped-slots.B67tIPc5.svg)

---

##### 具名作用域插槽

```vue
<MyComponent>
  <template #header="headerProps">
    {{ headerProps }}
  </template>

  <template #default="defaultProps">
    {{ defaultProps }}
  </template>

  <template #footer="footerProps">
    {{ footerProps }}
  </template>
</MyComponent>

<slot name="header" message="hello"></slot>
```

注意插槽上的 `name` 是一个 Vue 特别保留的 attribute，不会作为 props 传递给插槽。因此最终 `headerProps` 的结果是 `{ message: 'hello' }`。

---

### 依赖注入

#### Prop 逐级透传问题

深层传递props很麻烦

![Prop 逐级透传的过程图示](https://cn.vuejs.org/assets/prop-drilling.XJXa8UE-.png)

`provide` 和 `inject` 可以帮助我们解决这一问题

![Provide/inject 模式](https://cn.vuejs.org/assets/provide-inject.C0gAIfVn.png)

#### Provide (提供)

要为组件后代提供数据，需要使用到 [`provide()`](https://cn.vuejs.org/api/composition-api-dependency-injection.html#provide) 函数：

```vue
<script setup>
import { provide } from 'vue'

provide(/* 注入名 */ 'message', /* 值 */ 'hello!')
</script>
```

`provide()` 函数接收两个参数。第一个参数被称为**注入名**，可以是一个字符串或是一个 `Symbol`。

第二个参数是提供的值，值可以是任意类型，包括响应式的状态，比如一个 ref：

```js
import { ref, provide } from 'vue'

const count = ref(0)
provide('key', count)
```

提供的响应式状态使后代组件可以由此和提供者建立响应式的联系。

---

#### 应用层 Provide

除了在一个组件中提供依赖，我们还可以在整个应用层面提供依赖：

```js
import { createApp } from 'vue'

const app = createApp({})

app.provide(/* 注入名 */ 'message', /* 值 */ 'hello!')
```

在应用级别提供的数据在该应用内的所有组件中都可以注入。这在你编写[插件](https://cn.vuejs.org/guide/reusability/plugins.html)时会特别有用，因为插件一般都不会使用组件形式来提供值。

---

#### Inject (注入)

要注入上层组件提供的数据，需使用 [`inject()`](https://cn.vuejs.org/api/composition-api-dependency-injection.html#inject) 函数：

```vue
<script setup>
import { inject } from 'vue'

const message = inject('message')
</script>
```

如果有多个父组件提供了相同键的数据，注入将解析为组件链上最近的父组件所注入的值。（就近原则）

---

##### 注入默认值

```js
// 如果没有祖先组件提供 "message"
// `value` 会是 "这是默认值"
const value = inject('message', '这是默认值')
```

---

#### 和响应式数据配合使用

**建议尽可能将任何对响应式状态的变更都保持在供给方组件中**。如果要需要在注入方组件中更改数据，推荐在供给方组件内声明并提供一个更改数据的方法函数：

```vue
<!-- 在供给方组件内 -->
<script setup>
import { provide, ref } from 'vue'

const location = ref('North Pole')

function updateLocation() {
  location.value = 'South Pole'
}

provide('location', {
  location,
  updateLocation
})
</script>
```

```vue
<!-- 在注入方组件 -->
<script setup>
import { inject } from 'vue'

const { location, updateLocation } = inject('location')
</script>

<template>
  <button @click="updateLocation">{{ location }}</button>
</template>
```

如果想确保提供的数据不能被注入方的组件更改，你可以使用 [`readonly()`](https://cn.vuejs.org/api/reactivity-core.html#readonly) 来包装提供的值。

```vue
<script setup>
import { ref, provide, readonly } from 'vue'

const count = ref(0)
provide('read-only-count', readonly(count))
</script>
```

---

#### 使用 Symbol 作注入名

如果正在构建大型的应用，包含非常多的依赖提供，或者正在编写提供给其他开发者使用的组件库，建议最好使用 [Symbol](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Symbol) 来作为注入名以避免潜在的冲突。

推荐在一个单独的文件中导出这些注入名 Symbol：

```js
export const myInjectionKey = Symbol()
```

```js
// 在供给方组件中
import { provide } from 'vue'
import { myInjectionKey } from './keys.js'

provide(myInjectionKey, { 
  /* 要提供的数据 */
})
```

```js
// 注入方组件
import { inject } from 'vue'
import { myInjectionKey } from './keys.js'

const injected = inject(myInjectionKey)
```

---

### 异步组件

#### 基本用法

在大型项目中，我们可能需要拆分应用为更小的块，并仅在需要时再从服务器加载相关组件。

如果一次性把所有组件都打包下载，首页会加载很慢。异步组件允许你把某些组件拆出去，等真正要用时（比如用户点击了某个按钮、切换到某个路由）才从服务器加载。

---

核心 API：`defineAsyncComponent`

它接收一个**返回 Promise 的函数**，这个 Promise 最终 resolve 一个组件定义。

实际开发中，**99% 的情况都是用 ES 模块动态导入 `import()`**，它本身就返回 Promise：

```js
const AsyncComp = defineAsyncComponent(() =>
  import('./components/MyComponent.vue')
)
```

这样 Vite / Webpack 在打包时会**自动把 `MyComponent.vue` 拆成独立的 JS 文件**，只有 `AsyncComp` 真正被渲染时才会下载。

---

#### 惰性激活 3.5+

如果你正在使用[服务器端渲染](https://cn.vuejs.org/guide/scaling-up/ssr.html)，这一部分才会适用。

https://cn.vuejs.org/guide/components/async.html#lazy-hydration

---

## 逻辑复用

### 组合式函数

“组合式函数”(Composables) 是一个利用 Vue 的组合式 API 来封装和复用**有状态逻辑**的函数。

按照惯例，组合式函数名以“use”开头

如果想在多个组件中复用这个相同的逻辑，可以把这个逻辑以一个组合式函数的形式提取到外部文件中：

```js
import { ref, onMounted, onUnmounted } from 'vue'

// 按照惯例，组合式函数名以“use”开头
export function useMouse() {
  // 被组合式函数封装和管理的状态
  const x = ref(0)
  const y = ref(0)

  // 组合式函数可以随时更改其状态。
  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  // 一个组合式函数也可以挂靠在所属组件的生命周期上
  // 来启动和卸载副作用
  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  // 通过返回值暴露所管理的状态
  return { x, y }
}
```

```vue
<script setup>
import { useMouse } from './mouse.js'

const { x, y } = useMouse()
</script>

<template>Mouse position is at: {{ x }}, {{ y }}</template>
```

可以嵌套多个组合式函数：一个组合式函数可以调用一个或多个其他的组合式函数。

---

#### 异步状态示例

**如何封装带响应式输入的异步请求逻辑**。

重点：让 useFetch 能够响应 URL 的变化

实现的关键：watchEffect + toValue

```js
import { ref, watchEffect, toValue } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const error = ref(null)

  const fetchData = () => {
    // reset state before fetching..
    data.value = null
    error.value = null

    fetch(toValue(url))
      .then((res) => res.json())
      .then((json) => (data.value = json))
      .catch((err) => (error.value = err))
  }

  watchEffect(() => {
    fetchData()
  })

  return { data, error }
}
```

toValue(xxx)

![image-20260427194643364](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260427194643364.png)

---

#### 约定和最佳实践

##### 输入参数

习惯直接用toValue()处理参数，不管是原始值还是 ref 或 getter。

```js
import { toValue } from 'vue'

function useFeature(maybeRefOrGetter) {
  // 如果 maybeRefOrGetter 是一个 ref 或 getter，
  // 将返回它的规范化值。
  // 否则原样返回。
  const value = toValue(maybeRefOrGetter)
}
```

---

### 自定义指令

#### 介绍

[组件](https://cn.vuejs.org/guide/essentials/component-basics.html)和[组合式函数](https://cn.vuejs.org/guide/reusability/composables.html)。组件是主要的构建模块，而组合式函数则侧重于有状态的逻辑。另一方面，自定义指令主要是为了重用涉及普通元素的底层 DOM 访问的逻辑。

一个自定义指令由一个包含类似组件生命周期钩子的对象来定义。

例子：

```vue
<script setup>
// 在模板中启用 v-highlight
const vHighlight = {
  mounted: (el) => {
    el.classList.add('is-highlight')
  }
}
</script>

<template>
  <p v-highlight>This sentence is important!</p>
</template>
```

将一个自定义指令全局注册到应用层级也是一种常见的做法：

```js
const app = createApp({})

// 使 v-highlight 在所有组件中都可用
app.directive('highlight', {
  /* ... */
})
```

---

#### 自定义指令的使用时机

```vue
<script setup>
// 在模板中启用 v-focus
const vFocus = {
  mounted: (el) => el.focus()
}
</script>

<template>
  <input v-focus />
</template>
```

---

#### 指令钩子

```js
const myDirective = {
  // 在绑定元素的 attribute 前
  // 或事件监听器应用前调用
  created(el, binding, vnode) {
    // 下面会介绍各个参数的细节
  },
  // 在绑定元素的父组件
  // 及他自己的所有子节点都更新后调用
  updated(el, binding, vnode, prevVnode) {},
}
```

##### 钩子参数

- `el`：指令绑定到的元素。这可以用于直接操作 DOM。
- `binding`：一个对象，包含以下属性。
  - `value`：传递给指令的值。例如在 `v-my-directive="1 + 1"` 中，值是 `2`。
  - `oldValue`：之前的值，仅在 `beforeUpdate` 和 `updated` 中可用。无论值是否更改，它都可用。
  - `arg`：传递给指令的参数 (如果有的话)。例如在 `v-my-directive:foo` 中，参数是 `"foo"`。
  - `modifiers`：一个包含修饰符的对象 (如果有的话)。例如在 `v-my-directive.foo.bar` 中，修饰符对象是 `{ foo: true, bar: true }`。
  - `instance`：使用该指令的组件实例。
  - `dir`：指令的定义对象。
- `vnode`：代表绑定元素的底层 VNode。
- `prevVnode`：代表之前的渲染中指令所绑定元素的 VNode。仅在 `beforeUpdate` 和 `updated` 钩子中可用。

---

`binding` 参数会是一个这样的对象：

```js
{
  arg: 'foo',
  modifiers: { bar: true },
  value: /* `baz` 的值 */,
  oldValue: /* 上一次更新时 `baz` 的值 */
}
```

---

#### 简化形式

对于自定义指令来说，一个很常见的情况是仅仅需要在 `mounted` 和 `updated` 上实现相同的行为，除此之外并不需要其他钩子。这种情况下我们可以直接用一个函数来定义指令，如下所示：

```js
app.directive('color', (el, binding) => {
  // 这会在 `mounted` 和 `updated` 时都调用
  el.style.color = binding.value
})
```

---

#### 对象字面量

指令可以传一个对象：

```vue
<div v-demo="{ color: 'white', text: 'hello!' }"></div>
```

```js
app.directive('demo', (el, binding) => {
  console.log(binding.value.color) // => "white"
  console.log(binding.value.text) // => "hello!"
})
```

---

#### 在组件上使用

不推荐在组件上使用自定义指令。当组件具有多个根节点时可能会出现预期外的行为。

---

### 插件

#### 介绍

插件是**为 Vue 应用添加全局功能**的工具。它本质是一个对象（或函数），通过 `app.use(插件, 选项)` 安装，能让你在应用的任何地方使用它提供的功能。

---

使用场景：

1. 通过 [`app.component()`](https://cn.vuejs.org/api/application.html#app-component) 和 [`app.directive()`](https://cn.vuejs.org/api/application.html#app-directive) 注册一到多个全局组件或自定义指令。
2. 通过 [`app.provide()`](https://cn.vuejs.org/api/application.html#app-provide) 使一个资源[可被注入](https://cn.vuejs.org/guide/components/provide-inject.html)进整个应用。
3. 向 [`app.config.globalProperties`](https://cn.vuejs.org/api/application.html#app-config-globalproperties) 中添加一些全局实例属性或方法
4. 一个可能上述三种都包含了的功能库 (例如 [vue-router](https://github.com/vuejs/vue-router-next))。

---

安装：

```js
import { createApp } from 'vue'

const app = createApp({})

app.use(myPlugin, {
  /* 可选的选项 */
})
```

---

定义：一个插件可以是一个拥有 `install()` 方法的对象，也可以直接是一个安装函数本身。

```js
const myPlugin = {
  install(app, options) {
    // 配置此应用
  }
   
  install: (app, options) => {
    app.provide('i18n', options)
  }
}
```

---

编写（例子）：

插件文件 plugins/i18n.js：

```js
// plugins/i18n.js
export default {
  install(app, options) {
    // 1. 把翻译字典通过 provide 注入，组件可以用 inject 获取
    app.provide('i18n', options)

    // 2. 在全局属性上挂载 $translate 方法，模板中直接使用
    app.config.globalProperties.$translate = (key) => {
      // options 就是安装时传入的翻译字典
      // 用 key 按 '.' 分隔逐层取值，例如 'greetings.hello' → options.greetings.hello
      return key.split('.').reduce((obj, k) => {
        if (obj) return obj[k]
      }, options)
    }
  }
}
```

main.js 中安装插件：

```js
import { createApp } from 'vue'
import App from './App.vue'
import i18nPlugin from './plugins/i18n'

const app = createApp(App)

// 安装插件，第二个参数是翻译字典
app.use(i18nPlugin, {
  greetings: {
    hello: 'Bonjour!',
    goodbye: 'Au revoir!'
  },
  nav: {
    home: 'Accueil'
  }
})

app.mount('#app')
```

组件中使用：

```vue
<template>
  <h1>{{ $translate('greetings.hello') }}</h1>
</template>
```

---

##### 插件中的 Provide / Inject

```js
// plugins/i18n.js
export default {
  install: (app, options) => {
    app.provide('i18n', options)
  }
}
```

```js
<script setup>
import { inject } from 'vue'

const i18n = inject('i18n')

console.log(i18n.greetings.hello)
</script>
```

---

## 内置组件

#### Transition

Vue 提供了两个内置组件，可以帮助你制作基于状态变化的过渡和动画：

- `<Transition>` 会在一个元素或组件进入和离开 DOM 时应用动画。
- `<TransitionGroup>` 会在一个 `v-for` 列表中的元素或组件被插入，移动，或移除时应用动画。

---

##### `<Transition>` 组件

触发条件：

- 由 `v-if` 所触发的切换
- 由 `v-show` 所触发的切换
- 由特殊元素 `<component>` 切换的动态组件
- 改变特殊的 `key` 属性

---

示例：

```vue
<button @click="show = !show">Toggle</button>
<Transition>
  <p v-if="show">hello</p>
</Transition>
```

```css
/* 下面我们会解释这些 class 是做什么的 */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
```

---

##### 基于 CSS 的过渡效果

###### CSS 过渡 class

一共有 6 个应用于进入与离开过渡效果的 CSS class：

![过渡图示](https://cn.vuejs.org/assets/transition-classes.DYG5-69l.png)

1. `v-enter-from`：进入动画的起始状态。在元素插入之前添加，在元素插入完成后的下一帧移除。
2. `v-enter-active`：进入动画的生效状态。应用于整个进入动画阶段。在元素被插入之前添加，在过渡或动画完成之后移除。这个 class 可以被用来定义进入动画的持续时间、延迟与速度曲线类型。
3. `v-enter-to`：进入动画的结束状态。在元素插入完成后的下一帧被添加 (也就是 `v-enter-from` 被移除的同时)，在过渡或动画完成之后移除。
4. `v-leave-from`：离开动画的起始状态。在离开过渡效果被触发时立即添加，在一帧后被移除。
5. `v-leave-active`：离开动画的生效状态。应用于整个离开动画阶段。在离开过渡效果被触发时立即添加，在过渡或动画完成之后移除。这个 class 可以被用来定义离开动画的持续时间、延迟与速度曲线类型。
6. `v-leave-to`：离开动画的结束状态。在一个离开动画被触发后的下一帧被添加 (也就是 `v-leave-from` 被移除的同时)，在过渡或动画完成之后移除。

---

###### 为过渡效果命名

```vue
<Transition name="fade">
  ...
</Transition>
```

起名字之后不用 v- 前缀而是 name 前缀：

```css
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
```

---

###### CSS 的 animation

animation

```css
.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.25);
  }
  100% {
    transform: scale(1);
  }
}
```

`animation` 直接调用了一个名为 `bounce-in` 的**关键帧动画**。这个动画是一个独立的、已定义的“表演剧本”。只要元素上被加上了 `bounce-enter-active` 这个类，浏览器就会立刻完整地执行一次这个剧本，**不依赖于属性的变化**。

Transition 和 Animation 是两种不同的动画实现方式，在 `<Transition>` 组件中，只需要**二选一**，根据你的具体需求来决定使用哪种方式更合适。简单过渡，用 Transition；多个步骤、更复杂的动效，用 Animation。

用了 Animation ，就不用`v-enter-from`、`v-enter-to`、`v-leave-from`、`v-leave-to`了，直接在Animation里写v-enter-active、v-leave-active

---

###### 自定义过渡 class

**当使用第三方 CSS 动画库（如 Animate.css）时，它的动画类名是固定的，无法直接适配 Vue 默认的 `v-enter-active` 等类名**

此时可以向 `<Transition>` 传递以下的 props 来指定自定义的过渡 class：

- `enter-from-class`
- `enter-active-class`
- `enter-to-class`
- `leave-from-class`
- `leave-active-class`
- `leave-to-class`

```vue
<!-- 假设你已经在页面中引入了 Animate.css -->
<Transition
  name="custom-classes"
  enter-active-class="animate__animated animate__tada"
  leave-active-class="animate__animated animate__bounceOutRight"
>
  <p v-if="show">hello</p>
</Transition>
```

---

###### 同时使用 transition 和 animation

在某些场景中，可能想要在同一个元素上同时使用它们两个。举例来说，Vue 触发了一个 CSS 动画，同时鼠标悬停触发另一个 CSS 过渡。此时需要显式地传入 `type` prop 来声明，告诉 Vue 需要关心哪种类型，传入的值是 `animation` 或 `transition`：

```vue
<Transition type="animation">...</Transition>
```

---

###### 深层级过渡与显式过渡时长

https://cn.vuejs.org/guide/built-ins/transition#nested-transitions-and-explicit-transition-durations

---

##### JavaScript 钩子

https://cn.vuejs.org/guide/built-ins/transition#javascript-hooks

一些transition组件使用时机的函数

---

##### 可复用过渡效果

要创建一个可被复用的过渡，需要为 `<Transition>` 组件创建一个包装组件，并向内传入插槽内容：

```vue
<script>
// JavaScript 钩子逻辑...
</script>

<template>
  <!-- 包装内置的 Transition 组件 -->
  <Transition
    name="my-transition"
    @enter="onEnter"
    @leave="onLeave">
    <slot></slot> <!-- 向内传递插槽内容 -->
  </Transition>
</template>

<style>
/*
  必要的 CSS...
  注意：避免在这里使用 <style scoped>
  因为那不会应用到插槽内容上
*/
</style>
```

```vue
<MyTransition>
  <div v-if="show">Hello</div>
</MyTransition>
```

---

##### 出现时过渡

如果想在某个节点初次渲染时应用一个过渡效果，你可以添加 `appear` prop：

```vue
<Transition appear>
  ...
</Transition>
```

---

##### 元素间过渡

除了通过 `v-if` / `v-show` 切换一个元素，也可以通过 `v-if` / `v-else` / `v-else-if` 在几个组件间进行切换，只要确保任一时刻只会有一个元素被渲染即可：

```vue
<Transition>
  <button v-if="docState === 'saved'">Edit</button>
  <button v-else-if="docState === 'edited'">Save</button>
  <button v-else-if="docState === 'editing'">Cancel</button>
</Transition>
```

---

##### 过渡模式

在之前的例子中，进入和离开的元素都是在同时开始动画的。当想要先执行离开动画，然后在其完成**之后**再执行元素的进入动画。使用mode="out-in"

```vue
<Transition mode="out-in">
  ...
</Transition>
```

---

##### 组件间过渡

`<Transition>` 也可以作用于[动态组件](https://cn.vuejs.org/guide/essentials/component-basics.html#dynamic-components)之间的切换：

```vue
<Transition name="fade" mode="out-in">
  <component :is="activeComponent"></component>
</Transition>
```

使用场景：实现“整个组件模块带着动画无缝替换”的效果。

在构建单页应用时，经常需要根据用户操作（比如点击了“登录”按钮或“注册”按钮）来**整体替换**掉页面中间的一块区域。如果没有过渡动画，这种替换在视觉上是瞬间的、生硬的“跳变”。而 `<Transition>` 配合动态组件 `<component :is="...">`，可以让这个替换过程变得平滑且优雅。

---

##### 动态过渡

`<Transition>` 的 props (比如 `name`) 也可以是动态的。这让我们可以根据状态变化动态地应用不同类型的过渡：

```vue
<Transition :name="transitionName">
  <!-- ... -->
</Transition>
```

这个特性的用处是可以提前定义好多组 CSS 过渡或动画的 class，然后在它们之间动态切换。

---

##### 使用 Key Attribute 过渡

有时为了触发过渡，需要强制重新渲染 DOM 元素。

```vue
<script setup>
import { ref } from 'vue';
const count = ref(0);

setInterval(() => count.value++, 1000);
</script>

<template>
  <Transition>
    <span :key="count">{{ count }}</span>
  </Transition>
</template>
```

如果不使用 `key` attribute，则只有文本节点会被更新，因此不会发生过渡。但是，有了 `key` 属性，Vue 就知道在 `count` 改变时创建一个新的 `span` 元素，因此 `Transition` 组件有两个不同的元素在它们之间进行过渡。

---

### TransitionGroup

`<TransitionGroup>` 是一个内置组件，用于对 `v-for` 列表中的元素或组件的插入、移除和顺序改变添加动画效果。

---

#### 和 `<Transition>` 的区别

`<TransitionGroup>` 支持和 `<Transition>` 基本相同的 props、CSS 过渡 class 和 JavaScript 钩子监听器，但有以下几点区别：

- 默认情况下，它不会渲染一个容器元素。但你可以通过传入 `tag` prop 来指定一个元素作为容器元素来渲染。
- [过渡模式](https://cn.vuejs.org/guide/built-ins/transition.html#transition-modes)在这里不可用，因为我们不再是在互斥的元素之间进行切换。
- 列表中的每个元素都**必须**有一个独一无二的 `key` attribute。
- CSS 过渡 class 会被应用在列表内的元素上，**而不是**容器元素上。

---

#### 进入 / 离开动画

示例：

```vue
<TransitionGroup name="list" tag="ul">
  <li v-for="item in items" :key="item">
    {{ item }}
  </li>
</TransitionGroup>
```

```less
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
```

---

#### 移动动画

当某一项被插入或移除时，它周围的元素会立即发生“跳跃”而不是平稳地移动。可以通过添加一些额外的 CSS 规则来解决这个问题：

```css
.list-move, /* 对移动中的元素应用的过渡 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 确保将离开的元素从布局流中删除
  以便能够正确地计算移动的动画。 */
.list-leave-active {
  position: absolute;
}
```

---

#### 渐进延迟列表动画

跳出纯 CSS，用 JS 为每个元素创建**错落有致的进场序列**。

- **没有该动画**：所有元素瞬间同步出现，会显得有些生硬。
- **有了该动画**：元素一个接一个地滑入、淡入，产生富有引导性的视觉效果，非常适合在用户刚进入页面时使用。

💻 技术实现要点

1. **标记索引**：在 `v-for` 循环里，用 `:data-index="index"` 动态地把元素的序号印在 DOM 上。
2. **接管动画**：给 `<TransitionGroup>` 设置 `:css="false"`，告诉 Vue 纯 CSS 的动画我们不要了，全部交给 JavaScript 处理。
3. **错开执行**：在 JS 钩子（如 `onEnter`）中，读取元素的 `el.dataset.index` 序号，用它来动态计算动画的延迟时间（`delay`）。

---

### KeepAlive

在多个组件间动态切换时缓存被移除的组件实例。

#### 基本使用

看这个例子就知道什么情况下使用，解决了什么问题，有什么作用了。

![image-20260515183854666](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260515183854666.png)

```vue
<!-- 非活跃的组件将会被缓存！ -->
<KeepAlive>
  <component :is="activeComponent" />
</KeepAlive>
```

---

#### 包含/排除

`<KeepAlive>` 默认会缓存内部的所有组件实例，但可以通过 `include` 和 `exclude` prop 来定制该行为。实现按需缓存。

英文逗号，正则，数组都可以

```vue
<!-- 以英文逗号分隔的字符串 -->
<KeepAlive include="a,b">
  <component :is="view" />
</KeepAlive>

<!-- 正则表达式 (需使用 `v-bind`) -->
<KeepAlive :include="/a|b/">
  <component :is="view" />
</KeepAlive>

<!-- 数组 (需使用 `v-bind`) -->
<KeepAlive :include="['a', 'b']">
  <component :is="view" />
</KeepAlive>
```

```js
defineOptions({ name: 'CompA' })
```

---

#### 最大缓存实例数

传入 `max` prop 来限制可被缓存的最大组件实例数。如果缓存的实例数量即将超过指定的那个最大数量，则最久没有被访问的缓存实例将被销毁，以便为新的实例腾出空间。

```vue
<KeepAlive :max="10">
  <component :is="activeComponent" />
</KeepAlive>
```

---

#### 缓存实例的生命周期

当一个组件实例从 DOM 上移除但因为被 `<KeepAlive>` 缓存而仍作为组件树的一部分时，它将变为**不活跃**状态而不是被卸载。当一个组件实例作为缓存树的一部分插入到 DOM 中时，它将重新**被激活**。

一个持续存在的组件可以通过 [`onActivated()`](https://cn.vuejs.org/api/composition-api-lifecycle.html#onactivated) 和 [`onDeactivated()`](https://cn.vuejs.org/api/composition-api-lifecycle.html#ondeactivated) 注册相应的两个状态的生命周期钩子：

```js
<script setup>
import { onActivated, onDeactivated } from 'vue'

onActivated(() => {
  // 调用时机为首次挂载
  // 以及每次从缓存中被重新插入时
})

onDeactivated(() => {
  // 在从 DOM 上移除、进入缓存
  // 以及组件卸载时调用
})
</script>
```

请注意：

- `onActivated` 在组件挂载时也会调用，并且 `onDeactivated` 在组件卸载时也会调用。
- 这两个钩子不仅适用于 `<KeepAlive>` 缓存的根组件，也适用于缓存树中的后代组件。

---

### Teleport

可以将一个组件内部的一部分模板“传送”到该组件的 DOM 结构外层的位置去。

`<Teleport>` 让你把组件的一部分 HTML 搬到 DOM 的其他位置，同时保持组件逻辑完整。它是解决模态框、通知等 UI 元素样式困境的标准方案，实现了“逻辑归属”与“视觉呈现”的分离。

解决问题：

`<Teleport>` 的核心作用是**打破 DOM 结构和组件逻辑之间的强绑定**。

传统组件树结构下，子组件的模板内容必然渲染在父组件的 DOM 子树里。但这会导致两个实际难题：

- **CSS 布局受限**：像 `position: fixed`、`z-index` 等样式，很容易被设置了 `transform`、`filter`、`perspective` 或 `overflow: hidden` 的祖先元素破坏，导致模态框无法相对视口定位，或被意外裁剪。
- **层级覆盖问题**：组件的层级被限制在父组件的 `z-index` 上下文内。页面其他部分（如固定顶栏）可能有意料之外的高 `z-index`，会覆盖本该在最上层的模态框。

`<Teleport>` 让你可以**把模板片段传送到 DOM 树的任何位置（如 `<body>` 末尾）**，从而彻底避开这些样式限制，同时该模板片段仍保持与原组件的逻辑关系（`props`、`emit`、状态共享）。

应用场景：

任何需要**视觉上“脱离”当前组件层级，但逻辑上仍属于该组件**的 UI 元素，都适合用 `<Teleport>`。

---

#### 搭配组件使用

`<Teleport>` 只改变了渲染的 DOM 结构，它不会影响组件间的逻辑关系。也就是说，如果 `<Teleport>` 包含了一个组件，那么该组件始终和这个使用了 `<Teleport>` 的组件保持逻辑上的父子关系。传入的 props 和触发的事件也会照常工作。

---

#### 禁用 Teleport

在某些场景下可能需要视情况禁用 `<Teleport>`。举例来说，我们想要在桌面端将一个组件当做浮层来渲染，但在移动端则当作行内组件。我们可以通过对 `<Teleport>` 动态地传入一个 `disabled` prop 来处理这两种不同情况：

```vue
<Teleport :disabled="isMobile">
  ...
</Teleport>
```

然后我们可以动态地更新 `isMobile`。

---

#### 多个 Teleport 共享目标

对于此类场景，多个 `<Teleport>` 组件可以将其内容挂载在同一个目标元素上，而顺序就是简单的顺次追加，后挂载的将排在目标元素下更后面的位置上，但都在目标元素中。

```vue
<Teleport to="#modals">
  <div>A</div>
</Teleport>
<Teleport to="#modals">
  <div>B</div>
</Teleport>
```

即：

```html
<div id="modals">
  <div>A</div>
  <div>B</div>
</div>
```

---

#### 延迟解析的 Teleport 3.5+

在 Vue 3.5 及更高版本中，我们可以使用 `defer` prop 推迟 Teleport 的目标解析，直到应用的其他部分挂载。

```vue
<Teleport defer to="#late-div">...</Teleport>

<!-- 稍后出现于模板中的某处 -->
<div id="late-div"></div>
```

---

## 应用规模化

### 服务端渲染 (SSR)

#### 总览

##### 为什么要用 SSR？

- **更快的首屏加载**：这一点在慢网速或者运行缓慢的设备上尤为重要。服务端渲染的 HTML 无需等到所有的 JavaScript 都下载并执行完成之后才显示，所以你的用户将会更快地看到完整渲染的页面。除此之外，数据获取过程在首次访问时在服务端完成，相比于从客户端获取，可能有更快的数据库连接。这通常可以带来更高的[核心 Web 指标](https://web.dev/vitals/)评分、更好的用户体验，而对于那些“首屏加载速度与转化率直接相关”的应用来说，这点可能至关重要。
- **统一的心智模型**：你可以使用相同的语言以及相同的声明式、面向组件的心智模型来开发整个应用，而不需要在后端模板系统和前端框架之间来回切换。
- **更好的 SEO**：搜索引擎爬虫可以直接看到完全渲染的页面。

使用 SSR 时还有一些权衡之处需要考量：

- 开发中的限制。浏览器端特定的代码只能在某些生命周期钩子中使用；一些外部库可能需要特殊处理才能在服务端渲染的应用中运行。
- 更多的与构建配置和部署相关的要求。服务端渲染的应用需要一个能让 Node.js 服务器运行的环境，不像完全静态的 SPA 那样可以部署在任意的静态文件服务器上。
- 更高的服务端负载。在 Node.js 中渲染一个完整的应用要比仅仅托管静态文件更加占用 CPU 资源，因此如果你预期有高流量，请为相应的服务器负载做好准备，并采用合理的缓存策略。

在为你的应用使用 SSR 之前，你首先应该问自己是否真的需要它。这主要取决于首屏加载速度对应用的重要程度。例如，如果你正在开发一个内部的管理面板，初始加载时的那额外几百毫秒对你来说并不重要，这种情况下使用 SSR 就没有太多必要了。然而，在内容展示速度极其重要的场景下，SSR 可以尽可能地帮你实现最优的初始加载性能。

---

##### SSR vs. SSG

**静态站点生成** (Static-Site Generation，缩写为 SSG)，也被称为预渲染，是另一种流行的构建快速网站的技术。如果用服务端渲染一个页面所需的数据对每个用户来说都是相同的，那么我们可以只渲染一次，提前在构建过程中完成，而不是每次请求进来都重新渲染页面。预渲染的页面生成后作为静态 HTML 文件被服务器托管。

SSG 保留了和 SSR 应用相同的性能表现：它带来了优秀的首屏加载性能。同时，它比 SSR 应用的花销更小，也更容易部署，因为它输出的是静态 HTML 和资源文件。这里的关键词是**静态**：SSG 仅可以用于提供静态数据的页面，即数据在构建期间就是已知的，并且在多次请求之间不能被改变。每当数据变化时，都需要重新部署。

如果你调研 SSR 只是为了优化为数不多的营销页面的 SEO (例如 `/`、`/about` 和 `/contact` 等)，那么你可能需要 SSG 而不是 SSR。SSG 也非常适合构建基于内容的网站，比如文档站点或者博客。

---

SSR 是区分“初级前端”和“高级前端”的经典问题。面试官期待你能清晰地说出：

- **是什么**：服务端把 Vue 组件渲染成 HTML 字符串，返回给浏览器。
- **解决什么问题**：首屏加载慢、SEO 不友好。
- **有什么代价**：服务器压力大、开发限制多、需要 Node.js 环境。
- **什么时候用**：内容型网站（新闻、博客、电商）需要 SSR；后台管理系统不需要。
- **SSR vs SSG**：页面数据对所有用户都一样 → 用 SSG（构建时预渲染）；页面数据因人而异 → 用 SSR（请求时渲染）。

---

#### 书写 SSR 友好的代码

https://cn.vuejs.org/guide/scaling-up/ssr.html#writing-ssr-friendly-code

---

## 最佳实践

### 性能优化

#### 页面加载优化

##### 代码分割

router 懒加载

#### 更新优化

##### Props 稳定性

传原始数据，子组件自己算：

```vue
<ListItem
  v-for="item in list"
  :id="item.id"
  :active-id="activeId" />
```

- **后果**：只要 `activeId` 一变，**列表里所有的** `<ListItem>` 的 `active-id` 这个 prop 都变了。Vue 看到 prop 变了，就会触发对应组件的更新。所以，哪怕其中 99% 的项活跃状态根本没变，它们也得跟着重新跑一遍更新流程。

父组件提前算好，传结果给子组件：

```vue
<ListItem
  v-for="item in list"
  :id="item.id"
  :active="item.id === activeId" />
```

父组件在渲染时就提前算好了 `item.id === activeId` 的结果（`true` 或 `false`），然后把这个结果作为 `active` prop 传给 `<ListItem>`。

总结一下，这个技巧的核心思想就是让传给子组件的 props 尽量保持稳定。

---

##### `v-once`

`v-once` 是一个内置的指令，可以用来渲染依赖运行时数据但无需再更新的内容。它的整个子树都会在未来的更新中被跳过。

---

##### `v-memo`

`v-memo` 是一个内置指令，可以用来有条件地跳过某些大型子树或者 `v-for` 列表的更新。

---

## TypeScript

### TypeScript 与组合式 API

#### 为组件的 props 标注类型

`defineProps()` 宏函数支持从它的参数中推导类型：

```vue
<script setup lang="ts">
const props = defineProps({
  foo: { type: String, required: true },
  bar: Number
})

props.foo // string
props.bar // number | undefined
</script>
```

通过泛型参数来定义 props 的类型通常更直接：

```vue
<script setup lang="ts">
const props = defineProps<{
  foo: string
  bar?: number
}>()
</script>
```

也可以将 props 的类型移入一个单独的接口中：

```vue
<script setup lang="ts">
interface Props {
  foo: string
  bar?: number
}

const props = defineProps<Props>()
</script>
```

这同样适用于 `Props` 从另一个源文件中导入的情况。

```vue
<script setup lang="ts">
import type { Props } from './foo'

const props = defineProps<Props>()
</script>
```

---

##### Props 解构默认值

当使用基于类型的声明时，我们失去了为 props 声明默认值的能力。可以通过使用[响应式 Props 解构](https://cn.vuejs.org/guide/components/props.html#reactive-props-destructure)解决这个问题。 

```ts
interface Props {
  msg?: string
  labels?: string[]
}

const { msg = 'hello', labels = ['one', 'two'] } = defineProps<Props>()
```

---

##### 复杂的 prop 类型

```vue
<script setup lang="ts">
interface Book {
  title: string
  author: string
  year: number
}

const props = defineProps<{
  book: Book
}>()
</script>
```

**既需要类型推导，又需要运行时校验（比如必须为对象、或自定义校验规则）**：

```js
import type { PropType } from 'vue'

const props = defineProps({
  book: Object as PropType<Book>
})
```

---


#### 为组件的 emits 标注类型

```vue
<script setup lang="ts">
// 3.3+: 可选的、更简洁的语法
const emit = defineEmits<{
  change: [id: number]
  update: [value: string]
}>()
</script>
```

---

#### 为 `ref()` 标注类型

ref 会根据初始化时的值推导其类型：

```js
import { ref } from 'vue'

// 推导出的类型：Ref<number>
const year = ref(2020)

// => TS Error: Type 'string' is not assignable to type 'number'.
year.value = '2020'
```

有时可能想为 ref 内的值指定一个更复杂的类型，可以通过使用 `Ref` 这个类型：

```js
import { ref } from 'vue'
import type { Ref } from 'vue'

const year: Ref<string | number> = ref('2020')

year.value = 2020 // 成功！
```

或者，在调用 `ref()` 时传入一个泛型参数，来覆盖默认的推导行为：

```js
// 得到的类型：Ref<string | number>
const year = ref<string | number>('2020')

year.value = 2020 // 成功！
```

如果指定了一个泛型参数但没有给出初始值，那么最后得到的就将是一个包含 `undefined` 的联合类型：

```js
// 推导得到的类型：Ref<number | undefined>
const n = ref<number>()
```

---

#### 为 `reactive()` 标注类型

https://cn.vuejs.org/guide/typescript/composition-api.html#typing-reactive

---

#### 为 `computed()` 标注类型

`computed()` 会自动从其计算函数的返回值上推导出类型，可以通过泛型参数显式指定类型：

```js
const double = computed<number>(() => {
  // 若返回值不是 number 类型则会报错
})
```

---

#### 为事件处理函数标注类型

建议显式地为事件处理函数的参数标注类型。此外，在访问 `event` 上的属性时可能需要使用类型断言：

```ts
function handleChange(event: Event) {
  console.log((event.target as HTMLInputElement).value)
}
```

---

#### 为 provide / inject 标注类型

`InjectionKey` 接口：

provide 和 inject 通常会在不同的组件中运行。要正确地为注入的值标记类型，Vue 提供了一个 `InjectionKey` 接口，它是一个继承自 `Symbol` 的泛型类型，可以用来在提供者和消费者之间同步注入值的类型：

```js
import { provide, inject } from 'vue'
import type { InjectionKey } from 'vue'

const key = Symbol() as InjectionKey<string>

provide(key, 'foo') // 若提供的是非字符串值会导致错误

const foo = inject(key) // foo 的类型：string | undefined
```

建议将注入 key 的类型放在一个单独的文件中，这样它就可以被多个组件导入。如：'src/keys/injectionKeys.ts'

---

字符串注入 key ：

需要通过泛型参数显式声明：

```typescript
const foo = inject<string>('foo') // 类型：string | undefined
```

默认值：

```ts
const foo = inject<string>('foo', 'bar') // 类型：string
```

---

#### 为模板引用标注类型

在单文件组件中由 `useTemplateRef()` 创建的 ref 类型可以基于匹配的 ref attribute 所在的元素**自动推断**为静态类型。

在无法自动推断的情况下，仍然可以通过泛型参数将模板 ref 转换为显式类型。

```ts
const el = useTemplateRef<HTMLInputElement>('el')
```

---

#### 为自定义全局指令添加类型

https://cn.vuejs.org/guide/typescript/composition-api#typing-global-custom-directives

---

## 进阶主题

### 深入响应式系统

#### 响应性调试

组件调试钩子/计算属性调试/侦听器调试

有一些生命周期钩子可以进行调试：

https://cn.vuejs.org/guide/extras/reactivity-in-depth.html#reactivity-debugging

---

#### 与外部状态系统集成

##### 不可变数据

https://cn.vuejs.org/guide/extras/reactivity-in-depth.html#integration-with-external-state-systems

![image-20260524061246608](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260524061246608.png)

需要使用 Immer 库的场景：

![image-20260524062816288](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260524062816288.png)

---

##### 状态机

[状态机](https://en.wikipedia.org/wiki/Finite-state_machine)是一种数据模型，用于描述应用可能处于的所有可能状态，以及从一种状态转换到另一种状态的所有可能方式。

![image-20260524071742070](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260524071742070.png)

当你遇到**状态多、转换规则复杂、非法状态会导致严重问题**的场景时，状态机能带来巨大收益。

- **XState** 管理的是**状态流转规则**（“可以怎么变”），适合复杂交互、多步骤流程。
- **Immer** 管理的是**数据的不可变更新**（“怎么生成新值”），适合撤销/重做、快照、性能优化。
- 两者可以组合使用：XState 管理状态机逻辑，Immer 管理每个状态内部的复杂数据。

---

### 渲染机制

#### 虚拟 DOM

虚拟 DOM (Virtual DOM，简称 VDOM) 是一种编程概念，意为将目标所需的 UI 通过数据结构“虚拟”地表示出来，保存在内存中，然后将真实的 DOM 与之保持同步。

与其说虚拟 DOM 是一种具体的技术，不如说是一种模式，所以并没有一个标准的实现：

```js
const vnode = {
  type: 'div',
  props: {
    id: 'hello'
  },
  children: [
    /* 更多 vnode */
  ]
}
```

一个运行时渲染器将会遍历整个虚拟 DOM 树，并据此构建真实的 DOM 树。这个过程被称为**挂载** (mount)。

如果我们有两份虚拟 DOM 树，渲染器将会有比较地遍历它们，找出它们之间的区别，并应用这其中的变化到真实的 DOM 上。这个过程被称为**更新** (patch)，又被称为“比对”(diffing) 或“协调”(reconciliation)。

虚拟 DOM 带来的主要收益是它让开发者能够灵活、声明式地创建、检查和组合所需 UI 的结构，同时只需把具体的 DOM 操作留给渲染器去处理。

---

#### 渲染管线

已经挺简洁了，也挺重要的，要看看：https://cn.vuejs.org/guide/extras/rendering-mechanism.html#render-pipeline

---

#### 带编译时信息的虚拟 DOM

Vue 编译器用来提高虚拟 DOM 运行时性能的主要优化：

##### 缓存静态内容

在模板中常常有部分内容是不带任何动态绑定的：

```html
<div>
  <div>foo</div> <!-- 需缓存 -->
  <div>bar</div> <!-- 需缓存 -->
  <div>{{ dynamic }}</div>
</div>
```

`foo` 和 `bar` 这两个 div 是完全静态的，没有必要在重新渲染时再次创建和比对它们。渲染器在首次渲染时会将创建的这部分 vnode 缓存起来，并在后续的重新渲染中使用缓存的 vnode，渲染器知道新旧 vnode 在这部分是完全相同的，所以会完全跳过对它们的差异比对。

此外，当有足够多连续的静态元素时，它们还会再被压缩为一个“静态 vnode”，其中包含的是这些节点相应的纯 HTML 字符串。这些静态节点会直接通过 `innerHTML` 来挂载。

---

##### 更新类型标记

**在编译阶段，提前分析出每个动态元素“具体会怎么变”，并打上一个标记。** 这样在运行时，渲染器就能**跳过复杂的通用比对，直接针对变化类型做最少量的更新操作。**

它解决了什么问题：

传统的虚拟 DOM Diff 是“通用算法”：

1. 拿到旧虚拟节点和新虚拟节点。
2. 逐个属性比对：`class` 变了吗？`id` 变了吗？`value` 变了吗？文本内容变了吗？
3. 把变化应用到真实 DOM。

**问题**：大部分属性其实是静态的，根本不会变。比如 `<div :class="..." :id="..." :value="...">`，编译器知道它**只有 class、id、value 是动态的**，其他所有属性都是静态的。但传统的 Diff 算法不知道，它必须逐一检查所有属性。

**Vue 的优化**：编译器在编译模板时，就把这些信息提前分析出来，并编码成一个数字（patch flag）附在虚拟节点上。运行时渲染器看到这个标记，**跳过所有静态属性的比对，只更新标记的那几种类型**。

---

##### 树结构打平

“区块”概念：内部结构是稳定的一个部分可被称之为一个区块。没有用到任何结构性指令 (比如 `v-if` 或者 `v-for`)。

```html
<div> <!-- root block -->
  <div>...</div>         <!-- 不会追踪 -->
  <div :id="id"></div>   <!-- 要追踪 -->
  <div>                  <!-- 不会追踪 -->
    <div>{{ bar }}</div> <!-- 要追踪 -->
  </div>
</div>
```

`v-if` 和 `v-for` 指令会创建新的区块节点：

```html
<div> <!-- 根区块 -->
  <div>
    <div v-if> <!-- if 区块 -->
      ...
    </div>
  </div>
</div>
```

---

打平：

编译的结果会被打平为一个数组，仅包含所有动态的后代节点：

```
div (block root)
- div 带有 :id 绑定
- div 带有 {{ bar }} 绑定
```

当这个组件需要重渲染时，只需要遍历这个打平的树而非整棵树。这也就是我们所说的**树结构打平**，这大大减少了我们在虚拟 DOM 协调时需要遍历的节点数量。模板中任何的静态部分都会被高效地略过。

---

### 渲染函数 & JSX

#### 基本用法

写得挺好挺简洁的，不用总结了：

https://cn.vuejs.org/guide/extras/render-function.html#basic-usage

```vue
<script setup lang="ts">
import { ref, h } from 'vue'

const count = ref(1)

// 直接在 <script setup> 里声明 render 函数
// 这个函数名必须是 render
function render() {
  return h('div', `Count is: ${count.value}`)
}
</script>
```

---

#### 渲染函数案例

https://cn.vuejs.org/guide/extras/render-function.html#render-function-recipes

---

### Vue 与 Web Components

自定义元素

https://cn.vuejs.org/guide/extras/web-components.html#vue-and-web-components

---

### 动画技巧

#### 基于 CSS class 的动画

对于那些不是正在进入或离开 DOM 的元素，我们可以通过给它们动态添加 CSS class 来触发动画：

https://cn.vuejs.org/guide/extras/animation.html#class-based-animations

`<Transition>` 是为“元素进入/离开 DOM”设计的，但很多交互场景中，元素**始终存在于页面上**，只是它的**状态发生了变化**（如“变成禁用”、“刚刚更新过”）。这时候你不需要让元素消失再出现，而是希望它在原位做一个“提醒”动画。

![image-20260525043922287](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260525043922287.png)

**典型应用场景**

- **表单验证反馈**：输入不合法时，输入框抖动提示。
- **按钮状态提示**：点击后按钮短暂变红闪烁，提示操作完成。
- **数据更新提醒**：列表项数据变化时，高亮闪烁一下。
- **错误提示**：支付失败时，金额文字抖动。

---

#### 状态驱动的动画

有些过渡效果可以通过动态插值来实现，比如在交互时动态地给元素绑定样式。看下面这个例子：

https://cn.vuejs.org/guide/extras/animation.html#state-driven-animations

![image-20260525044740333](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260525044740333.png)

**不依赖任何固定的 CSS 动画或关键帧，而是让元素的样式属性直接由响应式数据驱动，再配合 CSS `transition` 来实现平滑过渡。**

---

#### 基于侦听器的动画

通过发挥一些创意，我们可以基于一些数字状态，配合侦听器给任何东西加上动画。例如，我们可以将数字本身变成动画：

https://cn.vuejs.org/guide/extras/animation.html#animating-with-watchers

就是一些小技巧

![image-20260525045709681](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20260525045709681.png)

---

















































































































































































