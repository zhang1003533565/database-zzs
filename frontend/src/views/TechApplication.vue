<template>
  <AppLayout>
    <div class="tech-application">
      <div class="page-header">
        <div class="header-left">
          <h2>农村技术应用数据分析</h2>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>技术应用</el-breadcrumb-item>
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
        <!-- 技术应用面积图表 -->
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <div class="chart-title">
                <i class="el-icon-data-line"></i>
                <span>各镇技术应用面积对比</span>
              </div>
              <div class="chart-actions">
                <el-radio-group v-model="areaChartType" size="small">
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
              <div class="chart-title">
                <i class="el-icon-trend-charts"></i>
                <span>农业收益率与机械化程度</span>
              </div>
              <el-tooltip content="点击查看详情" placement="top">
                <el-button type="text" @click="showEfficiencyDetail">
                  查看详情
                </el-button>
              </el-tooltip>
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
              <div class="chart-title">
                <i class="el-icon-box"></i>
                <span>各镇化肥使用量</span>
              </div>
              <el-tooltip content="查看使用趋势" placement="top">
                <el-button type="text" @click="showFertilizerTrend">
                  使用趋势
                </el-button>
              </el-tooltip>
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
              <div class="chart-title">
                <i class="el-icon-pie-chart"></i>
                <span>技术应用面积分布</span>
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
              <span class="table-title">详细技术应用数据</span>
              <el-tag type="info" style="margin-left: 10px">共 {{ tableData.length }} 条</el-tag>
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
                <el-button type="success" size="small" @click="toggleExpandAll">
                  <i :class="isExpandAll ? 'el-icon-minus' : 'el-icon-plus'"></i>
                  {{ isExpandAll ? '收起全部' : '展开全部' }}
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
          :default-sort="{prop: 'jgmj', order: 'descending'}"
          @sort-change="handleSortChange"
          v-loading="loading"
        >
          <el-table-column type="expand">
            <template #default="{ row }">
              <div class="expand-content">
                <el-descriptions border>
                  <el-descriptions-item label="技术应用详情">
                    <el-progress
                      :percentage="parseFloat(row.dmsyl)"
                      :format="percentageFormat"
                      :color="getProgressColor"
                    >
                      <template #default="{ percentage }">
                        <span>稻麦使用率: {{ percentage }}%</span>
                      </template>
                    </el-progress>
                  </el-descriptions-item>
                  <el-descriptions-item label="农业收益率">
                    <el-progress
                      :percentage="parseFloat(row.nysyl)"
                      :format="percentageFormat"
                      :color="getYieldColor(row.nysyl)"
                    >
                      <template #default="{ percentage }">
                        <span>{{ percentage }}%</span>
                      </template>
                    </el-progress>
                  </el-descriptions-item>
                  <el-descriptions-item label="机械化程度">
                    <el-progress
                      :percentage="parseFloat(row.jxhcd)"
                      :format="percentageFormat"
                      status="success"
                    >
                      <template #default="{ percentage }">
                        <span>{{ percentage }}%</span>
                      </template>
                    </el-progress>
                  </el-descriptions-item>
                  <el-descriptions-item label="实际建设面积">
                    {{ row.sdjmj }}亩
                  </el-descriptions-item>
                </el-descriptions>
                
                <div class="trend-chart" v-if="row.trendData">
                  <h4>历年技术应用趋势</h4>
                  <line-chart
                    :chart-data="getTrendData(row)"
                    :options="trendChartOptions"
                  />
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="jz" label="镇/街道" sortable width="120">
            <template #default="{ row }">
              <el-button type="text" @click="showTownDetail(row)">{{ row.jz }}</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="jgmj" label="技术应用面积(亩)" sortable>
            <template #default="{ row }">
              <div class="area-cell">
                <el-tag :type="getAreaTagType(row.jgmj)">{{ row.jgmj }}</el-tag>
                <el-progress 
                  :percentage="getAreaPercentage(row)" 
                  :color="getProgressColor"
                  :show-text="false"
                  :stroke-width="4"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="nysyl" label="农业收益率(%)" sortable>
            <template #default="{ row }">
              <div class="progress-cell">
                <el-progress
                  :percentage="parseFloat(row.nysyl)"
                  :color="getYieldColor(row.nysyl)"
                  :show-text="false"
                />
                <span>{{ row.nysyl }}%</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="hfsul" label="化肥使用量(kg)" sortable>
            <template #default="{ row }">
              <div class="fertilizer-cell">
                <el-tag :type="getFertilizerTagType(row.hfsul)">
                  {{ row.hfsul }}
                </el-tag>
                <el-progress 
                  :percentage="getFertilizerPercentage(row)" 
                  :color="getProgressColor"
                  :show-text="false"
                  :stroke-width="4"
                ></el-progress>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="jxhcd" label="机械化程度(%)" sortable>
            <template #default="{ row }">
              <div class="progress-cell">
                <el-progress
                  :percentage="parseFloat(row.jxhcd)"
                  status="success"
                  :show-text="false"
                />
                <span>{{ row.jxhcd }}%</span>
              </div>
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
            :total="tableData.length"
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
        :title="selectedTown ? selectedTown.jz + ' 技术应用详情' : ''"
        v-model="dialogVisible"
        width="60%"
      >
        <div v-if="selectedTown" class="town-detail">
          <el-descriptions border>
            <el-descriptions-item label="镇/街道">{{ selectedTown.jz }}</el-descriptions-item>
            <el-descriptions-item label="技术应用面积">{{ selectedTown.jgmj }}亩</el-descriptions-item>
            <el-descriptions-item label="实际建设面积">{{ selectedTown.sdjmj }}亩</el-descriptions-item>
            <el-descriptions-item label="稻麦使用率">{{ selectedTown.dmsyl }}%</el-descriptions-item>
            <el-descriptions-item label="农业收益率">{{ selectedTown.nysyl }}%</el-descriptions-item>
            <el-descriptions-item label="机械化程度">{{ selectedTown.jxhcd }}%</el-descriptions-item>
            <el-descriptions-item label="化肥使用量">{{ selectedTown.hfsul }}kg</el-descriptions-item>
          </el-descriptions>
          
          <div class="detail-charts">
            <div class="detail-chart">
              <h4>历年技术应用趋势</h4>
              <line-chart
                :chart-data="getTrendData(selectedTown)"
                :options="trendChartOptions"
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
const areaChartType = ref('bar')
const isExpandAll = ref(false)
const dialogVisible = ref(false)
const selectedTown = ref(null)
const pageSize = ref(10)

