<template>
  <el-container class="admin-layout">
    <el-header class="admin-header">
      <div class="header-left">
        <el-button
          :icon="Fold"
          circle
          class="collapse-btn"
          @click="isSidebarCollapsed = !isSidebarCollapsed"
        />
        <div class="logo-wrapper">
          <span class="logo">⚡ 控制台</span>
          <span class="badge">PRO</span>
        </div>
      </div>

      <div class="header-center">
        <nav class="nav-links">
          <router-link to="/admin/dashboard" class="nav-item" active-class="active">
            <el-icon><Odometer /></el-icon>
            <span>仪表盘</span>
          </router-link>
          <router-link to="/admin/articles" class="nav-item" active-class="active">
            <el-icon><Document /></el-icon>
            <span>文章</span>
          </router-link>
          <router-link to="/admin/userAdmin" class="nav-item" active-class="active">
            <el-icon><User /></el-icon>
            <span>用户</span>
          </router-link>
          <router-link to="/admin/settings" class="nav-item" active-class="active">
            <el-icon><Setting /></el-icon>
            <span>设置</span>
          </router-link>
        </nav>
      </div>

      <div class="header-right">
        <div class="search-wrapper">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索全站..."
            class="search-input"
            :prefix-icon="Search"
            @keyup.enter="handleSearch"
            clearable
          />
        </div>

        <el-badge is-dot class="notification-badge">
          <el-button :icon="Bell" circle class="icon-btn" />
        </el-badge>

        <el-dropdown @command="handleCommand" trigger="click">
          <div class="avatar-wrapper">
            <el-avatar :src="userAvatar" :size="42" class="user-avatar" />
            <div class="avatar-ring"></div>
          </div>
          <template #dropdown>
            <el-dropdown-menu class="dark-dropdown">
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>个人资料
              </el-dropdown-item>
              <el-dropdown-item command="front">
                <el-icon><Monitor /></el-icon>返回前台
              </el-dropdown-item>
              <el-dropdown-item divided command="logout" class="danger-item">
                <el-icon><SwitchButton /></el-icon>退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container class="main-container">
      <el-aside :width="isSidebarCollapsed ? '72px' : '260px'" class="admin-aside">
        <el-menu
          :default-active="activeMenu"
          :collapse="isSidebarCollapsed"
          :collapse-transition="false"
          router
          class="sidebar-menu"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><Odometer /></el-icon>
            <template #title><span>仪表盘</span></template>
          </el-menu-item>
          <el-menu-item index="/admin/articles">
            <el-icon><Document /></el-icon>
            <template #title><span>文章管理</span></template>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <template #title><span>用户管理</span></template>
          </el-menu-item>
          <el-menu-item index="/admin/comments">
            <el-icon><ChatDotRound /></el-icon>
            <template #title><span>评论审核</span></template>
          </el-menu-item>

          <el-sub-menu index="/admin/system">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </template>
            <el-menu-item index="/admin/settings/basic">基础配置</el-menu-item>
            <el-menu-item index="/admin/settings/seo">SEO 优化</el-menu-item>
            <el-menu-item index="/admin/settings/backup">备份管理</el-menu-item>
          </el-sub-menu>

          <el-divider class="dark-divider" />

          <el-menu-item index="/admin/logs">
            <el-icon><List /></el-icon>
            <template #title><span>操作日志</span></template>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>

    <el-tooltip content="唤醒 AI 引擎 (可拖拽)" placement="top" :show-after="500" :disabled="isDragging">
      <div
        class="ai-float-btn"
        :style="{ left: btnPosition.x + 'px', top: btnPosition.y + 'px', right: 'auto', bottom: 'auto' }"
        @mousedown="startDrag"
        @touchstart="startDrag"
      >
        <div class="glow-ring"></div>
        <el-icon :size="28"><Cpu /></el-icon>
      </div>
    </el-tooltip>

    <AiAssistant ref="aiAssistantRef" />
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  Fold, Search, Bell, Odometer, Document, User, Setting,
  ChatDotRound, List, Cpu, SwitchButton, Monitor
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import AiAssistant from '@/components/AiAssistant.vue'
import defaultAvatar from '@/assets/avatar/3.png'

const router = useRouter()
const route = useRoute()
const username = ref(localStorage.getItem('username') || 'Admin')
const userAvatar = ref(defaultAvatar)

const searchKeyword = ref('')
const isSidebarCollapsed = ref(false)
const aiAssistantRef = ref(null)

const activeMenu = computed(() => route.path)

// --- 炫酷 AI 悬浮球拖拽逻辑 ---
const btnPosition = ref({ x: -1000, y: -1000 })
const isDragging = ref(false)
let hasMoved = false
let startMouse = { x: 0, y: 0 }
let startPos = { x: 0, y: 0 }

onMounted(() => {
  // 初始位置右下角
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

  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) hasMoved = true

  let newX = startPos.x + dx
  let newY = startPos.y + dy

  const maxX = window.innerWidth - 70
  const maxY = window.innerHeight - 70
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

  if (!hasMoved) {
    aiAssistantRef.value?.open()
  }
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    ElMessage.success(`正在全站检索：${searchKeyword.value}`)
  }
}

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    ElMessage.success('已安全退出')
    router.push('/login')
  } else if (command === 'front') {
    router.push('/')
  } else if (command === 'profile') {
    router.push('/admin/profile')
  }
}
</script>

<style scoped>
/* ========== 全局布局 (深浅结合，突出控制台质感) ========== */
.admin-layout {
  height: 100vh;
  background: #f4f7fb; /* 主内容区浅色底，反衬深色外壳 */
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  overflow: hidden;
}

