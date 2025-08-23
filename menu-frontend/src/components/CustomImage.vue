<script setup lang="ts">
import { useImage } from '@vueuse/core'

const props = defineProps<{ src: string }>()

const { isLoading, error } = useImage({ src: props.src })

</script>

<template>
  <div class="w-full h-full rounded-2xl overflow-hidden">
    <img v-if="!isLoading && !error" :src="src" class="w-full h-full object-cover" alt="Meal" />
    <img v-else-if="error" src="https://placehold.co/600x400?text=Error" class="w-full h-full object-cover" alt="Fallback" />
    <div v-else class="w-full h-full bg-neutral-200 skeleton" aria-hidden="true"></div>
  </div>
</template>

<style scoped>
/* simple shimmer placeholder */
.skeleton { position: relative; overflow: hidden; }
.skeleton::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(100deg, transparent 20%, rgba(255,255,255,.6) 40%, transparent 60%);
  transform: translateX(-100%);
  animation: shimmer 1.2s infinite;
}
@keyframes shimmer { 100% { transform: translateX(100%); } }
</style>