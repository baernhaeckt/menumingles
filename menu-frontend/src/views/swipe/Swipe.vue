<script setup lang="ts">
import { httpClient } from '@/client/http-client'
import CustomImage from '@/components/CustomImage.vue'
import ThanksSwiping from '@/components/ThanksSwiping.vue'
import { API_IMAGE_GEN_URL } from '@/constants'
import { useAuthStore } from '@/stores/auth'
import { useSessionKeyStore } from '@/stores/sessionKey'
import '@interactjs/actions/drag'
import '@interactjs/actions/drop'
import '@interactjs/actions/resize'
import '@interactjs/auto-start'
import '@interactjs/dev-tools'
import '@interactjs/inertia'
import interact from '@interactjs/interact'
import '@interactjs/modifiers'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useToast } from 'vue-toast-notification'
import { z } from 'zod'

function onSwipeLeft() {
  const currentCard = getCurrentCard()
  menuDecisions.value.push({
    id: currentCard.id,
    name: currentCard.names,
    like: false,
  })
}

function onSwipeRight() {
  const currentCard = getCurrentCard()
  menuDecisions.value.push({
    id: currentCard.id,
    name: currentCard.names,
    like: true,
  })
}

function getCurrentCard() {
  return cards.value[cards.value.length - 1]
}

const auth = useAuthStore();
const sessionKeyStore = useSessionKeyStore();
const toast = useToast();

/**
 * Starts the planning process for the week.
 * Results must be kept in memory until all cards have been swiped.
 */
async function continuePlanningAsync() {
  const response = await httpClient.post('v1/planning/continue', undefined, {
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
  })
  return z
    .object({
      sessionKey: z.string(),
      menuSelection: z.array(
        z.object({
          name: z.string(),
          ingredients: z.string().transform((value) => value.split(',')),
        }),
      ),
    })
    .parse(response.data)
}

/**
 * Confirms the selected menu items
 * from the swiping.
 * @see continuePlanning must be called first to retrieve the sessionKey and the menu selection.
 */
async function selectMenuItemsAsync(request: { sessionKey: string; menuSelection: string[] }) {
  const response = await httpClient.post('v1/planning/selection', request, {
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
  })
  if (response.status === 204) {
    return
  }

  throw new Error('Failed to continue planning')
}

/**
 * Starts the discussion process for the week.
 * @see continuePlanning must be called first to retrieve the sessionKey and the menu selection.
 */
async function startDiscussionAsync(request: { sessionKey: string }) {
  const response = await httpClient.post('v1/discussion/start', request, {
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
  })
  if (response.status === 204) {
    return
  }

  throw new Error('Failed to start discussion')
}

async function finishSwipingAsync() {
  await selectMenuItemsAsync({
    sessionKey: sessionKeyStore.sessionKey!,
    menuSelection: menuDecisions.value
      .filter((decision) => decision.like)
      .map((selection) => selection.name)
      .flatMap((name) => name),
  });

  await startDiscussionAsync({
    sessionKey: sessionKeyStore.sessionKey!
  })

  swipingFinished.value = true;
  toast.success('<i class="ti ti-circle-check-filled"></i> Thank you for swiping');
}

onMounted(async () => {
  // Initialize session key store from localStorage
  sessionKeyStore.initFromStorage()

  const result = await continuePlanningAsync()
  sessionKeyStore.setSessionKey(result.sessionKey)

  if (result.menuSelection.length % 3 !== 0) {
    throw new Error(
      'Each card shows 3 menu items. The API returned an invalid number of items meaning it cannot be processed.',
    )
  }

  let count = 0
  for (let i = 0; i < result.menuSelection.length; i += 3) {
    cards.value.push({
      id: count,
      names: result.menuSelection.slice(i, i + 3).map((selection) => selection.name),
      ingredients: result.menuSelection
        .slice(i, i + 3)
        .map((selection) => selection.ingredients)
        .flatMap((ingredient) => ingredient),
    })
  }
})

const cards = ref<{ id: number; names: string[]; ingredients: string[] }[]>([])
const swipingFinished = ref(false)
const menuDecisions = ref<{ id: number; name: string[]; like: boolean }[]>([])

