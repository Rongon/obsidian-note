zustand

# 例子

```ts
import { create } from 'zustand'

type Store = {
  count: number
  inc: () => void
}

const useStore = create<Store>()((set) => ({
  count: 1,
  inc: () => set((state) => ({ count: state.count + 1 })),
}))

function Counter() {
  const { count, inc } = useStore()
  return (
    <div>
      <span>{count}</span>
      <button onClick={inc}>one up</button>
    </div>
  )
}
```

---

# 异步

没什么特别的，正常写异步方法，然后在set方法里更新

```js
const useStore = create( (set) = > {
	return {
		// 状态数据
		channelList: []
		// 异步方法
		fetchChannelList: async () => {
			const res = await fetch(URL)
			const jsonData = await res.json()
		}
		// 调用 set 方法更新状态
		set({
			channelList: jsonData.data.channels
		})
	}
})
```

---

# 切片

```js
import { create } from 'zustand'

// 创建counter相关切片
const createCountStroe = (set) => {
	return {
		count: 0,
		setCount: () => {
			set(state => ({ count: state.count + 1}))
		}
	}
}

// 创建channel相关切片
const createChannelStore = (set) => {
	return {
		channelList: []
		fetchGetList: async() => {
			const res = await fetch(URL)
			const jsonData = await res.json()
			set({ channelList: jsonData.channels })
		}
	}
}

// 组合切片
const useStore = create((...a) => ({
	...createCounterStore(...a),
	...createChannelStore(...a)
}))
```

---

# 深层次状态处理

 使用 immer 中间件：	npm install immer

```js
import { create } from 'zustand'
// 在zustand里的middleware中间件里引入
import { immer } from 'zustand/middleware/immer'

// 注意：使用 immer 中间件时的特殊结构
const useUserStore = create<User>()(immer(((set) => ({
    gourd: {
        oneChild: '大娃',
        twoChild: '二娃',
        threeChild: '三娃',
        fourChild: '四娃',
        fiveChild: '五娃',
        sixChild: '六娃',
        sevenChild: '七娃',
    },
    updateGourd: () => set((state) => {
        // 直接修改状态，无需手动合并
        state.gourd.oneChild = '大娃-超进化'
        state.gourd.twoChild = '二娃-谁来了'
        state.gourd.threeChild = '三娃-我来了'
    })
}))))
```

---

# 状态简化 useShallow

**解构/返回“新对象或新数组”时必须用；选择“单一基本类型值”时千万别用！**

**对象/嵌套对象使用，基本类型不使用**

回忆一下我们在使用`zustand`时，是这样引入状态的(如下),通过解构的方式引入状态，但是这样引入会引发一个问题，例如A组件用到了 `hobby.basketball` 状态，而B组件 没有用到 `hobby.basketball` 状态，但是更新`hobby.basketball`这个状态的时候，A组件和B组件都会重新渲染，这样就导致了不必要的重渲染，因为B组件并没有用到`hobby.basketball`这个状态。

