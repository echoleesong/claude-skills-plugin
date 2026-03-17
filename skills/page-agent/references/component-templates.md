# 组件模板

## Svelte 组件

```svelte
<script>
  import { onMount } from 'svelte'
  import { PageAgent } from 'page-agent'

  let agent = null
  let input = ''

  onMounted(() => {
    agent = new PageAgent({
      model: 'qwen-max',
      baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
      apiKey: 'YOUR_API_KEY',
      language: 'zh-CN',
    })
  })

  const execute = async () => {
    await agent?.execute(input)
    input = ''
  }
</script>

<div class="page-agent-container">
  <div class="input-wrapper">
    <input
      bind:value={input}
      on:keydown={(e) => e.key === 'Enter' && execute()}
      placeholder="输入指令..."
      class="agent-input"
    />
    <button on:click={execute} class="agent-button">执行</button>
  </div>
</div>

<style>
  .page-agent-container {
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
  }
  .input-wrapper {
    display: flex;
    gap: 0.5rem;
  }
  .agent-input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  .agent-button {
    padding: 0.5rem 1rem;
    background: #1890ff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
```

## Angular 组件

```typescript
import { Component, OnInit } from '@angular/core'
import { PageAgent } from 'page-agent'

@Component({
  selector: 'app-page-agent',
  template: `
    <div class="page-agent">
      <input
        [(ngModel)]="userInput"
        (keyup.enter)="execute()"
        placeholder="Enter command..."
      />
      <button (click)="execute()">Execute</button>
    </div>
  `,
  styles: [`
    .page-agent { display: flex; gap: 0.5rem; padding: 1rem; }
    input { flex: 1; padding: 0.5rem; }
    button { padding: 0.5rem 1rem; }
  `]
})
export class PageAgentComponent implements OnInit {
  agent: PageAgent | null = null
  userInput = ''

  ngOnInit() {
    this.agent = new PageAgent({
      model: 'gpt-4o',
      baseURL: 'https://api.openai.com/v1',
      apiKey: 'YOUR_API_KEY',
      language: 'en-US',
    })
  }

  async execute() {
    await this.agent?.execute(this.userInput)
    this.userInput = ''
  }
}
```

## Next.js 客户端组件

```tsx
'use client'

import { useEffect, useState } from 'react'
import { PageAgent } from 'page-agent'

export default function PageAgentWrapper() {
  const [agent, setAgent] = useState<PageAgent | null>(null)
  const [input, setInput] = useState('')
  const [apiKey, setApiKey] = useState('')

  useEffect(() => {
    // 从环境变量或用户输入获取 API Key
    if (typeof window !== 'undefined') {
      const key = localStorage.getItem('page-agent-api-key') || ''
      setApiKey(key)

      if (key) {
        const newAgent = new PageAgent({
          model: process.env.NEXT_PUBLIC_MODEL || 'gpt-4o',
          baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://api.openai.com/v1',
          apiKey: key,
          language: 'en-US',
        })
        setAgent(newAgent)
      }
    }
  }, [])

  const handleExecute = async () => {
    if (!agent) {
      alert('请先配置 API Key')
      return
    }
    await agent.execute(input)
    setInput('')
  }

  const saveApiKey = (key: string) => {
    setApiKey(key)
    localStorage.setItem('page-agent-api-key', key)

    const newAgent = new PageAgent({
      model: process.env.NEXT_PUBLIC_MODEL || 'gpt-4o',
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://api.openai.com/v1',
      apiKey: key,
      language: 'en-US',
    })
    setAgent(newAgent)
  }

  return (
    <div className="p-4 bg-gray-100 rounded-lg">
      {!apiKey ? (
        <input
          type="password"
          placeholder="输入 API Key..."
          onChange={(e) => saveApiKey(e.target.value)}
          className="w-full p-2 border rounded"
        />
      ) : (
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleExecute()}
            placeholder="输入指令..."
            className="flex-1 p-2 border rounded"
          />
          <button
            onClick={handleExecute}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            执行
          </button>
        </div>
      )}
    </div>
  )
}
```

## Nuxt 3 组件

```vue
<template>
  <div class="page-agent-wrapper">
    <input
      v-model="userInput"
      @keyup.enter="execute"
      placeholder="输入指令..."
    />
    <button @click="execute">执行</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { PageAgent } from 'page-agent'

const runtimeConfig = useRuntimeConfig()
const agent = ref<PageAgent | null>(null)
const userInput = ref('')

onMounted(() => {
  agent.value = new PageAgent({
    model: runtimeConfig.public.pageAgentModel || 'gpt-4o',
    baseURL: runtimeConfig.public.pageAgentApiUrl || 'https://api.openai.com/v1',
    apiKey: runtimeConfig.public.pageAgentApiKey,
    language: 'zh-CN',
  })
})

const execute = async () => {
  await agent.value?.execute(userInput.value)
  userInput.value = ''
}
</script>

<style scoped>
.page-agent-wrapper {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
}
input {
  flex: 1;
  padding: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
}
</style>
```

## 原生 JavaScript 集成

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Page Agent 示例</title>
  <style>
    .agent-container {
      padding: 1rem;
      background: #f0f0f0;
      border-radius: 8px;
    }
    .agent-input {
      width: 70%;
      padding: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    .agent-button {
      padding: 0.5rem 1rem;
      background: #1890ff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="agent-container">
    <input
      type="text"
      id="agentInput"
      class="agent-input"
      placeholder="输入指令..."
    />
    <button id="agentButton" class="agent-button">执行</button>
  </div>

  <script type="module">
    import { PageAgent } from './node_modules/page-agent/dist/index.js'

    const agent = new PageAgent({
      model: 'qwen-max',
      baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
      apiKey: 'YOUR_API_KEY',
      language: 'zh-CN',
    })

    const input = document.getElementById('agentInput')
    const button = document.getElementById('agentButton')

    const execute = async () => {
      const command = input.value
      await agent.execute(command)
      input.value = ''
    }

    button.addEventListener('click', execute)
    input.addEventListener('keyup', (e) => {
      if (e.key === 'Enter') execute()
    })
  </script>
</body>
</html>
```