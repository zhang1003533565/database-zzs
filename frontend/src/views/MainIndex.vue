<template>
  <AppLayout>
    <div class="agriculture-main-index">
      <div class="page-header">
        <div class="header-left">
          <h2>农业主要指标</h2>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>农业指标</el-breadcrumb-item>
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
        <!-- 柱状图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-data-line"></i>
                <span>各类农产品产量对比</span>
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
                <span>农业各产业占比</span>
              </div>
              <el-tooltip content="点击查看详情" placement="top">
                <el-button type="text" @click="showIndustryDetail">
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
              <el-tag type="info" style="margin-left: 10px">共 {{ tableData.length }} 条</el-tag>
            </div>
            <div class="header-right">
              <el-input
                v-model="searchQuery"
                placeholder="搜索指标..."
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
          :default-sort="{prop: 'ze2023', order: 'descending'}"
          v-loading="loading"
        >
          <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
          <el-table-column prop="zb" label="指标" sortable>
            <template #default="{ row }">
              <el-button type="text" @click="showIndicatorDetail(row)">{{ row.zb }}</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="ze2023" label="2023年数值" sortable>
            <template #default="{ row }">
              <el-tag :type="getTagType(row.ze2023)">{{ row.ze2023 }}{{ row.dw }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ze_last_year" label="去年数值" sortable>
            <template #default="{ row }">
              <el-tag :type="getTagType(row.ze_last_year)">{{ row.ze_last_year }}{{ row.dw }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="growthRate" label="增长率" sortable>
            <template #default="{ row }">
              <div class="growth-rate" :class="getGrowthRateClass(row)">
                <i :class="getGrowthRateIcon(row)"></i>
                {{ calculateGrowthRate(row) }}%
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" size="small" icon="el-icon-view" @click="showIndicatorDetail(row)">
                  详情
                </el-button>
                <el-button type="success" size="small" icon="el-icon-edit" @click="editIndicator">
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

      <!-- 指标详情对话框 -->
      <el-dialog
        :title="selectedIndicator ? selectedIndicator.zb + ' 详细信息' : ''"
        v-model="dialogVisible"
        width="50%"
      >
        <div v-if="selectedIndicator" class="indicator-detail">
          <el-descriptions border>
            <el-descriptions-item label="指标名称">{{ selectedIndicator.zb }}</el-descriptions-item>
            <el-descriptions-item label="2023年数值">{{ selectedIndicator.ze2023 }}{{ selectedIndicator.dw }}</el-descriptions-item>
            <el-descriptions-item label="去年数值">{{ selectedIndicator.ze_last_year }}{{ selectedIndicator.dw }}</el-descriptions-item>
            <el-descriptions-item label="增长率">{{ calculateGrowthRate(selectedIndicator) }}%</el-descriptions-item>
          </el-descriptions>
          
          <div class="detail-charts">
            <div class="detail-chart">
              <h4>历年数据趋势</h4>
              <line-chart
                :chart-data="getHistoricalData(selectedIndicator)"
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
const selectedIndicator = ref(null)
const pageSize = ref(10)

// 模拟API请求
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://129.211.82.112:8000//api/mainindex/basic/')
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
  try {
    const data = await fetchData()
    // 对数据进行处理，按序排列id并从1开始
    const sortedData = data.map((item, index) => ({
     ...item,
      id: (index + 1).toString()
    }))
    rawData.value = sortedData
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
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

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalProduction2023 = rawData.value.reduce((sum, item) => sum + parseFloat(item.ze2023), 0)
  const totalProductionLastYear = rawData.value.reduce((sum, item) => sum + parseFloat(item.ze_last_year), 0)
  const growthRate = ((totalProduction2023 - totalProductionLastYear) / totalProductionLastYear * 100).toFixed(1)
  const avgGrowthRate = (rawData.value.reduce((sum, item) => sum + parseFloat(calculateGrowthRate(item)), 0) / rawData.value.length).toFixed(1)

  return [
    {
      title: '2023年农业总产量',
      value: totalProduction2023.toFixed(2),
      icon: 'el-icon-data-line',
      type: 'primary',
      trend: growthRate > 0 ? 'up' : growthRate < 0 ? 'down' : 'stable',
      trendIcon: growthRate > 0 ? 'el-icon-top' : growthRate < 0 ? 'el-icon-bottom' : 'el-icon-right',
      trendText: growthRate > 0 ? `较去年增长${growthRate}%` : growthRate < 0 ? `较去年下降${Math.abs(parseFloat(growthRate))}%` : '与去年持平'
    },
    {
      title: '平均增长率',
      value: avgGrowthRate + '%',
      icon: 'el-icon-trend-charts',
      type: 'success',
      trend: avgGrowthRate > 0 ? 'up' : avgGrowthRate < 0 ? 'down' : 'stable',
      trendIcon: avgGrowthRate > 0 ? 'el-icon-top' : avgGrowthRate < 0 ? 'el-icon-bottom' : 'el-icon-right',
      trendText: `平均增速${avgGrowthRate}%`
    },
    {
      title: '指标数量',
      value: rawData.value.length,
      icon: 'el-icon-collection',
      type: 'warning',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '指标数量稳定'
    },
    {
      title: '数据更新时间',
      value: '2023-12',
      icon: 'el-icon-time',
      type: 'info',
      trend: 'stable',
      trendIcon: 'el-icon-refresh',
      trendText: '每月更新'
    }
  ]
})

// 表格数据
const tableData = computed(() => {
  return rawData.value.map(item => ({
   ...item,
    growthRate: calculateGrowthRate(item)
  }))
})

// 计算增长率
const calculateGrowthRate = (item) => {
  const lastYear = parseFloat(item.ze_last_year)
  const currentYear = parseFloat(item.ze2023)
  return lastYear === 0? 0 : ((currentYear - lastYear) / lastYear * 100).toFixed(1)
}

// 标签类型
const getTagType = (value) => {
  const num = parseFloat(value)
  if (num > 50) return 'danger'
  if (num > 20) return 'warning'
  if (num > 10) return'success'
  return 'info'
}

// 柱状图/折线图数据
const barChartData = computed(() => {
  const labels = rawData.value.map(item => item.zb)
  const ze2023Data = rawData.value.map(item => parseFloat(item.ze2023))
  const zeLastYearData = rawData.value.map(item => parseFloat(item.ze_last_year))

  return {
    labels,
    datasets: [
      {
        label: '2023年数值',
        data: ze2023Data,
        backgroundColor: '#36a2eb',
        borderColor: '#36a2eb',
        borderWidth: 1
      },
      {
        label: '去年数值',
        data: zeLastYearData,
        backgroundColor: '#ff6384',
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
          return `${context.dataset.label}: ${context.raw}${context.dataset.label === '2023年数值'? rawData.value[context.dataIndex].dw : rawData.value[context.dataIndex].dw}`
        }
      }
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

// 饼图数据
const pieChartData = computed(() => {
  const labels = rawData.value.filter(item => ['种植业', '林业', '牧业'].includes(item.zb)).map(item => item.zb)
  const data = rawData.value.filter(item => ['种植业', '林业', '牧业'].includes(item.zb)).map(item => parseFloat(item.ze2023))

  const backgroundColors = [
    '#FF6384', '#36A2EB', '#FFCE56'
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
          return `${label}: ${value}亿元 (${percentage}%)`
        }
      }
    }
  }
}

// 导出数据
const exportData = () => {
  ElMessage.success('导出数据成功')
  // 实际项目中这里应该实现导出逻辑，例如使用FileSaver.js等库将数据导出为CSV文件
}

// 新增的函数
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

const showIndustryDetail = () => {
  ElMessage.info('行业详情功能开发中')
}

const showIndicatorDetail = (row) => {
  selectedIndicator.value = row
  dialogVisible.value = true
}

const editIndicator = () => {
  ElMessage.info('编辑功能开发中')
}

const getHistoricalData = (indicator) => {
  if (!indicator) return null
  
  // 模拟5年历史数据
  const currentValue = parseFloat(indicator.ze2023)
  const years = ['2019', '2020', '2021', '2022', '2023']
  const data = years.map((year, index) => {
    if (index === years.length - 1) return currentValue
    // 生成一个在当前值80%-120%之间的随机值
    return currentValue * (0.8 + Math.random() * 0.4)
  })

  return {
    labels: years,
    datasets: [{
      label: indicator.zb,
      data: data,
      borderColor: '#409EFF',
      tension: 0.4,
      fill: false
    }]
  }
}

const getGrowthRateClass = (row) => {
  const rate = parseFloat(calculateGrowthRate(row))
  if (rate > 0) return 'positive'
  if (rate < 0) return 'negative'
  return 'neutral'
}

const getGrowthRateIcon = (row) => {
  const rate = parseFloat(calculateGrowthRate(row))
  if (rate > 0) return 'el-icon-top'
  if (rate < 0) return 'el-icon-bottom'
  return 'el-icon-right'
}

const handleSizeChange = (val) => {
  pageSize.value = val
}

const handleCurrentChange = () => {
  // 处理页码变化
}

// 初始化数据
onMounted(async () => {
  await refreshData()
})
</script>

<style scoped>
.agriculture-main-index {
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

.growth-rate {
  display: flex;
  align-items: center;
  gap: 4px;
}

.growth-rate.positive {
  color: #F56C6C;
}

.growth-rate.negative {
  color: #67C23A;
}

.growth-rate.neutral {
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.indicator-detail {
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