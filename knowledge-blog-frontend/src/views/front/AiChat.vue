<template>
  <div class="ai-chat-page">
    <div class="chat-header">
      <div class="header-left">
        <div class="status-indicator" :class="{ 'is-running': serviceStatus === 'running' }">
          <span class="pulse-dot"></span>
          <span class="status-text">{{ serviceStatus === 'running' ? 'AI 引擎已连接' : '引擎未启动' }}</span>
        </div>
      </div>
      <div class="header-right">
        <el-tag effect="light" round class="model-badge">
          <el-icon class="mr-1"><Cpu /></el-icon>
          {{ currentModel }}
        </el-tag>
        <el-button
          v-if="serviceStatus !== 'running'"
          type="primary"
          :loading="starting"
          @click="handleStartService"
          class="start-btn"
        >
          {{ starting ? '启动中...' : '唤醒 AI 助手' }}
        </el-button>
      </div>
    </div>

    <div class="chat-messages" ref="messageContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-item', msg.role]"
      >
        <div class="avatar">
          <img :src="msg.role === 'user' ? userAvatar : botAvatar" alt="avatar" />
        </div>
        <div class="bubble-wrapper">
          <div class="bubble">
            <div class="copy-action" @click="copyText(msg.content)" title="复制内容">
              <el-icon><CopyDocument /></el-icon>
            </div>

            <div class="content">{{ msg.content }}</div>
          </div>
          <div class="time">{{ msg.time }}</div>
        </div>
      </div>

      <div v-if="typing" class="message-item assistant">
        <div class="avatar">
          <img :src="botAvatar" alt="avatar" />
        </div>
        <div class="bubble-wrapper">
          <div class="bubble typing">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input-wrapper">
      <div class="input-card" :class="{ 'disabled-card': serviceStatus !== 'running' }">
        <el-input
          v-model="inputText"
          type="textarea"
          :autosize="{ minRows: 1, maxRows: 4 }"
          placeholder="给 AI 发送消息... (Enter 发送，Shift+Enter 换行)"
          @keydown.enter.exact.prevent="sendMessage"
          :disabled="serviceStatus !== 'running'"
          resize="none"
          class="custom-textarea"
        />
        <div class="input-actions">
          <el-button
            type="primary"
            :icon="Promotion"
            class="send-btn"
            @click="sendMessage"
            :disabled="!inputText.trim() || serviceStatus !== 'running'"
            :loading="sending"
          />
        </div>
      </div>
      <div class="input-footer-text">
        AI 生成的内容可能存在误差，请核实重要信息。
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Promotion, Cpu, CopyDocument } from '@element-plus/icons-vue'
import { ai_start, ai_chat } from '@/api/ai' // 引入新的 API
import userAvatarImg from '@/assets/avatar/1.png'
import botAvatarImg from '@/assets/avatar/3.png'

const userAvatar = ref(userAvatarImg)
const botAvatar = ref(botAvatarImg)

const serviceStatus = ref('stopped')
const starting = ref(false)
const sending = ref(false)
const typing = ref(false)
const currentModel = ref('qwen2:latest')

const messages = ref([
  {
    role: 'assistant',
    content: '你好！我是你的专属 AI 学习助手。请点击右上角唤醒我，开启我们的对话。',
    time: formatTime(new Date())
  }
])

const inputText = ref('')
const messageContainer = ref(null)

function formatTime(date) {
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

async function scrollToBottom() {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// 复制文本功能
const copyText = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage({
      message: '内容已复制到剪贴板',
      type: 'success',
      duration: 2000,
      plain: true
    })
  } catch (err) {
    ElMessage.error('复制失败，请手动选择复制')
  }
}

// 启动服务
async function handleStartService() {
  if (serviceStatus.value === 'running') return

  starting.value = true
  try {
    const res = await ai_start()
    if (res.code === 200) {
      serviceStatus.value = 'running'
      ElMessage.success('AI 引擎已成功唤醒！')
      messages.value.push({
        role: 'assistant',
        content: '我已经准备好了，请问有什么我可以帮你的？',
        time: formatTime(new Date())
      })
      scrollToBottom()
    } else {
      ElMessage.error(res.msg || '启动失败')
    }
  } catch (error) {
    console.error('启动失败:', error)
    ElMessage.error('网络连接异常，无法唤醒 AI')
  } finally {
    starting.value = false
  }
}

