<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const secondsLeft = ref(3)
let intervalId: number | undefined

const go = () => {
  router.replace('/chat')
}

onMounted(() => {
  intervalId = window.setInterval(() => {
    if (secondsLeft.value <= 1) {
      clearInterval(intervalId)
      go()
    } else {
      secondsLeft.value -= 1
    }
  }, 1000)
})

onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<template>
  <div class="p-10 flex flex-col items-center gap-5">
    <i class="ti ti-circle-check text-[140px] text-green-600"></i>
    <h2 class="text-3xl text-green-600 font-poetsen-one">Learned your interests</h2>
    <p class="text-neutral-500 text-center">
      We learned the meals you like and will automatically adjust the menu plan.<br />
      You can close this page now.
    </p>
    <p class="text-neutral-400">Redirecting in {{ secondsLeft }}s…</p>
  </div>
</template>

<style scoped></style>
