# Typescript

## TS的数据类型

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240105213032104.png" alt="image-20240105213032104" style="zoom:50%;" />

---

### 联合类型

```ts
let arr: (number | string)[] = [123, 456, 'abc']
```

---

### 类型别名

```ts
type ArrType = (number | string)[]
let arr1: ArrType = [1, 2, 3, 'abc']

// 可以组合使用
type ItemType = number | string
let arr5: ItemType[] = [1, 2, 3, 'abc']
let str1: ItemType = '123'
```

---

### 函数类型

```ts
//()后的: number可以省略
function add(a: number, b: number): number{
    return a + b
}

const fn = function(a: number, b: number): number{
    return a + b
}

const fn = (a: number, b: number): number => {
    return a + b
}
```

---

### 函数类型别名

```ts
type FnType = (a: number, b: number) => number

//声明式函数无法使用函数类型别名
function add(a: number, b: number): number{
    return a + b
}

const fn： FnType = function(a, b){
    return a + b
}

const fn： FnType = (a, b) => {
    return a + b
}
```

---

### 可选参数?

```ts
const print = (name: string, gender?: string): void => {
    if(name && gender) {
        console.log(name, gender)
    }
}
print('zzl', 'nan')
print('zzl')
```

---

### 对象类型

**优点：后台返回的接口无需查看接口文档，直接可以看到包含的属性**

```ts
type Person = {
    name: string,
    age: number,
    sayHi: (content: string) => void
}
let obj1: Person = {
    name: 'zzl',
    age: 24,
    sayHi(content) {
        console.log(content)
    }
}
```

---

### 接口类型

```ts
interface IPerson {
    name: string
    age: number
    sayHi: () => void
}
```

**和type类型相似，但是只能为对象定义**

**能用type就用type**

---

### 接口继承extends,&

```ts
interface IPerson {
    name: string
    age: number
    sayHi: () => void
}

interface IStudent extends IPerson {
    gender: string
    ...
}
```

**用type实现与interface相似的继承**

```ts
type IStudent = {
	...
} & IPerson
```

---

### 元组类型tuple

**限制数组的类型和长度**

```ts
let arr: [number, number] = [123, 456] 
```

---

### 字面量类型

**字面量：一眼就能看出是什么东西的变量。如：‘人’, 1, [], {}**

```ts
//const声明的变量不可修改，所以str的类型就为'hello ts'
const str = 'hello ts'
```

**一般配合type使用**

```ts
type Direction = '上' | '下' | '左' | '右'
function changeDirection(direction： Direction) {
	...
}
```

---

### 枚举类型enum

**方便与后端的交互，键默认从0开始**

```ts
enum Direction {
	up,
    down,
    left,
    right
}

function changeDirection(direction: Direction) {
    console.log(direction)
}

changeDirection(Direction.up)	//0
changeDirection(Direction.down)	//1
changeDirection(Direction.left)	//2
changeDirection(Direction.right)	//3
```

**数字枚举：可以修改键**

```ts
enum Direction {
	up = 100,
    down,
    left = 200,
    right
}

function changeDirection(direction: Direction) {
    console.log(direction)
}

changeDirection(Direction.up)	//100
changeDirection(Direction.down)	//101
changeDirection(Direction.left)	//200
changeDirection(Direction.right)	//201
```

**字符串枚举：可以修改为非数值**

```ts
enum Direction {
	up = '上',
    down = '下',
    left = 200,
    right
}

function changeDirection(direction: Direction) {
    console.log(direction)
}

changeDirection(Direction.up)	//上
changeDirection(Direction.down)	//下
changeDirection(Direction.left)	//200
changeDirection(Direction.right)	//201
```

**枚举原理：其本质就是一个对象而已**

**可以由键取值，也可以由值取键**

---

### 类型断言

**当函数获取到的结果类型比较宽泛，我们又知道具体类型，就可以使用类型断言，即手动给他个类型**

```ts
const a = document.getElementById('link') as HTMLAnchorElement
```

---

### 泛型

