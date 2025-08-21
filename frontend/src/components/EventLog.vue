<template>
  <div class="event-log">
    <h2>报警事件</h2>
    <div class="controls">
      <label>
        级别：
        <select v-model="level">
          <option value="">全部</option>
          <option value="info">info</option>
          <option value="warning">warning</option>
          <option value="error">error</option>
        </select>
      </label>
      <label>
        设备：
        <select v-model="deviceId">
          <option value="">全部</option>
          <option v-for="d in devices" :key="d.id" :value="d.id">{{ d.name }}</option>
        </select>
      </label>
      <label>
        时间：
        <select v-model="hours">
          <option value="1">1小时</option>
          <option value="24">24小时</option>
          <option value="168">7天</option>
        </select>
      </label>
      <button @click="refresh" :disabled="loading">刷新</button>
      <span v-if="loading">加载中...</span>
    </div>
    <table>
      <thead>
        <tr><th>时间</th><th>设备</th><th>级别</th><th>消息</th></tr>
      </thead>
      <tbody>
        <tr v-for="e in events" :key="e.id">
          <td>{{ formatTime(e.timestamp) }}</td>
          <td>{{ deviceName(e.device_id) }}</td>
          <td>{{ e.level }}</td>
          <td>{{ e.message }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'EventLog',
  data() {
    return { events: [], devices: [], loading: false, timer: null, level: '', deviceId: '', hours: '24' }
  },
  async created() {
    await this.loadDevices()
    await this.refresh()
    this.timer = setInterval(this.refresh, 5000) // 短轮询 5s
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    async loadDevices() {
      try {
        const res = await fetch('/api/devices/')
        this.devices = await res.json()
      } catch (e) { console.error('加载设备失败', e) }
    },
    deviceName(id) {
      const d = this.devices.find(x => x.id === id)
      return d ? d.name : id
    },
    formatTime(ts) { return new Date(ts).toLocaleString() },
    async refresh() {
      this.loading = true
      try {
        const params = new URLSearchParams()
        if (this.level) params.set('level', this.level)
        if (this.deviceId) params.set('device_id', this.deviceId)
        if (this.hours) {
          const end = new Date()
          const start = new Date(end.getTime() - Number(this.hours) * 3600 * 1000)
          params.set('start_time', start.toISOString())
          params.set('end_time', end.toISOString())
        }
        params.set('limit', '100')
        const res = await fetch('/api/events/?' + params.toString())
        this.events = await res.json()
      } catch (e) { console.error('加载事件失败', e) }
      finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.event-log { padding: 20px; }
.controls { margin-bottom: 10px; }
 table { width: 100%; border-collapse: collapse; }
 th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
</style>
