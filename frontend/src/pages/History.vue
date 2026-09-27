<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id"><router-link :to="`/runs/${r.id}`">#{{ r.id }}</router-link> {{ r.window_name }} {{ r.result?.meters }}m<span v-if="r.result?.track_meters !== undefined">｜轨 {{ r.result.track_meters }}m</span></li></ul></div></template>