```ts
// 当val可以为多种类型时，下面的代码就失去了代码提示.
function getId(val: number | string | boolean) {
	return val
}

//使用泛型，后指定类型
function getId<T> (val: T) {
    return val
}
console.log(getId<number>(123))
console.log(getId<string>('abc'))
console.log(getId<boolean>(true))

//简化写法，自动类型推断
const retult = getId(123)
const retult2 = getId('abc')
const retult3 = getId(false)
```

---

###  泛型约束<>

**T 既宽泛定义又添加约束**

```ts
//定义接口
interface ILength {
    length: number
}
//添加约束
function getId<T extends ILendth> (val: T) {
    console.log(val.length)
    return val
}
console.log(getId<string>('abcd'))
console.log(getId<number>(123))	//报错
console.log(getId<boolean>(false))	//报错
```

---

### 多个泛型keyof

```ts
//	key 继承 O 的全部类型
function getProp<O, K extends keyof O>(obj: O, key: K) {
    return obj[key]
}
const p1 = {
    name: 'zzl',
    gender: '男'
}
const result1 = getProp(p1, 'name')
const result1 = getProp(p1, 'age')	//报错
const result1 = getProp(p1, 'gender')
```

---

### 泛型接口

```ts
interface Student<T> {
    id: number
    name: T
    hobby: T[]
}

let s1: Student<string> = {
    id: 123,
    name: 'zzl',
    hobby: ['看电视', '玩游戏']
}

let s1: Student<number> = {
    id: 123,
    name: 001,
    hobby: [1, 2, 3]
}

// 常见
const arr1: Array<number> = [1, 2, 3]
const arr2: Array<string> = ['1', '2', '3']
```

---

## Vue与TypeScript

### defineProps

```vue
//props
export interface Props {
  msg?: string
  labels?: string[]
}
//默认值withDefaults
const props = withDefaults(defineProps<Props>(), {
  msg: 'hello',
  labels: () => ['one', 'two']
})

```

---

### defineEmits

```vue
// (e: 事件名, 参数名1: 类型， 参数名2：类型): void
const emit = defineEmits<{
	(e: 'func', gift: string): void
}>
```

---

### ref

```vue
//基本类型
const str1 = ref<string>('你好')
    
//引用类型
type Todo = {
    id: number,
    name: string,
    done: boolean
}    
const list = ref<Todo[]>([
    { id: 1, name: '吃饭', done: false},
    { id: 2, name: '睡觉', done: true},
    { id: 3, name: 'zzl', done: false},
])
```

---

### 事件类型PointEvent

```
const hClick = (e: PointerEvent) => {
	console.log(e.pageX, e.pageY)
}
```

---

### template ref

```
<img src='xxxxxxxxxxxx'>

const image1 = ref<HTMLImageElement | null>(null)
const hGetImage = () => {
	if(image1.value) {
	image1.value.src = ''
	}
}
```

---

### 第三方库

npm install @types/xxx

---

### 自用xxx.d.ts

​	多处用到相同类型，自建一个.d.ts，按需导出导入

​	<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240113042240733.png" alt="image-20240113042240733" style="zoom:67%;" /><img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240113042319931.png" alt="image-20240113042319931" style="zoom:67%;" />						

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240113042346614.png" alt="image-20240113042346614" style="zoom:67%;" />

---

### axios的ts提示

​	**axios.get<T>**

```vue
type ChannelsRes = {
	data: {
		channels: {
			id: number
			name: string
		}
	}
	message: string
}

async function getChannels() {
	const res = await axios.get<ChanneksRes>('xxxx')
    console.log(res.data.data.channels[0].name)
}
```

---

# 2026TS

https://zhongsp.github.io/TypeScript/zh/handbook/index.html

## 基础

### 基础类型

#### number

有两种: number和: bigint

---

#### array

```typescript
let list: number[] = [1, 2, 3];
```

```typescript
let list: Array<number> = [1, 2, 3];
```

---

#### tuple

**元组是一种特殊的数组类型**，用于**严格规定数组的长度、每个位置的元素类型**。

与普通数组（`type[]`）不同，元组要求**元素数量已知、类型顺序固定**。

```ts
let x: [string, number];
```

表示：`x`必须是一个**长度为 2 的数组**，第 1 个是 `string`，第 2 个是 `number`。

---

#### [enum](https://zhongsp.github.io/TypeScript/zh/handbook/basic-types.html#enum)

