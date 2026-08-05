# 微信小程序



----------------------

## appid

![image-20230906002802487](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230906002802487.png)

---

## 通信模型

![image-20230906012742372](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230906012742372.png)

---

## swiper组件的常用模型

![image-20230909012411312](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909012411312.png)

---

## imgae组件的mode属性

**控制图片的比例**

![image-20230909012452175](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909012452175.png)

---

## 常用事件

![image-20230909031512183](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909031512183.png)

---

## 事件对象event的属性列表

![image-20230909031740453](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909031740453.png)

---

## target和currentTarget的区别

**一般来说都用target，很少用到currentTarget**

![image-20230909032200496](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909032200496.png)

---

## 事件绑定

**小程序中没有onclick，转而用的是tap事件**

![image-20230909032711136](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909032711136.png)

---

## 事件传参

**小程序绑定时不能直接btnHandle(123)传参，只能使用data-*自定义属性传参**

![image-20230909034058932](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909034058932.png)

![image-20230909034200631](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230909034200631.png)

**通过event.target.dataset.参数名可以获取该参数**

---

## bindinput事件

**可以通过e.detail.value获取到输入框最新的值**

---

## 条件渲染

1. wx:if

![image-20230913040708007](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913040708007.png)

2. 结合<block>标签使用wx:if

​	一般使用<block>标签包裹住需要if渲染的其他标签，因为该标签不会被渲染出来，提高性能。

![image-20230913041229807](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913041229807.png)![image-20230913041244451](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913041244451.png)

3. hidden为true时隐藏元素，为false时显示元素。

![image-20230913043551625](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913043551625.png)

4. wx:if与hidden对比

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913043859648.png" alt="image-20230913043859648" style="zoom: 50%;" />

---

## 列表循环渲染

1. wx:for

![image-20230913044247376](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913044247376.png)![image-20230913044253484](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913044253484.png)

2. wx:key **给一个key提高渲染性能，建议把id当key，没有的时候用index**



![image-20230913044745181](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913044745181.png)

## rpx

​	rpx的实现原理：不同设备屏幕的大小不同，为了实现屏幕的自动适配，把所有设备的屏幕在宽度上等分为750份（即：当前屏幕的总宽度为750rpx），所以不同设备的1rpx的宽度是不同的。

​	一个屏幕总是等于750rpx，因此知道不同屏幕的大小px或者其他单位后就可以进行随意换算。

---

## 样式导入

​	@import "xxx.wxss";

---

## window节点常用的配置项

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913062216648.png" alt="image-20230913062216648" style="zoom: 50%;" />

---

## tabBar导航

### 介绍

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913063427464.png" alt="image-20230913063427464" style="zoom:50%;" />![image-20230913063433393](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913063433393.png)

- tabBar中只能配置最少2个、最多5个tab页签

- 当渲染顶部 tabBar时，不显示icon，只显示文本

---

### 其6个组成部分

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913064020716.png" alt="image-20230913064020716" style="zoom:50%;" />

---

### tabBar节点的配置项

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913064733805.png" alt="image-20230913064733805" style="zoom: 50%;" />

---

### 每个tab项的配置选项

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230913064807811.png" alt="image-20230913064807811" style="zoom: 50%;" />

---

## 常用的页面配置项

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230914080230938.png" alt="image-20230914080230938" style="zoom: 50%;" />

---

## 网络请求

### 两个限制

1. 只能请求HTTPS的接口
2. 必须将接口的域名添加到信任列表中

---

### get/post

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230914084357649.png" alt="image-20230914084357649" style="zoom: 50%;" />

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230914084336377.png" alt="image-20230914084336377" style="zoom:50%;" />

---

### 刚加载就请求数据

​	在onload函数里this.xxx使用函数

---

## 页面导航

### 声明式导航

​	**使用navigator组件**

1. 跳转到tabBar页面

​	open-type属性设置为switchTab

2. 跳转到非tabBar页面

​	不设置就可以了

3. 后退导航

​	open-type设置为navigateBack；

​	delta属性可以设置后退级数，后退1级可以不设置。

---

### 编程式导航

​	**调用wx.switchTab(obj obj)方法**

1. 跳转到tabBar页面

![image-20230915100820498](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230915100820498.png)

2. 跳转到非tabBar页面

![image-20230916070958390](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916070958390.png)

3. 后退导航

![image-20230916071200736](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916071200736.png)

---

## 导航传参

### 声明式

![image-20230916071935417](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916071935417.png)

### 编程式

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916072056306.png" alt="image-20230916072056306" style="zoom:50%;" />

### 在onload中可以接收导航参数

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916072330897.png" alt="image-20230916072330897" style="zoom:80%;" />

---

