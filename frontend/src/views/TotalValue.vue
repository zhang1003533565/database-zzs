<template>
  <AppLayout>
    <div class="total-value">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-left">
          <h2>农业历年总产值</h2>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>农业总产值</el-breadcrumb-item>
            <el-breadcrumb-item>历年产值</el-breadcrumb-item>
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
        <!-- 总产值图表 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-data-line"></i>
                <span>历年农业总产值变化</span>
              </div>
              <div class="chart-actions">
                <el-radio-group v-model="totalValueChartType" size="small">
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
              v-if="totalValueChartType === 'bar'"
              :chart-data="totalValueChartData"
              :options="totalValueChartOptions"
            />
            <line-chart
              v-else
              :chart-data="totalValueChartData"
              :options="totalValueChartOptions"
            />
          </div>
        </el-card>

        <!-- 其他相关图表 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-data-analysis"></i>
                <span>历年农业指标与总产值对比</span>
              </div>
              <el-tooltip content="查看详情" placement="top">
                <el-button type="text" @click="showIndexDetail">
                  查看详情
                </el-button>
              </el-tooltip>
            </div>
          </template>
          <div class="chart-wrapper">
            <line-chart
              :chart-data="relatedIndexChartData"
              :options="relatedIndexChartOptions"
            />
          </div>
        </el-card>
      </div>

      <!-- 第二行图表 -->
      <div class="chart-container">
        <!-- 其他图表示例 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-trend-charts"></i>
                <span>历年农业指标变化</span>
              </div>
              <el-tooltip content="切换指标" placement="top">
                <el-select v-model="selectedIndex" size="small" style="width: 120px">
                  <el-option label="指标一" value="yy"></el-option>
                  <el-option label="指标二" value="fy"></el-option>
                </el-select>
              </el-tooltip>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              :chart-data="anotherIndexChartData"
              :options="anotherIndexChartOptions"
            />
          </div>
        </el-card>

        <!-- 面积分布饼图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-pie-chart"></i>
                <span>农业相关面积分布</span>
              </div>
              <el-tooltip content="查看分布详情" placement="top">
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
              <span class="table-title">详细农业历年数据</span>
              <el-tag type="info" style="margin-left: 10px">共 {{ tableData.length }} 条</el-tag>
            </div>
            <div class="header-right">
              <el-input
                v-model="searchQuery"
                placeholder="搜索年份/指标..."
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
          :default-sort="{prop: 'nyzcz', order: 'descending'}"
          v-loading="loading"
          @sort-change="handleSortChange"
        >
          <el-table-column type="expand">
            <template #default="{row}">
              <div class="expand-content">
                <el-descriptions border>
                  <el-descriptions-item label="年份">{{ row.year }}</el-descriptions-item>
                  <el-descriptions-item label="农业总产值">{{ row.nyzcz }}</el-descriptions-item>
                  <el-descriptions-item label="其他指标">{{ row.yy }}</el-descriptions-item>
                  <el-descriptions-item label="另一指标">{{ row.fy }}</el-descriptions-item>
                </el-descriptions>
                <div class="trend-analysis">
                  <h4>同比分析</h4>
                  <div class="analysis-item">
                    <span>总产值增长率：</span>
                    <el-progress 
                      :percentage="getGrowthRate(row.nyzcz)" 
                      :color="getProgressColor(getGrowthRate(row.nyzcz))"
                      :format="percentageFormat"
                    ></el-progress>
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="year" label="年份" sortable width="120">
            <template #default="{row}">
              <el-button type="text" @click="showYearDetail(row)">{{ row.year }}</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="nyzcz" label="农业总产值" sortable>
            <template #default="{row}">
              <div class="value-cell">
                <el-tag :type="getTotalValueTagType(row.nyzcz)">{{ row.nyzcz }}</el-tag>
                <el-progress 
                  :percentage="getValuePercentage(row.nyzcz)" 
                  :color="getProgressColor(getValuePercentage(row.nyzcz))"
                  :format="percentageFormat"
                  :stroke-width="4"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="yy" label="其他指标" sortable>
            <template #default="{row}">
              <el-tag :type="getOtherTagType(row.yy)">{{ row.yy }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="fy" label="另一指标" sortable>
            <template #default="{row}">
              <el-tag :type="getAnotherTagType(row.fy)">{{ row.fy }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{row}">
              <el-button-group>
                <el-button type="primary" size="small" icon="el-icon-view" @click="showYearDetail(row)">
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

      <!-- 年度详情对话框 -->
      <el-dialog
        :title="selectedYear ? selectedYear.year + '年度详细数据' : ''"
        v-model="dialogVisible"
        width="60%"
      >
        <div v-if="selectedYear" class="detail-content">
          <el-descriptions border>
            <el-descriptions-item label="年份">{{ selectedYear.year }}</el-descriptions-item>
            <el-descriptions-item label="农业总产值">{{ selectedYear.nyzcz }}</el-descriptions-item>
            <el-descriptions-item label="其他指标">{{ selectedYear.yy }}</el-descriptions-item>
            <el-descriptions-item label="另一指标">{{ selectedYear.fy }}</el-descriptions-item>
          </el-descriptions>
          
          <div class="trend-chart">
            <h4>历年趋势对比</h4>
            <line-chart
              :chart-data="getYearTrendData(selectedYear)"
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

// 使用您提供的API数据
const rawData = ref([])

const loading = ref(false)
const searchQuery = ref('')
const selectedIndex = ref('yy')
const dialogVisible = ref(false)
const selectedYear = ref(null)
const pageSize = ref(10)

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://129.211.82.112:8000/api/totalvalue/basic/')
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

const totalValueChartType = ref('bar')

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalValue = rawData.value.reduce((sum, item) => sum + parseFloat(item.nyzcz), 0)
  const avgValue = totalValue / rawData.value.length
  const maxValue = Math.max(...rawData.value.map(item => parseFloat(item.nyzcz)))
  const growthRate = ((maxValue - avgValue) / avgValue * 100).toFixed(2)

  return [
    {
      title: '总产值累计',
      value: totalValue.toLocaleString(),
      icon: 'el-icon-money',
      type: 'primary',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '持续增长'
    },
    {
      title: '平均产值',
      value: avgValue.toLocaleString(),
      icon: 'el-icon-data-line',
      type: 'success',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: `增长${growthRate}%`
    },
    {
      title: '最高产值',
      value: maxValue.toLocaleString(),
      icon: 'el-icon-top',
      type: 'warning',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '历史新高'
    },
    {
      title: '数据总量',
      value: rawData.value.length,
      icon: 'el-icon-document',
      type: 'info',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '数据完整'
    }
  ]
})