**用有意义的名字代替难以记忆的数字或字符串，让代码更易读、更安全。**

 场景一：表示状态（最常见）

比如一个订单，它的状态是固定的几种。

```ts
// ❌ 使用无意义的数字
function getOrderStatusText(status: number) {
  if (status === 1) return '待支付'
  if (status === 2) return '已支付'
  // ... 1、2 是什么意思？维护起来很痛苦
}

// ✅ 使用枚举
enum OrderStatus {
  Pending = 1,
  Paid = 2,
  Shipped = 3,
  Completed = 4
}

function getOrderStatusText(status: OrderStatus) {
  if (status === OrderStatus.Pending) return '待支付'
  // ... 代码可读性大幅提升
}

// 调用时语义清晰，也不会传错值
getOrderStatusText(OrderStatus.Paid)
```

小知识点看上面的“枚举类型enum”

---

#### unknown

`unknown` 类型表示“**我现在还不知道这个值是什么类型**”。它和 `any` 不同——`any` 是“关掉类型检查”，而 `unknown` 是“先保留类型检查，等我弄清楚再操作”。

**原则**：当你无法确定一个值的类型，但**不希望关闭类型检查**时，用 `unknown`。

| 场景             | 为什么用 `unknown`？                                         |
| :--------------- | :----------------------------------------------------------- |
| **API 返回值**   | 后端返回的数据结构可能不稳定，你不想假设它一定是什么类型     |
| **用户输入**     | 用户输入的内容可能是任意类型，你需要先校验                   |
| **第三方库**     | 没有类型定义的库返回的值，你不想直接用 `any`                 |
| **动态内容**     | `JSON.parse` 返回的是 `any`，更好的实践是标注为 `unknown`    |
| **错误处理**     | `catch` 到的 `error` 在 TS 4.0+ 默认就是 `unknown`           |
| **通用工具函数** | 你的函数能接收任何类型的参数，但内部需要根据运行时类型做不同处理 |

---

#### any

尽量不要用

---

#### void

它表示没有任何类型。 当一个函数没有返回值时，你通常会见到其返回值类型是`void`：

```ts
function warnUser(): void {
    console.log("This is my warning message");
}
```

声明一个`void`类型的变量没有什么大用

---

#### undefined`和`null

和`void`相似，它们的本身的类型用处不是很大，可以使用联合类型`xxx | null | undefined`。

---

#### never

日常开发中最实用的场景是**穷尽性检查**——用类型系统确保你处理了所有可能的情况，不遗漏任何分支。

```ts
type Shape = 'circle' | 'square' | 'triangle'

function getArea(shape: Shape): number {
  switch (shape) {
    case 'circle':
      return Math.PI * 3 ** 2
    case 'square':
      return 4 * 4
    case 'triangle':
      return (3 * 4) / 2
    default:
      // 如果上面的 case 覆盖了所有可能，shape 在这里就是 never
      // 如果有一天 Shape 新增了类型，这里就会编译报错，强制你来处理
      const _exhaustiveCheck: never = shape
      return _exhaustiveCheck
  }
}
```

如果未来有人给 `Shape` 加了 `'rectangle'`，`default` 分支的 `shape` 就不再是 `never`，TypeScript 会立刻报错，提醒你“还有新类型没处理”。这是用类型系统帮你避免运行时遗漏。

---

#### object

当你写一个工具函数，想说“参数必须是个对象（包括数组、函数等），但不能是数字、字符串等原始值”时，就用 `object`。要明确拒绝原始类型，只接受对象、数组、函数等

---

### [联合类型和交叉类型](https://zhongsp.github.io/TypeScript/zh/handbook/unions-and-intersections.html#联合类型和交叉类型)

#### [具有公共字段的联合](https://zhongsp.github.io/TypeScript/zh/handbook/unions-and-intersections.html#具有公共字段的联合)

如果我们有一个联合类型的值，则只能访问联合中所有类型共有的成员。

```ts
// @errors: 2339

interface Bird {
  fly(): void;
  layEggs(): void;
}

interface Fish {
  swim(): void;
  layEggs(): void;
}

declare function getSmallPet(): Fish | Bird;

let pet = getSmallPet();
pet.layEggs();

// 只有两种可能类型中的一种可用
pet.swim();

```