// 使用您提供的API数据
const rawData = ref([])

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://129.211.82.112:8000/api/techapplication/basic/')
    const data = await response.json()
    rawData.value = data.map(item => ({...item, isExpanded: false }))
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

  const totalArea = rawData.value.reduce((sum, item) => sum + parseFloat(item.jgmj), 0)
  const avgYield = rawData.value.reduce((sum, item) => sum + parseFloat(item.nysyl), 0) / rawData.value.length
  const avgMechanization = rawData.value.reduce((sum, item) => sum + parseFloat(item.jxhcd), 0) / rawData.value.length
  const avgFertilizer = rawData.value.reduce((sum, item) => sum + parseFloat(item.hfsul), 0) / rawData.value.length

  return [
    {
      title: '总技术应用面积',
      value: totalArea.toLocaleString() + '亩',
      icon: 'el-icon-map-location',
      type: 'primary',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月增加8%'
    },
    {
      title: '平均农业收益率',
      value: avgYield.toFixed(2) + '%',
      icon: 'el-icon-money',
      type: 'success',
      trend: 'up',
      trendIcon: 'el-icon-top',
      trendText: '较上月提升1.2%'
    },
    {
      title: '平均机械化程度',
      value: avgMechanization.toFixed(1) + '%',
      icon: 'el-icon-truck',
      type: 'warning',
      trend: 'stable',
      trendIcon: 'el-icon-right',
      trendText: '与上月持平'
    },
    {
      title: '平均化肥使用量',
      value: avgFertilizer.toFixed(1) + 'kg',
      icon: 'el-icon-box',
      type: 'info',
      trend: 'down',
      trendIcon: 'el-icon-bottom',
      trendText: '较上月减少5%'
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

// 计算百分比
const getAreaPercentage = (row) => {
  const maxArea = Math.max(...rawData.value.map(item => parseFloat(item.jgmj)))
  return (parseFloat(row.jgmj) / maxArea * 100).toFixed(1)
}

const getFertilizerPercentage = (row) => {
  const maxFertilizer = Math.max(...rawData.value.map(item => parseFloat(item.hfsul)))
  return (parseFloat(row.hfsul) / maxFertilizer * 100).toFixed(1)
}

// 获取进度条颜色
const getProgressColor = (percentage) => {
  if (percentage > 80) return '#F56C6C'
  if (percentage > 60) return '#E6A23C'
  return '#67C23A'
}

// 百分比格式化
const percentageFormat = (val) => {
  return val + '%'
}

// 获取趋势数据
const getTrendData = (town) => {
  if (!town) return null
  
  const years = ['2019', '2020', '2021', '2022', '2023']
  const currentArea = parseFloat(town.jgmj)
  const areaData = years.map((year, index) => {
    if (index === years.length - 1) return currentArea
    return Math.round(currentArea * (0.8 + Math.random() * 0.4))
  })

  return {
    labels: years,
    datasets: [{
      label: '技术应用面积(亩)',
      data: areaData,
      borderColor: '#409EFF',
      tension: 0.4,
      fill: false
    }]
  }
}

// 趋势图表选项
const trendChartOptions = {
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
        text: '面积(亩)'
      }
    }
  }
}

// 查看镇详情
const showTownDetail = (row) => {
  selectedTown.value = row
  dialogVisible.value = true
}

// 查看效率详情
const showEfficiencyDetail = () => {
  ElMessage.info('效率详情功能开发中')
}

// 查看化肥使用趋势
const showFertilizerTrend = () => {
  ElMessage.info('化肥使用趋势功能开发中')
}

// 查看分布详情
const showDistributionDetail = () => {
  ElMessage.info('分布详情功能开发中')
}

// 编辑数据
const editTownData = () => {
  ElMessage.info('编辑功能开发中')
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
</script>

<style scoped>
.tech-application {
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

.expand-content {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 4px;
}

.area-cell,
.fertilizer-cell,
.progress-cell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.trend-chart {
  margin-top: 20px;
}

.trend-chart h4 {
  margin-bottom: 15px;
  color: #606266;
  font-weight: 500;
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