// 表格数据
const tableData = computed(() => {
  return rawData.value.slice()
})

// 总产值图表数据
const totalValueChartData = computed(() => {
  const labels = tableData.value.map(item => item.year)
  const totalValueData = tableData.value.map(item => parseFloat(item.nyzcz))

  return {
    labels,
    datasets: [
      {
        label: '农业总产值',
        data: totalValueData,
        backgroundColor: '#36a2eb',
        borderColor: '#36a2eb',
        borderWidth: 1
      }
    ]
  }
})

const totalValueChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.raw.toLocaleString()}`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '农业总产值',
        font: {
          size: 14
        }
      },
      min: 0,
      max: 400000,
      ticks: {
        stepSize: 50000
      }
    }
  }
}

// 其他相关指标图表数据
const relatedIndexChartData = computed(() => {
  const labels = tableData.value.map(item => item.year)
  const yyData = tableData.value.map(item => parseFloat(item.yy))
  const nyszcData = tableData.value.map(item => parseFloat(item.nyzcz))

  return {
    labels,
    datasets: [
      {
        label: '其他指标',
        data: yyData,
        backgroundColor: '#ff6384',
        borderColor: '#ff6384',
        borderWidth: 2,
        tension: 0.3,
        yAxisID: 'y'
      },
      {
        label: '农业总产值',
        data: nyszcData,
        backgroundColor: '#36a2eb',
        borderColor: '#36a2eb',
        borderWidth: 2,
        tension: 0.3,
        yAxisID: 'y1'
      }
    ]
  }
})

const relatedIndexChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      type: 'linear',
      display: true,
      position: 'left',
      title: {
        display: true,
        text: '其他指标',
        font: {
          size: 14
        }
      },
      min: 0,
      max: 60000,
      ticks: {
        stepSize: 5000
      }
    },
    y1: {
      type: 'linear',
      display: true,
      position: 'right',
      title: {
        display: true,
        text: '农业总产值',
        font: {
          size: 14
        }
      },
      min: 0,
      max: 350000,
      ticks: {
        stepSize: 50000
      },
      grid: {
        drawOnChartArea: false
      }
    }
  },
  interaction: {
    mode: 'index',
    intersect: false
  }
}

// 另一指标图表数据
const anotherIndexChartData = computed(() => {
  const labels = tableData.value.map(item => item.year)
  const fyData = tableData.value.map(item => parseFloat(item.fy))

  return {
    labels,
    datasets: [
      {
        label: '另一指标',
        data: fyData,
        backgroundColor: labels.map((_, i) =>
          i % 2 === 0 ? '#9966ff' : '#ff9f40'
        ),
        borderColor: labels.map((_, i) =>
          i % 2 === 0 ? '#9966ff' : '#ff9f40'
        ),
        borderWidth: 1
      }
    ]
  }
})

const anotherIndexChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `指标值: ${context.raw.toLocaleString()}`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '指标值',
        font: {
          size: 14
        }
      },
      min: 0,
      max: 1000,
      ticks: {
        stepSize: 5000
      }
    }
  }
}

// 饼图数据
const pieChartData = computed(() => {
  const labels = tableData.value.map(item => item.year)
  const data = tableData.value.map(item => parseFloat(item.nyzcz))

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
          return `${label}: ${value.toLocaleString()} (${percentage}%)`
        }
      }
    }
  }
}

// 标签类型
const getTotalValueTagType = (value) => {
  const num = parseFloat(value)
  if (num > 200000) return 'danger'
  if (num > 100000) return 'warning'
  if (num > 50000) return 'success'
  return 'info'
}

const getOtherTagType = (value) => {
  const num = parseFloat(value)
  if (num > 10000) return 'danger'
  if (num > 5000) return 'warning'
  if (num > 1000) return 'success'
  return 'info'
}

const getAnotherTagType = (value) => {
  const num = parseFloat(value)
  if (num > 1000) return 'danger'
  if (num > 500) return 'warning'
  if (num > 100) return 'success'
  return 'info'
}

// 表格排序
const handleSortChange = ({ column, prop, order }) => {
  if (!prop || !order) return
  
  const sortedData = [...rawData.value].sort((a, b) => {
    const valueA = parseFloat(a[prop])
    const valueB = parseFloat(b[prop])
    return order === 'ascending' ? valueA - valueB : valueB - valueA
  })
  
  rawData.value = sortedData
  ElMessage.info(`按${column.label} ${order === 'ascending' ? '升序' : '降序'}排序`)
}

// 搜索过滤
const filteredTableData = computed(() => {
  if (!searchQuery.value) return tableData.value
  return tableData.value.filter(item => {
    return Object.values(item).some(val => 
      String(val).toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

// 计算增长率
const getGrowthRate = (value) => {
  const num = parseFloat(value)
  const avg = rawData.value.reduce((sum, item) => sum + parseFloat(item.nyzcz), 0) / rawData.value.length
  return ((num - avg) / avg * 100).toFixed(1)
}

// 获取进度条颜色
const getProgressColor = (value) => {
  const num = parseFloat(value)
  if (num > 50) return '#67C23A'
  if (num > 0) return '#E6A23C'
  return '#F56C6C'
}

// 计算数值百分比
const getValuePercentage = (value) => {
  const num = parseFloat(value)
  const max = Math.max(...rawData.value.map(item => parseFloat(item.nyzcz)))
  return (num / max * 100).toFixed(1)
}

// 百分比格式化
const percentageFormat = (val) => {
  return val + '%'
}

// 年度趋势数据
const getYearTrendData = (year) => {
  if (!year) return null
  
  const years = rawData.value.map(item => item.year).sort()
  const values = years.map(y => {
    const item = rawData.value.find(d => d.year === y)
    return parseFloat(item.nyzcz)
  })

  return {
    labels: years,
    datasets: [
      {
        label: '农业总产值',
        data: values,
        borderColor: '#409EFF',
        tension: 0.4,
        fill: false
      }
    ]
  }
}

const trendChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
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
        text: '总产值'
      }
    }
  }
}

// 查看年度详情
const showYearDetail = (row) => {
  selectedYear.value = row
  dialogVisible.value = true
}

// 显示指标详情
const showIndexDetail = () => {
  ElMessage.info('指标详情功能开发中')
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

// 编辑数据
const editData = () => {
  ElMessage.info('编辑功能开发中')
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
.total-value {
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

.primary .stat-icon {
  color: #409EFF;
}

.success .stat-icon {
  color: #67C23A;
}

.warning .stat-icon {
  color: #E6A23C;
}

.info .stat-icon {
  color: #909399;
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

.value-cell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.expand-content {
  padding: 20px;
}

.trend-analysis {
  margin-top: 20px;
}

.trend-analysis h4 {
  margin-bottom: 15px;
  color: #606266;
}

.analysis-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
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
  .total-value {
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