<script setup lang="ts">
import '@interactjs/auto-start'
import '@interactjs/actions/drag'
import '@interactjs/actions/drop'
import '@interactjs/actions/resize'
import '@interactjs/modifiers'
import '@interactjs/dev-tools'
import "@interactjs/inertia"
import interact from '@interactjs/interact'

function onSwipeLeft() {
  console.log('Swiped left')
}

function onSwipeRight() {
  console.log('Swiped right')
}

function setTransform(el: HTMLElement, x: number) {
  el.style.transform = `translate(${x}px, 0px)`
  el.dataset.x = String(x)
}

function getX(el: HTMLElement) {
  return parseFloat(el.dataset.x || '0') || 0
}

function animateTo(el: HTMLElement, x: number) {
  el.style.transition = 'transform 300ms ease'
  setTransform(el, x)
  const onEnd = () => {
    el.style.transition = ''
    el.removeEventListener('transitionend', onEnd)
  }
  el.addEventListener('transitionend', onEnd)
}

interact('.item').draggable({
  lockAxis: 'x',
  inertia: {
    // lower resistance = longer glide
    resistance: 15,     // default ~20; try 5–15 for more momentum
    minSpeed: 20,      // px/s needed to trigger inertia (raise to require a "flick")
    endSpeed: 4,       // px/s where inertia stops
    allowResume: true,  // let users grab the card again mid-inertia
  },
  listeners: {
    start(event) {
      const target = event.target as HTMLElement
      // Ensure we start from current x (important if previously moved)
      if (!target.dataset.x) setTransform(target, 0)
    },
    move(event) {
      const target = event.target as HTMLElement
      // Accumulate by delta to avoid any layout/padding offsets
      const x = getX(target) + event.dx
      target.style.transition = '' // disable transition during drag
      setTransform(target, x)
    },
    end(event) {
      const target = event.target as HTMLElement
      const x = getX(target)

      // Threshold: 80% of viewport width
      const threshold = window.innerWidth * 0.8

      if (Math.abs(x) >= threshold) {
        // Animate off-screen and signal
        const direction = x > 0 ? 1 : -1
        const offscreenX = direction * window.innerWidth * 1.2 // push a bit farther than edge
        animateTo(target, offscreenX)
        // Trigger callback
        if (direction > 0) onSwipeRight()
        else onSwipeLeft()
        // Optionally: reset after animation for next card (if applicable)
        // setTimeout(() => setTransform(target, 0), 320)
      } else {
        // Snap back to center
        animateTo(target, 0)
      }
    },
  },
})
</script>

<template>
  <div class="grow pt-6 flex flex-col">
    <div class="grow bg-blue-600 h-full w-full relative">
      <div class="absolute w-full h-full item px-6 pt-3">
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
              <h5 class="text-3xl text-neutral-900 font-poetsen-one text-center">Do you like this food?</h5>
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

/* Prevent browser from hijacking touch gestures (scroll, back-swipe) */
.item {
  touch-action: none;
}
</style>
