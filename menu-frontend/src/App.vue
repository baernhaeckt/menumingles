<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth.ts'
import { storeToRefs } from 'pinia'

const auth = useAuthStore()
const { isAuthenticated, getGravatarUrl } = storeToRefs(auth)

auth.initFromCookie();
</script>

<template>
  <nav class="bg-white px-6 py-4 flex flex-row gap-5">
    <RouterLink to="/" class="inline-flex flex-row items-center gap-5">
      <img alt="Vue logo" class="logo w-auto h-16" src="@/assets/transgourmet-short.png" />
      <span class="text-3xl font-normal text-red-600 font-poetsen-one">Menu Mingle</span>
    </RouterLink>
    <div class="ms-auto flex flex-row flex-nowrap items-center">
      <div v-if="isAuthenticated">
        <RouterLink v-if="getGravatarUrl" to="/account/profile">
          <img
            :src="getGravatarUrl"
            alt="gravatar"
            class="w-10 h-10 rounded-full"
          />
        </RouterLink>
        <RouterLink
          v-else
          to="/account/profile"
          class="bg-neutral-300 hover:bg-neutral-400 w-12 h-12 rounded-full flex items-center justify-center"
        >
          <i class="ti ti-user text-3xl" />
        </RouterLink>      </div>
      <RouterLink
        v-else
        to="/auth/login"
        class="bg-neutral-300 hover:bg-neutral-400 w-12 h-12 rounded-full flex items-center justify-center"
      >
        <i class="ti ti-user text-3xl" />
      </RouterLink>
    </div>
  </nav>

  <main id="main-sec" class="grow min-h-0 w-full">
    <RouterView />
  </main>
</template>

<style scoped></style>
