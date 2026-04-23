<template>
  <div class="home-page">
    <!-- 欢迎横幅 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">探索无限知识</h1>
        <p class="hero-subtitle">分享技术心得 · 记录生活点滴 · 连接同频伙伴</p>
        <el-button type="success" round size="large" @click="startExplore">开始阅读</el-button>
      </div>
      <div class="hero-decoration">
        <img
          src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600&auto=format&fit=crop"
          alt="reading illustration"
          class="hero-image"
        />
      </div>
    </section>

    <!-- 主体：文章列表 + 侧边栏 -->
    <div class="home-main">
      <!-- 左侧文章列表 -->
      <div class="article-list">
        <div class="section-header">
          <h2 class="section-title">📰 最新文章</h2>
          <router-link to="/articles" class="more-link">查看更多 →</router-link>
        </div>

        <el-row :gutter="24">
          <el-col v-for="article in articles" :key="article.id" :xs="24" :sm="12" :md="8">
            <el-card class="article-card" shadow="hover" @click="goToArticle(article.id)">
              <div class="card-cover">
                <img :src="article.cover" :alt="article.title" />
                <div class="category-tag">{{ article.category }}</div>
              </div>
              <div class="card-body">
                <h3 class="article-title">{{ article.title }}</h3>
                <p class="article-summary">{{ article.summary }}</p>
                <div class="article-meta">
                  <span class="author">
                    <el-icon><User /></el-icon> {{ article.author }}
                  </span>
                  <span class="date">
                    <el-icon><Calendar /></el-icon> {{ article.date }}
                  </span>
                </div>
                <div class="article-stats">
                  <span><el-icon><View /></el-icon> {{ article.views }}</span>
                  <span><el-icon><Star /></el-icon> {{ article.likes }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 右侧边栏 -->
      <div class="sidebar">
        <!-- 个人信息卡片 -->
        <el-card class="profile-card" shadow="hover">
          <div class="profile-header">
            <el-avatar :size="64" :src="profileAvatar" />
            <div class="profile-info">
              <h4>{{ username }}</h4>
              <p>博主 · 终身学习者</p>
            </div>
          </div>
          <el-divider />
          <div class="profile-stats">
            <div class="stat-item">
              <div class="stat-value">{{ articles.length }}</div>
              <div class="stat-label">文章</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">128</div>
              <div class="stat-label">粉丝</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">1.2k</div>
              <div class="stat-label">获赞</div>
            </div>
          </div>
        </el-card>

        <!-- 热门文章卡片 -->
        <el-card class="hot-card" shadow="hover">
          <template #header>
            <span class="card-header-title">🔥 热门文章</span>
          </template>
          <ul class="hot-list">
            <li v-for="item in hotArticles" :key="item.id" @click="goToArticle(item.id)">
              <span class="hot-title">{{ item.title }}</span>
              <span class="hot-views"><el-icon><View /></el-icon> {{ item.views }}</span>
            </li>
          </ul>
        </el-card>

        <!-- 标签云 -->
        <el-card class="tags-card" shadow="hover">
          <template #header>
            <span class="card-header-title">🏷️ 热门标签</span>
          </template>
          <div class="tag-cloud">
            <el-tag v-for="tag in tags" :key="tag" class="tag-item" effect="plain" round>
              {{ tag }}
            </el-tag>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Calendar, View, Star } from '@element-plus/icons-vue'

const router = useRouter()
const username = ref(localStorage.getItem('username') || '访客')
const profileAvatar = ref('https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=128&h=128&fit=crop&crop=faces&auto=format')

// 模拟文章数据
const articles = ref([
  {
    id: 1,
    title: 'FastAPI + Vue3 全栈开发实战',
    summary: '从零搭建个人知识博客，包含用户认证、文章管理、AI助手等完整功能。',
    cover: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=240&fit=crop&auto=format',
    category: '后端',
    author: '博主',
    date: '2026-04-15',
    views: 1234,
    likes: 89
  },
  {
    id: 2,
    title: 'Python 代码生成器：一键生成 Model 与 DAO',
    summary: '根据数据库表自动生成 Pydantic 模型和 DAO 层，大幅提升开发效率。',
    cover: 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=400&h=240&fit=crop&auto=format',
    category: 'Python',
    author: '博主',
    date: '2026-04-10',
    views: 2567,
    likes: 156
  },
  {
    id: 3,
    title: 'Vue3 组合式 API 最佳实践',
    summary: '深入理解响应式原理，掌握组合式函数与 Pinia 状态管理。',
    cover: 'https://images.unsplash.com/photo-1581276879432-15e50529f34b?w=400&h=240&fit=crop&auto=format',
    category: '前端',
    author: '博主',
    date: '2026-03-28',
    views: 982,
    likes: 67
  }
])

