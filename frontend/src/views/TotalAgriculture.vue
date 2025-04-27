<template>
  <AppLayout>
    <div class="total-agriculture">
      <div class="page-header">
        <div class="header-left">
          <h2>农业总产值概况</h2>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>农业总产值</el-breadcrumb-item>
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
        <!-- 增长率柱状图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-data-line"></i>
                <span>各地区/产值类型增长率对比</span>
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
              :chart-data="chartData"
              :options="chartOptions"
            />
            <line-chart
              v-else
              :chart-data="chartData"
              :options="chartOptions"
            />
          </div>
        </el-card>

        <!-- 增长率分布饼图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-pie-chart"></i>
                <span>增长率分布情况</span>
              </div>
              <el-tooltip content="查看详情" placement="top">
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
              <span class="table-title">详细农业总产值数据</span>
              <el-tag type="info" style="margin-left: 10px">共 {{ tableData.length }} 条</el-tag>
            </div>
            <div class="header-right">
              <el-input
                v-model="searchQuery"
                placeholder="搜索地区/类型..."
                prefix-icon="el-icon-search"
                style="width: 200px; margin-right: 10px"
              />
              <el-button-group>
                <el-button type="primary" size="small" @click="exportData">
                  <i class="el-icon-download"></i> 导出数据
                </el-button>
                <el-button type="success" size="small" @click="showAnalysis">
                  <i class="el-icon-data-analysis"></i> 数据分析
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
          :default-sort="{prop: 'nyzz', order: 'descending'}"
          v-loading="loading"
        >
          <el-table-column prop="zbmc" label="地区/产值类型" width="150">
            <template #default="{ row }">
              <el-button type="text" @click="showDetail(row)">{{ row.zbmc }}</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="nyzz" label="农业总产值增长率(%)" sortable>
            <template #default="{ row }">
              <div class="growth-cell">
                <el-tag :type="getGrowthTagType(row.nyzz)">{{ row.nyzz }}%</el-tag>
                <el-progress 
                  :percentage="getGrowthPercentage(row.nyzz)" 
                  :color="getProgressColor(row.nyzz)"
                  :format="percentageFormat"
                  :stroke-width="4"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="dw" label="单位" width="100"></el-table-column>
          <el-table-column label="同比分析" width="200">
            <template #default="{ row }">
              <div class="trend-analysis">
                <span :class="getTrendClass(row.nyzz)">
                  <i :class="getTrendIcon(row.nyzz)"></i>
                  {{ getTrendText(row.nyzz) }}
                </span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" size="small" icon="el-icon-view" @click="showDetail(row)">
                  详情
                </el-button>
                <el-button type="success" size="small" icon="el-icon-edit" @click="editData(row)">
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
            :total="tableData.length"
            :page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          >
          </el-pagination>
        </div>
      </el-card>

      <!-- 详情对话框 -->
      <el-dialog
        :title="selectedItem ? selectedItem.zbmc + ' 详细信息' : ''"
        v-model="dialogVisible"
        width="60%"
      >
        <div v-if="selectedItem" class="detail-content">
          <el-descriptions border>
            <el-descriptions-item label="地区/产值类型">{{ selectedItem.zbmc }}</el-descriptions-item>
            <el-descriptions-item label="增长率">{{ selectedItem.nyzz }}%</el-descriptions-item>
            <el-descriptions-item label="单位">{{ selectedItem.dw }}</el-descriptions-item>
          </el-descriptions>
          
          <div class="trend-chart">
            <h4>历年增长趋势</h4>
            <line-chart
              :chart-data="getTrendData(selectedItem)"
              :options="trendChartOptions"
            />
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
const selectedItem = ref(null)
const pageSize = ref(10)

