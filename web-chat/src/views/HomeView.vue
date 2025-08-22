<script setup lang="ts">
</script>

<template>
  <div class="pt-10 flex flex-col gap-5">
    <RouterLink to="/chat">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Open Chat
      </button>
    </RouterLink>

    <RouterLink to="/auth/login">
      <button
        class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center w-full"
      >
        Login
      </button>
    </RouterLink>
  </div>
</template>