---

## 进阶

### 高级类型

#### [类型守卫与类型区分](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#类型守卫与类型区分type-guards-and-differentiating-types)

联合类型适合于那些值可以为不同类型的情况。

 但当我们想确切地了解是否为`Fish`时怎么办？ 

JavaScript里常用来区分2个可能值的方法是检查成员是否存在。

```ts
interface Bird {
    fly();
    layEggs();
}

interface Fish {
    swim();
    layEggs();
}

function getSmallPet(): Fish | Bird {
    // ...
}

let pet = getSmallPet();
```

##### [用户自定义的类型守卫](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#用户自定义的类型守卫)

类型守卫就是一些表达式，它们会在运行时检查以确保在某个作用域里的类型。

###### [使用类型判定](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#使用类型判定)

要定义一个类型守卫，我们只要简单地定义一个函数，它的返回值是一个_类型谓词_：

```ts
function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}

// 'swim' 和 'fly' 调用都没有问题了
if (isFish(pet)) {
    pet.swim();
}
else {
    pet.fly();
}
```

在这个例子里，`pet is Fish`就是类型谓词。 谓词为`parameterName is Type`这种形式，`parameterName`必须是来自于当前函数签名里的一个参数名。

---

###### [使用`in`操作符](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#使用in操作符)

```ts
function move(pet: Fish | Bird) {
    if ("swim" in pet) {
        return pet.swim();
    }
    return pet.fly();
}
```

---

|                      | 自定义类型守卫           | `in` 操作符              |
| :------------------- | :----------------------- | :----------------------- |
| **本质**             | 封装在函数里的类型判断   | 语言内置的类型判断       |
| **需要额外函数吗？** | 需要                     | 不需要                   |
| **能复用吗？**       | ✅ 可以多处调用           | ❌ 每次都要写一遍         |
| **适合场景**         | 判断逻辑复杂、需多次使用 | 判断逻辑简单、只需用一次 |

---

#### [可辨识联合](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#可辨识联合discriminated-unions)

```ts
interface Square {
    kind: "square";
    size: number;
}
interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}
interface Circle {
    kind: "circle";
    radius: number;
}

type Shape = Square | Rectangle | Circle;

function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.height * s.width;
        case "circle": return Math.PI * s.radius ** 2;
    }
}
```

##### [完整性检查](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#完整性检查)

当没有涵盖所有可辨识联合的变化时，我们想让编译器可以通知我们。 比如，如果我们添加了`Triangle`到`Shape`，我们同时还需要更新`area`:

使用`never`类型，编译器用它来进行完整性检查：

```ts
function assertNever(x: never): never {
    throw new Error("Unexpected object: " + x);
}
function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.height * s.width;
        case "circle": return Math.PI * s.radius ** 2;
        default: return assertNever(s); // error here if there are missing cases
    }
}
```

---

#### [索引类型](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#索引类型index-types)

首先是`keyof T`，**索引类型查询操作符**。 对于任何类型`T`，`keyof T`的结果为`T`上已知的公共属性名的联合。 例如：

```ts
interface Car {
    manufacturer: string;
    model: string;
    year: number;
}

let carProps: keyof Car; // the union of ('manufacturer' | 'model' | 'year')
```

---

#### [映射类型](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#映射类型)

一个常见的任务是将一个已知的类型每个属性都变为可选的或者我们想要一个只读版本：

```ts
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
}
type Partial<T> = {
    [P in keyof T]?: T[P];
}
```

需要注意的是这个语法描述的是类型而非成员。 若想添加成员，则可以使用交叉类型：

```ts
// 这样使用
type PartialWithNewMember<T> = {
  [P in keyof T]?: T[P];
} & { newMember: boolean }
// 不要这样使用
// 这会报错！
type PartialWithNewMember<T> = {
  [P in keyof T]?: T[P];
  newMember: boolean;
}
```

---

#### [有条件类型中的类型推断](https://zhongsp.github.io/TypeScript/zh/reference/advanced-types.html#有条件类型中的类型推断)

##### infer

`infer` 是 TypeScript 条件类型中的**类型推断关键字**。它只能在 `extends` 的条件子句中使用，用来声明一个待推断的类型变量，然后在 `true` 分支中引用这个变量，从而实现从某个类型结构中**提取出部分类型**。