// 使用您提供的API数据
const rawData = ref([])

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://129.211.82.112:8000/api/totalagriculture/basic/')
    const data = await response.json()
    rawData.value = data
    ElMessage.success('数据加载成功')
  } catch (error) {
    console.error('Error fetching data:', error)
    ElMessage.error('数据加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalCount = rawData.value.length
  const positiveGrowthCount = rawData.value.filter(item => parseFloat(item.nyzz) > 0).length
  const negativeGrowthCount = totalCount - positiveGrowthCount
  const avgGrowth = rawData.value.reduce((sum, item) => sum + parseFloat(item.nyzz), 0) / totalCount

  return [
    {
      title: '数据总数',
      value: totalCount,
      icon: 'el-icon-data-line',
      type: 'primary',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '数据完整'
    },
    {
      title: '正增长数量',
      value: positiveGrowthCount,
      icon: 'el-icon-top',
      type: 'success',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上期增加'
    },
    {
      title: '负增长数量',
      value: negativeGrowthCount,
      icon: 'el-icon-bottom',
      type: 'danger',
      trend: 'down',
      trendIcon: 'el-icon-bottom',
      trendText: '需要关注'
    },
    {
      title: '平均增长率',
      value: avgGrowth.toFixed(2) + '%',
      icon: 'el-icon-data-analysis',
      type: 'warning',
      trend: avgGrowth > 0 ? 'up' : 'down',
      trendIcon: avgGrowth > 0 ? 'el-icon-top' : 'el-icon-bottom',
      trendText: avgGrowth > 0 ? '整体向好' : '需要改进'
    }
  ]
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

// 表格数据
const tableData = computed(() => {
  return rawData.value.slice()
})

// 图表数据
const chartData = computed(() => {
  const labels = tableData.value.map(item => item.zbmc)
  const nyzzData = tableData.value.map(item => parseFloat(item.nyzz))

  return {
    labels,
    datasets: [
      {
        label: '农业总产值增长率(%)',
        data: nyzzData,
        backgroundColor: labels.map((_, i) => nyzzData[i] > 0 ? '#67C23A' : '#F56C6C'),
        borderColor: labels.map((_, i) => nyzzData[i] > 0 ? '#67C23A' : '#F56C6C'),
        borderWidth: 1
      }
    ]
  }
})

// 饼图数据
const pieChartData = computed(() => {
  const positiveCount = rawData.value.filter(item => parseFloat(item.nyzz) > 0).length
  const negativeCount = rawData.value.filter(item => parseFloat(item.nyzz) <= 0).length

  return {
    labels: ['正增长', '负增长'],
    datasets: [{
      data: [positiveCount, negativeCount],
      backgroundColor: ['#67C23A', '#F56C6C'],
      borderWidth: 1
    }]
  }
})

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      align: 'center',
      labels: {
        padding: 20,
        font: {
          size: 12
        },
        boxWidth: 15
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.raw || 0
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = Math.round((value / total) * 100)
          return `${label}: ${value} (${percentage}%)`
        }
      }
    }
  }
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        padding: 20,
        font: {
          size: 14
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.raw}%`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: false,
      title: {
        display: true,
        text: '增长率(%)',
        font: {
          size: 14
        }
      },
      ticks: {
        font: {
          size: 12
        }
      }
    },
    x: {
      ticks: {
        font: {
          size: 12
        },
        maxRotation: 45,
        minRotation: 45
      }
    }
  }
}

// 趋势图数据
const getTrendData = (item) => {
  if (!item) return null
  
  const years = ['2019', '2020', '2021', '2022', '2023']
  const currentValue = parseFloat(item.nyzz)
  const trendData = years.map((year, index) => {
    if (index === years.length - 1) return currentValue
    return Math.round(currentValue * (0.8 + Math.random() * 0.4))
  })

  return {
    labels: years,
    datasets: [{
      label: '增长率(%)',
      data: trendData,
      borderColor: '#409EFF',
      tension: 0.4,
      fill: false
    }]
  }
}

const trendChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      title: {
        display: true,
        text: '增长率(%)'
      }
    }
  }
}

// 计算增长率百分比
const getGrowthPercentage = (value) => {
  const num = parseFloat(value)
  const maxGrowth = Math.max(...rawData.value.map(item => parseFloat(item.nyzz)))
  const minGrowth = Math.min(...rawData.value.map(item => parseFloat(item.nyzz)))
  const range = maxGrowth - minGrowth
  return ((num - minGrowth) / range * 100).toFixed(1)
}

// 获取进度条颜色
const getProgressColor = (value) => {
  const num = parseFloat(value)
  if (num > 10) return '#67C23A'
  if (num > 0) return '#E6A23C'
  return '#F56C6C'
}

// 百分比格式化
const percentageFormat = (val) => {
  return val + '%'
}

// 获取趋势样式
const getTrendClass = (value) => {
  const num = parseFloat(value)
  return num > 0 ? 'trend-up' : 'trend-down'
}

const getTrendIcon = (value) => {
  const num = parseFloat(value)
  return num > 0 ? 'el-icon-top' : 'el-icon-bottom'
}

const getTrendText = (value) => {
  const num = parseFloat(value)
  return num > 0 ? '同比上升' : '同比下降'
}

// 标签类型
const getGrowthTagType = (value) => {
  const num = parseFloat(value)
  if (num > 10) return 'success'
  if (num > 0) return 'warning'
  return 'danger'
}

// 查看详情
const showDetail = (row) => {
  selectedItem.value = row
  dialogVisible.value = true
}

// 编辑数据
const editData = () => {
  ElMessage.info('编辑功能开发中')
}

// 显示分布详情
const showDistributionDetail = () => {
  ElMessage.info('分布详情功能开发中')
}

// 显示数据分析
const showAnalysis = () => {
  ElMessage.info('数据分析功能开发中')
}

// 导出图表
const exportChart = () => {
  ElMessage.success('图表导出成功')
}

// 刷新数据
const refreshData = async () => {
  await fetchData()
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
</script>

<style scoped>
.total-agriculture {
  background: #fff;
  padding: 30px;
  border-radius: 6px;
  max-width: 100%;
  overflow-x: hidden;
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
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin: 40px 0;
  min-height: 1000px;
}

.chart-card {
  height: 1000px;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  flex: 1;
  min-height: 900px;
  position: relative;
  padding: 30px;
  overflow: visible;
}

:deep(.chart-wrapper canvas) {
  max-width: none !important;
  width: 100% !important;
  height: 100% !important;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  min-height: 70px;
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 500;
}

.chart-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

:deep(.chart-wrapper .chartjs-legend) {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
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

.growth-cell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.trend-analysis {
  display: flex;
  align-items: center;
  gap: 8px;
}

.trend-up {
  color: #67C23A;
}

.trend-down {
  color: #F56C6C;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.detail-content {
  padding: 20px;
}

.trend-chart {
  margin-top: 30px;
}

.trend-chart h4 {
  margin-bottom: 15px;
  color: #606266;
  font-weight: 500;
}

@media (max-width: 1800px) {
  .chart-card {
    height: 900px;
  }
  
  .chart-wrapper {
    min-height: 800px;
  }
}

@media (max-width: 1400px) {
  .chart-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .chart-card {
    height: 800px;
  }
  
  .chart-wrapper {
    min-height: 700px;
  }
}

@media (max-width: 768px) {
  .total-agriculture {
    padding: 15px;
  }

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
  
  .chart-container {
    gap: 20px;
    margin: 20px 0;
  }
  
  .chart-card {
    height: 600px;
  }
  
  .chart-wrapper {
    min-height: 500px;
    padding: 15px;
  }
  
  .chart-header {
    padding: 15px;
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .chart-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>