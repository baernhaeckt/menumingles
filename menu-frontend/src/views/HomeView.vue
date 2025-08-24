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
  <div class="pt-10 px-5 flex flex-col gap-5 max-w-[900px] mx-auto select-none mb-10">
    <img src="@/assets/home/step-1.png" alt="" class="md:w-1/2 h-auto -rotate-12" />
    <img
      src="@/assets/home/step-2.png"
      alt=""
      class="md:w-1/2 h-auto self-end md:-my-32 rotate-5 md:rotate-12"
    />
    <img src="@/assets/home/step-3.png" alt="" class="md:w-1/2 h-auto -rotate-7 md:rotate-0" />
  </div>

  <div class="px-5">
    <RouterLink to="/auth/register">
      <button
        class="rounded-3xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Register a new account
      </button>
    </RouterLink>
  </div>

  <div class="mt-[1000px] mb-20 px-5">
    <RouterLink v-if="isAuthenticated" to="/swipe">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Plan
      </button>
    </RouterLink>
  </div>
</template>
