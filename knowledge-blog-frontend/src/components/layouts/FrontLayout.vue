<template>
  <el-container class="front-layout">
    <el-header class="front-header">
      <div class="header-left">
        <el-button
          :icon="Fold"
          circle
          class="collapse-btn"
          @click="isSidebarCollapsed = !isSidebarCollapsed"
        />
        <div class="logo-wrapper">
          <span class="logo-icon">📘</span>
          <span class="logo-text">知识博客</span>
        </div>
      </div>

      <div class="header-center">
        <div class="search-wrapper">
          <el-input
            v-model="searchKeyword"
            placeholder="探索无限知识..."
            class="search-input"
            :prefix-icon="Search"
            @keyup.enter="handleSearch"
            clearable
          />
        </div>
      </div>

      <div class="header-right">
        <template v-if="!token">
          <el-button type="primary" class="login-btn" round @click="$router.push('/login')">
            登录 / 注册
          </el-button>
        </template>

        <template v-else>
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-action-area">
              <el-avatar :src="userAvatar" :size="48" class="user-avatar">
                {{ username.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username-text">{{ username }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="custom-dropdown">
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人主页
                </el-dropdown-item>
                <el-dropdown-item command="admin" v-if="token">
                  <el-icon><Setting /></el-icon>后台管理
                </el-dropdown-item>
                <el-dropdown-item divided command="logout" class="danger-item">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </div>
    </el-header>

    <el-container class="main-container">
      <el-aside :width="isSidebarCollapsed ? '72px' : '260px'" class="front-aside">
        <el-menu
          :default-active="activeMenu"
          :collapse="isSidebarCollapsed"
          :collapse-transition="false"
          router
          class="sidebar-menu"
        >
          <div class="menu-group-title" v-show="!isSidebarCollapsed">发现</div>
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <template #title><span>探索首页</span></template>
          </el-menu-item>
          <el-menu-item index="/forum">
            <el-icon><ChatDotRound /></el-icon>
            <template #title><span>交流论坛</span></template>
          </el-menu-item>
          <el-menu-item index="/learn">
            <el-icon><Reading /></el-icon>
            <template #title><span>学习宇宙</span></template>
          </el-menu-item>
          <el-menu-item index="/entertain">
            <el-icon><Film /></el-icon>
            <template #title><span>数字娱乐</span></template>
          </el-menu-item>

          <div class="menu-group-title mt-4" v-show="!isSidebarCollapsed">创作与工具</div>
          <el-sub-menu index="/ai">
            <template #title>
              <el-icon class="ai-icon-gradient"><Cpu /></el-icon>
              <span class="ai-text-gradient">AI 强力驱动</span>
            </template>
            <el-menu-item index="/ai/chat">智能对话</el-menu-item>
            <el-menu-item index="/ai/config">模型配置</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/diary">
            <el-icon><Notebook /></el-icon>
            <template #title><span>灵感日记</span></template>
          </el-menu-item>

          <el-divider class="menu-divider" />

          <el-menu-item index="/bookmarks">
            <el-icon><Star /></el-icon>
            <template #title><span>我的星标收藏</span></template>
          </el-menu-item>
          <el-menu-item index="/drafts">
            <el-icon><EditPen /></el-icon>
            <template #title><span>草稿箱</span></template>
          </el-menu-item>
        </el-menu>

        <div class="aside-footer" v-show="!isSidebarCollapsed">
          <p>© 2026 知识博客</p>
          <p>探索无限可能</p>
        </div>
      </el-aside>

      <el-main class="front-main" id="scroll-wrapper">
        <div class="content-wrapper">
          <router-view />
        </div>
      </el-main>
    </el-container>

    <el-tooltip content="唤醒 AI 智能助手 (可拖拽)" placement="top" :show-after="500" :disabled="isDragging">
      <div
        class="ai-float-btn"
        :style="{ left: btnPosition.x + 'px', top: btnPosition.y + 'px', right: 'auto', bottom: 'auto' }"
        @mousedown="startDrag"
        @touchstart="startDrag"
      >
        <el-icon :size="28"><Cpu /></el-icon>
      </div>
    </el-tooltip>

    <AiAssistant ref="aiAssistantRef" />
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import defaultAvatar from '@/assets/avatar/0.png'
import { useRouter, useRoute } from 'vue-router'
import {
  Search, Fold, HomeFilled, ChatDotRound, Notebook,
  Reading, Film, Cpu, User, Star, EditPen, Setting, SwitchButton
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import AiAssistant from '@/components/AiAssistant.vue'

const router = useRouter()
const route = useRoute()

const token = ref(localStorage.getItem('token') || 'mock-token')
const user = ref(JSON.parse(localStorage.getItem('user') || '{"username": "探索者"}'))
const username = computed(() => user.value.username || '游客')
const userAvatar = ref(defaultAvatar)

const searchKeyword = ref('')
const isSidebarCollapsed = ref(false)
const aiAssistantRef = ref(null)

const activeMenu = computed(() => route.path)

// --- 拖拽功能实现 ---
const btnPosition = ref({ x: -1000, y: -1000 }) // 初始隐藏，防止闪烁
const isDragging = ref(false)
let hasMoved = false
let startMouse = { x: 0, y: 0 }
let startPos = { x: 0, y: 0 }

onMounted(() => {
  // 初始化位置放在右下角
  btnPosition.value = {
    x: window.innerWidth - 100,
    y: window.innerHeight - 100
  }
})

const startDrag = (e) => {
  isDragging.value = true
  hasMoved = false
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  startMouse = { x: clientX, y: clientY }
  startPos = { x: btnPosition.value.x, y: btnPosition.value.y }

  document.addEventListener('mousemove', onDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchend', stopDrag)
}

const onDrag = (e) => {
  if (!isDragging.value) return
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  const dx = clientX - startMouse.x
  const dy = clientY - startMouse.y

  // 移动超过 3px 视为拖拽，而不是点击
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
    hasMoved = true
  }

  let newX = startPos.x + dx
  let newY = startPos.y + dy

  // 边界控制
  const maxX = window.innerWidth - 60
  const maxY = window.innerHeight - 60
  btnPosition.value.x = Math.max(10, Math.min(newX, maxX))
  btnPosition.value.y = Math.max(10, Math.min(newY, maxY))

  if (e.cancelable) e.preventDefault()
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchend', stopDrag)

  // 如果没有发生明显移动，说明是点击行为，打开 AI 助手
  if (!hasMoved) {
    aiAssistantRef.value?.open()
  }
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    ElMessage.success(`正在为您全网检索：${searchKeyword.value}`)
  } else {
    ElMessage.warning('请输入您想探索的内容')
  }
}

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('avatar')
    token.value = null
    ElMessage.success('期待您的再次访问')
    router.push('/login')
  } else if (command === 'admin') {
    router.push('/admin')
  } else if (command === 'profile') {
    router.push('/profile')
  }
}
</script>

