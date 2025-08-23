<script setup lang="ts">
import '@interactjs/auto-start'
import '@interactjs/actions/drag'
import '@interactjs/actions/resize'
import '@interactjs/modifiers'
import '@interactjs/dev-tools'
import interact from '@interactjs/interact'

interact('.item').draggable({
  listeners: {
    move(event) {
      console.log(event.pageX, event.pageY)
    },
  },
})
</script>

<template>
  <div class="grow p-6 flex flex-col">
    <div class="grow bg-blue-600 h-full w-full relative">
      <div class="absolute w-full h-full item pt-3">
        <div
          class="h-full bg-neutral-300 shadow-xl border border-neutral-400 border-solid rounded-3xl p-5"
        >
          <div class="flex flex-col gap-8 h-full">
            <div class="grow relative flex items-center justify-center">
              <div
                class="absolute w-5/7 -translate-x-14 -translate-y-22 md:-translate-x-16 md:-translate-y-16 bg-black md:w-1/2 aspect-video rounded-3xl overflow-hidden"
              >
                <img
                  src="@/assets/placeholer-food/chiken.jpg"
                  alt=""
                  class="w-full h-full object-cover"
                />
              </div>
              <div
                class="absolute w-6/8 translate-x-12 translate-y-0 md:translate-x-22 bg-black md:w-1/2 aspect-video rounded-3xl overflow-hidden"
              >
                <img
                  src="@/assets/placeholer-food/noodles.jpg"
                  alt=""
                  class="w-full h-full object-cover"
                />
              </div>
              <div
                class="absolute w-5/7 -translate-x-7 translate-y-24 md:-translate-x-24 md:translate-y-22 bg-black md:w-1/2 aspect-video rounded-3xl overflow-hidden"
              >
                <img
                  src="@/assets/placeholer-food/pot.jpg"
                  alt=""
                  class="w-full h-full object-cover"
                />
              </div>
            </div>

            <div>
              <h5 class="text-3xl font-poetsen-one text-center">Do you like this food?</h5>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="p-10 flex flex-row justify-between">
    <button
      class="bg-red-600 rounded-full aspect-square h-16 text-white flex items-center justify-center outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
    >
      <i class="ti ti-x text-4xl"></i>
    </button>
    <button
      class="bg-green-600 rounded-full aspect-square h-16 text-white flex items-center justify-center outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-green-200"
    >
      <i class="ti ti-heart-filled text-4xl"></i>
    </button>
  </div>
</template>

<style>
#main-sec {
  display: flex;
  flex-direction: column;
}
</style>
