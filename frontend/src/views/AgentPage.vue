<!-- views/AgentPage.vue -->
<template>
  <AppLayout>
    <div class="agent-page">
      <!-- 左侧选项栏 -->
      <div class="sidebar">
        <div class="sidebar-header">
          <h3>数据领域</h3>
        </div>
        <div class="domain-list">
          <div 
            v-for="domain in domains" 
            :key="domain.name"
            :class="['domain-item', { active: activeTab === domain.name }]"
            @click="activeTab = domain.name"
          >
            <i :class="domain.icon"></i>
            <span>{{ domain.label }}</span>
          </div>
        </div>
      </div>

      <!-- 右侧主要内容区 -->
      <div class="main-content">
        <div class="page-header">
          <h2>智能数据助手</h2>
          <p class="subtitle">{{ activeTab ? getCurrentDomain.label + '数据问答' : '请选择左侧数据领域开始问答' }}</p>
        </div>

        <!-- 聊天区域 -->
        <div class="chat-section">
          <div class="chat-container">
            <div class="chat-box">
              <div class="chat-log" ref="chatLog">
                <div v-for="(msg, index) in messages" :key="index" 
                     :class="['chat-msg', msg.role === 'user' ? 'user-msg' : 'ai-msg']">
                  <div class="msg-header">
                    <span class="role-icon">
                      <i :class="msg.role === 'user' ? 'el-icon-user' : 'el-icon-cpu'"></i>
                    </span>
                    <span class="role-name">{{ msg.role === 'user' ? '你' : 'AI助手' }}</span>
                  </div>
                  <div class="msg-content">{{ msg.text }}</div>
                </div>
                <div v-if="isTyping" class="chat-msg ai-msg typing">
                  <div class="msg-header">
                    <span class="role-icon"><i class="el-icon-cpu"></i></span>
                    <span class="role-name">AI助手</span>
                  </div>
                  <div class="msg-content">
                    正在思考<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
                  </div>
                </div>
              </div>

              <div class="chat-input">
                <el-input
                  v-model="input"
                  type="textarea"
                  :rows="3"
                  :placeholder="getPlaceholder"
                  @keyup.enter.ctrl="sendMessage"
                />
                <div class="input-actions">
                  <el-tooltip content="Ctrl + Enter 快速发送" placement="top">
                    <el-button type="primary" :loading="isTyping" @click="sendMessage">
                      <i class="el-icon-s-promotion"></i> 发送
                    </el-button>
                  </el-tooltip>
                  <el-button @click="clearChat" plain>
                    <i class="el-icon-delete"></i> 清空对话
                  </el-button>
                </div>
              </div>
            </div>

            <div class="chat-suggestions">
              <h4>💡 你可以这样问我</h4>
              <div class="suggestion-list">
                <div v-for="(suggestion, index) in getSuggestions" 
                     :key="index" 
                     class="suggestion-item"
                     @click="useSuggestion(suggestion)">
                  {{ suggestion }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import AppLayout from '@/components/AppLayout.vue'
import axios from 'axios'

const input = ref('')
const messages = ref([])
const history = ref([])
const isTyping = ref(false)
const activeTab = ref('')
const chatLog = ref(null)

// 定义所有数据领域
const domains = [
  {
    name: 'health',
    label: '卫生组织',
    icon: 'el-icon-first-aid-kit',
  },
  {
    name: 'mainIndex',
    label: '农业指标',
    icon: 'el-icon-data-line',
  },
  {
    name: 'rural',
    label: '基层组织',
    icon: 'el-icon-office-building',
  },
  {
    name: 'totalAgriculture',
    label: '农业总产值',
    icon: 'el-icon-money',
  },
  {
    name: 'techApplication',
    label: '科技应用',
    icon: 'el-icon-cpu',
  },
  {
    name: 'totalValue',
    label: '总值统计',
    icon: 'el-icon-data-analysis',
  },
  {
    name: 'general',
    label: '通用问答',
    icon: 'el-icon-chat-dot-round',
  }
]

// 获取当前选中的领域信息
const getCurrentDomain = computed(() => {
  return domains.find(d => d.name === activeTab.value) || {}
})

// 获取输入框提示文本
const getPlaceholder = computed(() => {
  if (!activeTab.value) return '请先选择左侧数据领域'
  if (activeTab.value === 'general') return '请输入你的问题，我会尽力回答...'
  return `请输入关于${getCurrentDomain.value.label}的问题...`
})

// 根据不同标签页显示不同的建议问题
const getSuggestions = computed(() => {
  const suggestions = {
    health: [
      "各村镇卫生所的分布情况如何？",
      "哪个地区的卫生室覆盖率最高？",
      "卫生室数量增长最快的地区是哪里？"
    ],
    mainIndex: [
      "近年来农业主要指标的变化趋势？",
      "哪些农业指标表现最好？",
      "农业各产业占比情况如何？"
    ],
    rural: [
      "农村基层组织的人口分布情况？",
      "各村镇年末人口数的对比？",
      "年末居住户数最多的地区是哪里？"
    ],
    totalAgriculture: [
      "农业总产值的增长情况如何？",
      "哪些地区的农业增长率最高？",
      "农业各产业的发展趋势分析"
    ],
    techApplication: [
      "农业科技应用的主要领域有哪些？",
      "科技对农业生产效率的提升情况？",
      "未来农业科技发展的趋势是什么？"
    ],
    totalValue: [
      "农业总产值的构成分析",
      "各产业对总产值的贡献率如何？",
      "总产值的年度增长趋势分析"
    ],
    general: [
      "农业发展有哪些主要挑战？",
      "如何提高农业生产效率？",
      "农村发展的未来趋势是什么？"
    ]
  }
  return suggestions[activeTab.value] || []
})

// 使用建议问题
const useSuggestion = (suggestion) => {
  input.value = suggestion
}

// 发送消息
const sendMessage = async () => {
  if (!input.value.trim()) return

  const userMessage = {
    role: 'user',
    text: input.value,
    domain: activeTab.value
  }
  
  messages.value.push(userMessage)

  try {
    isTyping.value = true
    const res = await axios.post('http://129.211.82.112:8000/api/chat/', {
      input: input.value,
      history: history.value,
      domain: activeTab.value
    })

    history.value = res.data.history
    await typeWriterEffect(res.data.reply)
    
    await nextTick()
    if (chatLog.value) {
      chatLog.value.scrollTop = chatLog.value.scrollHeight
    }
  } catch (err) {
    messages.value.push({ 
      role: 'ai', 
      text: '抱歉，服务出现了问题，请稍后重试' 
    })
    console.error(err)
  } finally {
    isTyping.value = false
    input.value = ''
  }
}

// 打字机效果
const typeWriterEffect = async (fullText) => {
  const aiMessage = { role: 'ai', text: '' }
  messages.value.push(aiMessage)

  for (let i = 0; i < fullText.length; i++) {
    await new Promise(resolve => setTimeout(resolve, 30))
    aiMessage.text += fullText[i]
    
    if (chatLog.value) {
      chatLog.value.scrollTop = chatLog.value.scrollHeight
    }
  }
}

// 清空对话
const clearChat = () => {
  messages.value = []
  history.value = []
}

// 监听标签页变化
watch(activeTab, () => {
  messages.value = []
  history.value = []
})
</script>

<style scoped>
.agent-page {
  display: flex;
  gap: 20px;
  min-height: calc(100vh - 80px);
}

.sidebar {
  width: 240px;
  background: #fff;
  border-radius: 8px;
  padding: 20px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid #ebeef5;
}

.sidebar-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.domain-list {
  padding: 20px 0;
}

.domain-item {
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.domain-item i {
  font-size: 20px;
  color: #909399;
  transition: all 0.3s;
}

.domain-item span {
  color: #606266;
  transition: all 0.3s;
}

.domain-item:hover {
  background: #f5f7fa;
}

.domain-item.active {
  background: #ecf5ff;
  border-left-color: #409EFF;
}

.domain-item.active i,
.domain-item.active span {
  color: #409EFF;
}

.main-content {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h2 {
  margin: 0;
  color: #303133;
  font-size: 28px;
}

.subtitle {
  color: #909399;
  margin-top: 10px;
}

.chat-section {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
}

.chat-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}

.chat-box {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 600px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-log {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 20px;
}

.chat-msg {
  margin-bottom: 20px;
  max-width: 80%;
}

.chat-msg.user-msg {
  margin-left: auto;
}

.msg-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.role-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-msg .role-icon {
  background: #67C23A;
}

.role-name {
  font-size: 14px;
  color: #606266;
}

.msg-content {
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  line-height: 1.5;
}

.user-msg .msg-content {
  background: #ecf5ff;
}

.chat-input {
  margin-top: auto;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.chat-suggestions {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-suggestions h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.suggestion-item {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #ebeef5;
}

.suggestion-item:hover {
  background: #ecf5ff;
  border-color: #409EFF;
}

.typing .dot {
  animation: blink 1s infinite;
  display: inline-block;
}

.typing .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

@media (max-width: 1200px) {
  .chat-container {
    grid-template-columns: 1fr;
  }
  
  .chat-suggestions {
    height: auto;
  }
  
  .suggestion-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .agent-page {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .main-content {
    padding: 15px;
  }
  
  .chat-box {
    height: 500px;
  }
  
  .chat-msg {
    max-width: 90%;
  }
}
</style>
