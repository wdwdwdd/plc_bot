<template>
  <div class="data-table">
    <div class="table-filters">
      <select v-model="selectedDevice">
        <option v-for="device in devices" :key="device.id" :value="device.id">
          {{ device.name }}
        </option>
      </select>
      <select v-model="timeRange">
        <option value="1">最近1小时</option>
        <option value="24">最近24小时</option>
        <option value="168">最近7天</option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>时间</th>
          <th>数据点</th>
          <th>数值</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in tableData" :key="item.id">
          <td>{{ formatTime(item.timestamp) }}</td>
          <td>{{ item.point_name }}</td>
          <td>{{ formatValue(item.value) }}</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  data() {
    return {
      selectedDevice: null,
      timeRange: '24',
      currentPage: 1,
      tableData: [],
      devices: []
    }
  },
  async created() {
    try {
      const res = await fetch('/api/devices/')
      this.devices = await res.json()
      if (this.devices.length) {
        this.selectedDevice = this.devices[0].id
        await this.fetchData()
      }
    } catch (e) {
      console.error('加载设备失败', e)
    }
  },
  methods: {
    async fetchData() {
      if (!this.selectedDevice) return
      try {
        const response = await fetch(
          `/api/data/recent/${this.selectedDevice}?hours=${this.timeRange}`
        )
        this.tableData = await response.json()
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    },

    formatTime(timestamp) {
      return new Date(timestamp).toLocaleString()
    },

    formatValue(value) {
      return typeof value === 'number' ? value.toFixed(2) : value
    }
  },

  watch: {
    selectedDevice() {
      this.fetchData()
    },
    timeRange() {
      this.fetchData()
    }
  }
}
</script>

<style scoped>
.data-table {
  margin: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: left;
}

.table-filters {
  margin-bottom: 20px;
}

.table-filters select {
  margin-right: 10px;
  padding: 5px;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.pagination button {
  margin: 0 10px;
  padding: 5px 10px;
}
</style>
