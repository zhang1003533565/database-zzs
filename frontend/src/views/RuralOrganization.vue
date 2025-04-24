<template>
  <AppLayout>
    <div class="rural-organization">
      <h2>农村基层组织</h2>

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
        <!-- 柱状图/折线图 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>各村镇年末人口数对比</span>
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
              <span>年末居住户数分布比例</span>
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
          :data="sortedTableData"
          border
          style="width: 100%"
          :default-sort = "{prop: 'ncrk', order: 'descending'}"
        >
          <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
          <el-table-column prop="jz" label="镇/街道" sortable></el-table-column>
          <el-table-column prop="cmxz" label="村民小组数" sortable></el-table-column>
          <el-table-column prop="ncrk" label="年末人口数" sortable></el-table-column>
          <el-table-column prop="cmwyh" label="村民委员会数" sortable></el-table-column>
          <el-table-column prop="ncjzrk" label="年末居住人口数" sortable></el-table-column>
          <el-table-column prop="ncjzhs" label="年末居住户数" sortable></el-table-column>
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

// 模拟API请求
const fetchData = async () => {
  // 实际项目中这里应该是真实的API调用
  return [
    {
        "id": "1",
        "jz": "朱家角镇",
        "cmxz": "348",
        "ncrk": "44819",
        "cmwyh": "28",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "18414",
        "ncjzhs": "7988"
    },
    {
        "id": "2",
        "jz": "练塘镇",
        "cmxz": "409",
        "ncrk": "50019",
        "cmwyh": "25",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "25607",
        "ncjzhs": "14124"
    },
    {
        "id": "3",
        "jz": "金泽镇",
        "cmxz": "432",
        "ncrk": "54275",
        "cmwyh": "30",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "29371",
        "ncjzhs": "15086"
    },
    {
        "id": "4",
        "jz": "华新镇",
        "cmxz": "227",
        "ncrk": "32349",
        "cmwyh": "19",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "25854",
        "ncjzhs": "7441"
    },
    {
        "id": "5",
        "jz": "重固镇",
        "cmxz": "144",
        "ncrk": "16869",
        "cmwyh": "9",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "7766",
        "ncjzhs": "3150"
    },
    {
        "id": "6",
        "jz": "赵巷镇",
        "cmxz": "128",
        "ncrk": "21035",
        "cmwyh": "8",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "8399",
        "ncjzhs": "2799"
    },
    {
        "id": "7",
        "jz": "徐泾镇",
        "cmxz": "108",
        "ncrk": "25154",
        "cmwyh": "9",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "19770",
        "ncjzhs": "5649"
    },
    {
        "id": "8",
        "jz": "白鹤镇",
        "cmxz": "322",
        "ncrk": "40471",
        "cmwyh": "21",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "29880",
        "ncjzhs": "9943"
    },
    {
        "id": "9",
        "jz": "夏阳街道",
        "cmxz": "91",
        "ncrk": "11907",
        "cmwyh": "8",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "5875",
        "ncjzhs": "2204"
    },
    {
        "id": "10",
        "jz": "香花桥街道",
        "cmxz": "296",
        "ncrk": "32498",
        "cmwyh": "22",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "5317",
        "ncjzhs": "2263"
    },
    {
        "id": "11",
        "jz": "盈浦街道",
        "cmxz": "61",
        "ncrk": "6716",
        "cmwyh": "5",
        "dsjzx_taskid": "20250411",
        "ncjzrk": "140",
        "ncjzhs": "78"
    }
  ]
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

  const totalNcrk = rawData.value.reduce((sum, item) => sum + parseInt(item.ncrk), 0)
  const totalNcjzhs = rawData.value.reduce((sum, item) => sum + parseInt(item.ncjzhs), 0)
  const avgNcjzrk = (rawData.value.reduce((sum, item) => sum + parseInt(item.ncjzrk), 0) / rawData.value.length).toFixed(1)

  return [
    {
      title: '总年末人口数',
      value: totalNcrk,
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月增加8%'
    },
    {
      title: '总年末居住户数',
      value: totalNcjzhs,
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上月持平'
    },
    {
      title: '平均年末居住人口数',
      value: avgNcjzrk + '人',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月提升3%'
    },
    {
      title: '涉及村镇数',
      value: rawData.value.length,
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '覆盖全部村镇'
    }
  ]
})

// 表格数据（按ID排序）
const sortedTableData = computed(() => {
  return [...rawData.value].sort((a, b) => parseInt(a.id) - parseInt(b.id))
})

// 柱状图/折线图数据（按ID排序）
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

// 饼图数据（按ID排序）
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

// 导出数据
const exportData = () => {
  ElMessage.success('导出数据成功')
  // 实际项目中这里应该实现导出逻辑
}
</script>

<style scoped>
.rural-organization {
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