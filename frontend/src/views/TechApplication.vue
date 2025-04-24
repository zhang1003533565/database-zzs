<template>
  <AppLayout>
    <div class="tech-application">
      <h2>农村技术应用数据分析</h2>

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
        <!-- 技术应用面积图表 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>各镇技术应用面积对比</span>
              <el-select v-model="areaChartType" size="small" style="width: 120px">
                <el-option label="柱状图" value="bar"></el-option>
                <el-option label="折线图" value="line"></el-option>
              </el-select>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              v-if="areaChartType === 'bar'"
              :chart-data="areaChartData"
              :options="areaChartOptions"
            />
            <line-chart
              v-else
              :chart-data="areaChartData"
              :options="areaChartOptions"
            />
          </div>
        </el-card>

        <!-- 收益率图表 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>农业收益率与机械化程度</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <line-chart
              :chart-data="efficiencyChartData"
              :options="efficiencyChartOptions"
            />
          </div>
        </el-card>
      </div>

      <!-- 第二行图表 -->
      <div class="chart-container">
        <!-- 化肥使用量图表 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>各镇化肥使用量</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              :chart-data="fertilizerChartData"
              :options="fertilizerChartOptions"
            />
          </div>
        </el-card>

        <!-- 面积分布饼图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>技术应用面积分布</span>
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
            <span>详细技术应用数据</span>
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
          :default-sort="{prop: 'jgmj', order: 'descending'}"
          @sort-change="handleSortChange"
        >
          <el-table-column type="expand">
            <template #default="{row}">
              <div class="expand-content">
                <p><strong>技术应用详情:</strong></p>
                <p>稻麦使用率: {{ row.dmsyl }}%</p>
                <p>农业收益率: {{ row.nysyl }}%</p>
                <p>机械化程度: {{ row.jxhcd }}%</p>
                <p>实际建设面积: {{ row.sdjmj }}亩</p>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="jz" label="镇/街道" sortable width="120"></el-table-column>
          <el-table-column prop="jgmj" label="技术应用面积(亩)" sortable>
            <template #default="{row}">
              <el-tag :type="getAreaTagType(row.jgmj)">{{ row.jgmj }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="nysyl" label="农业收益率(%)" sortable>
            <template #default="{row}">
              <el-progress
                :percentage="parseFloat(row.nysyl)"
                :color="getYieldColor(row.nysyl)"
                :show-text="false"
              />
              <span style="margin-left: 8px">{{ row.nysyl }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="hfsul" label="化肥使用量(kg)" sortable>
            <template #default="{row}">
              <el-tag :type="getFertilizerTagType(row.hfsul)">
                {{ row.hfsul }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="jxhcd" label="机械化程度(%)" sortable>
            <template #default="{row}">
              <el-progress
                :percentage="parseFloat(row.jxhcd)"
                status="success"
                :show-text="false"
              />
              <span style="margin-left: 8px">{{ row.jxhcd }}</span>
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
    const response = await fetch('http://127.0.0.1:8000/api/techapplication/basic/')
    const data = await response.json()
    rawData.value = data.map(item => ({...item, isExpanded: false })) // 添加isExpanded属性并初始化为false
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})

const areaChartType = ref('bar')
const isExpandAll = ref(false)

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalArea = rawData.value.reduce((sum, item) => sum + parseFloat(item.jgmj), 0)
  const avgYield = rawData.value.reduce((sum, item) => sum + parseFloat(item.nysyl), 0) / rawData.value.length
  const avgMechanization = rawData.value.reduce((sum, item) => sum + parseFloat(item.jxhcd), 0) / rawData.value.length
  const avgFertilizer = rawData.value.reduce((sum, item) => sum + parseFloat(item.hfsul), 0) / rawData.value.length

  return [
    {
      title: '总技术应用面积',
      value: totalArea.toLocaleString() + '亩',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月增加8%'
    },
    {
      title: '平均农业收益率',
      value: avgYield.toFixed(2) + '%',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月提升1.2%'
    },
    {
      title: '平均机械化程度',
      value: avgMechanization.toFixed(1) + '%',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上月持平'
    },
    {
      title: '平均化肥使用量',
      value: avgFertilizer.toFixed(1) + 'kg',
      trend: 'down',
      trendIcon: 'el-icon-bottom',
      trendText: '较上月减少5%'
    }
  ]
})

