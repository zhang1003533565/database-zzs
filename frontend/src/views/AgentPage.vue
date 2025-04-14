<!-- views/AgentPage.vue -->
<template>
  <AppLayout>
    <div class="agent-page">
      <h2>AI助手</h2>

      <div class="chat-box">
        <div class="chat-log">
          <div v-for="(msg, index) in messages" :key="index" class="chat-msg">
            <span class="role">{{ msg.role === 'user' ? '你' : 'AI' }}：</span>
            <span class="text">{{ msg.text }}</span>
          </div>
        </div>

        <div class="chat-input">
          <input v-model="input" @keyup.enter="sendMessage" placeholder="请输入你的问题..." />
          <button @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import AppLayout from '@/components/AppLayout.vue'
import axios from 'axios'

const input = ref('')
const messages = ref([])
const history = ref([])

const sendMessage = async () => {
  if (!input.value.trim()) return

  messages.value.push({ role: 'user', text: input.value })

  try {
    const res = await axios.post('http://129.211.82.112:8000/api/chat/', {
      input: input.value,
      history: history.value
    })
    // try {
    // const res = await axios.post('http://localhost:8000/api/chat/', {
    //   input: input.value,
    //   history: history.value
    // })
    messages.value.push({ role: 'ai', text: res.data.reply })
    history.value = res.data.history
  } catch (err) {
    messages.value.push({ role: 'ai', text: '❌ 出错了，请稍后重试' })
    console.error(err)
  }

  input.value = ''
}
</script>

<style scoped>
.agent-page {
  background: #fff;
  padding: 20px;
  border-radius: 6px;
}

/* 聊天 UI 样式 */
.chat-box {
  margin-top: 20px;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
}

.chat-log {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.chat-msg {
  margin: 6px 0;
}

.chat-msg .role {
  font-weight: bold;
  margin-right: 5px;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.chat-input button {
  padding: 6px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
}
</style>