// 热门文章
const hotArticles = ref([
  { id: 1, title: 'FastAPI + Vue3 全栈开发实战', views: 1234 },
  { id: 2, title: 'Python 代码生成器：一键生成 Model 与 DAO', views: 2567 },
  { id: 3, title: 'Vue3 组合式 API 最佳实践', views: 982 },
  { id: 4, title: 'MySQL 索引优化指南', views: 876 },
  { id: 5, title: 'Git 团队协作规范', views: 654 }
])

// 标签
const tags = ref(['Python', 'FastAPI', 'Vue3', 'MySQL', 'Docker', 'Git', 'AI', 'JavaScript'])

const startExplore = () => {
  router.push('/articles')
}

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}
</script>

<style scoped>
.home-page {
  max-width: 1280px;
  margin: 0 auto;
}

/* ========== 欢迎横幅 ========== */
.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(0, 206, 201, 0.1) 100%);
  border-radius: 32px;
  padding: 32px 40px;
  margin-bottom: 40px;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.hero-content {
  flex: 1;
}
.hero-title {
  font-size: 42px;
  font-weight: 700;
  background: linear-gradient(135deg, #1a3b3a, #2c5e5e);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 12px;
}
.hero-subtitle {
  font-size: 18px;
  color: #4a6a6a;
  margin-bottom: 28px;
}
.hero-decoration {
  width: 200px;
  height: 200px;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1);
}
.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ========== 主体布局 ========== */
.home-main {
  display: flex;
  gap: 30px;
}

.article-list {
  flex: 1;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.section-title {
  font-size: 24px;
  font-weight: 650;
  color: #1e3a3a;
}
.more-link {
  color: #2ecc71;
  text-decoration: none;
  font-weight: 500;
}
.more-link:hover {
  text-decoration: underline;
}

/* ========== 文章卡片 ========== */
.article-card {
  border-radius: 24px;
  overflow: hidden;
  margin-bottom: 24px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
}
.article-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.08);
}

.card-cover {
  position: relative;
  height: 160px;
  overflow: hidden;
}
.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.article-card:hover .card-cover img {
  transform: scale(1.05);
}

.category-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  color: white;
  padding: 4px 12px;
  border-radius: 40px;
  font-size: 12px;
  font-weight: 500;
}

.card-body {
  padding: 18px 16px;
}

.article-title {
  font-size: 18px;
  font-weight: 650;
  color: #1e2b3a;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  color: #5f7a7a;
  font-size: 14px;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  color: #7a8a9a;
  margin-bottom: 12px;
}
.article-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #7a8a9a;
}
.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ========== 侧边栏 ========== */
.sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card,
.hot-card,
.tags-card {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(8px);
  border: none;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
}
.profile-info h4 {
  margin: 0 0 4px;
  color: #1e2b3a;
}
.profile-info p {
  margin: 0;
  font-size: 13px;
  color: #6c7a89;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
}
.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e2b3a;
}
.stat-label {
  font-size: 13px;
  color: #6c7a89;
}

.card-header-title {
  font-weight: 600;
  color: #1e2b3a;
}

.hot-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.hot-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: color 0.2s;
}
.hot-list li:hover {
  color: #2ecc71;
}
.hot-list li:last-child {
  border-bottom: none;
}
.hot-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.hot-views {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #7a8a9a;
  margin-left: 12px;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.tag-item {
  cursor: pointer;
  background: rgba(46, 204, 113, 0.08);
  border-color: transparent;
  color: #1e3a3a;
  transition: all 0.2s;
}
.tag-item:hover {
  background: #2ecc71;
  color: white;
}

/* ========== 响应式 ========== */
@media (max-width: 900px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }
  .hero-decoration {
    margin-top: 24px;
  }
  .home-main {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
  }
}
</style>
