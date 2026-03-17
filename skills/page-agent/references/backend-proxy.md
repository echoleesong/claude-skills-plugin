# 后端代理 API Key 方案

## 为什么需要后端代理？

直接在前端使用 API Key 存在安全风险：
- API Key 可能被泄露
- 无法控制使用配额
- 无法追踪和审计

## 方案 1: 简单的 Node.js 代理

### 服务器代码

```javascript
// server.js
const express = require('express')
const fetch = require('node-fetch')

const app = express()
app.use(express.json())
app.use(express.static('public'))

// 代理 Page Agent API 请求
app.post('/api/page-agent', async (req, res) => {
  try {
    const { model, messages } = req.body

    const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.DASHSCOPE_API_KEY}`,
      },
      body: JSON.stringify({
        model,
        messages,
      }),
    })

    const data = await response.json()
    res.json(data)
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000')
})
```

### 前端代码

```typescript
const agent = new PageAgent({
  model: 'qwen-max',
  baseURL: 'http://localhost:3000/api/page-agent',
  apiKey: '',  // 不需要，由后端处理
  language: 'zh-CN',
  customHeaders: {
    // 如果需要额外的认证
    'Authorization': `Bearer ${userToken}`,
  },
})
```

---

## 方案 2: Next.js API 路由

### API 路由

```typescript
// app/api/page-agent/route.ts
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { model, messages } = body

    const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.DASHSCOPE_API_KEY}`,
      },
      body: JSON.stringify({ model, messages }),
    })

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'API 请求失败' }, { status: 500 })
  }
}
```

### 环境变量

```bash
# .env.local
DASHSCOPE_API_KEY=your-actual-api-key
NEXT_PUBLIC_API_URL=/api/page-agent
NEXT_PUBLIC_MODEL=qwen-max
```

### 前端组件

```tsx
'use client'
import { useEffect, useState } from 'react'
import { PageAgent } from 'page-agent'

export function SecurePageAgent() {
  const [agent, setAgent] = useState<PageAgent | null>(null)
  const [input, setInput] = useState('')

  useEffect(() => {
    const newAgent = new PageAgent({
      model: process.env.NEXT_PUBLIC_MODEL || 'qwen-max',
      baseURL: process.env.NEXT_PUBLIC_API_URL || '/api/page-agent',
      apiKey: '',  // 由后端代理
      language: 'zh-CN',
    })
    setAgent(newAgent)
  }, [])

  const execute = async () => {
    await agent?.execute(input)
    setInput('')
  }

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyUp={(e) => e.key === 'Enter' && execute()}
        placeholder="输入指令..."
      />
      <button onClick={execute}>执行</button>
    </div>
  )
}
```

---

## 方案 3: 带认证的后端代理

### 服务器代码 (Node.js + Express + JWT)

```javascript
const express = require('express')
const jwt = require('jsonwebtoken')

const app = express()
app.use(express.json())
app.use(express.static('public'))

// 验证用户身份
function authenticateUser(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1]

  if (!token) {
    return res.status(401).json({ error: '未提供认证令牌' })
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (error) {
    return res.status(401).json({ error: '无效的认证令牌' })
  }
}

// 配额检查
async function checkQuota(userId) {
  // 从数据库查询用户配额
  // 返回 { allowed: boolean, remaining: number }
  return { allowed: true, remaining: 1000 }
}

// 代理 API
app.post('/api/page-agent', authenticateUser, async (req, res) => {
  try {
    const { quota } = await checkQuota(req.user.userId)
    if (!quota.allowed) {
      return res.status(429).json({ error: 'API 配额已用尽' })
    }

    const { model, messages } = req.body

    const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.DASHSCOPE_API_KEY}`,
      },
      body: JSON.stringify({ model, messages }),
    })

    const data = await response.json()

    // 记录使用情况
    await logUsage(req.user.userId, model)

    res.json(data)
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000')
})
```

---

## 方案 4: 使用 API Gateway

### AWS API Gateway + Lambda

```javascript
// lambda.js
exports.handler = async (event) => {
  try {
    const body = JSON.parse(event.body)
    const { model, messages } = body

    const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.DASHSCOPE_API_KEY}`,
      },
      body: JSON.stringify({ model, messages }),
    })

    const data = await response.json()

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    }
  }
}
```

---

## 安全最佳实践

1. **永远不要在前端硬编码 API Key**
2. **使用环境变量存储敏感信息**
3. **实施速率限制和配额管理**
4. **记录所有 API 调用用于审计**
5. **使用 HTTPS 加密通信**
6. **定期轮换 API Key**
7. **为不同用户使用不同的 API Key（如果可能）**

## 配额管理示例

```javascript
// 使用 Redis 管理配额
const redis = require('redis')
const client = redis.createClient()

async function checkAndDeductQuota(userId) {
  const key = `quota:${userId}`
  const remaining = await client.decr(key)

  if (remaining < 0) {
    await client.incr(key)  // 恢复
    return { allowed: false, remaining: 0 }
  }

  return { allowed: true, remaining }
}

// 初始化配额
async function initQuota(userId, limit) {
  const key = `quota:${userId}`
  const exists = await client.exists(key)

  if (!exists) {
    await client.set(key, limit)
    await client.expire(key, 86400)  // 24小时过期
  }
}
```