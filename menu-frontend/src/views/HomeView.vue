<script setup lang="ts">
import { useHead } from '@unhead/vue'
import { useAuthStore } from '@/stores/auth.ts'
import { storeToRefs } from 'pinia'

useHead({
  title: 'Home • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Welcome to Menu Mingles',
    },
  ],
  link: [
    {
      rel: 'icon',
    },
  ],
})


const auth = useAuthStore()
const { isAuthenticated } = storeToRefs(auth)
</script>

<template>
  <div class="pt-10 px-5 flex flex-col gap-5">
    <RouterLink v-if="isAuthenticated" to="/swipe">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Swipe
      </button>
    </RouterLink>
  </div>
</template>
