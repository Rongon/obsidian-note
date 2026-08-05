# React 状态驱动视图

npx create-react-app react-basic

---
## 基础语法
### 循环渲染map

```react
function App() {
  return (
    <div className="App">
      this is App
      <ul>
        {list.map(item => <li key={item.id}>{item.name}</li>)}
      </ul>
    </div>
  );
}
```

---

### 条件渲染&&/?:/ifelse

```react
// &&
{ flag && <span>this is a span</span> }

//三元运算符
{ flag ? <span>this is a span</span> : <span>this isn't a span</span> }
```

---

### 传递自定义参数()=>{}

```react
//如果想传递自定义参数，必须用箭头函数，不能直接调用函数
function App() {
    const clickHandler = (name, e) => {
        console.log('xxx')
    }
    return <button onClick={() => clickHandler('jack', e)}>click me</button>
}
```

---

### 组件

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240115052043640.png" alt="image-20240115052043640" style="zoom: 67%;" />

---

### useState状态变量

```react
import { useState } from "react"
//例：count为状态变量，setCount为修改函数，0为默认参数
const [count, setCount] = useState(0)
```

**修改规则：只能用函数来修改，包括数组，对象**

---

### 受控表单绑定

**使用useState控制表单状态**

![image-20240115054521504](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240115054521504.png)

```react
const [value, setValue] = useState('')

<input type='text' value={value} onChange={(e) => setValue(e.target.value)} />
```

---

### 获取DOM(useRef)

```react
import xxx

const inputRef = useRef(null)

<input type="text" ref={inputRef} />
//.current
console.log(inputRef.current)
```

---

### 父传子

**在父组件中的子组件标签内进行属性绑定，在子组件中props接收参数**

```react
function Son(props) {
  return (
    <div>
      this is Son: {props.name}
    </div>
  );
}

const name = 'fatherApp';

function App() {
  return (
    <div className="App">
      this is App
      <Son name={name}/>
    </div>
  );
}

export default App;
```

---

### 特殊的props：children

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240115062219042.png" alt="image-20240115062219042" style="zoom:50%;" />

---

### 子传父

**子组件调用父组件的方法同时传递参数过去**

```react
function Son({onGetMessage}) {
  const sonMsg = 'sonMsg' 
  return (
    <div className="App">
      <button onClick={()=>onGetMessage(sonMsg)}>get message</button>
    </div>
  );
}

function App() {
  const getMessage = () => {
    console.log('get message');
  }
  return (
    <div className="App">
      this is App
      <Son onGetMessage={getMessage}></Son>
    </div>
  );
}

export default App;

```

---

### 兄弟组件传递

**A----父----B**

**父组件可以通过useState维护传递**

---

### 跨层级传递

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240115072320879.png" alt="image-20240115072320879" style="zoom: 67%;" />

```react
import { createContext, useContext } from "react";

const Ctx = createContext()

function A() {
  return(
    <div>
      this is A 
      <B/>
    </div>
  )
}

function B() {
  const appMsg = useContext(Ctx);
  return(
    <div>
      this is B , {appMsg}
    </div>
  )
}

function App() {
  const appMsg = 'this is appMsg';
  return (
    <div className="App">
      <Ctx.Provider value={appMsg}>
        this is App
        <A/>
      </Ctx.Provider>
    </div>
  );
}

export default App;
```

---

### useEffect

用于创建不是由事件引起而是**由渲染本身引起的操作**，如：AJAX请求，更改DOM

useEffect(()=>{}, [])

第一个参数()=>{}：执行操作

第二个参数依赖项：空数组只在组件渲染完毕后执行一次，不同依赖性会有不同的操作

