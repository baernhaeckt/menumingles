<script setup lang="ts">
import { useAuthStore } from '@/stores/auth.ts'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logoutAndRedirect() {
  auth.logout()
  router.push({ name: 'home' })
}
</script>

<template>
  <RouterLink to="/chat">
    <button
      class="rounded-2xl bg-gray-300 hover:bg-gray-400 border border-gray-400 px-6 py-4 text-neutral-700 hover:text-white font-bold cursor-pointer flex flex-row gap-2 items-center"
    >
      <i class="ti ti-message-circle-filled text-2xl"></i>
      Chat
    </button>
  </RouterLink>
  <RouterLink to="/account/onboarding">
    <button
      class="rounded-2xl bg-gray-300 hover:bg-gray-400 border border-gray-400 px-6 py-4 text-neutral-700 hover:text-white font-bold cursor-pointer flex flex-row gap-2 items-center"
    >
      <i class="ti ti-wheat-off text-2xl"></i>
      Allergies & Goals
    </button>
  </RouterLink>
  <RouterLink to="/household/week">
    <button
      class="rounded-2xl bg-gray-300 hover:bg-gray-400 border border-gray-400 px-6 py-4 text-neutral-700 hover:text-white font-bold cursor-pointer flex flex-row gap-2 items-center"
    >
      <i class="ti ti-burger text-2xl"></i>
      Menu Plan
    </button>
  </RouterLink>
  <button
    @click="logoutAndRedirect"
    class="rounded-2xl bg-red-600 hover:bg-red-700 px-6 py-4 text-white font-bold cursor-pointer flex flex-row gap-2 items-center"
  >
    <i class="ti ti-logout text-2xl"></i>
    Logout
  </button>
</template>
