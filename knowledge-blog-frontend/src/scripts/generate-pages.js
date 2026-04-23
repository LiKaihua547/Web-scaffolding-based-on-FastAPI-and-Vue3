// scripts/generate-pages.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// 获取当前文件的目录路径 (ESM 下 __dirname 替代)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== 配置区域 ==========
const VIEWS_DIR = path.resolve(__dirname, '../views');      // views 根目录
const FRONT_DIR = path.join(VIEWS_DIR, 'front');                // 前台页面目录
const ADMIN_DIR = path.join(VIEWS_DIR, 'admin');                // 后台页面目录

// 要生成的页面配置
const PAGES = [
  { name: 'Forum', type: 'front' },
  { name: 'Diary', type: 'front' },
  { name: 'Learn', type: 'front' },
  { name: 'Entertain', type: 'front' },
  { name: 'AI', type: 'front', routePath: 'ai' },
  { name: 'Profile', type: 'front' },
  // 后台页面示例
  // { name: 'Users', type: 'admin' },
  // { name: 'Comments', type: 'admin' },
];

// ========== 模板 ==========
const getVueTemplate = (pageName) => `<template>
  <div class="${pageName.toLowerCase()}-page">
    <h1>${pageName} 页面</h1>
    <p>这里是 ${pageName} 页面的内容，待开发...</p>
  </div>
</template>

<script setup>
// ${pageName} 页面逻辑
</script>

<style scoped>
.${pageName.toLowerCase()}-page {
  padding: 20px;
}
</style>
`;

// ========== 确保目录存在 ==========
if (!fs.existsSync(FRONT_DIR)) fs.mkdirSync(FRONT_DIR, { recursive: true });
if (!fs.existsSync(ADMIN_DIR)) fs.mkdirSync(ADMIN_DIR, { recursive: true });

// ========== 生成文件并收集路由信息 ==========
const imports = [];
const frontRoutes = [];
const adminRoutes = [];

PAGES.forEach(({ name, type, routePath }) => {
  const dir = type === 'front' ? FRONT_DIR : ADMIN_DIR;
  const filePath = path.join(dir, `${name}.vue`);

  // 生成 Vue 文件（如果不存在则创建）
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, getVueTemplate(name), 'utf-8');
    console.log(`✅ 已生成：${filePath}`);
  } else {
    console.log(`⏭️ 跳过已存在：${filePath}`);
  }

  // 收集路由信息
  const importName = name;
  const componentPath = `@/views/${type}/${name}.vue`;
  const pathName = routePath || name.toLowerCase();

  imports.push(`import ${importName} from '${componentPath}'`);

  if (type === 'front') {
    frontRoutes.push(`      { path: '${pathName}', name: '${importName}', component: ${importName} },`);
  } else {
    adminRoutes.push(`      { path: '${pathName}', name: '${importName}', component: ${importName} },`);
  }
});

// ========== 输出路由代码 ==========
console.log('\n\n========== 请将以下代码复制到 router/index.js 中 ==========\n');

// 输出导入语句
console.log('// 自动生成的页面导入');
imports.forEach(imp => console.log(imp));
console.log('');

// 输出前台路由
if (frontRoutes.length > 0) {
  console.log('// 前台路由 children 中添加：');
  frontRoutes.forEach(r => console.log(r));
  console.log('');
}

// 输出后台路由
if (adminRoutes.length > 0) {
  console.log('// 后台路由 children 中添加：');
  adminRoutes.forEach(r => console.log(r));
  console.log('');
}

console.log('========== 复制结束 ==========\n');
