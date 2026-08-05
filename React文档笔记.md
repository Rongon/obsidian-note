react

## 描述UI

### 使用JSX书写标签语言

#### 为什么多个 JSX 标签需要被一个父元素包裹？

​	JSX 虽然看起来很像 HTML，但在底层其实被转化为了 JavaScript 对象，你不能在一个函数中返回多个对象，除非用一个数组把他们包装起来。

---

#### 使用JSX转化器

​	现有的 HTML 中的所有属性转化 JSX 的格式是很繁琐的。我们建议使用 [转化器](https://transform.tools/html-to-jsx) 将 HTML 和 SVG 标签转化为 JSX。这种转化器在实践中非常有用。

---

### 在JSX中通过大括号使用JS

---

### 将Props传递给组件

#### 父子组件传递

父组件传递props：

```react
export default function Profile() {
  return (
    <Avatar
      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}
      size={100}
    />
  );
}
```

子组件读取props：

```react
function Avatar({ person, size }) {
  // 在这里 person 和 size 是可访问的
}
```

---

#### 将jsx作为子组件传递children prop

​	爷组件Profile将子组件Avatar作为jsx传递给了父组件Card，父组件Card将size person属性传递给了子组件Avatar

```react
import Avatar from './Avatar.js';

function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

export default function Profile() {
  return (
    <Card>
      <Avatar
        size={100}
        person={{ 
          name: 'Katsuko Saruhashi',
          imageId: 'YfeOqp2'
        }}
      />
    </Card>
  );
}
```

---

### 渲染列表

#### 步骤: map()

​	需要时还可以使用filter()过滤数据之后再map()

```react
const people = [
  '凯瑟琳·约翰逊: 数学家',
  '马里奥·莫利纳: 化学家',
  '穆罕默德·阿卜杜勒·萨拉姆: 物理学家',
  '珀西·莱温·朱利亚: 化学家',
  '苏布拉马尼扬·钱德拉塞卡: 天体物理学家',
];

const listItems = people.map(person => <li>{person}</li>);

return <ul>{listItems}</ul>;
```

---

## 添加交互

### 响应事件

#### 普通函数

​	事件处理函数有如下特点:

​	- 通常在你的组件 **内部** 定义。

​	- 名称以 `handle` 开头，后跟事件名称。

---

#### 命名普通函数的prop

​	按照惯例，事件处理函数 props 应该以 `on` 开头。

---

#### 事件传播/冒泡

```react
export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('你点击了 toolbar ！');
    }}>
      <button onClick={() => alert('正在播放！')}>
        播放电影
      </button>
      <button onClick={() => alert('正在上传！')}>
        上传图片
      </button>
    </div>
  );
}
```

​	正在播放！->你点击了 toolbar ！	正在上传！->你点击了 toolbar ！

​	**阻止传播**： `e.stopPropagation()` 

​	**阻止默认行为**：`e.preventDefault()`

---

### 把一系列state更新加入队列

#### 在下次渲染前多次更新同一个state

```react
// 无效
	<button onClick={() => {
        setNumber(number + 1);
        setNumber(number + 1);
        setNumber(number + 1);
	}}>+3</button>

//正解
	<button onClick={() => {
        setNumber(n => n + 1);
        setNumber(n => n + 1);
        setNumber(n => n + 1);
	}}>+3</button>
```

#### 命名惯例

通常可以通过相应 state 变量的第一个字母来命名更新函数的参数：

```react
setEnabled(e => !e);
setLastName(ln => ln.reverse());
setFriendCount(fc => fc * 2);
```

---

#### 更新state中的对象

​	**当对象中有多个属性只想更改其中一个时，可以使用展开语法**

```react
setPerson({
  ...person, // 复制上一个 person 中的所有字段
  firstName: e.target.value // 但是覆盖 firstName 字段 
});
```

---

​	**使用immer库可以扁平化，不用展开而是用平常的语法修改state里的对象**

```react
updatePerson(draft => {
  draft.artwork.city = 'Lagos';
});
```

---

#### 更新数组

​	**要使用返回新数组的方法以避免修改原数组**

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240827144026484.png" alt="image-20240827144026484" style="zoom:50%;" />

​	**使用 `immer`库就可以使用所有方法了**

---

## 状态管理

### 对state进行保留和重置

#### 状态与渲染树中的位置相关 

​	**只要一个组件还被渲染在 UI 树的相同位置，React 就会保留它的 state。** 如果它被移除，或者一个不同的组件被渲染在相同的位置，那么 React 就会丢掉它的 state。

​	假如点击事件用另一个组件切换了该UI树中的组件，那么state会消失，再切换回来会重置。

​	并且，**当你在相同位置渲染不同的组件时，组件的整个子树都会被重置**。一般来说，**如果你想在重新渲染时保留 state，几次渲染中的树形结构就应该相互“匹配”**。结构不同就会导致 state 的销毁，因为 React 会在将一个组件从树中移除时销毁它的 state。

---

### 迁移状态逻辑至reducer中

#### 步骤

1. 将设置状态的逻辑 **修改** 成 dispatch 的一个 action；
2. **编写** 一个 reducer 函数；
3. 在你的组件中 **使用** reducer。

---

1. 将setxxx改成dispatch

```react
//改之前
function handleAddTask(text) {
  setTasks([
    ...tasks,
    {
      id: nextId++,
      text: text,
      done: false,
    },
  ]);
}

function handleChangeTask(task) {
  setTasks(
    tasks.map((t) => {
      if (t.id === task.id) {
        return task;
      } else {
        return t;
      }
    })
  );
}

function handleDeleteTask(taskId) {
  setTasks(tasks.filter((t) => t.id !== taskId));
}
//改之后
//dispatch里的对象叫做'action'
function handleAddTask(text) {
  dispatch({
    type: 'added',
    id: nextId++,
    text: text,
  });
}

function handleChangeTask(task) {
  dispatch({
    type: 'changed',
    task: task,
  });
}

function handleDeleteTask(taskId) {
  dispatch({
    type: 'deleted',
    id: taskId,
  });
}
```

2. 编写一个reducer函数

​	由于 `reducer` 函数接受 `state`（tasks）作为参数，因此可以 **在组件之外声明它**。这减少了代码的缩进级别，提升了代码的可读性。

```react
//通常使用switch匹配
function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [
        ...tasks,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];
    }
    case 'changed': {
      return tasks.map((t) => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter((t) => t.id !== action.id);
    }
    default: {
      throw Error('未知 action: ' + action.type);
    }
  }
}
```

3. 在组件中引入

```react
import { useReducer } from 'react';
//替换前
const [tasks, setTasks] = useState(initialTasks);
//替换后
const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
```

`useReducer` 钩子接受 2 个参数：

1. 一个 reducer 函数
2. 一个初始的 state

它返回如下内容：

1. 一个有状态的值
2. 一个 dispatch 函数（用来 “派发” 用户操作给 reducer）

---

#### 使用immer简化reducer中的增删改等操作

​	`draft`

```react
//改之前
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';
import tasksReducer from './tasksReducer.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task,
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId,
    });
  }

  return (
    <>
      <h1>布拉格的行程安排</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: '参观卡夫卡博物馆', done: true},
  {id: 1, text: '看木偶戏', done: false},
  {id: 2, text: '打卡列侬墙', done: false},
];
export default function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [
        ...tasks,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];
    }
    case 'changed': {
      return tasks.map((t) => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter((t) => t.id !== action.id);
    }
    default: {
      throw Error('未知 action：' + action.type);
    }
  }
}


//改之后
import { useImmerReducer } from 'use-immer';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

function tasksReducer(draft, action) {
  switch (action.type) {
    case 'added': {
      draft.push({//主要修改了这里，可以直接push
        id: action.id,
        text: action.text,
        done: false,
      });
      break;
    }
    case 'changed': {
      const index = draft.findIndex((t) => t.id === action.task.id);
      draft[index] = action.task;//可以直接修改
      break;
    }
    case 'deleted': {
      return draft.filter((t) => t.id !== action.id);
    }
    default: {
      throw Error('未知 action：' + action.type);
    }
  }
}

export default function TaskApp() {
  const [tasks, dispatch] = useImmerReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task,
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId,
    });
  }

  return (
    <>
      <h1>布拉格的行程安排</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: '参观卡夫卡博物馆', done: true},
  {id: 1, text: '看木偶戏', done: false},
  {id: 2, text: '打卡列侬墙', done: false},
];
```

---

### 使用context深层传递参数

#### 步骤

1. **创建** 一个 context
2. 在需要数据的组件内 **使用** 刚刚创建的 context
3. 在指定数据的组件中 **提供** 这个 context

---

1. 创建

```react
//LevelContext.js
import { createContext } from 'react';

export const LevelContext = createContext(1);

```

2. 使用

```react
import { useContext } from 'react';
import { LevelContext } from './LevelContext.js';

export default function Heading({ children }) {
  const level = useContext(LevelContext);
  // ...
}
```

3. 提供

```react
import { LevelContext } from './LevelContext.js';

export default function Section({ level, children }) {
  return (
    <section className="section">
      <LevelContext.Provider value={level}>
        {children}
      </LevelContext.Provider>
    </section>
  );
}
```

---

#### Context 会穿过中间层级的组件 

​	Context 的工作方式可能会让你想起 CSS 属性继承。在 CSS 中，你可以为一个 `<div>` 手动指定 `color: blue`，并且其中的任何 DOM 节点，无论多深，都会继承那个颜色，除非中间的其他 DOM 节点用 `color: green` 来覆盖它。

​	类似地，在 React 中，覆盖来自上层的某些 context 的唯一方法是将子组件包裹到一个提供不同值的 context provider 中。

​	在 CSS 中，诸如 `color` 和 `background-color` 之类的不同属性不会覆盖彼此。你可以设置所有 `<div>` 的 `color` 为红色，而不会影响 `background-color`。

​	类似地，**不同的 React context 不会覆盖彼此**。你通过 `createContext()` 创建的每个 context 都和其他 context 完全分离，只有使用和提供 **那个特定的** context 的组件才会联系在一起。一个组件可以轻松地使用或者提供许多不同的 context。

---

#### 写在你使用 context 之前 

​	使用 Context 看起来非常诱人！然而，这也意味着它也太容易被过度使用了。**如果你只想把一些 props 传递到多个层级中，这并不意味着你需要把这些信息放到 context 里。**

在使用 context 之前，你可以考虑以下几种替代方案：

1. **从 传递 props开始。** 如果你的组件看起来不起眼，那么通过十几个组件向下传递一堆 props 并不罕见。这有点像是在埋头苦干，但是这样做可以让哪些组件用了哪些数据变得十分清晰！维护你代码的人会很高兴你用 props 让数据流变得更加清晰。

2. **抽象组件并 将 JSX 作为 `children` 传递给它们。** 如果你通过很多层不使用该数据的中间组件（并且只会向下传递）来传递数据，这通常意味着你在此过程中忘记了抽象组件。

   ​	举个例子，你可能想传递一些像 `posts` 的数据 props 到不会直接使用这个参数的组件，类似 `<Layout posts={posts} />`。取而代之的是，让 `Layout` 把 `children` 当做一个参数，然后渲染 `<Layout><Posts posts={posts} /></Layout>`。这样就减少了定义数据的组件和使用数据的组件之间的层级。

如果这两种方法都不适合你，再考虑使用 context。

#### Context 的使用场景 

- **主题：** 如果你的应用允许用户更改其外观（例如暗夜模式），你可以在应用顶层放一个 context provider，并在需要调整其外观的组件中使用该 context。
- **当前账户：** 许多组件可能需要知道当前登录的用户信息。将它放到 context 中可以方便地在树中的任何位置读取它。某些应用还允许你同时操作多个账户（例如，以不同用户的身份发表评论）。在这些情况下，将 UI 的一部分包裹到具有不同账户数据的 provider 中会很方便。
- **路由：** 大多数路由解决方案在其内部使用 context 来保存当前路由。这就是每个链接“知道”它是否处于活动状态的方式。如果你创建自己的路由库，你可能也会这么做。
- **状态管理：** 随着你的应用的增长，最终在靠近应用顶部的位置可能会有很多 state。许多遥远的下层组件可能想要修改它们。通常 将 reducer 与 context 搭配使用来管理复杂的状态并将其传递给深层的组件来避免过多的麻烦。

​	Context 不局限于静态值。如果你在下一次渲染时传递不同的值，React 将会更新读取它的所有下层组件！这就是 context 经常和 state 结合使用的原因。

一般而言，如果树中不同部分的远距离组件需要某些信息，context 将会对你大有帮助。

---

### 使用reducer和context拓展应用

#### 结合使用reducer和context

步骤：

1. **创建** context。
2. 将 state 和 dispatch **放入** context。
3. 在组件树的任何地方 **使用** context。

---

1. 

```react
import { createContext } from 'react';
//创建两个context来对应reducer的tasks和initial
export const TasksContext = createContext(null);
export const TasksDispatchContext = createContext(null);
```

2. 

```react
import { TasksContext, TasksDispatchContext } from './TasksContext.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  // ...
  return (
    <TasksContext.Provider value={tasks}>
      <TasksDispatchContext.Provider value={dispatch}>
        ...
      </TasksDispatchContext.Provider>
    </TasksContext.Provider>
  );
}
```

3. 

```react
export default function TaskList() {
  const tasks = useContext(TasksContext);
  // ...
  
export default function AddTask() {
  const [text, setText] = useState('');
  const dispatch = useContext(TasksDispatchContext);
  // ...
  return (
    // ...
    <button onClick={() => {
      setText('');
      dispatch({
        type: 'added',
        id: nextId++,
        text: text,
      });
    }}>Add</button>
    // ...
```

---

#### 将相关逻辑迁移到一个文件当中 

```react
import { createContext, useReducer } from 'react';

export const TasksContext = createContext(null);
export const TasksDispatchContext = createContext(null);

export function TasksProvider({ children }) {
  const [tasks, dispatch] = useReducer(
    tasksReducer,
    initialTasks
  );

  return (
    <TasksContext.Provider value={tasks}>
      <TasksDispatchContext.Provider value={dispatch}>
        {children}
      </TasksDispatchContext.Provider>
    </TasksContext.Provider>
  );
}

function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [...tasks, {
        id: action.id,
        text: action.text,
        done: false
      }];
    }
    case 'changed': {
      return tasks.map(t => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

const initialTasks = [
  { id: 0, text: 'Philosopher’s Path', done: true },
  { id: 1, text: 'Visit the temple', done: false },
  { id: 2, text: 'Drink matcha', done: false }
];
```

---

## 脱围机制

​	情景：需要使用浏览器 API 聚焦输入框，或者在没有 React 的情况下实现视频播放器，或者连接并监听远程服务器的消息

---

### 使用ref引用值

​	当你希望组件“记住”某些信息，但又不想让这些信息 触发新的渲染 时，你可以使用 **ref** 。同vue的ref。

​	**步骤：**

```react
import { useRef } from 'react';

const ref = useRef(0);
//useRef 返回一个这样的对象:
{ 
  current: 0 // 你向 useRef 传入的值
}
```

---

#### 何时使用 ref 

​	通常，当组件需要“跳出” React 并与外部 API 通信时，会用到 ref —— 通常是不会影响组件外观的浏览器 API。以下是这些罕见情况中的几个：

- 存储 [timeout ID](https://developer.mozilla.org/docs/Web/API/setTimeout)
- 存储和操作 [DOM 元素](https://developer.mozilla.org/docs/Web/API/Element)
- 存储不需要被用来计算 JSX 的其他对象。

如果组件需要存储一些值，但不影响渲染逻辑，请选择 ref。

---

#### ref 的最佳实践 

遵循这些原则将使你的组件更具可预测性：

- **将 ref 视为脱围机制**。当你使用外部系统或浏览器 API 时，ref 很有用。如果你很大一部分应用程序逻辑和数据流都依赖于 ref，你可能需要重新考虑你的方法。
- **不要在渲染过程中读取或写入 `ref.current`。** 如果渲染过程中需要某些信息，请使用 [state](https://zh-hans.react.dev/learn/state-a-components-memory) 代替。由于 React 不知道 `ref.current` 何时发生变化，即使在渲染时读取它也会使组件的行为难以预测。（唯一的例外是像 `if (!ref.current) ref.current = new Thing()` 这样的代码，它只在第一次渲染期间设置一次 ref。）

---

#### ref 和 DOM 

​	你可以将 ref 指向任何值。但是，ref 最常见的用法是访问 DOM 元素。例如，如果你想以编程方式聚焦一个输入框，滚动到它或测量它的尺寸和位置。这种用法就会派上用场。

​	当你将 ref 传递给 JSX 中的 `ref` 属性时，比如 `<div ref={myRef}>`，React 会将相应的 DOM 元素放入 `myRef.current` 中。当元素从 DOM 中删除时，React 会将 `myRef.current` 更新为 `null`。

---

### 使用ref操作DOM

#### 访问另一个组件的 DOM 节点 

​	React 不允许组件访问其他组件的 DOM 节点。甚至自己的子组件也不行！如果你尝试将 ref 放在 **你自己的** 组件上，例如 `<MyInput />`，默认情况下你会得到 `null`。

​	**想要** 暴露其 DOM 节点的组件必须**选择**该行为。一个组件可以指定将它的 ref “转发”给一个子组件。下面是 `MyInput` 如何使用 `forwardRef` API：

```react
const MyInput = forwardRef((props, ref) => {
  return <input {...props} ref={ref} />;
});
```

​	在设计系统中，将低级组件（如按钮、输入框等）的 ref 转发到它们的 DOM 节点是一种常见模式。另一方面，像表单、列表或页面段落这样的高级组件通常不会暴露它们的 DOM 节点，以避免对 DOM 结构的意外依赖。

---

#### 限制暴露的功能

​	在上面的例子中，`MyInput` 暴露了原始的 DOM 元素 input。这让父组件可以对其调用`focus()`。

​	然而，这也让父组件能够做其他事情 —— 例如，改变其 CSS 样式。在一些不常见的情况下，你可能希望限制暴露的功能。你可以用 `useImperativeHandle` 做到这一点：

```react
import { forwardRef, useRef, useImperativeHandle } from 'react';

const MyInput = forwardRef((props, ref) => {
  const realInputRef = useRef(null);
  useImperativeHandle(ref, () => ({
    // 只暴露 focus，没有别的
    focus() {
      realInputRef.current.focus();
    },
  }));
  return <input {...props} ref={realInputRef} />;
});

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={handleClick}>
        聚焦输入框
      </button>
    </>
  );
}

```

---

#### 用 flushSync 同步更新 state

​	在 React 中，state 更新是排队进行的。通常，这就是你想要的。

​	但是，在这个示例中会导致问题，因为 `setTodos` 不会立即更新 DOM。因此，当你将列表滚动到最后一个元素时，尚未添加待办事项。这就是为什么滚动总是“落后”一项的原因。

​	要解决此问题，你可以强制 React 同步更新（“刷新”）DOM。 为此，从 `react-dom` 导入 `flushSync` 并**将 state 更新包裹** 到 `flushSync` 调用中：

```react
flushSync(() => {
  setTodos([ ...todos, newTodo]);
});
listRef.current.lastChild.scrollIntoView();
```

---

### 使用effect同步

​	如果你想使用 ref 执行某些操作，但没有特定的事件可以执行此操作，你可能需要一个 effect。有些组件需要与外部系统同步，如根据state控制非react组件。

 **React的两种组件逻辑：**

1.  渲染UI：返回JSX，代码必须是纯粹的、不加修改的映射，像数学公式一样

2. 事件处理：更新输入字段/提交http等用户操作引起的”副作用”

 	effect作用：实现由渲染本身，而不是事件引起的副作用（同步作用）

#### 为什么要用effect

```react
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  if (isPlaying) {
    ref.current.play();  // 渲染期间不能调用 `play()`。 
  } else {
    ref.current.pause(); // 同样，调用 `pause()` 也不行。
  }

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  return (
    <>
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? '暂停' : '播放'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

​	这段代码之所以不正确，是因为它试图在渲染期间对 DOM 节点进行操作（即在组件内部，在返回dom前执行某些逻辑）。在 React 中，JSX 的渲染必须是纯粹操作，不应该包含任何像修改 DOM 的副作用。

​	而且，当第一次调用 `VideoPlayer` 时，对应的 DOM 节点甚至还不存在！如果连 DOM 节点都没有，那么如何调用 `play()` 或 `pause()` 方法呢！在返回 JSX 之前，React 不知道要创建什么 DOM。

​	解决办法是 **使用 `useEffect` 包裹副作用，把它分离到渲染逻辑的计算过程之外**：

```react
import { useEffect, useRef } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      ref.current.play();
    } else {
      ref.current.pause();
    }
  });

  return <video ref={ref} src={src} loop playsInline />;
}
```

---

#### 步骤：

1.  声明
2.  指定依赖（不指定-每次/[]-挂载后一次/[x]-x变化即执行）（使用Object.is比较）（Effect 使用的组件主体中的所有变量都应该在依赖列表中）（依赖数组中可以省略ref）
3.  必要时添加清理函数（清理函数应当确保获取数据的过程以及获取到的结果不会继续影响程序运行）

```react
import { useEffect } from 'react';

