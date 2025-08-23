<script setup lang="ts">
import { useHead } from '@unhead/vue'

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
</script>

<template>
  <div class="pt-10 px-5 flex flex-col gap-5">
    <RouterLink to="/chat">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Open Chat
      </button>
    </RouterLink>

    <div class="grid grid-cols-2 gap-5">
      <RouterLink to="/auth/login">
        <button
          class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
        >
          Login
        </button>
      </RouterLink>

      <RouterLink to="/auth/register">
        <button
          class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
        >
          Register
        </button>
      </RouterLink>
    </div>

    <RouterLink to="/account/profile">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Account Profile
      </button>
    </RouterLink>

    <RouterLink to="/swipe">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Swipe
      </button>
    </RouterLink>
  </div>
</template>
