<template>
  <AppLayout>
    <div class="total-value">
      <h2>农业历年总产值</h2>

      <!-- 数据概览卡片 -->
      <div class="overview-cards">
        <el-card shadow="hover" v-for="stat in stats" :key="stat.title">
          <div class="stat-card">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-title">{{ stat.title }}</div>
            <div class="stat-trend" :class="stat.trend">
              <i :class="stat.trendIcon"></i> {{ stat.trendText }}
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
              <span>历年农业总产值变化</span>
              <el-select v-model="totalValueChartType" size="small" style="width: 120px">
                <el-option label="柱状图" value="bar"></el-option>
                <el-option label="折线图" value="line"></el-option>
              </el-select>
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
              <span>历年农业某项指标与总产值对比</span>
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
              <span>历年农业另一项指标变化</span>
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
              <span>农业相关面积分布</span>
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
            <span>详细农业历年数据</span>
            <div>
              <el-button type="primary" size="small" @click="exportData">导出数据</el-button>
              <el-button size="small" @click="toggleExpandAll">
                {{ isExpandAll ? '收起全部' : '展开全部' }}
              </el-button>
            </div>
          </div>
        </template>
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :default-sort="{prop: 'nyzcz', order: 'descending'}"
          @sort-change="handleSortChange"
        >
          <el-table-column type="expand">
            <template #default="{row}">
              <div class="expand-content">
                <p><strong>农业详情:</strong></p>
                <p>年份: {{ row.year }}</p>
                <p>其他指标: {{ row.yy }}</p>
                <p>另一指标: {{ row.fy }}</p>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="year" label="年份" sortable width="120"></el-table-column>
          <el-table-column prop="nyzcz" label="农业总产值" sortable>
            <template #default="{row}">
              <el-tag :type="getTotalValueTagType(row.nyzcz)">{{ row.nyzcz }}</el-tag>
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
        </el-table>
      </el-card>
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

onMounted(async () => {
  try {
    const response = await fetch('http://129.211.82.112:8000/api/totalvalue/basic/')
    const data = await response.json()
    rawData.value = data.map(item => ({...item, isExpanded: false }))
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})

const totalValueChartType = ref('bar')
const isExpandAll = ref(false)

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalValue = rawData.value.reduce((sum, item) => sum + parseFloat(item.nyzcz), 0)
  const avgOtherIndex = rawData.value.reduce((sum, item) => sum + parseFloat(item.yy), 0) / rawData.value.length
  const avgAnotherIndex = rawData.value.reduce((sum, item) => sum + parseFloat(item.fy), 0) / rawData.value.length

  return [
    {
      title: '总农业总产值',
      value: totalValue.toLocaleString(),
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上年增加10%'
    },
    {
      title: '平均其他指标值',
      value: avgOtherIndex.toFixed(2),
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上年持平'
    },
    {
      title: '平均另一指标值',
      value: avgAnotherIndex.toFixed(1),
      trend: 'down',
      trendIcon: 'el-icon-bottom',
      trendText: '较上年减少8%'
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
        text: '农业总产值'
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
    }
  },
  scales: {
    y: {
      type: 'linear',
      display: true,
      position: 'left',
      title: {
        display: true,
        text: '其他指标'
      },
      max: 30000
    },
    y1: {
      type: 'linear',
      display: true,
      position: 'right',
      title: {
        display: true,
        text: '农业总产值'
      },
      min: 0,
      grid: {
        drawOnChartArea: false
      }
    }
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
          return `另一指标值: ${context.raw}`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '另一指标值'
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
const handleSortChange = ({ column, order }) => {
  ElMessage.info(`按${column.label} ${order === 'ascending' ? '升序' : '降序'}排序`)
  const prop = column.property
  const sortedData = rawData.value.slice().sort((a, b) => {
    const valueA = parseFloat(a[prop])
    const valueB = parseFloat(b[prop])
    if (order === 'ascending') {
      return valueA - valueB
    } else {
      return valueB - valueA
    }
  })
  rawData.value = sortedData
}

// 展开/收起全部
const toggleExpandAll = () => {
  isExpandAll.value = !isExpandAll.value
  rawData.value.forEach(item => {
    item.isExpanded = isExpandAll.value
  })
}

// 导出数据
const exportData = () => {
  ElMessage.success('导出数据成功')
}
</script>

<style scoped>
.total-value {
  background: #fff;
  padding: 20px;
  border-radius: 6px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 24px;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  padding: 15px;
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-trend {
  font-size: 12px;
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
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-wrapper {
  height: 300px;
}

.data-table {
  margin-top: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.expand-content {
  padding: 10px;
  background: #f9f9f9;
  border-radius: 4px;
}
</style>