function MyComponent() {
	useEffect(() => {
	// 每次渲染后都会执行此处的代码
	},[x]);
	return <div />;
}
```

---

#### useMemo()缓存昂贵的计算

​	但是，`getFilteredTodos()` 的耗时可能会很长，或者你有很多 `todos`。这些情况下，当 `newTodo` 这样不相关的 state 变量变化时，你并不想重新执行 `getFilteredTodos()`。

​	你可以使用 [`useMemo`](https://zh-hans.react.dev/reference/react/useMemo) Hook 缓存（或者说 记忆memoize）一个昂贵的计算。

```react
import { useMemo, useState } from 'react';

function TodoList({ todos, filter }) {
  const [newTodo, setNewTodo] = useState('');
  const visibleTodos = useMemo(() => {
    // ✅ 除非 todos 或 filter 发生变化，否则不会重新执行
    return getFilteredTodos(todos, filter);
  }, [todos, filter]);
  // ...
}

//或者写成一行：
import { useMemo, useState } from 'react';

function TodoList({ todos, filter }) {
  const [newTodo, setNewTodo] = useState('');
  // ✅ 除非 todos 或 filter 发生变化，否则不会重新执行 getFilteredTodos()
  const visibleTodos = useMemo(() => getFilteredTodos(todos, filter), [todos, filter]);
  // ...
}
```

​	**这会告诉 React，除非 `todos` 或 `filter` 发生变化，否则不要重新执行传入的函数**。

​	React 会在初次渲染的时候记住 `getFilteredTodos()` 的返回值。在下一次渲染中，它会检查 `todos` 或 `filter` 是否发生了变化。

​	如果它们跟上次渲染时一样，`useMemo` 会直接返回它最后保存的结果。如果不一样，React 将再次调用传入的函数（并保存它的结果）。

​	你传入 [`useMemo`](https://zh-hans.react.dev/reference/react/useMemo) 的函数会在渲染期间执行，所以它仅适用于 纯函数 场景。

---

#### 如何判断计算是昂贵的

​	一般来说只有你创建或循环遍历了成千上万个对象时才会很耗费时间。如果你想确认一下，可以添加控制台输出来测量某一段代码的执行时间：

```react
console.time('筛选数组');
const visibleTodos = getFilteredTodos(todos, filter);
console.timeEnd('筛选数组');
```

​	触发要测量的交互（例如，在输入框中输入）。你会在控制台中看到类似 `筛选数组：0.15ms` 这样的输出日志。如果总耗时达到了一定量级（比方说 `1ms` 或更多），那么把计算结果记忆（memoize）起来可能是有意义的。

---

#### 在普通函数中共享逻辑

​	假设你有一个产品页面，上面有两个按钮（购买和付款），都可以让你购买该产品。当用户将产品添加进购物车时，你想显示一个通知。

​	在两个按钮的 click 事件处理函数中都调用 `showNotification()` 感觉有点重复，所以你可能想把这个逻辑放在一个 Effect 中：

```react
function ProductPage({ product, addToCart }) {
  // 🔴 避免：在 Effect 中处理属于事件特定的逻辑
  useEffect(() => {
    if (product.isInCart) {
      showNotification(`已添加 ${product.name} 进购物车！`);
    }
  }, [product]);

  function handleBuyClick() {
    addToCart(product);
  }

  function handleCheckoutClick() {
    addToCart(product);
    navigateTo('/checkout');
  }
  // ...
}
```

​	这个 Effect 是多余的。而且很可能会导致问题。

​	例如，假设你的应用在页面重新加载之前 “记住” 了购物车中的产品。如果你把一个产品添加到购物车中并刷新页面，通知将再次出现。每次刷新该产品页面时，它都会出现。

​	这是因为 `product.isInCart` 在页面加载时已经是 `true` 了，所以上面的 Effect 每次都会调用 `showNotification()`。

​	**当你不确定某些代码应该放在 Effect 中还是事件处理函数中时，先自问 为什么 要执行这些代码。Effect 只用来执行那些显示给用户时组件 需要执行 的代码**。

​	在这个例子中，通知应该在用户 **按下按钮** 后出现，而不是因为页面显示出来时！

```react
function ProductPage({ product, addToCart }) {
  // ✅ 非常好：事件特定的逻辑在事件处理函数中处理
  function buyProduct() {
    addToCart(product);
    showNotification(`已添加 ${product.name} 进购物车！`);
  }

  function handleBuyClick() {
    buyProduct();
  }

  function handleCheckoutClick() {
    buyProduct();
    navigateTo('/checkout');
  }
  // ...
}

