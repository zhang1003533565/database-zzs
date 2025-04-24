<template>
  <AppLayout>
    <div class="agriculture-main-index">
      <h2>农业主要指标</h2>

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
              <span>各类农产品产量对比</span>
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
              <span>农业各产业占比</span>
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
          :default-sort="{prop: 'ze2023', order: 'descending'}"
        >
          <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
          <el-table-column prop="zb" label="指标" sortable></el-table-column>
          <el-table-column prop="ze2023" label="2023年数值" sortable>
            <template #default="{row}">
              <el-tag :type="getTagType(row.ze2023)">{{ row.ze2023 }}{{ row.dw }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ze_last_year" label="去年数值" sortable>
            <template #default="{row}">
              <el-tag :type="getTagType(row.ze_last_year)">{{ row.ze_last_year }}{{ row.dw }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="growthRate" label="增长率" sortable>
            <template #default="{row}">
              {{ calculateGrowthRate(row) }}%
            </template>
          </el-table-column>
        </el-table>
      </el-card> <!-- 这里添加了正确的结束标签 -->
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

// 模拟API请求
const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/mainindex/basic/');
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

// 统计数据
const stats = computed(() => {
  if (rawData.value.length === 0) return []

  const totalProduction2023 = rawData.value.reduce((sum, item) => sum + parseFloat(item.ze2023), 0)
  const totalProductionLastYear = rawData.value.reduce((sum, item) => sum + parseFloat(item.ze_last_year), 0)
  const growthRate = ((totalProduction2023 - totalProductionLastYear) / totalProductionLastYear * 100).toFixed(1)

  return [
    {
      title: '2023年农业总产量',
      value: totalProduction2023.toFixed(2),
      trend: growthRate > 0? 'up' : growthRate < 0? 'down' :'stable',
      trendIcon: growthRate > 0? 'el-icon-top' : growthRate < 0? 'el-icon-bottom' : 'el-icon-right',
      trendText: growthRate > 0? `较去年增长${growthRate}%` : growthRate < 0? `较去年下降${Math.abs(parseFloat(growthRate))}%` : '与去年持平'
    },
    {
      title: '指标数量',
      value: rawData.value.length,
      trend:'stable',
      trendIcon: 'el-icon-right',
      trendText: '无变化'
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
</script>

<style scoped>
.agriculture-main-index {
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
  grid-template-columns: repeat(2, 1fr);
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
    grid-template-columns: repeat(1, 1fr);
  }

 .chart-container {
    grid-template-columns: 1fr;
  }
}
</style>