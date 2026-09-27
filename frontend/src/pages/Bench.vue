<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const motor = ref(false); const extLeft = ref(0.15); const extRight = ref(0.15); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  const s = await getJSON('/api/settings')
  const d = parseFloat(s.default_track_ext)
  if (!isNaN(d)) { extLeft.value = d; extRight.value = d }
})
async function go(save){
  err.value = ''
  try {
    if (save) {
      const body = { window_id: wid.value, fabric_id: fid.value, save: true }
      if (motor.value) Object.assign(body, { motor_track: true, ext_left: extLeft.value, ext_right: extRight.value })
      out.value = await postJSON('/api/estimate', body)
    } else {
      const q = motor.value ? `&motor_track=true&ext_left=${extLeft.value}&ext_right=${extRight.value}` : ''
      out.value = await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}${q}`)
    }
  } catch(e) { out.value = null; err.value = '计算失败：外延不能小于 0' }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label><input type="checkbox" v-model="motor" /> 电动轨</label>
<template v-if="motor">
  <label>左外延 <input type="number" step="0.01" min="0" v-model.number="extLeft" /> m</label>
  <label>右外延 <input type="number" step="0.01" min="0" v-model.number="extRight" /> m</label>
</template>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" />
<p v-if="out && out.track_meters !== undefined">电动轨长 {{ out.track_meters }} m（左外延 {{ out.track_ext_left }} m，右外延 {{ out.track_ext_right }} m）</p>
</div></template>
