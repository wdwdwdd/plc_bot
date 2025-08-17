<template>
  <div class="device-card" :class="{ 'is-offline': !device.is_active }">
    <div class="card-header">
      <h3>{{ device.name }}</h3>
      <span class="status-badge" :class="{ 'is-online': device.is_active }">
        {{ device.is_active ? '在线' : '离线' }}
      </span>
    </div>
    <div class="card-body">
      <p>IP: {{ device.ip_address }}</p>
      <p>端口: {{ device.port }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeviceCard',
  props: {
    device: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.device-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  background: white;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.is-online {
  background: #4caf50;
  color: white;
}

.is-offline {
  opacity: 0.6;
}
</style>
