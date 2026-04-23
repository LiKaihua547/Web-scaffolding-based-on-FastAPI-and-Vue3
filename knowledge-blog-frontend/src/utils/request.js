// src/utils/request.js
import axios from 'axios'

// 创建 Axios 实例
// 1. baseURL 从环境变量读取，实现开发/生产环境自动切换[reference:10]
// 2. timeout 设置请求超时时间[reference:11]
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 50000 // 请求超时时间
})

// ----- 请求拦截器 -----
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么：例如，从 Pinia 或 localStorage 获取 token 并添加到 header
    // 暂时留空，后续集成用户认证时再补充
    return config
  },
  error => {
    // 对请求错误做些什么
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// ----- 响应拦截器 -----
service.interceptors.response.use(
  response => {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么，这里直接返回后端定义的 data 部分
    const res = response.data
    // 可以根据后端约定的数据结构，在这里做统一的判断
    return res
  },
  error => {
    // 超出 2xx 范围的状态码都会触发该函数。
    console.error('响应错误:', error)
    // 对响应错误做点什么，比如根据状态码进行统一的错误提示或跳转登录页[reference:12]
    return Promise.reject(error)
  }
)

export default service
