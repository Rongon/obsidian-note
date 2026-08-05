# canvas

## 基本用法

### 元素

​	一个html元素，`<canvas>` 标签只有两个属性**——** width 和 height，默认300/150

```html
<canvas id="tutorial" width="150" height="150"></canvas>
```

```js
var canvas = document.getElementById("tutorial");
var ctx = canvas.getContext("2d");
// Draw a rectangle
ctx.fillStyle = "blue";
ctx.fillRect(10, 10, 150, 100);
```

​	**如果绘制出来的图像是扭曲的，用 width 和 height 明确规定宽高，而不是用 CSS。**

---

### 兼容替换

```html
<canvas id="stockGraph" width="150" height="150">
  current stock price: $3.15 +0.15
</canvas>

<canvas id="clock" width="150" height="150">
  <img src="images/clock.png" width="150" height="150" alt="" />
</canvas>

```

---

## 绘制图形

​	`canvas`只支持两种形式的图形绘制：矩形和路径（由一系列点连成的线段）。

### 矩形

canvas 提供了四种方法绘制矩形：

- `fillRect(x, y, width, height)`

  绘制一个填充的矩形

- `strokeRect(x, y, width, height)`

  绘制一个矩形的边框

- `clearRect(x, y, width, height)`

  清除指定矩形区域，让清除部分完全透明。

- `rect(x, y, width, height)`

---

### 绘制路径

1. 首先，你需要创建路径起始点。`beginPath()`
2. 然后你使用画图命令去画出路径。`stroke()`/`moveTo()`/`lineTo()`
3. 之后你把路径封闭。`closePath()`
4. 一旦路径生成，你就能通过描边或填充路径区域来渲染图形。`fill()`

如：绘制三角形

```js
function draw() {
  var canvas = document.getElementById("canvas");
  if (canvas.getContext) {
    var ctx = canvas.getContext("2d");

    ctx.beginPath();
    ctx.moveTo(75, 50);
    ctx.lineTo(100, 75);
    ctx.lineTo(100, 25);
    ctx.fill();
  }
}
draw()
```

---

### 圆弧

​	`arc(x, y, radius, startAngle, endAngle, anticlockwise)`

​	**`arc()` 函数中表示角的单位是弧度，不是角度。弧度=(Math.PI/180)*角度。`anticlockwise`true为逆，false为顺，不给为顺。**

---

### Path2D对象

​	为了简化代码和提高性能，`Path2D`对象用来缓存或记录绘画命令，这样将能快速地回顾路径。`Path2D()`会返回一个新初始化的 Path2D 对象（可能将某一个路径作为变量——创建一个它的副本，或者将一个包含 SVG path 数据的字符串作为变量）。

```js
new Path2D(); // 空的 Path 对象
new Path2D(path); // 克隆 Path 对象
new Path2D(d); // 从 SVG 建立 Path 对象
```

​	Path2D API 添加了 `addPath`方法作为将`path`结合起来的方法。当你想要从几个元素中来创建对象时，这将会很实用。比如：`Path2D.addPath(path [, transform\])`添加了一条路径到当前路径（可能添加了一个变换矩阵）。

---

## 样式

### 颜色

有两个属性可以做到：`fillStyle` 和 `strokeStyle`。

- `fillStyle = color`

  设置图形的填充颜色。

- `strokeStyle = color`

  设置图形轮廓的颜色。

---

### 线型

[`lineWidth = value`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/lineWidth)设置线条宽度。	[`setLineDash(segments)`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/setLineDash)设置当前虚线样式。

```js
// 设置虚线样式
context.setLineDash([10, 5]); // 10像素实线，5像素空白
```

---

### 阴影

[`shadowOffsetX = float`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/shadowOffsetX)

`shadowOffsetX` 和 `shadowOffsetY` 用来设定阴影在 X 和 Y 轴的延伸距离，它们是不受变换矩阵所影响的。负值表示阴影会往上或左延伸，正值则表示会往下或右延伸，它们默认都为 `0`。

[`shadowBlur = float`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/shadowBlur)

