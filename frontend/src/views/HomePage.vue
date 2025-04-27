<template>
  <AppLayout>
    <div class="home-page">
      <h2>农业数据综合分析平台</h2>
      
      <!-- 欢迎卡片 -->
      <el-card class="welcome-card" shadow="hover">
        <div class="welcome-content">
          <h3>欢迎使用农业数据综合分析平台</h3>
          <p>本平台提供全面的农业数据分析和可视化服务，助力农业发展决策</p>
          <div class="welcome-stats">
            <div class="stat-item">
              <div class="stat-num">6</div>
              <div class="stat-label">数据模块</div>
            </div>
            <div class="stat-item">
              <div class="stat-num">12</div>
              <div class="stat-label">图表类型</div>
            </div>
            <div class="stat-item">
              <div class="stat-num">100+</div>
              <div class="stat-label">数据指标</div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 数据概览卡片 -->
      <div class="overview-cards">
        <el-card shadow="hover" v-for="stat in stats" :key="stat.title" class="stat-card">
          <router-link :to="stat.route" class="stat-link">
            <div class="stat-icon">
              <i :class="stat.icon"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-trend" :class="stat.trend">
                <i :class="stat.trendIcon"></i>
                {{ stat.trendText }}
              </div>
            </div>
          </router-link>
        </el-card>
      </div>

      <!-- 主要图表区域 -->
      <div class="chart-container">
        <!-- 农业总产值趋势 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>农业总产值趋势</span>
              <div class="chart-actions">
                <el-select v-model="valueTimeRange" size="small" style="width: 120px; margin-right: 10px">
                  <el-option label="近5年" value="5"></el-option>
                  <el-option label="近3年" value="3"></el-option>
                  <el-option label="近1年" value="1"></el-option>
                </el-select>
                <router-link to="/total-value" class="more-link">查看更多</router-link>
              </div>
            </div>
          </template>
          <div class="chart-wrapper">
            <line-chart
              v-if="totalValueData"
              :chart-data="totalValueData"
              :options="totalValueOptions"
            />
          </div>
        </el-card>

        <!-- 技术应用分布 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>技术应用分布</span>
              <div class="chart-actions">
                <el-radio-group v-model="techViewType" size="small">
                  <el-radio-button label="area">面积</el-radio-button>
                  <el-radio-button label="count">数量</el-radio-button>
                </el-radio-group>
                <router-link to="/tech-application" class="more-link" style="margin-left: 10px">查看更多</router-link>
              </div>
            </div>
          </template>
          <div class="chart-wrapper">
            <pie-chart
              v-if="techDistributionData"
              :chart-data="techDistributionData"
              :options="techDistributionOptions"
            />
          </div>
        </el-card>
      </div>

      <!-- 第二行图表 -->
      <div class="chart-container">
        <!-- 农村基层组织分布 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>农村基层组织分布</span>
              <router-link to="/rural-organization" class="more-link">查看更多</router-link>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              v-if="ruralOrgData"
              :chart-data="ruralOrgData"
              :options="ruralOrgOptions"
            />
          </div>
        </el-card>

        <!-- 卫生组织覆盖率 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>卫生组织覆盖率</span>
              <router-link to="/health-organization" class="more-link">查看更多</router-link>
            </div>
          </template>
          <div class="chart-wrapper health-coverage">
            <div v-for="item in healthCoverage" :key="item.region" class="coverage-item">
              <el-progress
                type="dashboard"
                :percentage="item.coverage"
                :color="item.color"
              >
                <template #default="{ percentage }">
                  <div class="progress-content">
                    <div class="progress-value">{{ percentage }}%</div>
                    <div class="progress-label">{{ item.region }}</div>
                  </div>
                </template>
              </el-progress>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 快速访问区域 -->
      <div class="quick-access">
        <el-card shadow="hover" class="quick-access-card">
          <template #header>
            <div class="card-header">
              <span>快速访问</span>
              <el-radio-group v-model="quickLinkLayout" size="small">
                <el-radio-button label="grid">网格</el-radio-button>
                <el-radio-button label="list">列表</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="quick-links" :class="quickLinkLayout">
            <router-link v-for="link in quickLinks" 
                        :key="link.route" 
                        :to="link.route" 
                        class="quick-link-item">
              <el-button type="primary" plain>
                <i :class="link.icon"></i>
                {{ link.title }}
                <span class="link-desc" v-if="quickLinkLayout === 'list'">{{ link.description }}</span>
              </el-button>
            </router-link>
          </div>
        </el-card>
      </div>

      <!-- 最新动态 -->
      <el-card shadow="hover" class="updates-card">
        <template #header>
          <div class="card-header">
            <span>最新动态</span>
            <el-button type="text">查看全部</el-button>
          </div>
        </template>
        <div class="updates-list">
          <div v-for="update in latestUpdates" :key="update.id" class="update-item">
            <div class="update-icon">
              <i :class="update.icon"></i>
            </div>
            <div class="update-content">
              <div class="update-title">{{ update.title }}</div>
              <div class="update-time">{{ update.time }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/components/AppLayout.vue'
import { LineChart, PieChart, BarChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

// 控制变量
const valueTimeRange = ref('5')
const techViewType = ref('area')
const quickLinkLayout = ref('grid')

// 统计数据
const stats = ref([
  {
    title: '农业总产值',
    value: '23.5亿元',
    icon: 'el-icon-money',
    route: '/total-value',
    trend: 'up',
    trendIcon: 'el-icon-top',
    trendText: '同比增长8.2%'
  },
  {
    title: '技术应用面积',
    value: '15,000亩',
    icon: 'el-icon-monitor',
    route: '/tech-application',
    trend: 'up',
    trendIcon: 'el-icon-top',
    trendText: '同比增长5.8%'
  },
  {
    title: '卫生组织数量',
    value: '156个',
    icon: 'el-icon-first-aid-kit',
    route: '/health-organization',
    trend: 'stable',
    trendIcon: 'el-icon-right',
    trendText: '较上月持平'
  },
  {
    title: '基层组织数量',
    value: '89个',
    icon: 'el-icon-office-building',
    route: '/rural-organization',
    trend: 'up',
    trendIcon: 'el-icon-top',
    trendText: '新增3个'
  }
])

// 快速访问链接
const quickLinks = ref([
  { 
    title: '农业总产值', 
    route: '/total-value', 
    icon: 'el-icon-money',
    description: '查看历年农业总产值数据及分析'
  },
  { 
    title: '技术应用', 
    route: '/tech-application', 
    icon: 'el-icon-monitor',
    description: '农业技术应用情况统计与分析'
  },
  { 
    title: '卫生组织', 
    route: '/health-organization', 
    icon: 'el-icon-first-aid-kit',
    description: '农村卫生组织分布与覆盖情况'
  },
  { 
    title: '基层组织', 
    route: '/rural-organization', 
    icon: 'el-icon-office-building',
    description: '农村基层组织建设情况'
  },
  { 
    title: '主要指标', 
    route: '/main-index', 
    icon: 'el-icon-data-line',
    description: '农业发展主要指标监测'
  },
  { 
    title: '农业概况', 
    route: '/total-agriculture', 
    icon: 'el-icon-crop',
    description: '农业发展整体概况分析'
  }
])

// 最新动态
const latestUpdates = ref([
  {
    id: 1,
    title: '2023年农业总产值统计数据已更新',
    time: '2024-01-15',
    icon: 'el-icon-refresh'
  },
  {
    id: 2,
    title: '新增3个农村基层组织',
    time: '2024-01-12',
    icon: 'el-icon-plus'
  },
  {
    id: 3,
    title: '技术应用覆盖率达到新高',
    time: '2024-01-10',
    icon: 'el-icon-top'
  },
  {
    id: 4,
    title: '农村卫生组织建设完成年度目标',
    time: '2024-01-08',
    icon: 'el-icon-check'
  }
])

// 卫生组织覆盖率数据
const healthCoverage = ref([
  { region: '东部', coverage: 95, color: '#67C23A' },
  { region: '中部', coverage: 85, color: '#E6A23C' },
  { region: '西部', coverage: 75, color: '#F56C6C' }
])

// 图表数据
const totalValueData = ref({
  labels: ['2019', '2020', '2021', '2022', '2023'],
  datasets: [{
    label: '农业总产值(亿元)',
    data: [18.5, 19.8, 21.2, 22.4, 23.5],
    borderColor: '#409EFF',
    tension: 0.4,
    fill: true,
    backgroundColor: 'rgba(64, 158, 255, 0.1)'
  }]
})

const totalValueOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        display: true,
        drawBorder: false
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}

const techDistributionData = computed(() => ({
  labels: ['种植业', '林业', '牧业', '渔业'],
  datasets: [{
    data: techViewType.value === 'area' ? [40, 25, 20, 15] : [45, 20, 25, 10],
    backgroundColor: ['#67C23A', '#409EFF', '#E6A23C', '#F56C6C']
  }]
}))

const techDistributionOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'right'
    }
  }
}