// Progressive image loading: track which cards should load images
const cardsToLoadImages = ref<Set<number>>(new Set())
const progressiveLoadingTimer = ref<number | null>(null)

const topIndex = computed(() => cards.value.length - 1)

// Function to start progressive loading of cards
function startProgressiveLoading() {
  // Clear any existing timer
  if (progressiveLoadingTimer.value) {
    clearTimeout(progressiveLoadingTimer.value)
  }

  // Start progressive loading with delays
  let currentIndex = topIndex.value
  let delay = 0

  // Load current card immediately
  if (currentIndex >= 0) {
    cardsToLoadImages.value.add(currentIndex)
  }

  // Progressively load cards below with increasing delays
  // This ensures that if user stays on one card, all cards below will eventually load
  for (let i = 1; i <= 5; i++) { // Load up to 5 cards ahead for better coverage
    const cardIndex = currentIndex - i
    if (cardIndex >= 0) {
      delay += 300 // Reduced to 300ms for faster progressive loading
      progressiveLoadingTimer.value = window.setTimeout(() => {
        cardsToLoadImages.value.add(cardIndex)
      }, delay)
    }
  }
}

// Watch for changes in topIndex and trigger progressive loading
watch(topIndex, (newTopIndex) => {
  startProgressiveLoading()
}, { immediate: true })

// Clean up timer when component unmounts
onUnmounted(() => {
  if (progressiveLoadingTimer.value) {
    clearTimeout(progressiveLoadingTimer.value)
  }
})

// Function to check if a card should load its images
function shouldLoadImages(cardIndex: number): boolean {
  return cardsToLoadImages.value.has(cardIndex)
}

// Container ref to find the current top card element for programmatic swipes
const deck = ref<HTMLElement | null>(null)

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

  const onEnd = async () => {
    el.removeEventListener('transitionend', onEnd)
    if (dir > 0) onSwipeRight()
    else onSwipeLeft()

    // Remove the top card after the animation completes
    cards.value.pop()

    if (cards.value.length === 0) {
      await finishSwipingAsync()
    }
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
    async end(event) {
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
        else onSwipeLeft()

        // Remove the top card after the animation completes
        cards.value.pop()

        if (cards.value.length === 0) {
          await finishSwipingAsync()
        }
      } else {
        // Snap back immediately, no delay
        target.style.transition = 'transform 220ms cubic-bezier(.22,.61,.36,1)'
        setTransform(target, 0)
      }
    },
  },
})

function getImage(name: string) {
  const url = new URL(API_IMAGE_GEN_URL)
  url.searchParams.append('name', name)
  return url.toString()
}
</script>