shadowBlur 用于设定阴影的模糊程度，其数值并不跟像素数量挂钩，也不受变换矩阵的影响，默认为 `0`。

[`shadowColor = color`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/shadowColor)

shadowColor 是标准的 CSS 颜色值，用于设定阴影颜色效果，默认是全透明的黑色。

---

## 绘制文本

canvas 提供了两种方法来渲染文本：

- [`fillText(text, x, y [, maxWidth\])`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/fillText)
- [`strokeText(text, x, y [, maxWidth\])`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/strokeText)

---

### 预测量文本宽度

[`measureText()`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/measureText)

```js
 var text = ctx.measureText("foo"); // TextMetrics object
 text.width; // 16;
```

---

## 使用图像

### 步骤

1. 获得一个指向[`HTMLImageElement`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLImageElement)的对象或者另一个 canvas 元素的引用作为源，也可以通过提供一个 URL 的方式来使用图片
2. 使用`drawImage()`函数将图片绘制到画布上

---

### 图片源

- **[`HTMLImageElement`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLImageElement)**

  这些图片是由 `Image()` 函数构造出来的，或者任何的 <img> 元素

- **[`HTMLVideoElement`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLVideoElement)**

  用一个 HTML 的 [``](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/video)元素作为你的图片源，可以从视频中抓取当前帧作为一个图像

- **[`HTMLCanvasElement`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLCanvasElement)**

  可以使用另一个 [``](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/canvas) 元素作为你的图片源。

