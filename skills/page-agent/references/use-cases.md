# 实际应用场景示例

## 场景 1: 企业 CRM 系统 - 智能数据录入

### 需求
将复杂的 CRM 表单填写流程简化为自然语言指令

### 实现

```typescript
// CRMAgent.ts
import { PageAgent } from 'page-agent'

export class CRMAgent {
  private agent: PageAgent

  constructor() {
    this.agent = new PageAgent({
      model: 'qwen-max',
      baseURL: '/api/page-agent',  // 使用后端代理
      apiKey: '',
      language: 'zh-CN',
      onBeforeAction: async (action) => {
        // 敏感操作需要确认
        if (action.description.includes('删除') || action.description.includes('提交')) {
          const confirmed = confirm(`即将执行: ${action.description}\n确认继续？`)
          return confirmed
        }
        return true
      },
    })
  }

  // 添加新客户
  async addCustomer(data: {
    name: string
    company: string
    email: string
    phone: string
    notes?: string
  }) {
    const prompt = `
      添加新客户到 CRM 系统：
      - 姓名：${data.name}
      - 公司：${data.company}
      - 邮箱：${data.email}
      - 电话：${data.phone}
      ${data.notes ? `- 备注：${data.notes}` : ''}
    `
    return await this.agent.execute(prompt)
  }

  // 搜索客户
  async searchCustomer(keyword: string) {
    return await this.agent.execute(`搜索客户：${keyword}`)
  }

  // 更新客户信息
  async updateCustomer(customerId: string, updates: Record<string, any>) {
    const updateText = Object.entries(updates)
      .map(([key, value]) => `${key} 改为 ${value}`)
      .join('，')
    return await this.agent.execute(`更新客户 ${customerId} 的信息：${updateText}`)
  }
}
```

### Vue 组件使用

```vue
<template>
  <div class="crm-page-agent">
    <h3>智能 CRM 助手</h3>
    <div class="quick-actions">
      <button @click="addCustomer">添加客户</button>
      <button @click="searchCustomer">搜索客户</button>
    </div>
    <div v-if="showAddForm" class="add-form">
      <input v-model="formData.name" placeholder="姓名">
      <input v-model="formData.company" placeholder="公司">
      <input v-model="formData.email" placeholder="邮箱">
      <input v-model="formData.phone" placeholder="电话">
      <textarea v-model="formData.notes" placeholder="备注"></textarea>
      <button @click="handleAddCustomer">确认添加</button>
    </div>
    <div v-if="showSearch" class="search-form">
      <input v-model="searchKeyword" placeholder="搜索关键词" @keyup.enter="handleSearch">
      <button @click="handleSearch">搜索</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { CRMAgent } from './CRMAgent'

const crmAgent = new CRMAgent()
const showAddForm = ref(false)
const showSearch = ref(false)
const searchKeyword = ref('')

const formData = ref({
  name: '',
  company: '',
  email: '',
  phone: '',
  notes: '',
})

const addCustomer = () => {
  showAddForm.value = true
  showSearch.value = false
}

const searchCustomer = () => {
  showSearch.value = true
  showAddForm.value = false
}

const handleAddCustomer = async () => {
  await crmAgent.addCustomer(formData.value)
  // 清空表单
  formData.value = { name: '', company: '', email: '', phone: '', notes: '' }
  showAddForm.value = false
}

const handleSearch = async () => {
  await crmAgent.searchCustomer(searchKeyword.value)
}
</script>
```

---

## 场景 2: ERP 系统 - 批量操作自动化

### 需求
将重复性的 ERP 操作自动化，减少点击次数

### 实现

```typescript
// ERPAgent.ts
import { PageAgent } from 'page-agent'

export class ERPAgent {
  private agent: PageAgent

  constructor() {
    this.agent = new PageAgent({
      model: 'qwen-max',
      baseURL: '/api/page-agent',
      apiKey: '',
      language: 'zh-CN',
    })
  }

  // 批量审批
  async batchApprove(documents: string[]) {
    const prompt = `批量审批以下 ${documents.length} 个文档：${documents.join('、')}`
    return await this.agent.execute(prompt)
  }

  // 创建采购订单
  async createPurchaseOrder(order: {
    supplier: string
    items: Array<{ name: string; quantity: number; price: number }>
    deliveryDate: string
  }) {
    const itemsText = order.items
      .map(item => `${item.name} x ${item.quantity} (单价${item.price})`)
      .join('，')
    const prompt = `
      创建采购订单：
      - 供应商：${order.supplier}
      - 商品：${itemsText}
      - 交货日期：${order.deliveryDate}
    `
    return await this.agent.execute(prompt)
  }

  // 生成报表
  async generateReport(type: string, startDate: string, endDate: string) {
    return await this.agent.execute(
      `生成 ${type} 报表，时间范围：${startDate} 至 ${endDate}`
    )
  }
}
```

---

## 场景 3: 电商后台 - 订单处理

### 需求
快速处理订单，包括查询、修改状态、退款等

### 实现

