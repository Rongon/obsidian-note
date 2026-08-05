eslint + prettier + stylelint + oxlint

# eslint

① 核心防坑：它与 ESLint 的“相爱相杀”

**“ESLint 管代码质量（语法错误），Prettier 管代码面子（长相）。为了防止它们打架，我们会用 `eslint-config-prettier` 强行关闭 ESLint 里的所有格式化规则，让 Prettier 独揽格式化大权。”**

```ts
import skipFormatting from 'eslint-config-prettier/flat'
```

---

