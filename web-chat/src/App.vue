<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <nav class="bg-white px-6 py-4">
    <RouterLink to="/" class="flex flex-row items-center gap-5">
      <img alt="Vue logo" class="logo w-auto h-16" src="@/assets/transgourmet-short.png" />
      <span class="text-3xl font-normal text-red-600 font-poetsen-one">Menu Mingle</span>
    </RouterLink>
  </nav>

  <main id="main-sec" class="grow min-h-0">
    <RouterView />
  </main>
</template>

<style scoped></style>