```react
import { useEffect, useState } from "react";

const URL = "http://geek.itheima.net/v1_0/channels";

function App() {
  const [list, setList] = useState([]);
  useEffect(() => {
    async function getList() {
      const res = await fetch(URL);
      const resList = await res.json();
      setList(resList.data.channels);
    }
    getList();
  }, []);
  return (
    <div className="App">
      this is App
      <ul>
        {list.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

#### **依赖项：**

useEffect(()=>{}, )

useEffect(()=>{}, [])

useEffect(()=>{}, [count])

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240116013846752.png" alt="image-20240116013846752" style="zoom: 50%;" />

---

#### 清除副作用

​	比如在useEffect中开启了一个定时器，在组件卸载时清除这个定时器。

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240116015250313.png" alt="image-20240116015250313" style="zoom:50%;" />

---

### 自定义hook

​	use开头的函数，通过自定义hook实现逻辑的封装和复用。

```react
function useGetList(){
    xxx
    return{
        //返回函数外要使用的变量
    }
}
```

---

### ReactHooks使用规则

1. 不能在组件外使用
2. 不能在if/for/其他函数中使用

---

## Redux

1. reducer函数定义状态

​	参数：

​		state: 初始状态

​		action.type:标记如何修改

```react
function reducer(state= { count: 0 }, action) {
    if(action.type === 'INCREMENT') {
        return { count: state.count + 1 }
    }
    if(action.type === 'DECREMENT') {
        return { count: state.count + 1 }
    }
    return state
}
```

2. 使用reducer函数生成store实例

```react
const store = Redux.createState(reducer)
```

3. 通过store.subscribe订阅数据变化

```react
store.subscribe(() => {
    console.log("xxxxxx")
})
```

4. store.dispatch函数声明type

```react
store.dispatch({
    type: 'INCREMENT'
})
```

5. 通过store.getState获取最新状态更新到视图中

```
document.getEmlementById('count').innerText = store.getState().count
```

**reducer**/**state**/**action**

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240116030513444.png" alt="image-20240116030513444" style="zoom:50%;" />

---

### Redux的两个插件

![image-20240116031201873](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240116031201873.png)

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240116031216794.png" alt="image-20240116031216794" style="zoom: 67%;" />

#### reduxjs/toolkit的createSlice方法

**counterStore.js**

```react
import { createSlice } from "@reduxjs/toolkit";

const counterStore = createSlice({
    name: "counter",
    // 初始化state
    initialState: {
    count: 0,
    },
    // 修改状态的方法
    reducers: {
        increment(state) {
            state.count += 1;
        },
        decrement(state) {
            state.count -= 1;
        },
    },
});
// 解构actionCreater函数
const { increment, decrement } = counterStore.actions;
// 获取reducer
const reducer = counterStore.reducer;
// 按需导出actionCreater
export { increment, decrement };
// 以默认方式导出reducer
export default reducer;
```

**store/index.js**

```react
import { configureStore } from "@reduxjs/toolkit";

import counterReducer from './modules/counterStore'

const store = configureStore({
    reducer: {
        counter: counterReducer
    }
})

export default store
```

#### react-redux内置Provide组件

**根index.js**

```react
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import store from './store';
import { Provider } from 'react-redux';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Provider store={store}>
        <App />
    </Provider>
);
```

#### useSelector使用

​	在组件中要使用store数据，就要使用useSelector函数

```react
import { useSelector } from "react-redux";

function App() {
  const { count } = useSelector(state => state.counter);
  return (
    <div className="App">
      this is App:{count}
    </div>
  );
}

export default App;
```

#### useDispatch修改

```react
import { useSelector, useDispatch } from "react-redux";
import { increment, decrement } from './store/modules/counterStore'

function App() {
  const { count } = useSelector(state => state.counter);
  const dispatch = useDispatch()
  return (
    <div className="App">
      <button onClick={() => dispatch(increment())}>+</button>
      this is App:{count}
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  );
}

export default App;
```

#### 提交action传参（action.payload）

```react
addToNum(state, action) {
	state.count = action.payload
}
```

```
<button onClick={()=>dispatch(addToNum(10))}></button>
```

#### 异步

```react
const { setChannels } = channelStore.actions

const fetchChannelList = () => {
    return async dispatch => {
        try {
            const res = await axios.get('http://geek.itheima.net/v1_0/channels')
            dispatch(setChannels(res.data.data.channels))
        } catch (error) {
            console.log(error)
        }
    }
}
```

```react
  // 使用useEffect触发异步请求
  useEffect(() => {
    dispatch(fetchChannelList())
  }, [dispatch])