// 发送消息与调用真实接口
async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || serviceStatus.value !== 'running') return

  // 1. 将用户消息渲染到界面
  messages.value.push({
    role: 'user',
    content: text,
    time: formatTime(new Date())
  })
  inputText.value = ''
  scrollToBottom()

  // 2. 开启加载与打字机动画状态
  typing.value = true
  sending.value = true

  try {
    // 3. 构建发送给后端的 payload (过滤掉 time，只保留 role 和 content)
    const payload = {
      model: currentModel.value,
      messages: messages.value.map(msg => ({
        role: msg.role,
        content: msg.content
      }))
    }

    // 4. 发起真实的接口请求
    const res = await ai_chat(payload)

    // 5. 校验结果并追加 AI 回复
    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data.reply,
        time: formatTime(new Date())
      })
    } else {
      ElMessage.error(res.msg || '获取回复失败，请稍后再试')
    }
  } catch (error) {
    console.error('请求接口失败:', error)
    ElMessage.error('网络请求异常，请检查后端服务是否正常运行')
  } finally {
    // 6. 关闭状态并滚动到底部
    typing.value = false
    sending.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
/* ========== 页面级变量 ========== */
.ai-chat-page {
  --bg-color: #FFFFFF;
  --header-bg: rgba(255, 255, 255, 0.9);
  --border-color: #F1F5F9;
  --user-bg: #6366F1;
  --ai-bg: #F8FAFC;
  --text-main: #1E293B;
  --text-white: #FFFFFF;
  --text-muted: #94A3B8;

  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  background: var(--bg-color);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--border-color);
}

/* ========== 顶部状态栏 ========== */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: var(--header-bg);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  z-index: 10;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
}
.pulse-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #CBD5E1;
  position: relative;
}
.is-running .pulse-dot {
  background: #10B981;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
  animation: pulse-ring 1.5s infinite cubic-bezier(0.66, 0, 0, 1);
}
@keyframes pulse-ring {
  to { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
}
.status-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-main);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.model-badge {
  font-weight: 600;
  color: var(--user-bg);
  background: #EEF2FF;
  border: none;
}
.start-btn {
  background: var(--user-bg);
  border: none;
  font-weight: 600;
  border-radius: 8px;
  padding: 8px 16px;
}
.start-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* ========== 消息区域 ========== */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 10%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: #FAFAFA;
}

.message-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.message-item.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #FFF;
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bubble-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 75%;
}
.message-item.user .bubble-wrapper {
  align-items: flex-end;
}

.bubble {
  position: relative;
  padding: 14px 20px;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.6;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  /* 允许在长单词处断行并保留空白符以支持简易排版 */
  white-space: pre-wrap;
}

.copy-action {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.8);
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transform: scale(0.9);
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
  border: 1px solid var(--border-color);
}
.message-item:hover .copy-action {
  opacity: 1;
  transform: scale(1);
}
.copy-action:hover {
  background: #FFF;
  color: var(--user-bg);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.bubble .content {
  padding-right: 24px;
  word-break: break-word;
}

.assistant .bubble {
  background: var(--bg-color);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  border-top-left-radius: 4px;
}

.user .bubble {
  background: var(--user-bg);
  color: var(--text-white);
  border-top-right-radius: 4px;
}
.user .copy-action {
  background: rgba(0, 0, 0, 0.15);
  border: none;
  color: rgba(255, 255, 255, 0.8);
}
.user .copy-action:hover {
  background: rgba(0, 0, 0, 0.3);
  color: #FFF;
}

.bubble-wrapper .time {
  font-size: 12px;
  margin-top: 6px;
  color: var(--text-muted);
  font-family: monospace;
}

/* 正在输入动画 */
.typing {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 16px 20px;
}
.dot {
  width: 6px;
  height: 6px;
  background: var(--user-bg);
  border-radius: 50%;
  animation: typing-bounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing-bounce {
  0%, 80%, 100% { transform: scale(0.4); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

/* ========== 底部输入区域 ========== */
.chat-input-wrapper {
  padding: 20px 10%;
  background: linear-gradient(to top, #FAFAFA 60%, transparent);
}

.input-card {
  display: flex;
  align-items: flex-end;
  background: var(--bg-color);
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 10px 14px 10px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
}
.input-card:focus-within {
  border-color: #A5B4FC;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.08);
}
.input-card.disabled-card {
  background: #F8FAFC;
  opacity: 0.8;
}

.custom-textarea :deep(.el-textarea__inner) {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 4px 0;
  color: var(--text-main);
  font-size: 15px;
  line-height: 1.5;
}
.custom-textarea :deep(.el-textarea__inner:focus) {
  box-shadow: none;
}

.input-actions {
  padding: 0 0 2px 12px;
}

.send-btn {
  background: var(--user-bg);
  border: none;
  border-radius: 45px;
  width: 40px;
  height: 40px;
  font-size: 18px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.send-btn:not(:disabled):hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.input-footer-text {
  text-align: center;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 12px;
}
</style>