![image](https://message163.github.io/react-docs/assets/repeat.Bw2FAn1K.jpg)

`useShallow` 只检查顶层对象的引用是否变化，如果顶层对象的引用没有变化（即使其内部属性或子对象发生了变化，但这些变化不影响顶层对象的引用），使用 useShallow 的组件将不会重新渲染。

```js
import useUserStore from '../../store/user';
import { useShallow } from 'zustand/react/shallow';
export default function Right() {
    console.log('B组件渲染')
    const { rap, name } = useUserStore(useShallow((state) => ({
        rap: state.hobby.rap,
        name: state.name
    })))
    return (
        <div className="right">
            <h1>B组件</h1>
            <div>
                <div>姓名：<span>{name}</span></div>
                <div>rap：<span>{rap}</span></div>
            </div>
        </div>
    )
}
```

---

# 中间件

例子：

```js
const logger = (config) => (set, get, api) => config((...args) => {
    console.log(api)
    console.log('before', get())
    set(...args)
    console.log('after', get())
}, get, api)
```

参数解释：

1. config (外层函数参数)
   - 类型：函数 (set, get, api) => StoreApi
   - 作用：原始创建 store 的配置函数，由用户传入。中间件需要包装这个函数。
2. set (内层函数参数)
   - 类型：函数 (partialState) => void
   - 作用：原始的状态更新函数，用于修改 store 的状态。
3. get (内层函数参数)
   - 类型：函数 () => State
   - 作用：获取当前 store 的状态值。
4. api (内层函数参数)
   - 类型：对象 StoreApi
   - 作用：包含 store 的完整 API（如 setState, getState, subscribe, destroy 等方法）。

---

## 内置中间件 devtools

```js
// 1.从zustand里引入
import { devtools } from 'zustand/middleware'
const useUserStore = create<User>()(
    immer(
        // 2.放在immer里面包裹内容
        devtools((set) => ({
            name: '坤坤',
            age: 18,
            hobby: {
                sing: '坤式唱腔',
                dance: '坤式舞步',
                rap: '坤式rap',
                basketball: '坤式篮球'
            },
            setHobbyRap: (rap: string) => set((state) => {
                state.hobby.rap = rap
            }),
            setHobbyBasketball: (basketball: string) => set((state) => {
                state.hobby.basketball = basketball
            })
        }),
            // 3.可以传递参数
            {
                enabled: true, // 是否开启devtools
                name: '用户信息', // 仓库名称
            }
        )
    )
)
```

---

## 持久化中间件persist

zustand内置了持久化中间件，无需引入第三方库。默认存储在 localStorage 中，可以指定存储方式。

```js
// 1.从zustand中引入persist
import { persist, createJSONStorage } from 'zustand/middleware'
const useUserStore = create<User>()(
    immer(
        // 2.注册中间件
        persist((set) => ({
            name: '坤坤',
            age: 18,
            hobby: {
                sing: '坤式唱腔',
                dance: '坤式舞步',
                rap: '坤式rap',
                basketball: '坤式篮球'
            },
            setHobbyRap: (rap: string) => set((state) => {
                state.hobby.rap = rap
            }),
            setHobbyBasketball: (basketball: string) => set((state) => {
                state.hobby.basketball = basketball
            })
        }),
            {
                name: 'user', // 仓库名称(唯一)
                storage: createJSONStorage(() => localStorage), // 3.存储方式 可选 localStorage sessionStorage IndexedDB 默认localStorage
            	// 4.partialize可以部分状态持久化，比如去掉hobby
                partialize: (state) => ({
                    name: state.name,
                    age: state.age,
                    hobby: state.hobby
                })
            }
        )
    )
)
```

---

清空缓存Api, 在页面中添加一个按钮，点击按钮清空缓存,在增加persist中间件之后会自动增加一个clearStorage方法,用于清空缓存。

clearStorage()

```js
import useUserStore from '../../store/user';
const App = () => {
    const clear = () => {
        useUserStore.persist.clearStorage()
    }
    return <div onClick={clear}>清空缓存</div>
}
```

---

# 订阅

决定用不用订阅，本质上是在问：**“数据的变化频率”和“界面（UI）的更新频率”是否一致？**

- **一致（数据变了，UI 就得变）** ──► **不用订阅**，直接用选择器 Hook。
- **不一致（数据频繁变，但 UI 偶尔才变一次 / 或者 UI 根本不需要变）** ──► **使用订阅**，把它挡在 React 渲染机制的外面。

## 示例：

```js
const store = create((set) => ({
  count: 0,
}));
//外部订阅
store.subscribe((state) => {
  console.log(state.count);
});
//组件内部订阅
useEffect(() => {
  store.subscribe((state) => {
    console.log(state.count);
  });
}, []);
```

---

## 订阅单个状态中间件`subscribeWithSelector` 

**大多数情况下都要使用**

持续优化，目前的订阅只要是store内部任意的state发生变化，都会触发回调函数，我们希望只订阅age的变化，可以使用中间件`subscribeWithSelector` 订阅单个状态。

```js
import { subscribeWithSelector } from 'zustand/middleware'
const store = create(subscribeWithSelector((set) => ({
  age: 0,
  name: '张三',
})));
const [status,setStatus] = useState('单身')
//订阅age的变化 并且组件渲染一次
useStore.subscribe(state => state.age, (age,prevAge) => {
   if(age >= 26){
    setStatus('结婚')
   }else{
    setStatus('单身')
   }
});
```

---

## 补充用法

1. subscribe 会返回一个取消订阅的函数，可以手动取消订阅。

```js
const unSubscribe = useStore.subscribe((state) => {
  console.log(state.age);
});
unSubscribe(); //取消订阅
```

2. 当你使用了`subscribeWithSelector`中间件的时候会多出来第三个参数`options`

- equalityFn 比较函数
- fireImmediately 是否立即触发

```js
const unSubscribe = useStore.subscribe(state => state.age, (age,prevAge) => {
  console.log(age,prevAge);
}, {
  equalityFn: (a, b) => a === b, // 默认是浅比较，如果需要深比较，可以传入一个比较函数
  fireImmediately: true, // 默认是false，如果需要立即触发，可以传入true
});
```

