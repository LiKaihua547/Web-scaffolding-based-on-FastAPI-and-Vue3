import { createRouter, createWebHistory } from 'vue-router'

// 布局组件
import FrontLayout from '@/components/layouts/FrontLayout.vue'
import AdminLayout from '@/components/layouts/AdminLayout.vue'

// 通用页面（无布局）
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

// 前台页面
import FrontHome from '@/views/front/Home.vue'
import Article from '@/views/front/Article.vue'
import Forum from '@/views/front/Forum.vue'
import Diary from '@/views/front/Diary.vue'
import Learn from '@/views/front/Learn.vue'
import Entertain from '@/views/front/Entertain.vue'
import AI from '@/views/front/AI.vue'
import Profile from '@/views/front/Profile.vue'
import AiChat from '@/views/front/AiChat.vue'
import AiConfig from '@/views/front/AiConfig.vue'
// 后台页面
import Dashboard from '@/views/admin/Dashboard.vue'
import Articles from '@/views/admin/Articles.vue'
import Settings from '@/views/admin/Settings.vue'
import UserAdmin from '@/views/admin/UserAdmin.vue'

const routes = [
  // 独立页面（无布局）
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },

  // 前台布局路由
  {
    path: '/',
    component: FrontLayout,
    children: [
      { path: '', name: 'Home', component: FrontHome },
      { path: 'article/:id', name: 'Article', component: Article },
      { path: 'forum', name: 'Forum', component: Forum },
      { path: 'diary', name: 'Diary', component: Diary },
      { path: 'learn', name: 'Learn', component: Learn },
      { path: 'entertain', name: 'Entertain', component: Entertain },
      { path: 'ai', name: 'AI', component: AI },
       {
      path: 'ai/chat',
      name: 'AiChat',
      component: AiChat,
    },
    {
      path: 'ai/config',
      name: 'AiConfig',
      component: AiConfig,
    },
      { path: 'profile', name: 'Profile', component: Profile },

    ]
  },

  // 后台布局路由（需要登录）
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', name: 'Dashboard', component: Dashboard },
      { path: 'articles', name: 'AdminArticles', component: Articles },
      { path: 'settings', name: 'Settings', component: Settings },
      { path: 'userAdmin', name: 'UserAdmin', component: UserAdmin },
    ]
  },

  // 404 重定向
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  let user = null
  try {
    user = userStr ? JSON.parse(userStr) : null
  } catch {
    user = null
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({ path: '/login', query: { redirect: to.fullPath } })
    } else {
      // 如果是后台路由，且用户不是管理员，则跳转首页
      if (to.path.startsWith('/admin') && !user?.is_superuser) {
        next('/')
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router
