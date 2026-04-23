<template>
  <div class="ai-chat-page">
    <!-- 顶部控制栏：启动按钮 + 状态 -->
    <div class="chat-header">
      <div class="header-left">
        <el-button
          type="primary"
          :icon="VideoPlay"
          :loading="starting"
          @click="handleStartService"
          class="start-btn"
        >
          {{ serviceStatus === 'running' ? '服务已启动' : '启动 AI 服务' }}
        </el-button>
        <el-tag
          :type="serviceStatus === 'running' ? 'success' : 'info'"
          effect="dark"
          round
          class="status-tag"
        >
          {{ serviceStatus === 'running' ? '在线' : '离线' }}
        </el-tag>
      </div>
      <div class="header-right">
        <span class="model-badge">🤖 {{ currentModel }}</span>
      </div>
    </div>

    <!-- 聊天消息区域 -->
    <div class="chat-messages" ref="messageContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-item', msg.role]"
      >
        <div class="avatar">
          <img :src="msg.role === 'user' ? userAvatar : botAvatar" alt="avatar" />
        </div>
        <div class="bubble">
          <div class="content">{{ msg.content }}</div>
          <div class="time">{{ msg.time }}</div>
        </div>
      </div>
      <div v-if="typing" class="message-item assistant">
        <div class="avatar">
          <img :src="botAvatar" alt="avatar" />
        </div>
        <div class="bubble typing">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>

    <!-- 底部输入框 -->
    <div class="chat-input">
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="2"
        placeholder="输入消息... (Enter 发送，Shift+Enter 换行)"
        @keydown.enter.exact.prevent="sendMessage"
        :disabled="serviceStatus !== 'running'"
        resize="none"
      />
      <el-button
        type="success"
        :icon="Promotion"
        @click="sendMessage"
        :disabled="!inputText.trim() || serviceStatus !== 'running'"
        :loading="sending"
        round
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { VideoPlay, Promotion } from '@element-plus/icons-vue'
import { ai_start } from '@/api/ai'  // 你的启动接口
import userAvatarImg from '@/assets/avatar/1.png'
import botAvatarImg from '@/assets/avatar/3.png'

// 头像图片
const userAvatar = ref(userAvatarImg)
const botAvatar = ref(botAvatarImg)

// 状态
const serviceStatus = ref('stopped')  // 'stopped' 或 'running'
const starting = ref(false)
const sending = ref(false)
const typing = ref(false)
const currentModel = ref('qwen2:latest')

// 消息列表
const messages = ref([
  {
    role: 'assistant',
    content: '你好！我是 AI 助手，你可以先点击上方按钮启动服务，然后开始对话。',
    time: formatTime(new Date())
  }
])

const inputText = ref('')
const messageContainer = ref(null)

// 格式化时间
function formatTime(date) {
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 滚动到底部
async function scrollToBottom() {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// 启动服务
async function handleStartService() {
  if (serviceStatus.value === 'running') {
    ElMessage.info('服务已在运行中')
    return
  }
  starting.value = true
  try {
    const res = await ai_start()
    // 根据你的后端响应结构判断，假设成功返回 code 200
    if (res.code === 200) {
      serviceStatus.value = 'running'
      ElMessage.success('AI 服务启动成功！')
      // 可以加一条系统消息
      messages.value.push({
        role: 'assistant',
        content: '服务已启动，现在可以开始对话了。',
        time: formatTime(new Date())
      })
      scrollToBottom()
    } else {
      ElMessage.error(res.msg || '启动失败')
    }
  } catch (error) {
    console.error('启动失败:', error)
    ElMessage.error('网络错误，启动失败')
  } finally {
    starting.value = false
  }
}

// 发送消息
async function sendMessage() {
  const text = inputText.value.trim()
  if (!text) return
  if (serviceStatus.value !== 'running') {
    ElMessage.warning('请先启动 AI 服务')
    return
  }

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: text,
    time: formatTime(new Date())
  })
  inputText.value = ''
  scrollToBottom()

  // 显示正在输入
  typing.value = true
  sending.value = true

  // 模拟 AI 回复（后续替换为真实 API）
  setTimeout(() => {
    typing.value = false
    messages.value.push({
      role: 'assistant',
      content: '这是一个模拟回复。实际将调用 ai 模型生成回复。',
      time: formatTime(new Date())
    })
    sending.value = false
    scrollToBottom()
  }, 1500)
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.ai-chat-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  background: linear-gradient(145deg, #1a2a3a 0%, #0f1a26 100%);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

/* 头部控制栏 */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0, 206, 201, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.start-btn {
  background: linear-gradient(135deg, #00cec9, #2ecc71);
  border: none;
  color: #0c141f;
  font-weight: bold;
  padding: 8px 20px;
  border-radius: 40px;
}
.start-btn:hover {
  opacity: 0.9;
  box-shadow: 0 0 15px #00cec9;
}

.status-tag {
  font-weight: 500;
}

.model-badge {
  color: #b0c4de;
  font-size: 14px;
  background: rgba(0, 0, 0, 0.3);
  padding: 6px 16px;
  border-radius: 40px;
  border: 1px solid rgba(0, 206, 201, 0.3);
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-item {
  display: flex;
  gap: 14px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid #00cec9;
  box-shadow: 0 0 8px rgba(0, 206, 201, 0.3);
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bubble {
  max-width: 70%;
  padding: 14px 18px;
  background: rgba(20, 35, 50, 0.8);
  backdrop-filter: blur(4px);
  border-radius: 20px;
  border: 1px solid rgba(0, 206, 201, 0.2);
  color: #e0e0e0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.message-item.user .bubble {
  background: linear-gradient(135deg, #00cec9, #2ecc71);
  color: #0c141f;
  border: none;
}

.bubble .content {
  word-break: break-word;
  line-height: 1.5;
}

.bubble .time {
  font-size: 11px;
  margin-top: 6px;
  opacity: 0.7;
  text-align: right;
}

/* 正在输入动画 */
.typing {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 14px 18px;
}
.dot {
  width: 8px;
  height: 8px;
  background: #00cec9;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
.dot:nth-child(3) { animation-delay: 0s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 输入框 */
.chat-input {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  padding: 20px 24px;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(8px);
  border-top: 1px solid rgba(0, 206, 201, 0.2);
}

.chat-input :deep(.el-textarea__inner) {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 206, 201, 0.3);
  color: #e0e0e0;
  border-radius: 20px;
  padding: 12px 16px;
}
.chat-input :deep(.el-textarea__inner:focus) {
  border-color: #00cec9;
  box-shadow: 0 0 8px #00cec9;
}
</style>
