# start

## vue

pnpm create vite

## 小程序

微信开发者工具

## uni-app

![image-20240508134013979](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508134013979.png)

![image-20240508134046536](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508134046536.png)

### react

npx create-react-app 项目名称 或 vite

---

# 项目

## 自定义插件

在开发项目的时候经常会用到svg矢量图,而且我们使用SVG以后，页面上加载的不再是图片资源,

这对页面性能来说是个很大的提升，而且我们SVG文件比img要小的很多，放在项目中几乎不占用资源。

1. **安装SVG依赖插件**

```
pnpm install vite-plugin-svg-icons -D
```

2. **在`vite.config.ts`中配置插件**

```typescript
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'
export default () => {
  return {
    plugins: [
      createSvgIconsPlugin({
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
        symbolId: 'icon-[dir]-[name]',
      }),
    ],
  }
}
```

3. **入口文件main.ts导入**

```
import 'virtual:svg-icons-register'
```
4. **svg封装为全局组件**

因为项目很多模块需要使用图标,因此把它封装为全局组件！！！

5. **在src/components目录下创建一个SvgIcon组件:代表如下**

```vue
<template>
  <div>
    <svg :style="{ width: width, height: height }">
      <use :xlink:href="prefix + name" :fill="color"></use>
    </svg>
  </div>
</template>

<script setup lang="ts">
defineProps({
  //xlink:href属性值的前缀
  prefix: {
    type: String,
    default: '#icon-'
  },
  //svg矢量图的名字
  name: String,
  //svg图标的颜色
  color: {
    type: String,
    default: ""
  },
  //svg宽度
  width: {
    type: String,
    default: '16px'
  },
  //svg高度
  height: {
    type: String,
    default: '16px'
  }

})
</script>
<style scoped></style>
```

5. **在src文件夹目录下创建一个index.ts文件：用于注册components文件夹内部全部全局组件！！！**

```typescript
import SvgIcon from '@/components/SvgIcon/svgIcon.vue';
import Category from '@/components/Category/category.vue';
// 全局对象
const allGlobalComponent: any = { SvgIcon, Category };
export default {
    // install固定方法
    install(app: any) {
        // 注册项目全部的全局组件
        Object.keys(allGlobalComponent).forEach(key => {
            // 注册为全局组件
            app.component(key, allGlobalComponent[key]);
        });
    }
}
```

6. **在入口文件引入src/index.ts文件,通过app.use方法安装自定义插件**

```typescript
import gloablComponent from './components/index';
app.use(gloablComponent);
```

---

## 自定义指令按钮权限

![image-20240508161311173](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508161311173.png)

![image-20240508161605938](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508161605938.png)

![image-20240508162855138](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508162855138.png)

el:

![image-20240508162219871](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508162219871.png)

option:

![image-20240508162237289](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240508162237289.png)

## 自定义指令原理

https://cn.vuejs.org/guide/reusability/custom-directives.html#custom-directives

自定义指令主要是为了重用涉及普通元素的底层 DOM 访问的逻辑。

---

## scale解决大屏适配

```vue
//获取数据大屏展示内容盒子的DOM元素
let screen = ref();
onMounted(() => {
    screen.value.style.transform = `scale(${getScale()}) translate(-50%,-50%)`
});
//定义大屏缩放比例（取小适配）
function getScale(w = 1920, h = 1080) {
    const ww = window.innerWidth / w;
    const wh = window.innerHeight / h;
    return ww < wh ? ww : wh;
}
//监听视口变化
window.onresize = () => {
    screen.value.style.transform = `scale(${getScale()}) translate(-50%,-50%)`
}
```

---

## 数据回显展示与更新

​	**存储已有的SPU对象**

```typescript
let SpuParams = ref<SpuData>({
  category3Id: '', //收集三级分类的ID
  spuName: '', //SPU的名字
  description: '', //SPU的描述
  tmId: '', //品牌的ID
  spuImageList: [],
  spuSaleAttrList: [],
})
//子组件书写一个方法
const initHasSpuData = async (spu: SpuData) => {
  //存储已有的SPU对象,将来在模板中展示
  SpuParams.value = spu
  。。。。。。
}
```

​	**展示SPU名称**

![image.png](https://cdn.nlark.com/yuque/0/2023/png/35431711/1686922904926-5dcdf523-c184-445d-a5e4-1661321e54aa.png?x-oss-process=image%2Fformat%2Cwebp)

​	**展示SPU品牌**

​	下方的红框展示的是所有品牌，上方的绑定的是一个数字也就是下方的第几个

![image.png](https://cdn.nlark.com/yuque/0/2023/png/35431711/1686922965037-e796b44f-ab15-42bf-9c3a-3523e314d104.png?x-oss-process=image%2Fformat%2Cwebp)

​	**SPU描述**

![image.png](https://cdn.nlark.com/yuque/0/2023/png/35431711/1686923031230-7dc16295-2f66-4b9e-bed3-847e8bd34821.png?x-oss-process=image%2Fformat%2Cwebp)

---

## 自定义 search 组件

### 自定义属性

1. 定义属性

![image-20240511141349904](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511141349904.png)

2. 通过属性绑定的形式，动态绑定 `style` 属性

![image-20240511141452531](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511141452531.png)

3. 自定义修改

![image-20240511142122189](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511142122189.png)

### 搜索框防抖

1. 在 data 中定义防抖的延时器 timerId 如下：

![image-20240511143124827](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511143124827.png)

2. 修改 `input` 事件处理函数如下：

![image-20240511143137353](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511143137353.png)

### 搜索建议列表

1. 在 data 中定义如下的数据节点，用来存放搜索建议的列表数据：

![image-20240511144326829](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511144326829.png)

2. 在防抖的 `setTimeout` 中，调用 `getSearchList` 方法获取搜索建议列表：

![image-20240511144340455](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511144340455.png)

3. 在 `methods` 中定义 `getSearchList` 方法如下：

![image-20240511144354249](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511144354249.png)

4. 渲染搜索建议列表

![image-20240511144443933](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511144443933.png)

5. 点击搜索建议的 Item 项，跳转到商品详情页面：

![image-20240511144717473](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511144717473.png)

### 搜索历史

不写了，差不多了

---

##	购物车商品vuex

###  动态统计购物车中商品的总数量

1. 在 `cart.js` 模块中，在 `getters` 节点下定义一个 `total` 方法，用来统计购物车中商品的总数量：

![image-20240511150259301](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511150259301.png)

2. 在商品详情页面的 `script` 标签中，按需导入 `mapGetters` 方法并进行使用：

![image-20240511150310669](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511150310669.png)

3. 通过 `watch` 侦听器，监听计算属性 `total` 值的变化，从而**动态为购物车按钮的徽标赋值**：

![image-20240511150322586](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511150322586.png)

### 将设置 tabBar 徽标的代码抽离为 mixins（vue3使用setup）

1. 把设置 tabBar 徽标的代码封装为一个 mixin 文件：

![image-20240511175713103](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511175713103.png)

2. 导入 `@/mixins/tabbar-badge.js` 模块并进行使用：

![image-20240511175813123](C:\Users\13035\AppData\Roaming\Typora\typora-user-images\image-20240511175813123.png)



