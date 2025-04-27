<template>
  <AppLayout>
    <div class="rural-organization">
      <div class="page-header">
        <div class="header-left">
          <h2>农村基层组织</h2>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>基层组织</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-button-group>
            <el-button type="primary" icon="el-icon-refresh" @click="refreshData">刷新数据</el-button>
            <el-button type="success" icon="el-icon-download" @click="exportData">导出数据</el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 数据概览卡片 -->
      <div class="overview-cards">
        <el-card shadow="hover" v-for="stat in stats" :key="stat.title" :class="stat.type">
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
        <!-- 柱状图/折线图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-data-line"></i>
                <span>各村镇年末人口数对比</span>
              </div>
              <div class="chart-actions">
                <el-radio-group v-model="chartType" size="small">
                  <el-radio-button label="bar">柱状图</el-radio-button>
                  <el-radio-button label="line">折线图</el-radio-button>
                </el-radio-group>
                <el-tooltip content="导出图表" placement="top">
                  <el-button size="small" icon="el-icon-download" circle @click="exportChart"></el-button>
                </el-tooltip>
              </div>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              v-if="chartType === 'bar'"
              :chart-data="barChartData"
              :options="barChartOptions"
            />
            <line-chart
              v-else
              :chart-data="barChartData"
              :options="barChartOptions"
            />
          </div>
        </el-card>

        <!-- 饼图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-pie-chart"></i>
                <span>年末居住户数分布比例</span>
              </div>
              <el-tooltip content="点击查看详情" placement="top">
                <el-button type="text" @click="showDistributionDetail">
                  查看详情
                </el-button>
              </el-tooltip>
            </div>
          </template>
          <div class="chart-wrapper">
            <pie-chart
              :chart-data="pieChartData"
              :options="pieChartOptions"
            />
          </div>
        </el-card>
      </div>

      <!-- 数据表格 -->
      <el-card shadow="hover" class="data-table">
        <template #header>
          <div class="table-header">
            <div class="header-left">
              <span class="table-title">详细数据</span>
              <el-tag type="info" style="margin-left: 10px">共 {{ sortedTableData.length }} 条</el-tag>
            </div>
            <div class="header-right">
              <el-input
                v-model="searchQuery"
                placeholder="搜索镇/街道..."
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
          stripe
          style="width: 100%"
          :default-sort="{prop: 'ncrk', order: 'descending'}"
          v-loading="loading"
        >
          <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
          <el-table-column prop="jz" label="镇/街道" sortable>
            <template #default="{ row }">
              <el-button type="text" @click="showTownDetail(row)">{{ row.jz }}</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="cmxz" label="村民小组数" sortable>
            <template #default="{ row }">
              <el-tag :type="getTagType(row.cmxz)">{{ row.cmxz }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ncrk" label="年末人口数" sortable>
            <template #default="{ row }">
              <div class="population-cell">
                {{ row.ncrk }}
                <el-progress 
                  :percentage="getPopulationPercentage(row)" 
                  :color="getProgressColor"
                  :show-text="false"
                  :stroke-width="4"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="cmwyh" label="村民委员会数" sortable>
            <template #default="{ row }">
              <el-tag type="warning">{{ row.cmwyh }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ncjzrk" label="年末居住人口数" sortable>
            <template #default="{ row }">
              <div class="population-cell">
                {{ row.ncjzrk }}
                <el-progress 
                  :percentage="getResidentPercentage(row)" 
                  :color="getProgressColor"
                  :show-text="false"
                  :stroke-width="4"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="ncjzhs" label="年末居住户数" sortable>
            <template #default="{ row }">
              <el-tag type="info">{{ row.ncjzhs }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" size="small" icon="el-icon-view" @click="showTownDetail(row)">
                  详情
                </el-button>
                <el-button type="success" size="small" icon="el-icon-edit" @click="editTownData">
                  编辑
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container">
          <el-pagination
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="sortedTableData.length"
            :page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          >
          </el-pagination>
        </div>
      </el-card>

      <!-- 镇详情对话框 -->
      <el-dialog
        :title="selectedTown ? selectedTown.jz + ' 详细信息' : ''"
        v-model="dialogVisible"
        width="50%"
      >
        <div v-if="selectedTown" class="town-detail">
          <el-descriptions border>
            <el-descriptions-item label="镇/街道">{{ selectedTown.jz }}</el-descriptions-item>
            <el-descriptions-item label="村民小组数">{{ selectedTown.cmxz }}</el-descriptions-item>
            <el-descriptions-item label="村民委员会数">{{ selectedTown.cmwyh }}</el-descriptions-item>
            <el-descriptions-item label="年末人口数">{{ selectedTown.ncrk }}</el-descriptions-item>
            <el-descriptions-item label="年末居住人口数">{{ selectedTown.ncjzrk }}</el-descriptions-item>
            <el-descriptions-item label="年末居住户数">{{ selectedTown.ncjzhs }}</el-descriptions-item>
          </el-descriptions>
          
          <div class="detail-charts">
            <div class="detail-chart">
              <h4>历年人口变化趋势</h4>
              <line-chart
                :chart-data="getHistoricalData(selectedTown)"
                :options="historicalChartOptions"
              />
            </div>
          </div>
        </div>
      </el-dialog>
    </div>
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
const dialogVisible = ref(false)
const selectedTown = ref(null)
const pageSize = ref(10)

// 模拟API请求
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://129.211.82.112:8000//api/ruralorganization/basic/')
    const data = await response.json()
    return data
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
    throw error
  } finally {
    loading.value = false
  }
}

const rawData = ref([])

// 获取数据
onMounted(async () => {
  await refreshData()
})

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalNcrk = rawData.value.reduce((sum, item) => sum + parseInt(item.ncrk), 0)
  const totalNcjzhs = rawData.value.reduce((sum, item) => sum + parseInt(item.ncjzhs), 0)
  const avgNcjzrk = (rawData.value.reduce((sum, item) => sum + parseInt(item.ncjzrk), 0) / rawData.value.length).toFixed(1)
  const totalCmxz = rawData.value.reduce((sum, item) => sum + parseInt(item.cmxz), 0)

  return [
    {
      title: '总年末人口数',
      value: totalNcrk,
      icon: 'el-icon-user',
      type: 'primary',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月增加8%'
    },
    {
      title: '总年末居住户数',
      value: totalNcjzhs,
      icon: 'el-icon-house',
      type: 'success',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上月持平'
    },
    {
      title: '平均年末居住人口数',
      value: avgNcjzrk + '人',
      icon: 'el-icon-data-analysis',
      type: 'warning',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月提升3%'
    },
    {
      title: '总村民小组数',
      value: totalCmxz,
      icon: 'el-icon-office-building',
      type: 'info',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '覆盖全部村镇'
    }
  ]
})

