<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <el-header class="top-bar">
      <div class="logo-title">
        <img src="/logo.png" alt="logo" class="logo" />
        <span class="title">青浦区农业数据可视化平台</span>
      </div>

      <el-menu
        class="top-menu"
        mode="horizontal"
        :default-active="activeIndex"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#409EFF"
        @select="handleSelect"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/health-organization">农村卫生组织</el-menu-item>
        <el-menu-item index="/main-index">农村主要指标</el-menu-item>
        <el-menu-item index="/rural-organization">农村基层组织</el-menu-item>
        <el-menu-item index="/tech-application">农业技术应用</el-menu-item>
        <el-menu-item index="/total-value">农业历年总产值</el-menu-item>
        <el-menu-item index="/total-agriculture">农业总产值概况</el-menu-item>
        <el-menu-item index="/agent-page">AI助手</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 内容区域 -->
    <el-main class="main-content">
      <router-view></router-view>
    </el-main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const activeIndex = ref(route.path)

// 每次路由变动，更新菜单高亮
watch(
  () => route.path,
  (newPath) => {
    activeIndex.value = newPath
  }
)

const handleSelect = (key) => {
  router.push(key)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #f0f2f5;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #001529;
  padding: 0 20px;
  height: 64px;
}

.logo-title {
  display: flex;
  align-items: center;
}

.logo {
  width: 40px;
  height: 40px;
}

.title {
  font-size: 20px;
  color: #fff;
  margin-left: 15px;
  font-weight: bold;
}

.top-menu {
  flex-grow: 1;
  margin-left: 50px;
  border-bottom: none;
}

.main-content {
  padding: 30px;
}
</style>
