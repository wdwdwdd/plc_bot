import { createStore } from 'vuex'

export default createStore({
  state: {
    devices: [],
    currentDevice: null,
    realtimeData: {},
    alarms: []
  },
  
  mutations: {
    SET_DEVICES(state, devices) {
      state.devices = devices
    },
    SET_CURRENT_DEVICE(state, device) {
      state.currentDevice = device
    },
    UPDATE_REALTIME_DATA(state, { deviceId, data }) {
      state.realtimeData[deviceId] = data
    },
    ADD_ALARM(state, alarm) {
      state.alarms.unshift(alarm)
    }
  },
  
  actions: {
    async fetchDevices({ commit }) {
      const response = await fetch('/api/devices')
      const devices = await response.json()
      commit('SET_DEVICES', devices)
    },
    
    async fetchRealtimeData({ commit }, deviceId) {
      const response = await fetch(`/api/data/realtime/${deviceId}`)
      const data = await response.json()
      commit('UPDATE_REALTIME_DATA', { deviceId, data })
    }
  }
})