<template>
  <template v-if="cards.length > 0">
    <div class="grow pt-6 flex flex-col">
      <div class="grow h-full w-full relative overflow-hidden" ref="deck">
        <div
             v-for="(card, i) in cards"
             :key="card.id"
             :class="{ item: i === topIndex, 'pointer-events-none -translate-y-1.5': i !== topIndex }"
             class="absolute w-full h-full px-6 pt-3 pb-6">
          <div class="h-full max-w-[500px] mx-auto bg-gradient-to-br from-white to-neutral-50 shadow-lg rounded-3xl p-6 overflow-hidden">
            <div class="flex flex-col h-full">
              <!-- Dish Images Section -->
              <div class="grow relative flex items-center justify-center mb-6">
                <!-- Background decorative elements -->
                <div class="absolute inset-0 bg-gradient-to-br from-orange-50 to-yellow-50 rounded-2xl opacity-60"></div>

                <!-- Dish 1 - Top left, slightly rotated -->
                <div class="absolute top-12 left-12 w-32 h-32 md:top-16 md:left-16 md:w-40 md:h-40 transform -rotate-6 hover:rotate-0 transition-transform duration-300 z-20">
                  <div class="relative w-full h-full">
                    <div class="absolute inset-0 bg-white rounded-2xl shadow-lg border-2 border-white"></div>
                    <div class="absolute inset-1 rounded-xl overflow-hidden">
                      <CustomImage v-if="shouldLoadImages(i)" :src="getImage(card.names[0])" />
                      <div v-else class="w-full h-full bg-neutral-200 skeleton" aria-hidden="true"></div>
                    </div>
                    <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 bg-white px-3 py-1 rounded-full shadow-md border border-neutral-200 z-20">
                      <span class="text-xs font-medium text-neutral-700 truncate max-w-20">{{ card.names[0] }}</span>
                    </div>
                  </div>
                </div>

                <!-- Dish 2 - Center, larger, no rotation -->
                <div class="relative w-40 h-40 md:w-48 md:h-48 transform hover:scale-105 transition-transform duration-300 z-30">
                  <div class="relative w-full h-full">
                    <div class="absolute inset-0 bg-white rounded-2xl shadow-xl border-2 border-white"></div>
                    <div class="absolute inset-1 rounded-xl overflow-hidden">
                      <CustomImage v-if="shouldLoadImages(i)" :src="getImage(card.names[1])" />
                      <div v-else class="w-full h-full bg-neutral-200 skeleton" aria-hidden="true"></div>
                    </div>
                    <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 bg-white px-3 py-1 rounded-full shadow-md border border-neutral-200 z-30">
                      <span class="text-xs font-medium text-neutral-700 truncate max-w-24">{{ card.names[1] }}</span>
                    </div>
                  </div>
                </div>

                <!-- Dish 3 - Bottom right, slightly rotated -->
                <div class="absolute bottom-12 right-12 w-32 h-32 md:bottom-16 md:right-16 md:w-40 md:h-40 transform rotate-6 hover:rotate-0 transition-transform duration-300 z-20">
                  <div class="relative w-full h-full">
                    <div class="absolute inset-0 bg-white rounded-2xl shadow-lg border-2 border-white"></div>
                    <div class="absolute inset-1 rounded-xl overflow-hidden">
                      <CustomImage v-if="shouldLoadImages(i)" :src="getImage(card.names[2])" />
                      <div v-else class="w-full h-full bg-neutral-200 skeleton" aria-hidden="true"></div>
                    </div>
                    <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-1/2 bg-white px-3 py-1 rounded-full shadow-md border border-neutral-200 z-20">
                      <span class="text-xs font-medium text-neutral-700 truncate max-w-20">{{ card.names[2] }}</span>
                    </div>
                  </div>
                </div>

                <!-- Decorative food icons -->
                <div class="absolute top-2 right-2 text-orange-400 opacity-30">
                  <i class="ti ti-utensils text-2xl"></i>
                </div>
                <div class="absolute bottom-2 left-2 text-yellow-400 opacity-30">
                  <i class="ti ti-chef-hat text-2xl"></i>
                </div>
              </div>

              <!-- Question Section -->
              <div class="text-center">
                <h5 class="text-2xl md:text-3xl text-neutral-800 font-poetsen-one mb-2">
                  Do you like this food?
                </h5>
                <p class="text-sm text-neutral-600">
                  Swipe right to like, left to pass
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="p-10 py-6 flex flex-row justify-between">
      <button
              @click="swipeByButton('left')"
              class="bg-red-600 hover:bg-red-700 cursor-pointer rounded-full aspect-square h-16 text-white flex items-center justify-center outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200">
        <i class="ti ti-x text-4xl"></i>
      </button>
      <button
              @click="swipeByButton('right')"
              class="bg-green-600 hover:bg-green-700 cursor-pointer rounded-full aspect-square h-16 text-white flex items-center justify-center outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-green-200">
        <i class="ti ti-heart-filled text-4xl"></i>
      </button>
    </div>
  </template>

  <ThanksSwiping v-else-if="swipingFinished" />
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

/* Skeleton loading animation for progressive image loading */
.skeleton {
  position: relative;
  overflow: hidden;
}

.skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(100deg, transparent 20%, rgba(255, 255, 255, .6) 40%, transparent 60%);
  transform: translateX(-100%);
  animation: shimmer 1.2s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>
