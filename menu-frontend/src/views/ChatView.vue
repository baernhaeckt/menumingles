<script setup lang="ts">
  import { IconUser, IconFridge, IconSend } from "@tabler/icons-vue";
</script>

<template>
  <div class="p-10 h-full flex flex-col grow gap-4">
    <div class="w-3/4">
      <div class="flex flex-row gap-3">
        <div class="bg-neutral-300 rounded-full w-10 h-10 p-2 aspect-square">
          <IconFridge class="w-full h-full text-neutral-600" />
        </div>
        <div class="text-neutral-700 bg-neutral-300 p-4 pt-3 rounded-2xl">
          <span class="block font-bold text-blue-500">Fridge</span>
          <span>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text</span>
        </div>
      </div>
    </div>

    <div class="w-3/4">
      <div class="flex flex-row gap-3">
        <div class="bg-neutral-300 rounded-full w-10 h-10 p-2 aspect-square">
          <IconUser class="w-full h-full text-neutral-600" />
        </div>
        <div class="text-neutral-700 bg-neutral-300 p-4 pt-3 rounded-2xl">
          <span class="block font-bold text-green-600">Mom</span>
          <span>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text</span>
        </div>
      </div>
    </div>

    <div class="w-3/4 self-end">
      <div class="flex flex-row-reverse gap-3">
        <div class="bg-neutral-300 rounded-full w-10 h-10 p-2 aspect-square">
          <IconUser class="w-full h-full text-neutral-600" />
        </div>
        <div class="text-neutral-800 bg-red-200 p-4 pt-3 rounded-2xl">
          <span>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text</span>
        </div>
      </div>
    </div>
  </div>
  <div class="rounded-tl-2xl rounded-tr-2xl bg-red-200 mx-4! px-5 py-4 drop-shadow-[0_-10px_40px_rgba(0,0,0,0.15)]">
    <div class="w-full flex flex-row gap-5">
      <input type="text" class="bg-white rounded-2xl grow px-4 outline-4 outline-transparent focus:outline-rose-600" placeholder="Type a message..." />
      <button class="bg-rose-600 hover:bg-rose-700 cursor-pointer rounded-3xl px-4 aspect-square text-white">
        <IconSend />
      </button>
    </div>
  </div>
</template>

<style>
#main-sec {
  display: flex;
  flex-direction: column;
}
</style>
