<script setup lang="ts">
import '@interactjs/auto-start'
import '@interactjs/actions/drag'
import '@interactjs/actions/drop'
import '@interactjs/actions/resize'
import '@interactjs/modifiers'
import '@interactjs/dev-tools'
import '@interactjs/inertia'
import interact from '@interactjs/interact'
import { computed, ref } from 'vue'
import { useVibrate } from '@vueuse/core'

function onSwipeLeft() {
  vibrate();
  console.log('Swiped left')
}

function onSwipeRight() {
  vibrate();
  console.log('Swiped right')
}

const cards = ref([
  { id: 1, title: 'Card 1', img: 'chiken.jpg' },
  { id: 2, title: 'Card 2', img: 'noodles.jpg' },
  { id: 3, title: 'Card 3', img: 'pot.jpg' },
])

const topIndex = computed(() => cards.value.length - 1)

const { vibrate } = useVibrate({ pattern: [100, 80, 50] });

// Container ref to find the current top card element for programmatic swipes
const deck = ref<HTMLElement | null>(null);

// Programmatic swipe via buttons: animate the top card off-screen with same feel
function swipeByButton(direction: 'left' | 'right') {
  const el = deck.value?.querySelector('.item') as HTMLElement | null
  if (!el) return

  // ensure a baseline transform state
  if (!el.dataset.x) setTransform(el, 0)

  const container = el.parentElement
  const width = container?.getBoundingClientRect().width || window.innerWidth
  const dir = direction === 'right' ? 1 : -1
  const offscreenX = dir * (width * 1.2)
  const x = getX(el)

  // Duration proportional to remaining distance for a snappy feel
  const remaining = Math.min(Math.abs(offscreenX - x), width * 1.2)
  const duration = Math.max(160, Math.min(320, (remaining / (width * 1.2)) * 280))

  el.style.transition = `transform ${duration}ms cubic-bezier(.22,.61,.36,1)`
  setTransform(el, offscreenX)

  const onEnd = () => {
    el.removeEventListener('transitionend', onEnd)
    if (dir > 0) onSwipeRight()
    else onSwipeLeft()
    // Remove the top card after the animation completes
    cards.value.pop()
  }
  el.addEventListener('transitionend', onEnd, { once: true })
}

function setTransform(el: HTMLElement, x: number) {
  el.style.transform = `translate(${x}px, 0px)`
  el.dataset.x = String(x)
}

function getX(el: HTMLElement) {
  return parseFloat(el.dataset.x || '0') || 0
}

interact('.item').draggable({
  lockAxis: 'x',
  inertia: false,
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

      // Use container width if available; fallback to viewport
      const container = target.parentElement
      const width = container?.getBoundingClientRect().width || window.innerWidth

      const threshold = width * 0.3

      // Velocity-based projection (px/s -> project over ~250ms)
      const vx = event.velocityX || 0
      const PROJECTION_TIME = 0.25 // seconds
      const MAX_EXTRA = width * 0.5 // cap extra distance
      const projected = x + Math.max(-MAX_EXTRA, Math.min(MAX_EXTRA, vx * PROJECTION_TIME))

      // Consider as "flick" if speed is high enough
      const FLICK_SPEED = 350 // px/s
      const isFlick = Math.abs(vx) >= FLICK_SPEED

      // Decide with projection (for flicks) or current x (for slow releases)
      const decideX = isFlick ? projected : x

      if (Math.abs(decideX) >= threshold) {
        const direction = decideX > 0 ? 1 : -1
        const offscreenX = direction * (width * 1.2)

        // Duration proportional to remaining distance for a snappy feel
        const remaining = Math.min(Math.abs(offscreenX - x), width * 1.2)
        const duration = Math.max(160, Math.min(320, (remaining / (width * 1.2)) * 280))

        target.style.transition = `transform ${duration}ms cubic-bezier(.22,.61,.36,1)`
        setTransform(target, offscreenX)

        if (direction > 0) onSwipeRight()
        else onSwipeLeft();

        cards.value.pop();
      } else {
        // Snap back immediately, no delay
        target.style.transition = 'transform 220ms cubic-bezier(.22,.61,.36,1)'
        setTransform(target, 0)
      }
    },
  },
})
</script>

<template>
  <div class="grow pt-6 flex flex-col">
    <div class="grow h-full w-full relative overflow-hidden" ref="deck">
      <div
        v-for="(card, i) in cards"
        :key="card.id"
        :class="{ item: i === topIndex, 'pointer-events-none -translate-y-1.5': i !== topIndex }"
        class="absolute w-full h-full px-6 pt-3 pb-6"
      >
        <div
          class="h-full max-w-[500px] mx-auto bg-red bg-neutral-300 shadow-xl border border-neutral-400 border-solid rounded-3xl p-5"
        >
          <div class="flex flex-col gap-8 h-full">
            <div class="grow relative flex items-center justify-center">
              <div
                class="absolute w-5/7 -translate-x-14 -translate-y-22 md:-translate-x-20 md:-translate-y-24 md:w-1/2 aspect-video rounded-3xl overflow-hidden"
              >
                <img
                  src="@/assets/placeholer-food/chiken.jpg"
                  alt=""
                  class="w-full h-full object-cover"
                />
              </div>
              <div
                class="absolute w-6/8 translate-x-12 translate-y-0 md:translate-x-32 md:w-1/2 aspect-video rounded-3xl overflow-hidden"
              >
                <img
                  src="@/assets/placeholer-food/noodles.jpg"
                  alt=""
                  class="w-full h-full object-cover"
                />
              </div>
              <div
                class="absolute w-5/7 -translate-x-7 translate-y-24 md:-translate-x-22 md:translate-y-18 md:w-1/2 aspect-video rounded-3xl overflow-hidden"
              >
                <img
                  src="@/assets/placeholer-food/pot.jpg"
                  alt=""
                  class="w-full h-full object-cover"
                />
              </div>
            </div>

            <div>
              <h5 class="text-3xl text-neutral-900 font-poetsen-one text-center">
                Do you like this food?
              </h5>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="p-10 py-6 flex flex-row justify-between">
    <button
      @click="swipeByButton('left')"
      class="bg-red-600 hover:bg-red-700 cursor-pointer rounded-full aspect-square h-16 text-white flex items-center justify-center outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
    >
      <i class="ti ti-x text-4xl"></i>
    </button>
    <button
      @click="swipeByButton('right')"
      class="bg-green-600 hover:bg-green-700 cursor-pointer rounded-full aspect-square h-16 text-white flex items-center justify-center outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-green-200"
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
