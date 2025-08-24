<script setup lang="ts">
import CustomImage from '@/components/CustomImage.vue'
import { API_IMAGE_GEN_URL } from '@/constants'
import { ref } from 'vue'

const providers = [
  {
    id: 'migros',
  },
  {
    id: 'coop',
  },
]

const items = [
  {
    name: 'Milk',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Bread',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Eggs',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Cheese',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Butter',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Flour',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Sugar',
    image: 'https://placehold.co/600x400',
  },
  {
    name: 'Coffee',
    image: 'https://placehold.co/600x400',
  },
]

const selectedIndex = ref<(typeof providers)[number]['id']>('coop')

function changeProvider(provider: (typeof providers)[number]) {
  selectedIndex.value = provider.id
}

function getImage(name: string) {
  const url = new URL(API_IMAGE_GEN_URL)
  url.searchParams.append('name', name)
  return url.toString()
}
</script>

<template>
  <div class="rounded-4xl bg-neutral-100 w-full flex flex-row gap-3 mt-5 mb-5">
    <button
            @click="changeProvider(provider)"
            v-for="(provider, index) in providers"
            class="h-16 py-2.5 rounded-s-3xl w-full cursor-pointer"
            :class="{ 'ps-3': index === 0, 'pe-3': index === providers.length - 1 }">
      <div
           class="h-full w-full rounded-3xl p-2"
           :class="{ 'bg-neutral-300': selectedIndex === provider.id }">
        <img
             :src="`/assets/food-store-logo/${provider.id}.png`"
             :alt="`Logo ${provider.id}`"
             class="h-full mx-auto object-contain" />
      </div>
    </button>
  </div>

  <div class="rounded-4xl bg-neutral-100 w-full p-5">
    <div class="flex flex-col gap-2">
      <div v-for="shoppingItem in items" class="flex flex-row items-center gap-5">
        <div class="w-24 h-14">
          <CustomImage :src="getImage(shoppingItem.name)" />
        </div>
        <h5 class="text-neutral-800 font-bold">{{ shoppingItem.name }}</h5>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
