<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({}); const ext = ref(''); const msg = ref('')
onMounted(async () => { s.value = await getJSON('/api/settings'); ext.value = s.value.default_track_ext ?? '' })
async function save(){
  msg.value = ''
  try {
    s.value = await postJSON('/api/settings', { key: 'default_track_ext', value: String(ext.value) })
    msg.value = '已保存'
  } catch(e) { msg.value = '保存失败：外延需为不小于 0 的数字' }
}
</script>
<template><div class="page"><h1>设置</h1>
<p>默认褶倍 {{ s.default_fullness }}</p>
<p>默认外延 <input type="number" step="0.01" min="0" v-model="ext" /> m <button @click="save">保存</button> {{ msg }}</p>
</div></template>