```ts
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : any;
```

- `(...args: any[]) => infer R`：匹配任意函数，并推断返回值类型为 `R`。
- 如果 `T` 是函数，则得到 `R`；否则返回 `any`。

---

 自定义 `infer` 示例

 **提取数组元素类型：**

```ts
type ElementType<T> = T extends (infer U)[] ? U : never;
```

---

 嵌套条件类型中的 `infer`（链式匹配）

条件类型可以串联，形成一个“优先级”依次匹配的流水线。

```ts
type Unpacked<T> =
  T extends (infer U)[] ? U :
  T extends (...args: any[]) => infer U ? U :
  T extends Promise<infer U> ? U :
  T;
```

- 先检查是否为数组，提取元素类型。
- 再检查是否为函数，提取返回值类型。
- 再检查是否为 Promise，提取包裹类型。
- 都不是则返回原类型。

---

### 实用工具类型

| 工具类型                   | 作用                                     |
| :------------------------- | :--------------------------------------- |
| `Partial<T>`               | 让所有属性变为可选                       |
| `Required<T>`              | 让所有属性变为必填                       |
| `Readonly<T>`              | 让所有属性变为只读                       |
| `Pick<T, K>`               | 从 `T` 中挑选部分属性组成新类型          |
| `Omit<T, K>`               | 从 `T` 中剔除部分属性后得到新类型        |
| `Record<K, T>`             | 创建键名为 `K`、值类型为 `T` 的对象类型  |
| `Exclude<T, U>`            | 从联合类型 `T` 中排除可赋值给 `U` 的类型 |
| `Extract<T, U>`            | 从联合类型 `T` 中提取可赋值给 `U` 的类型 |
| `NonNullable<T>`           | 从 `T` 中剔除 `null` 和 `undefined`      |
| `ReturnType<T>`            | 获取函数类型的返回值类型                 |
| `Parameters<T>`            | 获取函数类型的参数类型（返回元组）       |
| `InstanceType<T>`          | 获取构造函数类型的实例类型               |
| `ConstructorParameters<T>` | 获取构造函数类型的参数类型（返回元组）   |
| `Uppercase<S>`             | 将字符串字面量 `S` 转为大写              |
| `Lowercase<S>`             | 将字符串字面量 `S` 转为小写              |
| `Capitalize<S>`            | 将字符串字面量 `S` 首字母大写            |
| `Uncapitalize<S>`          | 将字符串字面量 `S` 首字母小写            |

例子：

```ts
interface Todo {
    title: string;
    description: string;
}

function updateTodo(todo: Todo, fieldsToUpdate: Partial<Todo>) {
    return { ...todo, ...fieldsToUpdate };
}

const todo1 = {
    title: 'organize desk',
    description: 'clear clutter',
};

const todo2 = updateTodo(todo1, {
    description: 'throw out trash',
});
```

---

### [Decorators](https://zhongsp.github.io/TypeScript/zh/reference/decorators.html#decorators) 装饰器

https://zhongsp.github.io/TypeScript/zh/reference/decorators.html#decorators

暂时不学

---

### [Iterators 和 Generators](https://zhongsp.github.io/TypeScript/zh/reference/iterators-and-generators.html#iterators-和-generators)

- 想遍历**属性名** → 用 `for...in`（适合普通对象 `{}`）。
- 想遍历**属性值** → 用 `for...of`（适合数组 `[]`、`Map`、`Set` 等可迭代对象）。

---

## 工程配置

### [tsconfig.json](https://zhongsp.github.io/TypeScript/zh/project-config/tsconfig.json.html#tsconfigjson)

 🥇 必学（面试常问，项目必须会配）4

| 选项               | 类型      | 描述                                                         |
| :----------------- | :-------- | :----------------------------------------------------------- |
| `strict`           | `boolean` | 启用所有严格检查。包含 `noImplicitAny`、`strictNullChecks`、`strictFunctionTypes` 等 |
| `target`           | `string`  | 指定输出的 JS 目标版本：`ES3` / `ES5` / `ES6` / `ES2015` ~ `ES2020` / `ESNext` |
| `module`           | `string`  | 指定模块系统：`None` / `CommonJS` / `AMD` / `System` / `UMD` / `ES6` / `ES2015` / `ESNext` |
| `moduleResolution` | `string`  | 模块解析策略：`Node` 或 `Classic`（现代项目一律用 `Node`）   |

 🥈 常用（项目中经常出现，需要知道作用）15

