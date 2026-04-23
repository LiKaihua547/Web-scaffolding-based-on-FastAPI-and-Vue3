// src/api/article.js
import request from '@/utils/request'

/**
 * 获取文章列表
 * @param {Object} params - 查询参数，例如 { page: 1, size: 10 }
 */
export function getArticles(params) {
  return request({
    url: '/articles',
    method: 'get',
    params
  })
}

/**
 * 获取文章详情
 * @param {string} slug - 文章的 slug
 */
export function getArticle(slug) {
  return request({
    url: `/articles/${slug}`,
    method: 'get'
  })
}

// 后续可以继续添加创建、更新、删除文章的 API