<style scoped>
/* ========== 全局色彩与变量 ========== */
.front-layout {
  --app-bg: #F8FAFC;
  --header-bg: rgba(255, 255, 255, 0.85);
  --sidebar-bg: #FFFFFF;
  --primary-color: #6366F1;
  --primary-hover: #EEF2FF;
  --text-main: #1E293B;
  --text-muted: #64748B;
  --border-light: #E2E8F0;

  min-height: 100vh;
  background: var(--app-bg);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text-main);
}

/* ========== 顶部导航 ========== */
.front-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 72px;
  background: var(--header-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-light);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 18px;
  transition: all 0.3s ease;
}
.collapse-btn:hover {
  background: var(--primary-hover);
  color: var(--primary-color);
  transform: scale(1.05);
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
.logo-icon {
  font-size: 26px;
}
.logo-text {
  font-size: 22px;
  font-weight: 800;
  background: linear-gradient(135deg, #4F46E5 0%, #9333EA 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: -0.5px;
}

/* ========== 搜索框 ========== */
.header-center {
  flex: 2;
  display: flex;
  justify-content: center;
}

.search-wrapper {
  position: relative;
  width: 100%;
  max-width: 480px;
  display: flex;
  align-items: center;
}
.search-input :deep(.el-input__wrapper) {
  background: #F1F5F9;
  border-radius: 20px;
  box-shadow: none !important;
  border: 1px solid transparent;
  padding-left: 16px;
  padding-right: 50px;
  height: 42px;
  transition: all 0.3s ease;
}
.search-input :deep(.el-input__wrapper.is-focus) {
  background: #FFFFFF;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

/* ========== 头像与用户操作 ========== */
.header-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.login-btn {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border: none;
  font-weight: 600;
  padding: 8px 24px;
}

.user-action-area {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 4px 16px 4px 4px;
  border-radius: 40px;
  transition: background 0.3s;
}
.user-action-area:hover {
  background: #F1F5F9;
}
.user-avatar {
  border: 2px solid #FFFFFF;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.username-text {
  font-weight: 600;
  font-size: 15px;
  color: var(--text-main);
}
.danger-item {
  color: #EF4444 !important;
}

/* ========== 侧边栏 ========== */
.front-aside {
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border-light);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.sidebar-menu {
  border-right: none;
  padding: 16px 12px;
  flex: 1;
  overflow-y: auto;
}
.sidebar-menu::-webkit-scrollbar {
  display: none;
}

.menu-group-title {
  font-size: 12px;
  font-weight: 700;
  color: #94A3B8;
  padding: 8px 12px;
  letter-spacing: 1px;
}
.mt-4 {
  margin-top: 16px;
}

/* 菜单项基础样式 */
.sidebar-menu :deep(.el-menu-item),
.sidebar-menu :deep(.el-sub-menu__title) {
  border-radius: 10px;
  margin-bottom: 4px;
  height: 46px;
  line-height: 46px;
  color: var(--text-muted);
  font-weight: 500;
}
.sidebar-menu :deep(.el-menu-item .el-icon),
.sidebar-menu :deep(.el-sub-menu__title .el-icon) {
  font-size: 18px;
}

/* 悬停与激活态 */
.sidebar-menu :deep(.el-menu-item:hover),
.sidebar-menu :deep(.el-sub-menu__title:hover) {
  background: var(--primary-hover);
  color: var(--primary-color);
}
.sidebar-menu :deep(.el-menu-item.is-active) {
  background: var(--primary-hover);
  color: var(--primary-color);
  font-weight: 600;
  position: relative;
}
.sidebar-menu :deep(.el-menu-item.is-active::before) {
  content: '';
  position: absolute;
  left: -12px;
  top: 50%;
  transform: translateY(-50%);
  height: 20px;
  width: 4px;
  background: var(--primary-color);
  border-radius: 0 4px 4px 0;
}

/* AI 专属色彩 */
.ai-text-gradient {
  background: linear-gradient(90deg, #F59E0B, #EC4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
}
.ai-icon-gradient {
  color: #EC4899 !important;
}

/* 【优化 2】折叠状态深度修复：让图标绝对居中，不再贴边 */
.sidebar-menu.el-menu--collapse {
  width: 100%;
}
.sidebar-menu.el-menu--collapse :deep(.el-menu-item),
.sidebar-menu.el-menu--collapse :deep(.el-sub-menu__title),
.sidebar-menu.el-menu--collapse :deep(.el-menu-tooltip__trigger) {
  padding: 0 !important;
  justify-content: center;
  align-items: center;
  display: flex;
}
.sidebar-menu.el-menu--collapse :deep(.el-menu-item.is-active::before) {
  display: none;
}

.menu-divider {
  margin: 12px 0;
  border-color: var(--border-light);
}

.aside-footer {
  padding: 16px;
  text-align: center;
  font-size: 12px;
  color: #CBD5E1;
  border-top: 1px solid var(--border-light);
}

/* ========== 主内容区 ========== */
.front-main {
  padding: 24px 32px;
  height: calc(100vh - 72px);
  overflow-y: auto;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100%;
}

/* ========== 悬浮按钮 (支持拖拽后的优化样式) ========== */
.ai-float-btn {
  position: fixed;
  width: 60px;
  height: 60px;
  border-radius: 20px;
  background: linear-gradient(135deg, #6366F1, #D946EF);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: grab;
  z-index: 1000;
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.6),
              0 8px 10px -6px rgba(217, 70, 239, 0.5);
  transition: transform 0.2s, box-shadow 0.2s;
  /* 允许脱离普通流被自由拖拽 */
  user-select: none;
  touch-action: none;
}

.ai-float-btn:active {
  cursor: grabbing;
  transform: scale(0.95);
  box-shadow: 0 5px 15px -5px rgba(99, 102, 241, 0.4);
}

/* ========== 响应式适配 ========== */
@media (max-width: 992px) {
  .header-center { display: none; }
}
@media (max-width: 768px) {
  .front-header { padding: 0 16px; }
  .front-main { padding: 16px; }
  .front-aside {
    position: absolute;
    height: calc(100vh - 72px);
    z-index: 90;
    box-shadow: 4px 0 16px rgba(0,0,0,0.05);
  }
}
</style>
