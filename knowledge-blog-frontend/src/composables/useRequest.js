// src/composables/useRequest.js
import { ref, unref } from 'vue'

export function useRequest(apiFunc, options = {}) {
  const { immediate = false } = options

  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const execute = async (...args) => {
    loading.value = true
    error.value = null
    try {
      const res = await apiFunc(...args)
      data.value = res
      return res
    } catch (err) {
      error.value = err
      console.error('请求失败:', err)
    } finally {
      loading.value = false
    }
  }

  if (immediate) {
    execute()
  }

  return {
    data,
    loading,
    error,
    execute
  }
}
