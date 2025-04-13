<template>
  <div>
    <el-card>
      <h2>农业主要指标列表</h2>
      <el-table :data="tableData" style="width: 100%" border>
        <el-table-column prop="dw" label="单位" width="120" />
        <el-table-column prop="ze_last_year" label="比去年增长" width="140" />
        <el-table-column prop="ze2023" label="2023年产值" width="140" />
        <el-table-column prop="zb" label="指标名称" />
        <el-table-column prop="dsjzx_taskid" label="批次号" width="140" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const tableData = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('/api/mainindex/basic/')
    tableData.value = res.data
  } catch (error) {
    console.error('获取数据失败:', error)
  }
})
</script>
