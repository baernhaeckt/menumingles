<script setup lang="ts">
import { IconLogin2 } from '@tabler/icons-vue'
</script>

<template>
  <div class="block bg-white mt-10! p-5 rounded-3xl">
    <h1 class="text-center text-red-600 font-poetsen-one text-3xl mb-12!">Login</h1>

    <div class="w-1/2! mx-auto mb-5">
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

    <div class="w-1/2! mx-auto mb-5">
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

    <div class="w-1/2! mx-auto mb-5">
      <button
        class="rounded-2xl bg-red-600 hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 ring-red-500! ring-offset-red-500!"
      >
        Login
        <IconLogin2 size="1.2rem" />
      </button>
    </div>
  </div>
</template>

<style scoped></style>