/* ========== 顶部导航 (暗黑系) ========== */
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 72px;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 240px;
}
.collapse-btn {
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 18px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.collapse-btn:hover {
  background: linear-gradient(135deg, #00cec9, #2ecc71);
  color: white;
  border-color: transparent;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 0 15px rgba(0, 206, 201, 0.4);
}

.logo-wrapper {
  display: flex;
  align-items: center;
}
.logo {
  font-size: 22px;
  font-weight: 900;
  background: linear-gradient(to right, #00f2fe 0%, #4facfe 100%, #00f2fe);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: 1px;
  animation: shine 3s linear infinite;
}
@keyframes shine {
  to { background-position: 200% center; }
}
.badge {
  font-size: 10px;
  background: rgba(0, 242, 254, 0.15);
  color: #00f2fe;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(0, 242, 254, 0.3);
  font-weight: 700;
  margin-left: 8px;
  letter-spacing: 1px;
}

/* 中间导航 (悬浮药丸风格) */
.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}
.nav-links {
  display: flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.03);
  padding: 6px;
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #94a3b8;
  text-decoration: none;
  border-radius: 40px;
  transition: all 0.3s;
}
.nav-item:hover {
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.08);
}
.nav-item.active {
  background: linear-gradient(135deg, #00f2fe, #4facfe);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
}

/* 右侧区域 */
.header-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 20px;
  width: 260px;
}

/* 赛博搜索框 */
.search-wrapper {
  width: 180px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.search-wrapper:focus-within {
  width: 240px;
}
.search-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05) !important;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
  border-radius: 40px;
  transition: all 0.3s;
}
.search-input :deep(.el-input__wrapper.is-focus) {
  background: rgba(0, 242, 254, 0.05) !important;
  box-shadow: inset 0 0 0 1px #00f2fe !important;
}
.search-input :deep(.el-input__inner) {
  color: #e2e8f0;
}
.search-input :deep(.el-input__prefix) {
  color: #94a3b8;
}
.search-input :deep(.el-input__wrapper.is-focus .el-input__prefix) {
  color: #00f2fe;
}

/* 图标按钮 */
.icon-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  transition: all 0.3s;
}
.icon-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.3);
}
.notification-badge :deep(.el-badge__content.is-dot) {
  background: #ff007f; /* 赛博粉红通知点 */
  box-shadow: 0 0 8px #ff007f;
  right: 6px;
  top: 6px;
}

/* 头像 & 霓虹呼吸环 */
.avatar-wrapper {
  position: relative;
  cursor: pointer;
  width: 42px;
  height: 42px;
  border-radius: 50%;
}
.avatar-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 50%;
  background: linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
  z-index: -1;
  animation: spin-bg 4s linear infinite;
  opacity: 0.7;
}
.user-avatar {
  border: 2px solid #0f172a;
}
@keyframes spin-bg {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ========== 侧边栏 (暗黑系) ========== */
.admin-aside {
  background: rgba(15, 23, 42, 0.98);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  z-index: 99;
}

.sidebar-menu {
  border-right: none;
  background: transparent;
  padding: 16px 12px;
}
/* 覆盖 Element Plus 默认样式 */
.sidebar-menu :deep(.el-menu-item),
.sidebar-menu :deep(.el-sub-menu__title) {
  border-radius: 12px;
  margin-bottom: 8px;
  height: 50px;
  line-height: 50px;
  color: #94a3b8;
  font-weight: 500;
  transition: all 0.3s ease;
}
.sidebar-menu :deep(.el-menu-item:hover),
.sidebar-menu :deep(.el-sub-menu__title:hover) {
  background: rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
  transform: translateX(4px);
}
.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(0, 242, 254, 0.15) 0%, transparent 100%);
  color: #00f2fe;
  font-weight: 700;
  border-left: 4px solid #00f2fe;
}
.sidebar-menu :deep(.el-menu-item.is-active .el-icon) {
  color: #00f2fe;
  filter: drop-shadow(0 0 5px rgba(0, 242, 254, 0.5));
}
.dark-divider {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  margin: 16px 0;
}

/* 折叠状态居中修复 */
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
.sidebar-menu.el-menu--collapse :deep(.el-menu-item.is-active) {
  border-left: none;
  background: rgba(0, 242, 254, 0.15);
  width: 44px;
  margin: 8px auto;
  border-radius: 12px;
}
.sidebar-menu.el-menu--collapse :deep(.el-menu-item:hover) {
  transform: scale(1.1);
}

/* ========== 主内容 ========== */
.admin-main {
  padding: 24px;
  height: calc(100vh - 72px);
  overflow-y: auto;
  position: relative;
}

/* ========== 拖拽 AI 引擎按钮 (极客发光版) ========== */
.ai-float-btn {
  position: fixed;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #0f172a;
  border: 2px solid #00f2fe;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00f2fe;
  cursor: grab;
  z-index: 9999;
  user-select: none;
  touch-action: none;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 0 20px rgba(0, 242, 254, 0.3), inset 0 0 15px rgba(0, 242, 254, 0.2);
}

.ai-float-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 0 30px rgba(0, 242, 254, 0.6), inset 0 0 20px rgba(0, 242, 254, 0.4);
}

.ai-float-btn:active {
  cursor: grabbing;
  transform: scale(0.95);
  box-shadow: 0 0 10px rgba(0, 242, 254, 0.8);
}

/* 引擎波纹光环 */
.glow-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #00f2fe;
  animation: radar-pulse 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}

@keyframes radar-pulse {
  0% { transform: scale(0.9); opacity: 1; }
  100% { transform: scale(1.6); opacity: 0; }
}

/* ========== 响应式 ========== */
@media (max-width: 992px) {
  .header-center { display: none; }
}
</style>