## 下拉刷新

### 全局/局部开启

​	将enablePullDownRefresh设置为true

### 监听页面下拉刷新事件

​	![image-20230916082833834](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916082833834.png)

### 停止下拉刷新

​	下拉刷新后效果**不会主动消失**，需要手动消失。调用wx.stopPullDownRefresh()方法。

---

## 上拉触底

### 监听上拉触底事件

​	![image-20230916083418835](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916083418835.png)

**问题：在底部反复拖动会重复触发该事件**

![image-20230916083729622](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916083729622.png)

### 上拉触底距离

![image-20230916083859503](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916083859503.png)

### 上拉触底节流处理

​	定义一个flag，每次触底刷新与否变换一下true或false。

---

## 展示加载动画

​	调用wx.showLoading(Object object)方法

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916085044419.png" alt="image-20230916085044419" style="zoom: 33%;" />

​	在加载完成后主动调用关闭提示框：

![image-20230916085218958](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916085218958.png)

---

## WXS（一般用作过滤器）

### 应用场景

​	wxml 中**无法调用在页面xxx.js 中定义的函数**，但是，wxml 中可以调用 wxs 中定义的函数。因此，小程序中 wxs 的典型应用场景就是“过滤器”。

### 与JavaScript的区别

1. 

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916103713561.png" alt="image-20230916103713561" style="zoom: 33%;" />

2. 不能作为组件的事件回调

​	一般wxs就是**配合{{}}语法**使用。

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916120840003.png" alt="image-20230916120840003" style="zoom:80%;" />

​	而不能：

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916120847029.png" alt="image-20230916120847029" style="zoom:80%;" />

3. 隔离性

​	wxs不能调用js中定义的函数；不能调用小程序提供的api。（其实就是配合{{}}作为过滤器使用）

### 内嵌式

​	<wxs></wsx>可以内嵌在<wxml></wxml>中，**必须提供module属性**，用来指定当前wxs模块名称，如：

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916104349840.png" alt="image-20230916104349840" style="zoom:67%;" />

### 外联式

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20230916105020646.png" alt="image-20230916105020646" style="zoom: 50%;" />

---

## 自定义组件

	### 格式

​	在xxx.json中定义

```
  "usingComponents": {
    "my-test1": "/components/test/test"
  }
```

### 组件与页面的不同

![image-20231003033409207](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003033409207.png)

### 注意点

![image-20231003033821043](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003033821043.png)

### 修改样式隔离选项

![image-20231003034257379](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003034257379.png)

![image-20231003034312307](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003034312307.png)

### 自定义方法

​	一般以下划线开始命名。

### properties属性

​	在小程序组件中，**properties**是组件的对外属性，**用来接收外界传递到组件中的数据**：

![image-20231003035416645](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003035416645.png)

### data和properties的区别

![image-20231003035751241](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003035751241.png)

​	由于data数据和properties属性在本质上没有任何区别，因此 properties属性的值也可以用于页面渲染,或使用setData为properties中的属性重新赋值。

## 数据监听器

​	数据监听器用于监听和响应任何属性和数据字段的变化，从而执行特定的操作。它的作用类似于vue中的watch侦听器。

![image-20231003050721432](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003050721432.png)

### 监听对象属性的变化

​	数据监听器支持监听对象中单个或多个属性的变化：

![image-20231003051806163](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003051806163.png)

​	监听所有属性的变化：使用通配符如：rgb.**

## 纯数据字段

​	纯数据字段指的是那些**不用于界面渲染的data字段**。

​	应用场景：例如有些情况下，某些data中的字段既不会展示在界面上，也不会传递给其他组件，仅仅在当前组件内部使用。带有这种特性的data字段适合被设置为纯数据字段。

​	好处：纯数据字段有助于提升页面更新的性能。

### 规则

​	在**Component**构造器的**options**节点中，指定**pureDataPattern**为一个正则表达式，字段名符合这个正则表达式的字段将成为纯数据字段：

​	![image-20231003054813912](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231003054813912.png)

---

## 自定义组件生命周期

![image-20231019052227191](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019052227191.png)

### 主要的3个

![image-20231019052252639](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019052252639.png)

---

## 自定义组件所在页面生命周期函数

![image-20231019052922809](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019052922809.png)

---

## 插槽

### 单个插槽

![image-20231019055224962](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019055224962.png)

### 具名插槽

​	**启用：**再组件.js文件中

![image-20231019055441814](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019055441814.png)

​	**定义：**

![image-20231019055540293](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019055540293.png)

![image-20231019055559092](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019055559092.png)

---

## 自定义组件通信

### 父子组件通信的3种方式

![image-20231019055841879](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019055841879.png)

### 属性绑定