// 表格数据
const tableData = computed(() => {
  return rawData.value.slice()
})

// 面积图表数据
const areaChartData = computed(() => {
  const labels = tableData.value.map(item => item.jz)
  const jgmjData = tableData.value.map(item => parseFloat(item.jgmj))
  const sdjmjData = tableData.value.map(item => parseFloat(item.sdjmj))

  return {
    labels,
    datasets: [
      {
        label: '技术应用面积(亩)',
        data: jgmjData,
        backgroundColor: '#36a2eb',
        borderColor: '#36a2eb',
        borderWidth: 1
      },
      {
        label: '实际建设面积(亩)',
        data: sdjmjData,
        backgroundColor: '#4bc0c0',
        borderColor: '#4bc0c0',
        borderWidth: 1
      }
    ]
  }
})

const areaChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.raw.toLocaleString()}亩`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '面积(亩)'
      }
    }
  }
}

// 收益率图表数据
const efficiencyChartData = computed(() => {
  const labels = tableData.value.map(item => item.jz)
  const nysylData = tableData.value.map(item => parseFloat(item.nysyl))
  const jxhcdData = tableData.value.map(item => parseFloat(item.jxhcd))

  return {
    labels,
    datasets: [
      {
        label: '农业收益率(%)',
        data: nysylData,
        backgroundColor: '#ff6384',
        borderColor: '#ff6384',
        borderWidth: 2,
        tension: 0.3,
        yAxisID: 'y'
      },
      {
        label: '机械化程度(%)',
        data: jxhcdData,
        backgroundColor: '#ffcd56',
        borderColor: '#ffcd56',
        borderWidth: 2,
        tension: 0.3,
        yAxisID: 'y1'
      }
    ]
  }
})

const efficiencyChartOptions = {
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
        text: '农业收益率(%)'
      },
      max: 50
    },
    y1: {
      type: 'linear',
      display: true,
      position: 'right',
      title: {
        display: true,
        text: '机械化程度(%)'
      },
      min: 0,
      max: 100,
      grid: {
        drawOnChartArea: false
      }
    }
  }
}

// 化肥使用量图表
const fertilizerChartData = computed(() => {
  const labels = tableData.value.map(item => item.jz)
  const hfsulData = tableData.value.map(item => parseFloat(item.hfsul))

  return {
    labels,
    datasets: [
      {
        label: '化肥使用量(kg)',
        data: hfsulData,
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

const fertilizerChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `化肥使用量: ${context.raw}kg`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '化肥使用量(kg)'
      }
    }
  }
}

// 饼图数据
const pieChartData = computed(() => {
  const labels = tableData.value.map(item => item.jz)
  const data = tableData.value.map(item => parseFloat(item.jgmj))

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
          return `${label}: ${value.toLocaleString()}亩 (${percentage}%)`
        }
      }
    }
  }
}

// 标签类型
const getAreaTagType = (value) => {
  const num = parseFloat(value)
  if (num > 20000) return 'danger'
  if (num > 10000) return 'warning'
  if (num > 5000) return 'success'
  return 'info'
}

const getFertilizerTagType = (value) => {
  const num = parseFloat(value)
  if (num > 2000) return 'danger'
  if (num > 1000) return 'warning'
  if (num > 500) return 'success'
  return 'info'
}

const getYieldColor = (value) => {
  const num = parseFloat(value)
  if (num > 30) return '#67C23A'
  if (num > 15) return '#E6A23C'
  return '#F56C6C'
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
  // 实际项目中这里应该实现导出逻辑
}
</script>

<style scoped>
.tech-application {
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
  grid-template-columns: repeat(4, 1fr);
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
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-wrapper {
  height: calc(100% - 60px);
  position: relative;
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

.expand-content p {
  margin: 5px 0;
}

@media (max-width: 1200px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
}
</style>
