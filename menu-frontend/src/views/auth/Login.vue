<script setup lang="ts">
import { IconLogin2 } from '@tabler/icons-vue'
</script>

<template>
  <div class="block bg-white mt-10! p-5 py-12 md:py-24 mx-4 rounded-3xl">
    <img src="@/assets/illustrations/undraw_enter_nwx3.svg" alt="illustration" class="h-36 w-auto mx-auto mb-16" />
    <h1 class="text-center text-red-600 font-poetsen-one text-3xl md:text-5xl mb-2">Login</h1>
    <h2 class="mb-12! text-center text-lg md:text-2xl text-neutral-500">Welcome back!</h2>

    <div class="md:w-1/2! mx-auto mb-5">
      <label class="text-neutral-600" for="account-email"
        >Email <span class="text-orange-500">*</span></label
      >
      <input
        id="account-email"
        type="email"
        placeholder="dan@mingle.xyz"
        class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
      />
    </div>

    <div class="md:w-1/2! mx-auto mb-10">
      <label class="text-neutral-600" for="account-password"
        >Password <span class="text-orange-500">*</span></label
      >
      <input
        id="account-password"
        type="password"
        placeholder="●●●●●●●●●●●●"
        class= "w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
      />
    </div>

    <div class="md:w-1/2! mx-auto">
      <button
        class="rounded-2xl bg-red-600 hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
      >
        Login
        <IconLogin2 size="1.2rem" />
      </button>
    </div>
  </div>
</template>

<style scoped></style>