```typescript
// OrderAgent.ts
import { PageAgent } from 'page-agent'

export class OrderAgent {
  private agent: PageAgent

  constructor() {
    this.agent = new PageAgent({
      model: 'qwen-max',
      baseURL: '/api/page-agent',
      apiKey: '',
      language: 'zh-CN',
      onBeforeAction: async (action) => {
        // 退款等敏感操作需要二次确认
        if (action.description.includes('退款') || action.description.includes('取消订单')) {
          const confirmed = confirm(`即将执行: ${action.description}\n确认继续？`)
          return confirmed
        }
        return true
      },
    })
  }

  // 查询订单
  async searchOrder(orderId?: string, phone?: string) {
    if (orderId) {
      return await this.agent.execute(`查询订单号：${orderId}`)
    } else if (phone) {
      return await this.agent.execute(`查询手机号 ${phone} 的所有订单`)
    }
  }

  // 修改订单状态
  async updateOrderStatus(orderId: string, newStatus: string) {
    return await this.agent.execute(`将订单 ${orderId} 的状态改为：${newStatus}`)
  }

  // 退款处理
  async processRefund(orderId: string, amount?: number, reason?: string) {
    let prompt = `处理订单 ${orderId} 的退款`
    if (amount) prompt += `，金额：${amount} 元`
    if (reason) prompt += `，原因：${reason}`
    return await this.agent.execute(prompt)
  }

  // 发货
  async shipOrder(orderId: string, trackingNumber: string, carrier: string) {
    return await this.agent.execute(
      `订单 ${orderId} 已发货，物流单号：${trackingNumber}，快递公司：${carrier}`
    )
  }
}
```

---

## 场景 4: 无障碍访问 - 语音控制网页

### 需求
让视障用户通过语音命令操作网页

### 实现

```typescript
// AccessibilityAgent.ts
import { PageAgent } from 'page-agent'

export class AccessibilityAgent {
  private agent: PageAgent
  private recognition: SpeechRecognition | null = null

  constructor() {
    this.agent = new PageAgent({
      model: 'qwen-max',
      baseURL: '/api/page-agent',
      apiKey: '',
      language: 'zh-CN',
    })

    this.initSpeechRecognition()
  }

  private initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
      this.recognition = new webkitSpeechRecognition()
      this.recognition.continuous = false
      this.recognition.interimResults = false
      this.recognition.lang = 'zh-CN'
    }
  }

  // 开始语音识别
  startListening(callback: (command: string) => void) {
    if (!this.recognition) {
      alert('您的浏览器不支持语音识别')
      return
    }

    this.recognition.onresult = (event) => {
      const command = event.results[0][0].transcript
      callback(command)
    }

    this.recognition.onerror = (event) => {
      console.error('语音识别错误:', event.error)
    }

    this.recognition.start()
  }

  // 执行语音命令
  async executeCommand(command: string) {
    return await this.agent.execute(command)
  }
}
```

### Vue 组件

```vue
<template>
  <div class="accessibility-controls">
    <h3>语音控制</h3>
    <button @click="toggleListening" :class="{ active: isListening }">
      {{ isListening ? '停止聆听' : '开始聆听' }}
    </button>
    <div v-if="lastCommand" class="last-command">
      最后指令：{{ lastCommand }}
    </div>
    <div v-if="isListening" class="listening-indicator">
      🎤 正在聆听...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { AccessibilityAgent } from './AccessibilityAgent'

const agent = new AccessibilityAgent()
const isListening = ref(false)
const lastCommand = ref('')

const toggleListening = () => {
  if (isListening.value) {
    agent['recognition']?.stop()
    isListening.value = false
  } else {
    agent.startListening(async (command) => {
      lastCommand.value = command
      await agent.executeCommand(command)
      isListening.value = false
    })
    isListening.value = true
  }
}
</script>

<style scoped>
.accessibility-controls {
  padding: 1rem;
  background: #f0f0f0;
  border-radius: 8px;
}
button {
  padding: 0.5rem 1rem;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button.active {
  background: #ff4d4f;
}
.listening-indicator {
  margin-top: 0.5rem;
  color: #ff4d4f;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
```

---

## 场景 5: 表单填写助手 - 自动填充复杂表单

### 需求
从结构化数据自动填充复杂的多步骤表单

### 实现

```typescript
// FormFillAgent.ts
import { PageAgent } from 'page-agent'

interface FormData {
  [key: string]: any
}

export class FormFillAgent {
  private agent: PageAgent

  constructor() {
    this.agent = new PageAgent({
      model: 'qwen-max',
      baseURL: '/api/page-agent',
      apiKey: '',
      language: 'zh-CN',
    })
  }

  // 填充表单
  async fillForm(data: FormData) {
    const prompt = this.buildFormPrompt(data)
    return await this.agent.execute(prompt)
  }

  private buildFormPrompt(data: FormData): string {
    const entries = Object.entries(data).map(([key, value]) => {
      // 转换字段名，驼峰转中文
      const chineseKey = this.toChinese(key)
      return `- ${chineseKey}：${value}`
    })

    return `请填写表单，内容如下：\n${entries.join('\n')}`
  }

  private toEnglish(key: string): string {
    const map: Record<string, string> = {
      '姓名': 'name',
      '邮箱': 'email',
      '电话': 'phone',
      '地址': 'address',
      '公司': 'company',
    }
    return map[key] || key
  }
}

// 使用示例
const formAgent = new FormFillAgent()

// 填写用户注册表单
await formAgent.fillForm({
  name: '张三',
  email: 'zhang@example.com',
  phone: '13800138000',
  address: '北京市朝阳区',
})

// 填写物流订单表单
await formAgent.fillForm({
  收件人: '李四',
  电话: '13900139000',
  地址: '上海市浦东新区张江高科',
  物品: '笔记本电脑',
  重量: '2.5kg',
})
```