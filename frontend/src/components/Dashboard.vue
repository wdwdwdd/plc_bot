<template>
  <div class="dashboard">
    <h1>PLC监控仪表盘</h1>
    <div class="device-grid">
      <DeviceCard 
        v-for="device in devices"
        :key="device.id"
        :device="device"
      />
    </div>
    <DataTable :data="productionData" />
  </div>
</template>

<script>
import DeviceCard from './DeviceCard.vue'
import DataTable from './DataTable.vue'

export default {
  name: 'Dashboard',
  components: {
    DeviceCard,
    DataTable
  },
  data() {
    return {
      devices: [],
      productionData: []
    }
  },
  async created() {
    await this.fetchDevices()
  },
  methods: {
    async fetchDevices() {
      // 实现设备数据获取逻辑
    }
  }
}
</script>
