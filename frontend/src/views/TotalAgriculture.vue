<template>
  <AppLayout>
    <div class="total-agriculture">
      <h2>农业总产值概况</h2>

      <!-- 数据概览卡片 -->
      <div class="overview-cards">
        <el-card shadow="hover" v-for="stat in stats" :key="stat.title">
          <div class="stat-card">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-title">{{ stat.title }}</div>
          </div>
        </el-card>
      </div>

      <!-- 主要图表区域 -->
      <div class="chart-container">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>各地区/产值类型增长率对比</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <bar-chart
              :chart-data="chartData"
              :options="chartOptions"
            />
          </div>
        </el-card>
      </div>

      <!-- 数据表格 -->
      <el-card shadow="hover" class="data-table">
        <template #header>
          <div class="table-header">
            <span>详细农业总产值数据</span>
          </div>
        </template>
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          :default-sort="{prop: 'nyzz', order: 'descending'}"
        >
          <el-table-column prop="zbmc" label="地区/产值类型" width="150"></el-table-column>
          <el-table-column prop="nyzz" label="农业总产值增长率(%)">
            <template #default="{row}">
              <el-tag :type="getGrowthTagType(row.nyzz)">{{ row.nyzz }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="dw" label="单位"></el-table-column>
        </el-table>
      </el-card>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/components/AppLayout.vue'
import { BarChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

// 使用您提供的API数据
const rawData = ref([])

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/totalagriculture/basic/')
    const data = await response.json()
    rawData.value = data
  } catch (error) {
    console.error('Error fetching data:', error)
  }
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
      value: totalCount
    },
    {
      title: '正增长数量',
      value: positiveGrowthCount
    },
    {
      title: '负增长数量',
      value: negativeGrowthCount
    },
    {
      title: '平均增长率',
      value: avgGrowth.toFixed(2) + '%'
    }
  ]
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

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
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
        text: '增长率(%)'
      }
    }
  }
}

// 标签类型
const getGrowthTagType = (value) => {
  const num = parseFloat(value)
  if (num > 0) return 'success'
  return 'danger'
}
</script>

<style scoped>
.total-agriculture {
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

.chart-container {
  display: grid;
  grid-template-columns: 1fr;
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
</style>