- **[`ImageBitmap`](https://developer.mozilla.org/zh-CN/docs/Web/API/ImageBitmap)**

  这是一个高性能的位图，可以低延迟地绘制，它可以从上述的所有源以及其他几种源中生成。

---

```js
function draw() {
  var ctx = document.getElementById("canvas").getContext("2d");
  var img = new Image();
  img.onload = function () {
    ctx.drawImage(img, 0, 0);
    ctx.beginPath();
    ctx.moveTo(30, 96);
    ctx.lineTo(70, 66);
    ctx.lineTo(103, 76);
    ctx.lineTo(170, 15);
    ctx.stroke();
  };
  img.src = "backdrop.png";
}
```

---

### 缩放

[`drawImage(image, x, y, width, height)`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/drawImage)    `width` 和 `height`，这两个参数用来控制 当向 canvas 画入时应该缩放的大小

---

### 切片

[`drawImage(image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/drawImage)

其他 8 个参数最好是参照右边的图解，前 4 个是定义图像源的切片位置和大小，后 4 个则是定义切片的目标显示位置和大小。

![img](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Using_images/canvas_drawimage.jpg)

---

## 变形 Transformations

### 状态的保存和恢复

[`save()`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/save)		[`restore()`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/restore)

---

### 移动

[`translate(x, y)`](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Transformations#translatex_y)

`translate`方法接受两个参数。*x *是左右偏移量，*y* 是上下偏移量。

---

### 旋转 Rotating

[`rotate(angle)`](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Transformations#rotateangle)

旋转的角度 (angle)，它是顺时针方向的，以弧度为单位的值。

---

### 缩放

[**`scale(x, y)`**](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Transformations#scalex_y)

x水平，y垂直，比1大放大，比1小缩小，复数镜像翻转

---

### 变形

[`transform(a, b, c, d, e, f)`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/transform)

a：水平方向的缩放	b：竖直方向的倾斜偏移	c：水平方向的倾斜偏移	

d：竖直方向的缩放	e：水平方向的移动	f：竖直方向的移动

[`setTransform(a, b, c, d, e, f)`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/setTransform)

这个方法会将当前的变形矩阵重置为单位矩阵，然后用相同的参数调用 `transform`方法。

[`resetTransform()`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/resetTransform)

重置当前变形为单位矩阵，它和调用以下语句是一样的：`ctx.setTransform(1, 0, 0, 1, 0, 0);`

---

### 裁剪路径

[`clip()`](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/clip)	将当前正在构建的路径转换为当前的裁剪路径。

```js
 // Create a circular clipping path
  ctx.beginPath();
  ctx.arc(0, 0, 60, 0, Math.PI * 2, true);
  ctx.clip();
```

---

## 基础动画

### 步骤：

1. **清空 canvas** 除非接下来要画的内容会完全充满 canvas（例如背景图），否则你需要清空所有。最简单的做法就是用 `clearRect` 方法。
2. **保存 canvas 状态** 如果你要改变一些会改变 canvas 状态的设置（样式，变形之类的），又要在每画一帧之时都是原始状态的话，你需要先保存一下。
3. **绘制动画图形（animated shapes）** 这一步才是重绘动画帧。
4. **恢复 canvas 状态** 如果已经保存了 canvas 的状态，可以先恢复它，然后重绘下一帧。

---

### 更新画布

[`setInterval(function, delay)`](https://developer.mozilla.org/en-US/docs/Web/API/setInterval)

当设定好间隔时间后，function 会定期执行。

[`setTimeout(function, delay)`](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout)

在设定好的时间之后执行函数

[`requestAnimationFrame(callback)`](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/requestAnimationFrame)

告诉浏览器你希望执行一个动画，并在重绘之前，请求浏览器执行一个特定的函数来更新动画。

---

## 像素操作

### imageData对象

[`ImageData`](https://developer.mozilla.org/zh-CN/docs/Web/API/ImageData)对象中存储着 canvas 对象真实的像素数据，它包含以下几个只读属性：

- [`width`](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas#width)

  图片宽度，单位是像素

- [`height`](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas#height)

  图片高度，单位是像素

- [`data`](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas#data)

  [`Uint8ClampedArray`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Uint8ClampedArray) (8位无符号数)类型的一维数组，包含着 RGBA 格式的整型数据，范围[0, 256)

---

剩下的看不懂了

https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas

---

## 优化

1. **在离屏 canvas 上预渲染相似的图形或重复的对象**

​	如果发现自己在每个动画帧上重复了一些相同的绘制操作，请考虑将其分流到屏幕外的画布上。然后，你可以根据需要频繁地将屏幕外图像渲染到主画布上，而不必首先重复生成该图像的步骤。

```js
myEntity.offscreenCanvas = document.createElement("canvas");
myEntity.offscreenCanvas.width = myEntity.width;
myEntity.offscreenCanvas.height = myEntity.height;
myEntity.offscreenContext = myEntity.offscreenCanvas.getContext("2d");

myEntity.render(myEntity.offscreenContext);

```

2. **避免浮点数的坐标点，用整数取而代之**

​	浏览器为了达到抗锯齿的效果会做额外的运算。为了避免这种情况，请保证在你调用`drawImage()`函数时，用`Math.floor()`函数对所有的坐标点取整。

3. **不要在用`drawImage`时缩放图像**

​	在离屏 canvas 中缓存图片的不同尺寸，而不要用`drawImage()`去缩放它们。

4. **使用多层画布去画一个复杂的场景**

​	在你的应用程序中，可能会发现某些对象需要经常移动或更改，而其他对象则保持相对静态。在这种情况下，可能的优化是使用多个`<canvas>`元素对你的项目进行分层。

​	例如，假设你有一个游戏，其 UI 位于顶部，中间是游戏性动作，底部是静态背景。在这种情况下，你可以将游戏分成三个`<canvas>`层。UI 将仅在用户输入时发生变化，游戏层随每个新框架发生变化，并且背景通常保持不变。

5. **用 CSS 设置大的背景图**

​	如果像大多数游戏那样，你有一张静态的背景图，用一个静态的div元素，结合`background` 特性，以及将它置于画布元素之后。这么做可以避免在每一帧在画布上绘制大图。

6. **用 CSS 变换特性缩放画布**

​	CSS 变换使用 GPU，因此速度更快。最好的情况是不直接缩放画布，或者具有较小的画布并按比例放大，而不是较大的画布并按比例缩小。

7. **关闭透明度**

​	如果你的游戏使用画布而且不需要透明，当使用 `HTMLCanvasElement.getContext()` 创建一个绘图上下文时把 `alpha` 选项设置为 `false` 。这个选项可以帮助浏览器进行内部优化。

```js
var ctx = canvas.getContext("2d", { alpha: false });
```

8. **更多特性**

- 将画布的函数调用集合到一起（例如，画一条折线，而不要画多条分开的直线）
- 避免不必要的画布状态改变
- 渲染画布中的不同点，而非整个新状态
- 尽可能避免 `shadowBlur`特性
- 尽可能避免`text rendering`
- 尝试不同的方法来清除画布 (`clearRect()`vs. `fillRect()`vs. 调整 canvas 大小)
- 有动画，请使用`window.requestAnimationFrame()` 而非`window.setInterval()`
- 请谨慎使用大型物理库

---







# SVG

## 基本形状

### 矩形

```html
<rect x="60" y="10" rx="10" ry="10" width="30" height="30"/>
```

rx：圆角的 x 方位的半径	ry：圆角的 y 方位的半径

---

### 圆形

```html
<circle cx="25" cy="75" r="20"/>
```

---

### 椭圆

```html
<ellipse cx="75" cy="75" rx="20" ry="5"/>
```

---

### 线条

```html
<line x1="10" x2="50" y1="110" y2="150" stroke="black" stroke-width="5"/>
```

---

### 折线

```html
<polyline points="60, 110 65, 120 70, 115 75, 130 80, 125 85, 140 90, 135 95, 150 100, 145"/>
```

---

### 多边形

​	`polygon`和折线很像，它们都是由连接一组点集的直线构成。不同的是，`polygon`的路径在最后一个点处自动回到第一个点。需要注意的是，矩形也是一种多边形，如果需要更多灵活性的话，你也可以用多边形创建一个矩形。

```html
<polygon points="50, 160 55, 180 70, 180 60, 190 65, 205 50, 195 35, 205 40, 190 30, 180 45, 180"/>
```

---

## 路径

### 基本

​	`path`可能是 SVG 中最常见的形状。你可以用 path 元素绘制矩形（直角矩形或者圆角矩形）、圆形、椭圆、折线形、多边形，以及一些其他的形状，例如贝塞尔曲线、2 次曲线等曲线。

```html
<path d="M20,230 Q40,205 50,230 T90,230" fill="none" stroke="blue" stroke-width="5"/>
```

---

### 直线

​	(M移动	M x y)	(L画线	L x y)	(H画水平线	H x)	(V画垂直线	V y)	(Z闭合)

```xml
 <path d="M 10 10 H 90 V 90 H 10 Z" fill="transparent" stroke="black"/>
```

---

### 贝塞尔曲线

​	**三次：**

​	C (起点M x y) x1 y1, x2 y2, x y

```xml
<path d="M 10 10 C 20 20, 40 20, 50 10" stroke="black" fill="transparent"/>
```

![image-20240903142048560](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903142048560.png)

​	**简写：**

​	S x2 y2, x y

​	通常情况下，一个点某一侧的控制点是它另一侧的控制点的对称（以保持斜率不变）。

​	S 命令可以用来创建与前面一样的贝塞尔曲线，但是，如果 S 命令跟在一个 C 或 S 命令后面，则它的第一个控制点会被假设成前一个命令曲线的第二个控制点的中心对称点。如果 S 命令单独使用，前面没有 C 或 S 命令，那当前点将作为第一个控制点。

```xml
<path d="M 10 80 C 40 10, 65 10, 95 80 S 150 150, 180 80" stroke="black" fill="transparent"/>
```

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903142525473.png" alt="image-20240903142525473" style="zoom:50%;" />

---

​	**二次：**

​	Q x1 y1, x y

```xml
 <path d="M 10 80 Q 95 10 180 80" stroke="black" fill="transparent"/>
```

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903142838314.png" alt="image-20240903142838314" style="zoom:50%;" />

​	**简写：**

​	T x y

​	就像三次贝塞尔曲线有一个 S 命令，二次贝塞尔曲线有一个差不多的 T 命令，可以通过更简短的参数，延长二次贝塞尔曲线。快捷命令 T 会通过前一个控制点，推断出一个新的控制点。

```xml
<path d="M 10 80 Q 52.5 10, 95 80 T 180 80" stroke="black" fill="transparent"/>
```

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903143019616.png" alt="image-20240903143019616" style="zoom:50%;" />

---

### 弧形

​	看不懂：https://developer.mozilla.org/zh-CN/docs/Web/SVG/Tutorial/Paths#%E5%BC%A7%E5%BD%A2

---

## 填充和边框

### 上色和描边

​	`fill`属性和`stroke`属性。`fill`属性设置对象内部的颜色，`stroke`属性设置绘制对象的线条的颜色。`fill-opacity`控制填充色的不透明度，属性`stroke-opacity`控制描边的不透明度。

```xml
 <rect x="10" y="10" width="100" height="100" stroke="blue" fill="purple"
       fill-opacity="0.5" stroke-opacity="0.8"/>
```



​							<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903151551458.png" alt="image-20240903151551458" style="zoom: 67%;" /><img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903151804776.png" alt="image-20240903151804776" style="zoom:50%;" />

```xml
<svg width="160" height="140" xmlns="http://www.w3.org/2000/svg" version="1.1">
  <line x1="40" x2="120" y1="20" y2="20" stroke="black" stroke-width="20" stroke-linecap="butt"/>
    
    <polyline points="40 60 80 20 120 60" stroke="black" stroke-width="20"
      stroke-linecap="butt" fill="none" stroke-linejoin="miter"/>
</svg>
```

---

​	可以通过指定`stroke-dasharray`属性，将虚线类型应用在描边上。

​	`stroke-dasharray`属性的参数，是一组用逗号分割的数字组成的数列每一组数字，第一个用来表示填色区域的长度，第二个用来表示非填色区域的长度。

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240903151922757.png" alt="image-20240903151922757" style="zoom:67%;" />

```xml
<path d="M 10 75 Q 50 10 100 75 T 190 75" stroke="black"
    stroke-linecap="round" stroke-dasharray="5,10,5" fill="none"/>
```

---

### 使用css

​	略有差异，暂时分开使用

---

## 渐变

### 线性  <linearGradient> 

​	需要在 SVG 文件的 ` defs ` 元素内部，创建一个 ` <linearGradient> ` 节点。

```xml
<svg width="120" height="240" version="1.1" xmlns="http://www.w3.org/2000/svg">
<defs>
    <linearGradient id="Gradient2" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="red" />
      <stop offset="50%" stop-color="black" stop-opacity="0" />
      <stop offset="100%" stop-color="blue" />
    </linearGradient>
</defs>
</svg>
```

​	offset（偏移）属性和 stop-color（颜色中值）属性

​	x1="0" x2="0" y1="0" y2="1" 控制水平垂直

---

## 径向(发散)<radialGradient >

```xml
<?xml version="1.0" standalone="no"?>
<svg width="120" height="240" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="Gradient" cx="0.5" cy="0.5" r="0.5" fx="0.25" fy="0.25">
      <stop offset="0%" stop-color="red" />
      <stop offset="100%" stop-color="blue" />
    </radialGradient>
  </defs>
</svg>
```

​	第一个点为中心点，由 cx 和 cy 属性及半径 r 来定义，描述了渐变边缘位置；第二个点为焦点，由 fx 和 fy 属性定义，描述了渐变的中心。

![image-20240905170247616](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240905170247616.png)

---

​	`spreadMethod`属性，该属性控制了当渐变到达终点的行为，但是此时该对象尚未被填充颜色。这个属性可以有三个值：pad、reflect 或 repeat。

​	Pad 填充对象剩下的空间。

​	reflect 反向渐变

​	repeat 继续渐变。

​						![image-20240905171048365](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240905171048365.png)![image-20240905171101212](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240905171101212.png)<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240905171109054.png" alt="image-20240905171109054"  />

---

## patterns

​	看不懂https://developer.mozilla.org/zh-CN/docs/Web/SVG/Tutorial/Patterns

## 文本(简陋)

### 基础

​	`text` 元素内部可以放任何的文字，和形状元素类似，属性`fill`可以给文本填充颜色，属性`stroke`可以给文本描边等

```xml
<text x="10" y="10">Hello World!</text>
```

---

### 设置字体属性

​	SVG 提供了一些属性，类似于 CSS。 如：`font-family`、`font-style`、`font-weight` 等

---

### 其他文本相关的元素

```xml
<text>
  <tspan font-weight="bold" fill="red">This is bold and red</tspan>
</text>
```

​	`tspan`元素有以下的自定义属性：https://developer.mozilla.org/zh-CN/docs/Web/SVG/Tutorial/Texts#%E5%85%B6%E4%BB%96%E6%96%87%E6%9C%AC%E7%9B%B8%E5%85%B3%E7%9A%84%E5%85%83%E7%B4%A0

---

## 基础变形transform

### g标签

​	唯一作用是可以把属性赋给一整个元素集合。

```xml
<g fill="red">
  <rect x="0" y="0" width="10" height="10" />
  <rect x="20" y="0" width="10" height="10" />
</g>
```

---

### 平移/旋转/斜切/缩放

- 平移：transform="translate(30,40)"

- 旋转：transform="rotate(45)"
- 斜切：利用一个矩形制作一个斜菱形。可用`skewX()`变形和`skewY()`变形。
- 缩放：`scale()`需要两个数字，作为比率计算如何缩放。0.5 表示收缩到 50%。*如果第二个数字被忽略了，它默认等于第一个值。*

---

## 剪切和遮盖

### 剪切

在 (100,100) 创建一个圆形，半径是 100。属性`clip-path`引用了一个带单个 rect 元素的`<clipPath>`元素。它内部的这个矩形将把画布的上半部分涂黑。

```xml
<defs>
    <clipPath id="cut-off-bottom">
      <rect x="0" y="0" width="200" height="100" />
    </clipPath>
</defs>

<circle cx="100" cy="100" r="100" clip-path="url(#cut-off-bottom)" />
```

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240906111600417.png" alt="image-20240906111600417" style="zoom:50%;" />

---

### 遮盖

如果想要让一个元素淡出，可以利用遮盖效果实现这一点。

```xml
<defs>
    <linearGradient id="Gradient">
      <stop offset="0" stop-color="white" stop-opacity="0" />
      <stop offset="1" stop-color="white" stop-opacity="1" />
    </linearGradient>
    <mask id="Mask">
      <rect x="0" y="0" width="200" height="200" fill="url(#Gradient)" />
    </mask>
</defs>

<rect x="0" y="0" width="200" height="200" fill="green" />
<rect x="0" y="0" width="200" height="200" fill="red" mask="url(#Mask)" />
```

有一个绿色矩形在底层，一个红色矩形在上层。后者有一个`mask`属性指向一个`mask`元素。`mask`元素的内容是一个单一的`rect`元素，它填充了一个透明到白色的渐变。作为红色矩形继承`mark`内容的`alpha`值（透明度）的结果，我们看到一个从绿色到红色渐变的输出：

<img src="C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240906112255778.png" alt="image-20240906112255778" style="zoom:50%;" />

---

### opacity

```xml
<rect x="0" y="0" width="100" height="100" opacity=".5" />
```

上面的矩形将绘制为半透明。填充和描边还有两个属性是`fill-opacity`和`stroke-opacity`，分别用来控制填充和描边的不透明度。需要注意的是描边将绘制在填充的上面。因此，如果你在一个元素上设置了描边透明度，但它同时设有填充，则描边的一半应用填充色，另一半将应用背景色。

---

## 嵌入图片

嵌入的图像变成一个普通的 SVG 元素。这意味着，你可以在其内容上用剪切、遮罩、滤镜、旋转以及其他 SVG 工具：

```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200">
  <image x="90" y="-65" width="128" height="146" transform="rotate(45)" xlink:href="https://developer.mozilla.org/zh-CN/docs/Web/SVG/Element/image/mdn_logo_only_color.png" />
</svg>
```

---

## 滤镜效果

https://developer.mozilla.org/zh-CN/docs/Web/SVG/Tutorial/Filter_effects

略显复杂，直接看原文吧，原文已经总结的非常简洁了，并且可以看到后面的总结略显草率，说明已经有点wie了。

---

