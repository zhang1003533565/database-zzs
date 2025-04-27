<template>
  <AppLayout>
    <div class="health-organization">
      <h2>农村卫生组织分布情况</h2>

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
        <!-- 柱状图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>各村镇卫生所数量对比</span>
              <el-select v-model="chartType" size="small" style="width: 120px">
                <el-option label="柱状图" value="bar"></el-option>
                <el-option label="折线图" value="line"></el-option>
              </el-select>
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
              <span>卫生所分布比例</span>
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
            <span>详细数据</span>
            <el-button type="primary" size="small" @click="exportData">导出数据</el-button>
          </div>
        </template>
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :default-sort = "{prop: 'xcyss', order: 'descending'}"
        >
          <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
          <el-table-column prop="zhen" label="镇/街道" sortable></el-table-column>
          <el-table-column prop="xcyss" label="乡村卫生室数" sortable>
            <template #default="{row}">
              <el-tag :type="getTagType(row.xcyss)">{{ row.xcyss }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="xzcs" label="行政村数" sortable></el-table-column>
          <el-table-column prop="ratio" label="卫生室覆盖率" sortable>
            <template #default="{row}">
              {{ calculateRatio(row) }}%
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

const fetchData = async () => {
  try {
    const response = await fetch('http://129.211.82.112:8000//api/health/basic/');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('获取数据失败:', error);
    throw error;
  }
}


const rawData = ref([])
const chartType = ref('bar')

// 获取数据
onMounted(async () => {
  try {
    rawData.value = await fetchData()
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
})

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalXcyss = rawData.value.reduce((sum, item) => sum + parseInt(item.xcyss), 0)
  const totalXzcs = rawData.value.reduce((sum, item) => sum + parseInt(item.xzcs), 0)
  const avgCoverage = (totalXcyss / totalXzcs * 100).toFixed(1)

  return [
    {
      title: '总乡村卫生室数',
      value: totalXcyss,
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月增加5%'
    },
    {
      title: '总行政村数',
      value: totalXzcs,
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上月持平'
    },
    {
      title: '平均覆盖率',
      value: avgCoverage + '%',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月提升2%'
    },
    {
      title: '覆盖村镇数',
      value: rawData.value.length,
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '覆盖全部村镇'
    }
  ]
})

// 表格数据
const tableData = computed(() => {
  return rawData.value.map(item => ({
    ...item,
    ratio: calculateRatio(item)
  }))
})

// 计算覆盖率
const calculateRatio = (item) => {
  const xcyss = parseInt(item.xcyss)
  const xzcs = parseInt(item.xzcs)
  return xzcs === 0 ? 0 : ((xcyss / xzcs) * 100).toFixed(1)
}

// 标签类型
const getTagType = (value) => {
  const num = parseInt(value)
  if (num > 40) return 'danger'
  if (num > 20) return 'warning'
  if (num > 10) return 'success'
  return 'info'
}

// 柱状图/折线图数据
const barChartData = computed(() => {
  const labels = rawData.value.map(item => item.zhen)
  const xcyssData = rawData.value.map(item => parseInt(item.xcyss))
  const xzcsData = rawData.value.map(item => parseInt(item.xzcs))

  return {
    labels,
    datasets: [
      {
        label: '乡村卫生室数',
        data: xcyssData,
        backgroundColor: '#36a2eb',
        borderColor: '#36a2eb',
        borderWidth: 1
      },
      {
        label: '行政村数',
        data: xzcsData,
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
      }
    }
  }
}

// 饼图数据
const pieChartData = computed(() => {
  const labels = rawData.value.map(item => item.zhen)
  const data = rawData.value.map(item => parseInt(item.xcyss))

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

// 导出数据
const exportData = () => {
  ElMessage.success('导出数据成功')
  // 实际项目中这里应该实现导出逻辑
}
</script>

<style scoped>
.health-organization {
  background: #fff;
  padding: 20px;
  border-radius: 6px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 24px;
  text-align: center;
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