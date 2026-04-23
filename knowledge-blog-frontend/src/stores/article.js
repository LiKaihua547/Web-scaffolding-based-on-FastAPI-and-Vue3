// src/stores/article.js
import { defineStore } from 'pinia'
import { getArticles, getArticle } from '@/api/article'

export const useArticleStore = defineStore('article', {
  state: () => ({
    list: [], // 文章列表
    current: null, // 当前查看文章详情
    loading: false
  }),

  actions: {
    async fetchArticles(params) {
      this.loading = true
      try {
        const res = await getArticles(params)
        this.list = res.data
        return res
      } catch (error) {
        console.error('获取文章列表失败:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchArticle(slug) {
      this.loading = true
      try {
        const res = await getArticle(slug)
        this.current = res.data
        return res
      } catch (error) {
        console.error('获取文章详情失败:', error)
      } finally {
        this.loading = false
      }
    }
  },
  // 开启持久化，刷新页面数据不丢失[reference:15]
  persist: {
    key: 'article-store',
    storage: localStorage,
    // 可选：只持久化指定的 state
    paths: ['list']
  }
})