const ruralOrgData = ref({
  labels: ['村委会', '合作社', '农民协会', '其他组织'],
  datasets: [{
    label: '组织数量',
    data: [45, 28, 15, 12],
    backgroundColor: ['#409EFF', '#67C23A', '#E6A23C', '#909399']
  }]
})

const ruralOrgOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        display: true,
        drawBorder: false
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}

// 获取实时数据
onMounted(async () => {
  try {
    // 这里可以添加实际的API调用来获取数据
    // const response = await fetch('your-api-endpoint')
    // const data = await response.json()
    // 更新stats和图表数据
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})
</script>

<style scoped>
.home-page {
  background: #fff;
  padding: 20px;
  border-radius: 6px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.welcome-card {
  margin-bottom: 30px;
  background: linear-gradient(135deg, #409EFF 0%, #36D1DC 100%);
  color: white;
}

.welcome-content {
  text-align: center;
  padding: 20px;
}

.welcome-content h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.welcome-stats {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-num {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  font-size: 40px;
  margin-right: 15px;
  color: #409EFF;
}

.stat-info {
  flex-grow: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.stat-trend.stable {
  color: #909399;
}

.chart-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  height: 400px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-actions {
  display: flex;
  align-items: center;
}

.more-link {
  font-size: 14px;
  color: #409EFF;
  text-decoration: none;
}

.chart-wrapper {
  height: calc(100% - 60px);
  position: relative;
  padding: 10px;
}

.health-coverage {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.progress-content {
  text-align: center;
}

.progress-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.progress-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.quick-access-card {
  margin-bottom: 20px;
}

.quick-links {
  display: grid;
  gap: 15px;
  padding: 10px;
}

.quick-links.grid {
  grid-template-columns: repeat(3, 1fr);
}

.quick-links.list {
  grid-template-columns: 1fr;
}

.quick-link-item {
  text-decoration: none;
}

.quick-link-item .el-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 15px;
}

.quick-link-item i {
  margin-right: 10px;
  font-size: 20px;
}

.link-desc {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}

.updates-card {
  margin-bottom: 20px;
}

.updates-list {
  display: grid;
  gap: 15px;
}

.update-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #EBEEF5;
}

.update-icon {
  font-size: 24px;
  color: #409EFF;
  margin-right: 15px;
}

.update-content {
  flex-grow: 1;
}

.update-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 5px;
}

.update-time {
  font-size: 12px;
  color: #909399;
}

@media (max-width: 1200px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-container {
    grid-template-columns: 1fr;
  }

  .quick-links.grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .welcome-stats {
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }

  .quick-links.grid {
    grid-template-columns: 1fr;
  }

  .welcome-stats {
    flex-direction: column;
    gap: 15px;
  }

  .health-coverage {
    flex-direction: column;
    gap: 20px;
  }
}
</style>
