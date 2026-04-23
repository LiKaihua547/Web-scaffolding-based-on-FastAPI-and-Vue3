<template>
  <el-dialog
    v-model="visible"
    :modal="false"
    :close-on-click-modal="false"
    draggable
    class="beautiful-ai-dialog"
    width="400px"
    top="15vh"
    :show-close="false"
  >
    <template #header="{ close }">
      <div class="ai-header">
        <div class="ai-header-info">
          <el-avatar :size="36" :src="botAvatar" class="bot-header-avatar" />
          <div class="bot-status">
            <span class="bot-name">✨ 智能助手</span>
            <span class="bot-online"><span class="dot"></span> AI Online</span>
          </div>
        </div>
        <el-button class="close-btn" :icon="Close" circle @click="close" />
      </div>
    </template>

    <div class="ai-assistant">
      <div class="chat-area" ref="chatAreaRef">
        <div v-for="(msg, idx) in messages" :key="idx" :class="['message-box', msg.role]">
          <div class="avatar" v-if="msg.role === 'assistant'">
            <el-avatar :size="28" :src="botAvatar" />
          </div>
          <div class="bubble">{{ msg.content }}</div>
        </div>

        <div v-if="loading" class="message-box assistant">
          <div class="avatar">
            <el-avatar :size="28" :src="botAvatar" />
          </div>
          <div class="bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <div class="input-area">
        <el-input
          v-model="inputText"
          placeholder="向助手提问..."
          @keyup.enter="sendMessage"
          :disabled="loading"
          class="chat-input"
        >
          <template #append>
            <el-button
              class="send-btn"
              :icon="Promotion"
              @click="sendMessage"
              :loading="loading"
              :disabled="!inputText.trim()"
            />
          </template>
        </el-input>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Promotion, Close } from '@element-plus/icons-vue'

const visible = ref(false)
const inputText = ref('')
const loading = ref(false)
const chatAreaRef = ref(null)

const messages = ref([
  { role: 'assistant', content: '你好！我是你的专属知识助理，有什么可以帮你的吗？' }
])

const botAvatar = 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=100&h=100&fit=crop&auto=format'

const open = () => {
  visible.value = true
  scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatAreaRef.value) {
    chatAreaRef.value.scrollTop = chatAreaRef.value.scrollHeight
  }
}

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  loading.value = true
  scrollToBottom()

  // 模拟请求后端的延迟
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: '这是一个测试回复。如果你想接入真实的 AI 接口，可以在这里把模拟请求换成 Axios 请求。'
    })
    loading.value = false
    scrollToBottom()
  }, 1200)
}

defineExpose({ open })
</script>

<style>
/* 覆盖 El-Dialog 的全局默认样式来美化弹窗 */
.beautiful-ai-dialog.el-dialog {
  border-radius: 24px !important;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15),
              0 0 0 1px rgba(0, 0, 0, 0.05) !important;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(20px);
  padding: 0 !important;
  margin-right: 20px; /* 控制它靠右边显示 */
  pointer-events: auto;
}

/* 隐藏自带的 Header 和 Body padding，自己掌控 */
.beautiful-ai-dialog .el-dialog__header {
  padding: 0 !important;
  margin: 0 !important;
}
.beautiful-ai-dialog .el-dialog__body {
  padding: 0 !important;
}
</style>

<style scoped>
/* ========== 自定义 Header区 ========== */
.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #EEF2FF, #FAFAFA);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  cursor: move; /* 提示这里可以拖动 */
}

.ai-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.bot-header-avatar {
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.bot-status {
  display: flex;
  flex-direction: column;
}
.bot-name {
  font-weight: 700;
  font-size: 15px;
  color: #1E293B;
}
.bot-online {
  font-size: 12px;
  color: #64748B;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 2px;
}
.bot-online .dot {
  width: 6px;
  height: 6px;
  background-color: #10B981;
  border-radius: 50%;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.close-btn {
  border: none;
  background: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.close-btn:hover {
  background: #FEE2E2;
  color: #EF4444;
}

/* ========== 聊天内容区 ========== */
.ai-assistant {
  display: flex;
  flex-direction: column;
  height: 480px; /* 固定弹窗高度 */
}

.chat-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: transparent;
}
.chat-area::-webkit-scrollbar {
  width: 6px;
}
.chat-area::-webkit-scrollbar-thumb {
  background: #E2E8F0;
  border-radius: 4px;
}

.message-box {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}
.message-box.user {
  flex-direction: row-reverse;
}

.avatar {
  flex-shrink: 0;
}

.bubble {
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.5;
  max-width: 85%;
  word-break: break-word;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}

.assistant .bubble {
  background: #F1F5F9;
  color: #334155;
  border-radius: 16px 16px 16px 4px; /* AI 气泡左下角变直 */
}

.user .bubble {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  color: white;
  border-radius: 16px 16px 4px 16px; /* 用户气泡右下角变直 */
}

/* 打字机动画 */
.typing {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 14px 18px;
}
.typing span {
  width: 6px;
  height: 6px;
  background: #94A3B8;
  border-radius: 50%;
  animation: jump 1.2s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes jump {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* ========== 底部输入框 ========== */
.input-area {
  padding: 16px;
  background: white;
  border-top: 1px solid rgba(0,0,0,0.05);
}

.chat-input :deep(.el-input__wrapper) {
  border-radius: 20px 0 0 20px;
  background: #F8FAFC;
  box-shadow: none;
  border: 1px solid #E2E8F0;
}
.chat-input :deep(.el-input__wrapper.is-focus) {
  border-color: #6366F1;
}
.chat-input :deep(.el-input-group__append) {
  border-radius: 0 20px 20px 0;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-left: none;
  padding: 0 16px;
}

.send-btn {
  color: #6366F1;
  font-size: 18px;
  transition: transform 0.2s;
}
.send-btn:not(:disabled):hover {
  transform: scale(1.1);
}
</style>
