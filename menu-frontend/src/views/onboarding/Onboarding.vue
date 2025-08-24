<script setup lang="ts">
import { ref } from 'vue'
import CustomImage from '@/components/CustomImage.vue'
import { useHead } from '@unhead/vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification'

const router = useRouter();
const toast = useToast();

useHead({
  title: 'Onboarding • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Trying to get to know you',
    },
  ],
  link: [
    {
      rel: 'icon',
    }
  ]
})

const possibleAllergies = [
  {
    name: 'Gluten',
  },
  {
    name: 'Egg',
  },
  {
    name: 'Peanuts',
  },
  {
    name: 'Soy',
  },
  {
    name: 'Sesame',
  },
  {
    name: 'Milk',
  },
]

const checkedAllergies = ref<(typeof possibleAllergies)[number]['name'][]>([])

const toggleAllergy = (allergen: (typeof possibleAllergies)[number]) => {
  if (checkedAllergies.value.includes(allergen.name)) {
    checkedAllergies.value = checkedAllergies.value.filter((a) => a !== allergen.name)
  } else {
    checkedAllergies.value.push(allergen.name)
  }
}

const possibleLongTermGoals = [
  {
    image: 'vegetables.jpg',
    name: 'Eat more vegetables',
  },
  {
    image: 'weight-loss.jpg',
    name: 'Lose weight',
  },
  {
    image: 'sugar.jpg',
    name: 'Reduce added sugar intake',
  },
  {
    image: 'water.jpg',
    name: 'Increase daily water consumption',
  },
  {
    image: 'grains.jpg',
    name: 'Incorporate more whole grains',
  },
  {
    image: 'processed-fast-food.jpg',
    name: 'Limit processed and fast foods',
  },
  {
    image: 'healthy-food.jpg',
    name: 'Eat balanced meals with protein, carbs, and healthy fats',
  },
]

const checkedLongTermGoals = ref<(typeof possibleLongTermGoals)[number]['name'][]>([])

const toggleLongTermGoal = (goal: (typeof possibleLongTermGoals)[number]) => {
  if (checkedLongTermGoals.value.includes(goal.name)) {
    checkedLongTermGoals.value = checkedLongTermGoals.value.filter((a) => a !== goal.name)
  } else {
    checkedLongTermGoals.value.push(goal.name)
  }
}

async function onSubmit() {
  await router.push({ name: 'chat' });
  await toast.success('<i class="ti ti-circle-check-filled"></i> Saved your allergies and goals. You can now start chatting with your twins!');
}
</script>

<template>
  <div class="block bg-white mt-10! p-5 mx-4 rounded-3xl">
    <h1 class="text-3xl md:text-5xl font-poetsen-one text-red-600 text-center mb-5">
      Welcome to Menu Mingles!
    </h1>

    <h5 class="text-xl text-neutral-500 mt-4 mb-2">Your allergies</h5>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      <div
        v-for="allergen in possibleAllergies"
        class="bg-neutral-200 rounded-3xl flex items-center flex-nowrap gap-2 outline-4 outline-transparent"
        :class="{ 'outline-red-500! bg-red-200!': checkedAllergies.includes(allergen.name) }"
      >
        <input
          @change="toggleAllergy(allergen)"
          type="checkbox"
          :id="allergen.name"
          class="ms-4 cursor-pointer select-none w-4 h-4 bg-gray-100! border-gray-300! focus:ring-blue-500! focus:ring-2!"
        />
        <label :for="allergen.name" class="grow py-3 cursor-pointer select-none">
          {{ allergen.name }}
        </label>
      </div>
    </div>

    <h5 class="text-xl text-neutral-500 mt-5 mb-2">Any long term goals?</h5>

    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      <div
        @click="toggleLongTermGoal(goal)"
        v-for="goal in possibleLongTermGoals"
        class="bg-neutral-200 rounded-3xl p-5 outline-4 outline-transparent cursor-pointer flex flex-col items-center justify-center gap-3 h-full"
        :class="{ 'outline-red-500! bg-red-200!': checkedLongTermGoals.includes(goal.name) }"
      >
        <div class="w-7/8 aspect-square">
          <CustomImage :src="`/assets/long-term-goals/${goal.image}`" />
        </div>

        <span class="text-center font-bold">{{ goal.name }}</span>
      </div>
    </div>

    <button
      @click="onSubmit"
      class="my-8 rounded-2xl bg-red-600 disabled:bg-gray-700 disabled:hover:bg-gray-700 disabled:cursor-not-allowed hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
    >
      <span class="hidden md:block">Continue</span>
      <i class="ti ti-arrow-right text-2xl"></i>
    </button>
  </div>
</template>

<style scoped></style>