​	属性绑定用于实现父向子传值，而且只能传递普通类型的数据，无法将方法传递给子组件。

父组件：

![image-20231019062101507](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019062101507.png)

子组件：

![image-20231019062123901](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019062123901.png)

### 事件绑定

	1. 在父组件js中：

![image-20231019063207712](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019063207712.png)

2. 在父组件html中：

![image-20231019063241674](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019063241674.png)

3. 在子组件中：

![image-20231019063314930](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019063314930.png)

### 获取各组件的实例

![image-20231019063910952](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019063910952.png)

### behaviors(共享一些东西)

1. 是什么

![image-20231019065610408](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019065610408.png)

![image-20231019065637365](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019065637365.png)

2. 创建

![image-20231019065713002](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019065713002.png)

3. 导入使用

![image-20231019065754978](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019065754978.png)

![image-20231019065849977](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019065849977.png)

4. 可用节点

![image-20231019065925582](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019065925582.png)

5. 同名字段的覆盖和组合规则

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231019070055731.png" alt="image-20231019070055731" style="zoom:150%;" />

---

## 小程序的全局数据共享(Mobx/vuex)

在小程序中，可使用 **mobx-miniprogram** 配合 **mobx-miniprogram-bindings** 实现全局数据共享。其中：

- **mobx-miniprogram** 用来创建 **Store** 实例对象
- **mobx-miniprogram-bindings** 用来把 **Store** 中的共享数据或方法，绑定到组件或页面中使用

![image-20231110145429580](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231110145429580.png)

### 将**store**绑定到页面中

1. 在页面.js中引入包
2. 在Page下的onLoad下引入Store
3. 在onUnload下卸载

### 在页面中使用store

1. 属性用直接{{}}使用
2. 方法通过定义方法使用

### 将store绑定到组件中

1. 在组件中引入包
2. 在Component下引入behaviors数组存放包里的东西
3. 定义storeBindings对象存放数据

---

## 分包

### 分包后项目的构成

分包后，小程序项目由**1个主包** + 多个分包组成：

- 主包：一般只包含项目的**启动页面**或**TabBar页面**、以及所有分包都需要用到的一些**公共资源**

- 分包：只包含和当前分包有关的页面和私有资源

![image-20231110170636178](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231110170636178.png)

### 加载规则

1. 在小程序启动时，默认会**下载主包**并**启动主包内页面**
   - tabBar页面需要放到主包中
2. 当用户进入分包内某个页面时，**客户端会把对应分包下载下来**，下载完成后再进行展示
   - 非tabBar页面可以按照功能的不同，划分为不同的分包之后，进行按需下载

### 分包体积限制
目前，小程序分包的大小有以下两个限制:
	- 整个小程序所有分包大小不超过**16M**（主包＋所有分包)

- 单个分包/主包大小不能超过**2M**

### 使用分包

![image-20231110172208061](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231110172208061.png)

在app.json中定义”subpackages“字段，”root“字段为名字，”name“为别名。

### 打包原则

- 小程序会按 **subpackages** 的配置进行分包，subpackages 之外的目录将被打包到主包中

- 主包也可以有自己的 pages (即最外层的pages字段)
- tabBar 页面必须在主包内
- 分包之间不能互相嵌套

### 引用原则

- 主包**无法引用**分包内的私有资源

- 分包之间**不能相互引用**私有资源

- 分包**可以引用**主包内的公共资源

---

## 独立分包（"independent": true）

​	独立分包**本质上也是分包**，只不过它比较特殊，**可以独立于主包和其他分包而单独运行**。

​	一个小程序可以有**多个**独立分包。

![image-20231111110712166](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231111110712166.png)

### 独立分包和普通分包的区别
最主要的区别：**是否依赖于主包才能运行**

- 普通分包必须依赖于主包才能运行
- 独立分包可以在不下载主包的情况下，独立运行

### 引用原则

独立分包和普通分包以及主包之间，是**相互隔绝**的，**不能相互引用彼此的资源**！例如：

1. 主包**无法引用**独立分包内的私有资源
2. 独立分包之间，**不能相互引用**私有资源
3. 独立分包和普通分包之间，**不能相互引用**私有资源
4. 独立分包中**不能引用**主包内的公共资源

## 分包预下载（preloadRule）

分包预下载指的是：在进入小程序的某个页面时，**由框架自动预下载可能需要的分包**，从而提升进入后续分包页面时的启动速度。

![image-20231111112032545](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231111112032545.png)

### 限制

同一个分包中的页面享有**共同的预下载大小限额2M**，例如:

![image-20231111112428503](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20231111112428503.png)

---

## 自定义tabBar

在app.json的tabBar中定义”custom“: ture



