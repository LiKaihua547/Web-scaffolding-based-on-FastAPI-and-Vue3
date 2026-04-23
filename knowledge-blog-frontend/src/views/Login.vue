<template>
  <div class="login-page">
    <!-- 背景装饰圆 -->
    <div class="bg-circle bg-circle-1"></div>
    <div class="bg-circle bg-circle-2"></div>
    <div class="bg-circle bg-circle-3"></div>

    <!-- 居中登录卡片 -->
    <el-card class="login-card" shadow="always">
      <!-- 头部品牌 -->
      <div class="card-header">
        <div class="brand-area">
          <h1 class="brand-title">📘 知识博客</h1>
          <p class="brand-desc">欢迎回来，继续你的知识旅程</p>
        </div>
        <div class="image-area">
          <img
            src="https://images.unsplash.com/photo-1512314889357-e157c22f938d?w=400&auto=format&fit=crop"
            alt="Login illustration"
            class="header-illustration"
          />
        </div>
      </div>

      <h2 class="form-title">登录账号</h2>
      <p class="form-subtitle">使用已注册的账号登录</p>

      <!-- 登录表单 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            clearable
            size="large"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
            size="large"
            class="custom-input"
          />
        </el-form-item>

        <!-- 登录按钮 -->
        <el-button
          type="success"
          size="large"
          :loading="loading"
          @click="handleLogin"
          class="login-btn"
          round
        >
          立即登录
        </el-button>

        <!-- 跳转注册 -->
        <div class="register-link">
          还没有账号？
          <router-link to="/register">去注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const formRef = ref(null)
const loading = ref(false)

// 表单数据，预填测试账号（方便你快速登录）
const form = reactive({
  username: '1',
  password: '111111',
})

// 表单校验规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
}

const handleLogin = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await login({ username: form.username, password: form.password })
      if (res.code === 200 && res.data) {
        const { token, user } = res.data
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
        ElMessage.success('登录成功')
        if (user.is_superuser) {
          router.push('/admin')
        } else {
          const redirect = route.query.redirect || '/'
          router.push(redirect)
        }
      } else {
        ElMessage.error(res.msg || '登录失败')
      }
    } catch (error) {
      ElMessage.error('网络错误')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* 页面背景：与注册页一致的柔和渐变 */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px 20px;
  background: linear-gradient(135deg, #e0f2e9 0%, #d1e9f5 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰圆 */
.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(5px);
  z-index: 0;
}
.bg-circle-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  left: -80px;
}
.bg-circle-2 {
  width: 300px;
  height: 300px;
  bottom: -60px;
  right: -40px;
  background: rgba(255, 255, 255, 0.2);
}
.bg-circle-3 {
  width: 200px;
  height: 200px;
  top: 40%;
  right: 10%;
  background: rgba(255, 255, 255, 0.15);
}

/* 登录卡片：大圆角、毛玻璃效果 */
.login-card {
  width: 100%;
  max-width: 480px;
  border-radius: 48px;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  box-shadow: 0 30px 50px -15px rgba(0, 20, 30, 0.2);
  border: none;
  padding: 30px 35px;
  position: relative;
  z-index: 10;
  transition: all 0.3s ease;
}

:deep(.el-card__body) {
  padding: 0;
}

/* 头部品牌区 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
}
.brand-area {
  flex: 1;
}
.brand-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a3b3a;
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}
.brand-desc {
  color: #4a6a6a;
  font-size: 15px;
  font-weight: 400;
}
.image-area {
  width: 80px;
  height: 80px;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.08);
  background: #f5fafc;
}
.header-illustration {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 表单标题 */
.form-title {
  font-size: 24px;
  font-weight: 650;
  color: #1e3a3a;
  margin-bottom: 5px;
}
.form-subtitle {
  color: #5f7a7a;
  font-size: 14px;
  margin-bottom: 28px;
}

/* 输入框圆角 */
.custom-input :deep(.el-input__wrapper) {
  border-radius: 40px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  border: 1px solid #e2eef2;
  transition: all 0.2s;
}
.custom-input :deep(.el-input__wrapper:hover) {
  border-color: #b0d3da;
}
.custom-input :deep(.el-input__wrapper.is-focus) {
  border-color: #2ecc71;
  box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.1);
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  height: 50px;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-top: 12px;
  background-color: #2ecc71;
  border-color: #2ecc71;
  border-radius: 60px;
  transition: all 0.25s;
}
.login-btn:hover {
  background-color: #27ae60;
  border-color: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(46, 204, 113, 0.25);
}

/* 注册链接 */
.register-link {
  text-align: center;
  margin-top: 22px;
  color: #547878;
  font-size: 15px;
}
.register-link a {
  color: #2ecc71;
  font-weight: 600;
  text-decoration: none;
  margin-left: 6px;
}
.register-link a:hover {
  text-decoration: underline;
}

/* 移动端适配 */
@media (max-width: 600px) {
  .login-card {
    padding: 20px 18px;
    border-radius: 36px;
  }
  .card-header {
    flex-direction: column;
    text-align: center;
  }
  .image-area {
    margin-top: 15px;
  }
  .brand-title {
    font-size: 28px;
  }
}
</style>
