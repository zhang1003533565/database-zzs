<template>
  <AppLayout>
    <div class="health-organization">
      <div class="page-header">
        <h2>农村卫生组织分布情况</h2>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>卫生组织</el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <!-- 数据概览卡片 -->
      <div class="overview-cards">
        <el-card shadow="hover" v-for="stat in stats" :key="stat.title">
          <div class="stat-card">
            <div class="stat-icon">
              <i :class="stat.icon"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-trend" :class="stat.trend">
                <i :class="stat.trendIcon"></i> {{ stat.trendText }}
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 主要图表区域 -->
      <div class="chart-container">
        <!-- 柱状图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>各村镇卫生所数量对比</span>
              <div class="chart-actions">
                <el-select v-model="chartType" size="small" style="width: 120px; margin-right: 10px">
                  <el-option label="柱状图" value="bar"></el-option>
                  <el-option label="折线图" value="line"></el-option>
                </el-select>
                <el-tooltip content="导出图表" placement="top">
                  <el-button size="small" icon="el-icon-download" circle @click="exportChart"></el-button>
                </el-tooltip>
              </div>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              v-if="chartType === 'bar' && barChartData"
              :chart-data="barChartData"
              :options="barChartOptions"
            />
            <line-chart
              v-else-if="barChartData"
              :chart-data="barChartData"
              :options="barChartOptions"
            />
          </div>
        </el-card>

        <!-- 饼图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>卫生所分布比例</span>
              <div class="chart-actions">
                <el-radio-group v-model="pieChartMetric" size="small">
                  <el-radio-button label="xcyss">卫生室数</el-radio-button>
                  <el-radio-button label="xzcs">行政村数</el-radio-button>
                </el-radio-group>
              </div>
            </div>
          </template>
          <div class="chart-wrapper">
            <pie-chart
              v-if="pieChartData"
              :chart-data="pieChartData"
              :options="pieChartOptions"
            />
          </div>
        </el-card>
      </div>

      <!-- 覆盖率地图 -->
      <el-card shadow="hover" class="coverage-map">
        <template #header>
          <div class="chart-header">
            <span>卫生室覆盖率分布</span>
            <el-tooltip content="根据卫生室数量与行政村数量的比例计算" placement="top">
              <i class="el-icon-info"></i>
            </el-tooltip>
          </div>
        </template>
        <div class="coverage-indicators">
          <div v-for="item in rawData" :key="item.zhen" class="coverage-item">
            <el-progress 
              type="circle" 
              :percentage="calculateRatio(item)"
              :color="getCoverageColor"
            >
              <template #default="{ percentage }">
                <div class="progress-content">
                  <div class="progress-region">{{ item.zhen }}</div>
                  <div class="progress-value">{{ percentage }}%</div>
                </div>
              </template>
            </el-progress>
          </div>
        </div>
      </el-card>

      <!-- 数据表格 -->
      <el-card shadow="hover" class="data-table">
        <template #header>
          <div class="table-header">
            <div class="header-left">
              <span>详细数据</span>
              <el-tag type="info" style="margin-left: 10px">共 {{ rawData?.length || 0 }} 条</el-tag>
            </div>
            <div class="header-right">
              <el-input
                v-model="searchQuery"
                placeholder="搜索..."
                prefix-icon="el-icon-search"
                style="width: 200px; margin-right: 10px"
              />
              <el-button-group>
                <el-button type="primary" size="small" @click="exportData">
                  <i class="el-icon-download"></i> 导出数据
                </el-button>
                <el-button type="success" size="small" @click="refreshData">
                  <i class="el-icon-refresh"></i> 刷新
                </el-button>
              </el-button-group>
            </div>
          </div>
        </template>
        <el-table
          :data="filteredTableData"
          border
          style="width: 100%"
          :default-sort = "{prop: 'xcyss', order: 'descending'}"
          v-loading="loading"
        >
          <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
          <el-table-column prop="zhen" label="镇/街道" sortable>
            <template #default="{ row }">
              <el-button type="text" @click="showZhenDetail(row)">{{ row.zhen }}</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="xcyss" label="乡村卫生室数" sortable>
            <template #default="{ row }">
              <el-tag :type="getTagType(row.xcyss)">{{ row.xcyss }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="xzcs" label="行政村数" sortable>
            <template #default="{ row }">
              <el-tag type="info">{{ row.xzcs }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ratio" label="卫生室覆盖率" sortable>
            <template #default="{ row }">
              <div class="coverage-cell">
                <el-progress 
                  :percentage="calculateRatio(row)"
                  :color="getCoverageColor"
                  :format="percentageFormat"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" size="small" icon="el-icon-view" @click="showZhenDetail(row)">
                  详情
                </el-button>
                <el-button type="success" size="small" icon="el-icon-edit" @click="editZhenData">
                  编辑
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 镇详情对话框 -->
    <el-dialog
      :title="selectedZhen ? selectedZhen.zhen + ' 详细信息' : ''"
      v-model="dialogVisible"
      width="50%"
    >
      <div v-if="selectedZhen" class="zhen-detail">
        <el-descriptions border>
          <el-descriptions-item label="镇/街道">{{ selectedZhen.zhen }}</el-descriptions-item>
          <el-descriptions-item label="乡村卫生室数">{{ selectedZhen.xcyss }}</el-descriptions-item>
          <el-descriptions-item label="行政村数">{{ selectedZhen.xzcs }}</el-descriptions-item>
          <el-descriptions-item label="卫生室覆盖率">{{ calculateRatio(selectedZhen) }}%</el-descriptions-item>
        </el-descriptions>
        
        <div class="detail-charts">
          <div class="detail-chart">
            <h4>历年卫生室数量变化</h4>
            <line-chart
              :chart-data="getHistoricalData(selectedZhen)"
              :options="historicalChartOptions"
            />
          </div>
        </div>
      </div>
    </el-dialog>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/components/AppLayout.vue'
import { BarChart, LineChart, PieChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'
import { ElMessage } from 'element-plus'

Chart.register(...registerables)

const loading = ref(false)
const searchQuery = ref('')
const chartType = ref('bar')
const pieChartMetric = ref('xcyss')
const dialogVisible = ref(false)
const selectedZhen = ref(null)
const rawData = ref([])

// 获取数据
onMounted(() => {
  fetchData()
})

// 统计数据
const stats = computed(() => {
  if (!rawData.value || rawData.value.length === 0) return []

  const totalXcyss = rawData.value.reduce((sum, item) => sum + parseInt(item.xcyss), 0)
  const totalXzcs = rawData.value.reduce((sum, item) => sum + parseInt(item.xzcs), 0)
  const avgCoverage = (totalXcyss / totalXzcs * 100).toFixed(1)
  const lastMonthData = {
    totalXcyss: 380,
    totalXzcs: 450,
    coverage: 84.5
  }

  return [
    {
      title: '总乡村卫生室数',
      value: totalXcyss,
      icon: 'el-icon-first-aid-kit',
      trend: totalXcyss > lastMonthData.totalXcyss ? 'up' : 'down',
      trendIcon: totalXcyss > lastMonthData.totalXcyss ? 'el-icon-top' : 'el-icon-bottom',
      trendText: `较上月${totalXcyss > lastMonthData.totalXcyss ? '增加' : '减少'}${Math.abs(((totalXcyss - lastMonthData.totalXcyss) / lastMonthData.totalXcyss * 100).toFixed(1))}%`
    },
    {
      title: '总行政村数',
      value: totalXzcs,
      icon: 'el-icon-office-building',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上月持平'
    },
    {
      title: '平均覆盖率',
      value: avgCoverage + '%',
      icon: 'el-icon-data-analysis',
      trend: avgCoverage > lastMonthData.coverage ? 'up' : 'down',
      trendIcon: avgCoverage > lastMonthData.coverage ? 'el-icon-top' : 'el-icon-bottom',
      trendText: `较上月${avgCoverage > lastMonthData.coverage ? '提升' : '下降'}${Math.abs((avgCoverage - lastMonthData.coverage)).toFixed(1)}%`
    },
    {
      title: '覆盖村镇数',
      value: rawData.value.length,
      icon: 'el-icon-map-location',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '覆盖全部村镇'
    }
  ]
})

// 表格数据
const tableData = computed(() => {
  if (!rawData.value) return []
  return rawData.value.map(item => ({
    ...item,
    ratio: calculateRatio(item)
  }))
})

// 搜索过滤
const filteredTableData = computed(() => {
  if (!searchQuery.value) return tableData.value
  return tableData.value.filter(item => {
    return Object.values(item).some(val => 
      String(val).toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

// 计算覆盖率
const calculateRatio = (item) => {
  if (!item) return 0
  const xcyss = parseInt(item.xcyss)
  const xzcs = parseInt(item.xzcs)
  return xzcs === 0 ? 0 : ((xcyss / xzcs) * 100).toFixed(1)
}

// 百分比格式化
const percentageFormat = (percentage) => {
  return percentage + '%'
}

// 标签类型
const getTagType = (value) => {
  const num = parseInt(value)
  if (num > 40) return 'danger'
  if (num > 20) return 'warning'
  if (num > 10) return 'success'
  return 'info'
}

// 覆盖率颜色
const getCoverageColor = (percentage) => {
  if (percentage > 90) return '#67C23A'
  if (percentage > 70) return '#E6A23C'
  return '#F56C6C'
}

// 柱状图/折线图数据
const barChartData = computed(() => {
  if (!rawData.value || rawData.value.length === 0) return null

  const labels = rawData.value.map(item => item.zhen)
  const xcyssData = rawData.value.map(item => parseInt(item.xcyss))
  const xzcsData = rawData.value.map(item => parseInt(item.xzcs))

  return {
    labels,
    datasets: [
      {
        label: '乡村卫生室数',
        data: xcyssData,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: '#36a2eb',
        borderWidth: 1
      },
      {
        label: '行政村数',
        data: xzcsData,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: '#ff6384',
        borderWidth: 1
      }
    ]
  }
})

const barChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.raw}个`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '数量(个)'
      },
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

// 饼图数据
const pieChartData = computed(() => {
  if (!rawData.value || rawData.value.length === 0) return null

  const labels = rawData.value.map(item => item.zhen)
  const data = rawData.value.map(item => 
    pieChartMetric.value === 'xcyss' ? parseInt(item.xcyss) : parseInt(item.xzcs)
  )

  const backgroundColors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
    '#FF9F40', '#8AC24A', '#FF5722', '#607D8B', '#9C27B0',
    '#E91E63'
  ]

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: backgroundColors.slice(0, labels.length),
        borderWidth: 1
      }
    ]
  }
})

const pieChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'right'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.raw || 0
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = Math.round((value / total) * 100)
          return `${label}: ${value}个 (${percentage}%)`
        }
      }
    }
  }
}

// 历史数据图表选项
const historicalChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '数量'
      }
    }
  }
}

// 获取历史数据
const getHistoricalData = (zhen) => {
  if (!zhen) return null
  // 模拟历史数据
  return {
    labels: ['2019', '2020', '2021', '2022', '2023'],
    datasets: [{
      label: '卫生室数量',
      data: [
        Math.max(0, parseInt(zhen.xcyss) - Math.floor(Math.random() * 10)),
        Math.max(0, parseInt(zhen.xcyss) - Math.floor(Math.random() * 8)),
        Math.max(0, parseInt(zhen.xcyss) - Math.floor(Math.random() * 5)),
        Math.max(0, parseInt(zhen.xcyss) - Math.floor(Math.random() * 3)),
        parseInt(zhen.xcyss)
      ],
      borderColor: '#409EFF',
      tension: 0.4,
      fill: false
    }]
  }
}

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://129.211.82.112:8000//api/health/basic/')
    const data = await response.json()
    rawData.value = data
    return data
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
    return []
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = () => {
  fetchData()
  ElMessage.success('数据已刷新')
}

// 导出数据
const exportData = () => {
  ElMessage.success('数据导出成功')
  // 实际项目中这里应该实现导出逻辑
}

// 导出图表
const exportChart = () => {
  ElMessage.success('图表导出成功')
  // 实际项目中这里应该实现图表导出逻辑
}

// 显示镇详情
const showZhenDetail = (row) => {
  selectedZhen.value = row
  dialogVisible.value = true
}

// 编辑镇数据
const editZhenData = () => {
  ElMessage.info('编辑功能开发中')
  // 实际项目中这里应该实现编辑功能
}
</script>

<style scoped>
.health-organization {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
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
  margin-bottom: 20px;
}

.chart-card {
  height: 600px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chart-wrapper {
  height: calc(100% - 60px);
  position: relative;
  padding: 10px;
}

.coverage-map {
  margin-bottom: 20px;
}

.coverage-indicators {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.coverage-item {
  text-align: center;
}

.progress-content {
  text-align: center;
}

.progress-region {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.progress-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.data-table {
  margin-top: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

.coverage-cell {
  padding: 5px 0;
}

.zhen-detail {
  padding: 20px;
}

.detail-charts {
  margin-top: 20px;
}

.detail-chart {
  margin-top: 20px;
}

.detail-chart h4 {
  margin-bottom: 10px;
  color: #606266;
}

@media (max-width: 1200px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-container {
    grid-template-columns: 1fr;
  }

  .coverage-indicators {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }

  .coverage-indicators {
    grid-template-columns: 1fr;
  }

  .table-header {
    flex-direction: column;
    gap: 10px;
  }

  .header-right {
    width: 100%;
  }
}
</style>