<script setup lang="ts">
import { useHead } from '@unhead/vue'

useHead({
  title: 'Week • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Manage your household menu plan',
    },
  ],
  link: [
    {
      rel: 'icon',
    },
  ],
})
</script>

<template>
  <div class="block bg-white mt-10! p-5 mx-4 rounded-3xl">
    <h1 class="text-3xl font-poetsen-one text-red-600">Week menu-plan</h1>
    <p>Here is your custom tailored menu plan for the week</p>

    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5">
      <div></div>
    </div>
  </div>
</template>

<style scoped></style>
