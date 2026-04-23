<template>
  <div class="register-page">
    <!-- 背景装饰圆 -->
    <div class="bg-circle bg-circle-1"></div>
    <div class="bg-circle bg-circle-2"></div>
    <div class="bg-circle bg-circle-3"></div>

    <!-- 居中注册卡片 -->
    <el-card class="register-card" shadow="always">
      <!-- 卡片头部：品牌 + 图片示意 -->
      <div class="card-header">
        <div class="brand-area">
          <h1 class="brand-title">📘 知识博客</h1>
          <p class="brand-desc">记录思考 · 分享见解 · 连接同好</p>
        </div>
        <div class="image-area">
          <img
            src="https://images.unsplash.com/photo-1512314889357-e157c22f938d?w=400&auto=format&fit=crop"
            alt="Writing notes"
            class="header-illustration"
          />
        </div>
      </div>

      <!-- 表单标题 -->
      <h2 class="form-title">创建你的账号</h2>
      <p class="form-subtitle">填写以下信息，开启知识之旅</p>

      <!-- 注册表单 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent
      >
        <!-- 第一行：用户名 + 昵称 -->
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
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
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="昵称" prop="nickname">
              <el-input
                v-model="form.nickname"
                placeholder="如何称呼你？"
                prefix-icon="UserFilled"
                clearable
                size="large"
                class="custom-input"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第二行：密码 + 确认密码 -->
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="至少6位"
                prefix-icon="Lock"
                show-password
                clearable
                size="large"
                class="custom-input"
              />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                placeholder="再次输入"
                prefix-icon="Lock"
                show-password
                clearable
                size="large"
                class="custom-input"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 第三行：邮箱 + 手机号 -->
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="form.email"
                placeholder="your@email.com"
                prefix-icon="Message"
                clearable
                size="large"
                class="custom-input"
              />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="手机号" prop="phone">
              <el-input
                v-model="form.phone"
                placeholder="选填"
                prefix-icon="Phone"
                clearable
                size="large"
                class="custom-input"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 头像链接 -->
        <el-form-item label="头像链接" prop="avatar">
          <el-input
            v-model="form.avatar"
            placeholder="可留空，后续上传"
            prefix-icon="Picture"
            clearable
            size="large"
            class="custom-input"
          />
        </el-form-item>

        <!-- 地址 -->
        <el-form-item label="地址" prop="address">
          <el-input
            v-model="form.address"
            placeholder="选填"
            prefix-icon="Location"
            clearable
            size="large"
            class="custom-input"
          />
        </el-form-item>

        <!-- 个人简介 -->
        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="form.bio"
            type="textarea"
            :rows="2"
            placeholder="简单介绍一下自己吧..."
            maxlength="200"
            show-word-limit
            class="custom-textarea"
          />
        </el-form-item>

        <!-- 注册按钮 -->
        <el-button
          type="success"
          size="large"
          :loading="loading"
          @click="handleRegister"
          class="register-btn"
          round
        >
          立即注册
        </el-button>

        <!-- 跳转登录 -->
        <div class="login-link">
          已有账号？
          <router-link to="/login">去登录</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '1',
  password: '111111',
  confirmPassword: '111111',
  email: '1@qq.com',
  phone: '18788889999',
  avatar: '1',
  address: '1',
  nickname: '1',
  bio: '1',
  is_active: 1,
  is_superuser: 0,
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
  email: [
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
  ],
}

const handleRegister = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      // 深拷贝并清理数据
      const submitData = {
        username: form.username,
        password: form.password,
        email: form.email || undefined,
        phone: form.phone || undefined,
        avatar: form.avatar || undefined,
        address: form.address || undefined,
        nickname: form.nickname || undefined,
        bio: form.bio || undefined,
        is_active: 1,            // 整数
        is_superuser: 0,         // 整数
      }
      // 删除 undefined 字段，避免传递 null 导致类型错误
      Object.keys(submitData).forEach(key => submitData[key] === undefined && delete submitData[key])

      const res = await register(submitData)
      if (res.code === 200) {
        ElMessage.success('注册成功！即将跳转登录页')
        setTimeout(() => router.push('/login'), 1500)
      } else {
        ElMessage.error(res.msg || '注册失败')
      }
    } catch (error) {
      ElMessage.error('网络错误，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* 整体页面背景：柔和渐变 + 装饰圆 */
.register-page {
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

/* 注册卡片：居中、大圆角、柔和阴影 */
.register-card {
  width: 100%;
  max-width: 780px;
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

/* 卡片头部：品牌文字 + 小图 */
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
  width: 100px;
  height: 100px;
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

/* 输入框自定义圆角 */
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
.custom-textarea :deep(.el-textarea__inner) {
  border-radius: 30px;
  border: 1px solid #e2eef2;
  padding: 12px 18px;
}
.custom-textarea :deep(.el-textarea__inner:hover) {
  border-color: #b0d3da;
}
.custom-textarea :deep(.el-textarea__inner:focus) {
  border-color: #2ecc71;
  box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.1);
}

/* 注册按钮 */
.register-btn {
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
.register-btn:hover {
  background-color: #27ae60;
  border-color: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(46, 204, 113, 0.25);
}

/* 登录链接 */
.login-link {
  text-align: center;
  margin-top: 22px;
  color: #547878;
  font-size: 15px;
}
.login-link a {
  color: #2ecc71;
  font-weight: 600;
  text-decoration: none;
  margin-left: 6px;
}
.login-link a:hover {
  text-decoration: underline;
}

/* 移动端适配 */
@media (max-width: 600px) {
  .register-card {
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
