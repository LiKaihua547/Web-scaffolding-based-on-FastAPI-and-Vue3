import request from '@/utils/request'

// 启动 AI 服务
export function ai_start() {
  return request({
    url: '/ai/start',
    method: 'get',
  })
}

// 获取 AI 状态 (可选，用于页面初始化时判断服务是否已启动)
export function ai_status() {
  return request({
    url: '/ai/status',
    method: 'get',
  })
}

// 发送对话消息
export function ai_chat(data) {
  return request({
    url: '/ai/chat',
    method: 'post',
    data: data
  })
}