```

​	这既移除了不必要的 Effect，又修复了问题。

---

### effect的生命周期

#### 每个 Effect 表示一个独立的同步过程

​	抵制将与 Effect 无关的逻辑添加到已经编写的 Effect 中，仅仅因为这些逻辑需要与 Effect 同时运行。

​	例如，假设你想在用户访问房间时发送一个分析事件。你已经有一个依赖于 `roomId` 的 Effect，所以你可能会想要将分析调用添加到那里：

```react
function ChatRoom({ roomId }) {
  useEffect(() => {
    logVisit(roomId);
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
  // ...
}
```

​	但是想象一下，如果以后给这个 Effect 添加了另一个需要重新建立连接的依赖项。如果这个 Effect 重新进行同步，它将为相同的房间调用 `logVisit(roomId)`，而这不是你的意图。

​	记录访问行为是 **一个独立的过程**，与连接不同。将它们作为两个单独的 Effect 编写：

```react
function ChatRoom({ roomId }) {
  useEffect(() => {
    logVisit(roomId);
  }, [roomId]);

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    // ...
  }, [roomId]);
  // ...
}
```

​	在上面的示例中，删除一个 Effect 不会影响另一个 Effect 的逻辑。这表明它们同步不同的内容，因此将它们拆分开是有意义的。

​	另一方面，如果将一个内聚的逻辑拆分成多个独立的 Effects，代码可能会看起来更加“清晰”，但 [维护起来会更加困难](https://zh-hans.react.dev/learn/you-might-not-need-an-effect#chains-of-computations)。

​	这就是为什么你应该考虑这些过程是相同还是独立的，而不是只考虑代码是否看起来更整洁。

---

### 将函数从effect中分开

#### 普通函数和effect的区别

​	**普通函数只有在你再次执行同样的交互时才会重新运行。Effect 和函数不一样，它只有在读取的 props 或 state 值和上一次渲染不一样时才会重新同步。**

​	假设你正在实现一个聊天室组件，需求如下：

1. 组件应该自动连接选中的聊天室。

2. 每当你点击“Send”按钮，组件应该在当前聊天界面发送一条消息。

​	从用户角度出发，发送消息是 **因为** 他点击了特定的“Send”按钮。这就是为什么发送消息应该使用事件处理函数。理函数是让你处理特定的交互操作的：

```react
function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');
  // ...
  function handleSendClick() {
    sendMessage(message);
  }
  // ...
  return (
    <>
      <input value={message} onChange={e => setMessage(e.target.value)} />
      <button onClick={handleSendClick}>Send</button>
    </>
  );
}
```

 	还需要让组件和聊天室保持连接。代码放哪里呢？

​	运行这个代码的 **原因** 不是特定的交互操作。用户为什么或怎么导航到聊天室屏幕的都不重要。既然用户正在看它并且能够和它交互，组件就要和选中的聊天服务器保持连接。即使聊天室组件显示的是应用的初始屏幕，用户根本还没有执行任何交互，仍然应该需要保持连接。这就是这里用 Effect 的原因：

```react
function ChatRoom({ roomId }) {
  // ...
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
  // ...
}
```

---

- **事件处理函数内部的逻辑是非响应式的**。除非用户又执行了同样的操作（例如点击），否则这段逻辑不会再运行。事件处理函数可以在“不响应”他们变化的情况下读取响应式值。
- **Effect 内部的逻辑是响应式的**。如果 Effect 要读取响应式值，你必须将它指定为依赖项。如果接下来的重新渲染引起那个值变化，React 就会使用新值重新运行 Effect 内的逻辑。

----

### 移除effect依赖

应该尽可能避免将对象和函数作为 Effect 依赖,尝试将它们移到组件外部、Effect 内部，或从中提取原始值。

---