| 选项                 | 类型       | 描述                                             |
| :------------------- | :--------- | :----------------------------------------------- |
| `lib`                | `string[]` | 指定包含的库文件，如 `["ES2020", "DOM"]`         |
| `jsx`                | `string`   | JSX 支持：`react` / `preserve` / `react-native`  |
| `baseUrl`            | `string`   | 解析非相对模块名的基准目录，配合 `paths` 使用    |
| `paths`              | `Object`   | 模块名到路径的映射，用来配置路径别名（如 `@/*`） |
| `outDir`             | `string`   | 输出目录                                         |
| `rootDir`            | `string`   | 源码根目录，控制输出目录结构                     |
| `esModuleInterop`    | `boolean`  | 允许从 CommonJS 模块默认导入，现代项目基本都开   |
| `allowJs`            | `boolean`  | 允许编译 `.js` 文件（迁移 JS 项目时常用）        |
| `declaration`        | `boolean`  | 生成 `.d.ts` 声明文件（库作者常用）              |
| `sourceMap`          | `boolean`  | 生成 `.map` 文件，方便调试                       |
| `skipLibCheck`       | `boolean`  | 跳过所有 `.d.ts` 的类型检查，能加快编译速度      |
| `noEmit`             | `boolean`  | 不生成输出文件（只用 TS 做类型检查时开启）       |
| `noEmitOnError`      | `boolean`  | 有类型错误时不生成输出文件                       |
| `noUnusedLocals`     | `boolean`  | 有未使用的局部变量时报错                         |
| `noUnusedParameters` | `boolean`  | 有未使用的参数时报错                             |

示例：

```json
{
  "compilerOptions": {
    // ========== 🥇 必学 ==========

    // strict: 开启所有严格检查
    "strict": true,

    // target: 编译结果的目标版本。ES2020 支持可选链、空值合并等语法
    "target": "ES2020",

    // module: 模块系统。ESNext 表示保持 ES Module 语法，由打包工具（Vite/Webpack）进一步处理
    "module": "ESNext",

    // moduleResolution: 模块解析方式。node 表示按照 Node.js 的规则找模块（node_modules）
    "moduleResolution": "node",

    // ========== 🥈 常用 ==========

    // lib: 编译时包含的库类型声明。ES2020 提供 JS 语法类型，DOM 提供浏览器 API 类型
    "lib": ["ES2020", "DOM"],

    // jsx: React 项目中 JSX 的处理方式。preserve 表示保留 JSX 让后续工具处理
    "jsx": "preserve",

    // baseUrl: 模块查找的基准目录
    "baseUrl": ".",

    // paths: 路径别名。@/* 映射到 src/*
    "paths": {
      "@/*": ["src/*"]
    },

    // outDir: 编译后的 JS 文件输出目录
    "outDir": "dist",

    // rootDir: 源码根目录，输出的目录结构与 rootDir 保持一致
    "rootDir": "src",

    // esModuleInterop: 允许用 import x from 'y' 方式导入 CommonJS 模块
    "esModuleInterop": true,

    // allowJs: 允许编译 JS 文件（迁移 JS 项目时用）
    "allowJs": true,

    // declaration: 生成 .d.ts 类型声明文件（库作者常用）
    "declaration": true,

    // sourceMap: 生成 .map 文件，方便浏览器调试
    "sourceMap": true,

    // skipLibCheck: 跳过所有 .d.ts 的类型检查，加快编译速度
    "skipLibCheck": true,

    // noEmit: 不生成输出，只做类型检查（CI 环境常用）
    "noEmit": false,

    // noEmitOnError: 有类型错误时不生成输出文件
    "noEmitOnError": true,

    // noUnusedLocals: 有未使用的局部变量时报错
    "noUnusedLocals": true,

    // noUnusedParameters: 有未使用的参数时报错
    "noUnusedParameters": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"],
  "exclude": ["node_modules", "dist"]
}
```

---