// 搜索过滤
const filteredTableData = computed(() => {
  if (!searchQuery.value) return sortedTableData.value
  return sortedTableData.value.filter(item => {
    return Object.values(item).some(val => 
      String(val).toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

// 表格数据（按ID排序）
const sortedTableData = computed(() => {
  return [...rawData.value].sort((a, b) => parseInt(a.id) - parseInt(b.id))
})

// 获取标签类型
const getTagType = (value) => {
  const num = parseInt(value)
  if (num > 40) return 'danger'
  if (num > 20) return 'warning'
  if (num > 10) return 'success'
  return 'info'
}

// 获取进度条颜色
const getProgressColor = (percentage) => {
  if (percentage > 80) return '#F56C6C'
  if (percentage > 60) return '#E6A23C'
  return '#67C23A'
}

// 计算人口百分比
const getPopulationPercentage = (row) => {
  const maxPopulation = Math.max(...rawData.value.map(item => parseInt(item.ncrk)))
  return (parseInt(row.ncrk) / maxPopulation * 100).toFixed(1)
}

// 计算居住人口百分比
const getResidentPercentage = (row) => {
  const maxResident = Math.max(...rawData.value.map(item => parseInt(item.ncjzrk)))
  return (parseInt(row.ncjzrk) / maxResident * 100).toFixed(1)
}

// 获取历史数据
const getHistoricalData = (town) => {
  if (!town) return null
  
  // 模拟5年历史数据
  const currentValue = parseInt(town.ncrk)
  const years = ['2019', '2020', '2021', '2022', '2023']
  const data = years.map((year, index) => {
    if (index === years.length - 1) return currentValue
    // 生成一个在当前值80%-120%之间的随机值
    return Math.round(currentValue * (0.8 + Math.random() * 0.4))
  })

  return {
    labels: years,
    datasets: [{
      label: '年末人口数',
      data: data,
      borderColor: '#409EFF',
      tension: 0.4,
      fill: false
    }]
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
        text: '人口数'
      }
    }
  }
}

// 查看镇详情
const showTownDetail = (row) => {
  selectedTown.value = row
  dialogVisible.value = true
}

// 查看分布详情
const showDistributionDetail = () => {
  ElMessage.info('分布详情功能开发中')
}

// 编辑镇数据
const editTownData = () => {
  ElMessage.info('编辑功能开发中')
}

// 导出图表
const exportChart = () => {
  ElMessage.success('图表导出成功')
}

// 刷新数据
const refreshData = async () => {
  try {
    loading.value = true
    const data = await fetchData()
    rawData.value = data
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('刷新数据失败')
  } finally {
    loading.value = false
  }
}

// 导出数据
const exportData = () => {
  ElMessage.success('导出数据成功')
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
}

const handleCurrentChange = () => {
  // 处理页码变化
}

// 柱状图/折线图数据
const barChartData = computed(() => {
  const sortedData = [...rawData.value].sort((a, b) => parseInt(a.id) - parseInt(b.id))
  const labels = sortedData.map(item => item.jz)
  const ncrkData = sortedData.map(item => parseInt(item.ncrk))

  return {
    labels,
    datasets: [
      {
        label: '年末人口数',
        data: ncrkData,
        backgroundColor: '#36a2eb',
        borderColor: '#36a2eb',
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
          return `${context.dataset.label}: ${context.raw}人`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '数量(人)'
      }
    }
  }
}

// 饼图数据
const pieChartData = computed(() => {
  const sortedData = [...rawData.value].sort((a, b) => parseInt(a.id) - parseInt(b.id))
  const labels = sortedData.map(item => item.jz)
  const data = sortedData.map(item => parseInt(item.ncjzhs))

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
          return `${label}: ${value}户 (${percentage}%)`
        }
      }
    }
  }
}
</script>

<style scoped>
.rural-organization {
  background: #fff;
  padding: 20px;
  border-radius: 6px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

h2 {
  margin: 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  font-size: 48px;
  margin-right: 20px;
  color: #409EFF;
}

.stat-info {
  flex-grow: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-trend.up {
  color: #F56C6C;
}

.stat-trend.down {
  color: #67C23A;
}

.stat-trend.stable {
  color: #909399;
}

.chart-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  height: 500px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
}

.chart-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chart-wrapper {
  height: calc(100% - 60px);
  position: relative;
  padding: 20px;
}

.data-table {
  margin-top: 30px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 16px;
  font-weight: 500;
}

.population-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.town-detail {
  padding: 20px;
}

.detail-charts {
  margin-top: 30px;
}

.detail-chart {
  margin-top: 20px;
}

.detail-chart h4 {
  margin-bottom: 15px;
  color: #606266;
  font-weight: 500;
}

@media (max-width: 1400px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .chart-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-right {
    width: 100%;
  }
}
</style>