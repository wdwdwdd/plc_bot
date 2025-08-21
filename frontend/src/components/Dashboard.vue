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
  </div>
</template>

<script>
import DeviceCard from './DeviceCard.vue'

export default {
  name: 'Dashboard',
  components: { DeviceCard },
  data() {
    return { devices: [] }
  },
  async created() {
    await this.fetchDevices()
  },
  methods: {
    async fetchDevices() {
      try {
        const res = await fetch('/api/devices/')
        this.devices = await res.json()
      } catch (e) {
        console.error('获取设备失败', e)
      }
    }
  }
}
</script>
