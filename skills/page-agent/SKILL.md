---
name: page-agent
description: Page Agent 集成助手 - 帮助开发者在 Web 项目中集成和配置阿里巴巴 Page Agent AI 助手。用于初始化 Page Agent、配置自定义 LLM（通义千问、OpenAI 等）、实现智能表单填写、开发自然语言 UI 交互、配置 Chrome 扩展实现跨页面任务。
---

# Page Agent 集成助手

帮助在 Web 项目中快速集成阿里巴巴 Page Agent，实现自然语言控制网页界面。

## 核心概念

Page Agent 是**运行在网页内的 JavaScript Agent**，不是浏览器自动化工具：
- ✅ 可以操作已加载网页的 DOM
- ❌ 无法自己打开新网页或导航
- ✅ 支持自然语言控制 UI
- ❌ 不能替代 Selenium/Playwright

## 快速集成

### 方式 1: CDN 一行代码（测试用）

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.5.8/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

⚠️ **注意**: 使用 Demo LLM，仅适合技术评估，需遵守使用条款。

### 方式 2: NPM 安装（生产推荐）

```bash
npm install page-agent
```

## 基础配置

### TypeScript/JavaScript

```typescript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
  model: 'qwen-max',                    // 或 gpt-4o, claude-3-5-sonnet-20241022 等
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: 'YOUR_API_KEY',
  language: 'zh-CN',                    // 或 'en-US'
})

await agent.execute('点击登录按钮')
```

### Vue 3 组件示例

```vue
<template>
  <div>
    <input v-model="userInput" placeholder="输入指令..." @keyup.enter="execute">
    <button @click="execute">执行</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { PageAgent } from 'page-agent'

const agent = ref(null)
const userInput = ref('')

onMounted(() => {
  agent.value = new PageAgent({
    model: 'qwen-max',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: 'YOUR_API_KEY',
    language: 'zh-CN',
  })
})

const execute = async () => {
  await agent.value.execute(userInput.value)
}
</script>
```

### React 组件示例

```tsx
import { useEffect, useState, useRef } from 'react'
import { PageAgent } from 'page-agent'

export function PageAgentComponent() {
  const agentRef = useRef<PageAgent | null>(null)
  const [input, setInput] = useState('')

  useEffect(() => {
    agentRef.current = new PageAgent({
      model: 'gpt-4o',
      baseURL: 'https://api.openai.com/v1',
      apiKey: 'YOUR_API_KEY',
      language: 'en-US',
    })
  }, [])

  const handleExecute = async () => {
    await agentRef.current?.execute(input)
  }

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleExecute()}
        placeholder="Enter command..."
      />
      <button onClick={handleExecute}>Execute</button>
    </div>
  )
}
```

## LLM 配置

### 阿里云通义千问

```typescript
const agent = new PageAgent({
  model: 'qwen-max',                    // qwen-max, qwen-plus, qwen-turbo
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: 'sk-xxx',
  language: 'zh-CN',
})
```

### OpenAI

```typescript
const agent = new PageAgent({
  model: 'gpt-4o',                      // gpt-4o, gpt-4o-mini, gpt-3.5-turbo
  baseURL: 'https://api.openai.com/v1',
  apiKey: 'sk-xxx',
  language: 'en-US',
})
```

### Claude

```typescript
const agent = new PageAgent({
  model: 'claude-3-5-sonnet-20241022',
  baseURL: 'https://api.anthropic.com/v1',
  apiKey: 'sk-ant-xxx',
  language: 'en-US',
})
```

### 自定义 OpenAI 兼容 API

```typescript
const agent = new PageAgent({
  model: 'your-model-name',
  baseURL: 'https://your-api-endpoint/v1',
  apiKey: 'your-api-key',
  language: 'zh-CN',
})
```

## 常见场景实现

### 智能表单填写

```typescript
// 用户说："帮我填写注册表单，姓名张三，邮箱zhang@example.com"
await agent.execute('填写注册表单：姓名张三，邮箱zhang@example.com')

// 或者分步引导
await agent.execute('找到注册表单的姓名输入框')
await agent.execute('填写张三到姓名输入框')
await agent.execute('填写 zhang@example.com 到邮箱输入框')
```

### 人机确认机制

```typescript
const agent = new PageAgent({
  model: 'gpt-4o',
  baseURL: 'https://api.openai.com/v1',
  apiKey: 'YOUR_API_KEY',
  language: 'en-US',
  onBeforeAction: async (action) => {
    // 在执行操作前请求用户确认
    const confirmed = confirm(`即将执行: ${action.description}\n确认继续？`)
    return confirmed
  },
})
```

### 多语言支持

```typescript
// 中文环境
const agentZh = new PageAgent({
  model: 'qwen-max',
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: 'YOUR_API_KEY',
  language: 'zh-CN',                    // 指令使用中文
})

// 英文环境
const agentEn = new PageAgent({
  model: 'gpt-4o',
  baseURL: 'https://api.openai.com/v1',
  apiKey: 'YOUR_API_KEY',
  language: 'en-US',                    // 指令使用英文
})
```

### 错误处理

```typescript
try {
  await agent.execute('点击提交按钮')
} catch (error) {
  if (error.message.includes('element not found')) {
    console.error('未找到目标元素')
    // 提供更友好的错误提示或备选方案
  } else if (error.message.includes('permission denied')) {
    console.error('操作被拒绝，可能需要权限')
  }
}
```

## Chrome 扩展集成

跨页面任务需要安装 Chrome 扩展：

```bash
# 安装扩展（从 Page Agent 官方文档获取）
# 在 manifest.json 中配置权限
```

扩展配置示例：
```json
{
  "manifest_version": 3,
  "permissions": ["activeTab", "scripting"],
  "background": {
    "service_worker": "background.js"
  }
}
```

## 最佳实践

1. **API Key 安全**: 不要在前端硬编码 API Key，使用环境变量或后端代理
2. **人机确认**: 对于敏感操作，始终使用 `onBeforeAction` 请求用户确认
3. **错误处理**: 捕获所有可能的错误，提供友好的用户体验
4. **语言匹配**: `language` 参数应与用户界面语言一致
5. **性能优化**: 避免频繁执行复杂操作，考虑批量处理

## 限制与注意事项

| 限制 | 说明 |
|------|------|
| 无法打开新页面 | 只能在已加载的网页内工作 |
| 跨域限制 | 受浏览器同源策略限制 |
| DOM 依赖 | 依赖网页的 DOM 结构，结构变化可能影响效果 |
| LLM 成本 | 每次操作都会调用 LLM，产生 API 费用 |
| 不适合自动化测试 | 不是为测试框架设计，无法替代 Cypress/Playwright |

## 参考资源

- [官方文档](https://alibaba.github.io/page-agent/docs/introduction/overview)
- [Demo](https://alibaba.github.io/page-agent/)
- [GitHub 仓库](https://github.com/alibaba/page-agent)
- [Chrome 扩展指南](https://alibaba.github.io/page-agent/docs/features/chrome-extension)

## 故障排查

**问题**: 找不到元素
- 检查元素是否在页面上可见
- 确认元素选择器是否正确
- 尝试更具体的描述（如"红色提交按钮"而非"提交按钮"）

**问题**: API 调用失败
- 验证 API Key 是否正确
- 检查网络连接
- 确认 LLM 服务可用

**问题**: 操作不响应
- 确认 `execute()` 被 await
- 检查控制台错误信息
- 验证网页 DOM 结构是否稳定