```

---

## ReactRouter

**npm i react-router-dom**

### createBrowserRouter, RouterProvide组件

```react
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

const router = createBrowserRouter([
  {
    path: '/login',
    element: <div>我是登录页</div>
  },
  {
    path: '/article',
    element: <div>我是文章页</div>
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router}></RouterProvider>
  </React.StrictMode>
);
```

---

### 声明式（Link组件）/编程式（useNavigate方法）导航

```react
import { Link, useNavigate } from 'react-router-dom'

const Login = () => {
    const navigate = useNavigate()
    return(
        <div>
            <div>我是登录页111111111111</div>
            //声明式导航
            <Link to='/article'>跳转到文章页</Link>
            //编程式导航
            <button onClick={() => {navigate('/article')}}>跳转到文章页</button>
        </div>
    )
}

export default Login
```

---

### 传参

#### useSearchParams()

```react
import { useSearchParams } from "react-router-dom"

const Article = () => {
    const [params] = useSearchParams()
    const id = params.get('id')
    const name = params.get('name')
    return (
        <div>我是文章页-searchParams传参/id：{id}/name：{name}</div>
    )
}
```

#### params()(要修改router.js)

```react
//article.js
import { useParams } from "react-router-dom"

const Article = () => {
    const {id, name} = useParams()
    return (
        <div>我是文章页-params传参/id：{id}/name：{name}</div>
    )
}

//router.js
import Login from "../page/Login/login";
import Article from "../page/Article/article";
import { createBrowserRouter } from 'react-router-dom'

const router = createBrowserRouter([
    {
        path: '/login',
        element: <Login />
    },
    {
        path: '/article/:id/:name',//这里修改
        element: <Article />
    }

])
```

---

### 嵌套路由

1. 使用children属性配置路由嵌套关系

```
{
    path: '/',
    element: <Layout />,
    children: [
        {
            path: '/about',
            element: <About />
        },
        {
            path: '/board',
            element: <Board />
        }
    ]
}
```

2. 使用**<Outlet/>**组件设定位置

```react
import { Link, Outlet } from 'react-router-dom'

const layout = () => {
    return(
        <div>
            <div>我是layout组件</div>
            <Link to='/about'>关于</Link>
            <Link to='/board'>面板</Link>
            <Outlet/>
        </div>
    )
}

export default layout
```

---

### 默认二级路由

**想要默认展示的路由不设置path，直接设置index: true**

![image-20240117064001123](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240117064001123.png)<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240117064125809.png" alt="image-20240117064125809" style="zoom: 67%;" />

---

### 404路由

![image-20240117064739474](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240117064739474.png)

---

### history和hash

![image-20240117065336964](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240117065336964.png)

1. history模式使用createBrowserRouter()

```
const router = createBrowserRouter([
    {},{}
])
```

2. hash模式使用createHashRouter()

```
const router = createHashRouter([
    {},{}
])
```

---

## blog项目

### @别名设置

​	**安装craco包**

```
npm i @craco/craco -D
```

​	**配置craco.config.js**

```
const path = require('path')

module.exports = {
  // webpack 配置
  webpack: {
    // 配置别名
    alias: {
      // 约定：使用 @ 表示 src 文件所在路径
      '@': path.resolve(__dirname, 'src')
    }
  }
}
```

​	**配置package.json**

```
"scripts": {
  "start": "craco start",
  "build": "craco build",
  "test": "craco test",
  "eject": "react-scripts eject"
}
```

​	**vscode联想设置,jsconfig.json**

```
{
  "compilerOptions": {
    "baseUrl": "./",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

---

### axios注入token

![image-20240208005946813](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240208005946813.png)

```react
// 添加请求拦截器
request.interceptors.request.use(
  (config) => {
    // 操作config 注入token
    // 1. 获取token
    // 2. 按照后端格式拼接token
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
```

---

### 使用Token做路由权限控制

![image-20240208011600576](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240208011600576.png)

```react
import { Navigate } from "react-router-dom";
import { getToken } from "@/utils/token";

export function AuthRoute({ children }) {
  const token = getToken();
  if (token) {
    return <>{children}</>
  }else{
    return <Navigate to={'/login'} replace></Navigate>
  }
}
```

---

### useLocation()获取路径

```react
const location = useLocation()
```

---

### 处理token失效

![image-20240208051533692](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240208051533692.png)

```react
```

---

### 富文本编辑器

![image-20240209222216999](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240209222216999.png)

---

### 打包

npm run build
npm install -g serve
serve -s build

---

### 懒加载

```react
// import Home from "@/pages/Home/Home";
// import Article from "@/pages/Article/Article";
// import Publish from "@/pages/Publish/Publish";


// 懒加载
const Home = lazy(() => import("@/pages/Home/home"));
const Article = lazy(() => import("@/pages/Article/article"));
const Publish = lazy(() => import("@/pages/Publish/publish"));

const router = createBrowserRouter([
  {
    path: "/",
    element: (<AuthRoute><Layout /></AuthRoute>),
    children: [
      {
        index: true,
        element: (
            //懒加载Suspense组件
          <Suspense fallback="Loading..."><Home></Home></Suspense>
        ),
      },
      {
        path: "article",
        element: (<Suspense fallback="Loading..."><Article></Article></Suspense>),
      },
      {
        path: "publish",
        element: (<Suspense fallback="Loading..."><Publish></Publish></Suspense>),
      },
    ],
  },
  {
    path: "/Login",
    element: <Login />,
  },
]);
```

---

### 包体积可视化

1. npm i source-map-explorer
2. "scripts": {
     "analyze": "source-map-explorer 'build/static/js/*.js'",
   }
3. npm run analyze

---

### cdn

1. craco.config.js

```react
// 添加自定义对于webpack的配置

const path = require('path')
const { whenProd, getPlugin, pluginByName } = require('@craco/craco')

module.exports = {
  // webpack 配置
  webpack: {
    // 配置别名
    alias: {
      // 约定：使用 @ 表示 src 文件所在路径
      '@': path.resolve(__dirname, 'src')
    },
    // 配置webpack
    // 配置CDN
    configure: (webpackConfig) => {
      let cdn = {
        js:[]
      }
      whenProd(() => {
        // key: 不参与打包的包(由dependencies依赖项中的key决定)
        // value: cdn文件中 挂载于全局的变量名称 为了替换之前在开发环境下
        webpackConfig.externals = {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
        // 配置现成的cdn资源地址
        // 实际开发的时候 用公司自己花钱买的cdn服务器
        cdn = {
          js: [
            'https://cdnjs.cloudflare.com/ajax/libs/react/18.1.0/umd/react.production.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.1.0/umd/react-dom.production.min.js',
          ]
        }
      })

      // 通过 htmlWebpackPlugin插件 在public/index.html注入cdn资源url
      const { isFound, match } = getPlugin(
        webpackConfig,
        pluginByName('HtmlWebpackPlugin')
      )

      if (isFound) {
        // 找到了HtmlWebpackPlugin的插件
        match.userOptions.files = cdn
      }

      return webpackConfig
    }
  }
}
```

2. index.html

```react
<body>
  <div id="root"></div>
  <!-- 加载第三发包的 CDN 链接 -->
  <% htmlWebpackPlugin.options.files.js.forEach(cdnURL => { %>
    <script src="<%= cdnURL %>"></script>
  <% }) %>
</body>
```

---

## 拓展-优化

### useReducer(与redux类似)

```react
// 1. 根据不同的action返回不同的新状态
function reducer(state, action) {
  switch (action.type) {
    case 'INC':
      return state + 1
    case 'DEC':
      return state - 1
    case 'UPDATE':
      return state + action.payload
    default:
      return state
  }
}
function App() {
  // 2. 使用useReducer分派action
  const [state, dispatch] = useReducer(reducer, 0)
  return (
    <div>
      {/* 3. 调用dispatch函数传入action对象 触发reducer函数，分派action操作，使用新状态更新视图 */}
      <button onClick={() => dispatch({ type: 'DEC' })}>-</button>
      {state}
      <button onClick={() => dispatch({ type: 'INC' })}>+</button>
      <button onClick={() => dispatch({ type: 'UPDATE', payload: 100 })}>
        update to 100
      </button>
    </div>
  )
}
```

---

### useMemo(缓存性能优化。一般不会用，除非计算量很大)

​	因为每当任何一个状态发生变化时，组件都会刷新而重新渲染，因此num的改变也会引起重新渲染从而执行函数，然而我们只想count变化时才执行函数重新渲染。

```react
function fib (n) {
  console.log('计算函数执行了')
  if (n < 3) return 1
  return fib(n - 2) + fib(n - 1)
}
function App() {
  const [count, setCount] = useState(0)
  // 计算斐波那契之和
  // const sum = fib(count)
  // 通过useMemo缓存计算结果，只有count发生变化时才重新计算
  const sum = useMemo(() => {
    return fib(count)
  }, [count])
  const [num, setNum] = useState(0)
  return (
    <>
      {sum}
      <button onClick={() => setCount(count + 1)}>+count:{count}</button>
      <button onClick={() => setNum(num + 1)}>+num:{num}</button>
    </>
  )
}
```

---

### memo()(只有props修改时才会重新渲染)

​	**因为react父组件更新渲染时子组件也会强制更新渲染，然而不必要**

```react
//只需将子组件用memo函数包裹一下即可
const MemoSon = memo(function Son() {
  console.log('子组件被重新渲染了')
  return <div>this is span</div>
})

function App() {
  const [, forceUpdate] = useState()
  console.log('父组件重新渲染了')
  return (
    <>
      //用MemoSon组件替换Son组件
      <MemoSon />
      <button onClick={() => forceUpdate(Math.random())}>update</button>
    </>
  )
}
```

---

### memo()的props的比较机制

​	react会对每一个prop使用OBject.is比较新值和老值

​	简单类型返回true，引用类型返回false

---

### useCallback()缓存函数

​	useCallback缓存之后的函数可以在组件渲染时保持引用稳定，也就是返回同一个引用

```react
const MemoSon = memo(function Son() {
  console.log('Son组件渲染了')
  return <div>this is son</div>
})
function App() {
  const [, forceUpate] = useState()
  console.log('父组件重新渲染了')
    //使用useCallback缓存onGetSonMessage函数
  const onGetSonMessage = useCallback((message) => {
    console.log(message)
  }, [])
  return (
    <div>
       /*将onGetSonMessage作为prop传给子组件*/
      <MemoSon onGetSonMessage={onGetSonMessage} />
      <button onClick={() => forceUpate(Math.random())}>update</button>
    </div>
  )
}
```

---

## 拓展

### forwardRef() 使用ref暴露DOM节点给父组件

​	如：父组件通过ref获取到子组件内部的input元素让其聚焦

```react
//子组件
const Input = forwardRef((props, ref) => {
    return <input type="text" ref={ref}/>
})
//父组件
function App(){
    //这样inputRef就可以获取到子组件的input实例
    const inputRef = useRef(null)
    return{
        <div>
        	<Input ref={inputRef}/>
        </div>
    }
}
```

---

### useInperativeHandle() 通过ref暴露子组件的方法

​	如：父组件通过ref获取到子组件内部的input元素的focus方法让其聚焦

```react
//子组件
const Input = forwardRef((prop, ref) => {
    const inputRef = useRef(null)
    //聚焦逻辑函数
    const focusHandler = () => {
        inputRef.current.focus()
    }
})
//暴露函数给父组件调用
useImperativeHandle(ref, () => {
    return {
        //想暴露什么函数就返回出去
        focusHandler
    }
    return <input type="text" ref={inputRef}/>
})
// 父组件
function App (){
	const sonRef = useRef(null)
	const focusHandler = () => {
		sonRef.current.focusHandler()
    }
	return(
        <>
    	<Son ref={sonRef} />
		<button onClick={focusHandler}>focus</button>
        </>
    )
}
```

---

### 老react的class组件

```react
class Counter extends Component {
  // 状态变量
  state = {
    count: 0,
  }
  // 事件回调
  clickHandler = () => {
    // 修改状态变量 触发UI组件渲染
    this.setState({
      count: this.state.count + 1,
    })
  }
  // UI模版
  render() {
    return <button onClick={this.clickHandler}>+{this.state.count}</button>
  }
}
function App() {
  return (
    <div>
      <Counter />
    </div>
  )
}
```

---

### 类组件的生命周期

![image-20240212064936594](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240212064936594.png)

---

### 类组件父子通信

#### 父传子

```react
//子组件
class Son extends Component {
    render(){
        //this.props.msg获取到父组件传递的数据
        return <div>我是子组件{this.props.msg}</div>
    }
}
//父组件
class Parent extends Component {
    state={
        msg: 'this is parent msg'
    }
    render(){
        //使用this
        return <div>我是父组件<Son msg={this.state.msg} /></div>
    }
}
```

#### 子传父

```react
// 子组件
class Son extends Component {
	render(){
	// 使用this.props.msg
	return <>
		<div>我是子组件 {this.props.msg}</div>
		<button onClick={() => this.props.onGetSonMsg("我是son组件中的数据"}>sendMsgToParent</button>
		</>
	}
}
// 父组件
class Parent extends Component {
	state = {
		msg: 'this is parent msg
    }
	getSonMsg = (sonMsg) => {
        console.Log(sonMsg)
    }
    render (){
		return <div>我是父组件<Son msg={this.state.msg} onGetSonMsg={this.getSonMsg} /></div>
    }
}
```

---

## 新状态管理器zustand

```react
import { create } from 'zustand'

//set固定，state固定
const useStore = create((set) => ({
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

### 异步

![image-20240213031006485](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213031006485.png)

![image-20240213031152516](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213031152516.png)

---

### 切片模式(多个store分块)

```react
// 创建counter相关切片
const createCounterStore = (set) => {
  return {
    count: 0,
    setCount: () => {
      set(state => ({ count: state.count + 1 }))
    }
  }
}
// 创建channel相关切片
const createChannelStore = (set) => {
  return {
    channelList: [],
    fetchGetList: async () => {
      const res = await fetch(URL)
      const jsonData = await res.json()
      set({ channelList: jsonData.data.channels })
    }
  }
}
// 组合切片
//形参...a为固定写法
const useStore = create((...a) => ({
  ...createCounterStore(...a),
  ...createChannelStore(...a)
}))
function App() {
    //引用组合useStore
  const {count, inc, channelList, fetchChannelList } = useStore()
  return (
    <>
      <button onClick={inc}>{count}</button>
      <ul>
        {channelList.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </>
  )
}
```

---

## react+ts+vite

npm create vite@latest react-ts-pro -- --template react+ts

---

### useState传递泛型参数

![image-20240213042428161](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213042428161.png)

---

### useState-设初始值null

​	**当我们不知道状态的初始值是什么，将useState的初始值为null是一个常见的做法，可以通过具体类型联合null来做显式注解**

![image-20240213043056775](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213043056775.png)

---

### props

![image-20240213043644483](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213043644483.png)

---

### children
​	**children是一个比较特殊的prop，支持多种不同类型数据的传入，需要通过一个内置的ReactNode类型来做注解**

​	**注解之后，children可以是多种类型，包括: React.ReactElement、string、number
React.ReactFragment 、React.ReactPortal 、boolean、null 、undefined**

![image-20240213044311746](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213044311746.png)

---

### useRef

​	**直接把要获取的dom元素的类型当成泛型参数传递给useRef**

​	**.current可以获取到当前dom，从而.出方法**

![image-20240213061927559](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213061927559.png)

---

### useRef作稳定的存储器

​	**把useRef当成引用稳定的存储器，可以通过泛型传入联合类型来做。如：定时器**

![image-20240213062456293](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240213062456293.png)

---

