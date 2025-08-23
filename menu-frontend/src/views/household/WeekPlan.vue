<script setup lang="ts">
import { useHead } from '@unhead/vue'
import dayjs from 'dayjs'

useHead({
  title: 'Week • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Manage your household menu plan',
    },
  ],
  link: [
    {
      rel: 'icon',
    },
  ],
})

const dates = [
  {
    date: dayjs().subtract(1, 'days').format('YYYY-MM-DD'),
    meals: [
      {
        name: 'Spaghetti Carbonara',
        ingredients: ['Italian', 'Antipasta', 'Sauce', 'Eggs', 'Meat', 'Spices', 'Cheese'],
        allergies: ['Gluten', 'Dairy', 'Egg'],
        image: 'https://example.com/spaghetti-carbonara.jpg',
      },
    ],
  },
  {
    date: dayjs().format('YYYY-MM-DD'),
    meals: [
      {
        name: 'Indian Curry',
        ingredients: [
          'Indian',
          'Rice',
          'Spices',
          'Meat',
          'Cheese',
          'Lentils',
          'Onions',
          'Tomatoes',
        ],
        allergies: ['Gluten', 'Dairy', 'Egg'],
        image: 'https://example.com/spaghetti-carbonara.jpg',
      },
    ],
  },
  {
    date: dayjs().add(1, 'days').format('YYYY-MM-DD'),
    meals: [
      {
        name: 'Embly',
        ingredients: ['Swiss', 'Onions', 'Tomatoes'],
        allergies: ['Gluten'],
        image: 'https://example.com/spaghetti-carbonara.jpg',
      },
      {
        name: 'Vegetarian Lasagna',
        ingredients: ['Italian', 'Cheese', 'Tomatoes'],
        allergies: [],
        image: 'https://example.com/spaghetti-carbonara.jpg',
      },
    ],
  },
  {
    date: dayjs().add(2, 'days').format('YYYY-MM-DD'),
    meals: [
      {
        name: 'Hamburger',
        ingredients: ['Meat', 'Cheese', 'Buns', 'Salad', 'Onions', 'Tomatoes', 'Bacon'],
        allergies: ['Gluten', 'Dairy', 'Egg', 'Meat'],
        image: 'https://example.com/spaghetti-carbonara.jpg',
      },
    ],
  },
]
</script>

<template>
  <div class="block bg-white mt-10! p-5 mx-4 rounded-3xl">
    <h1 class="text-5xl font-poetsen-one text-red-600 text-center">
      <i class="ti ti-calendar-week"></i>
      Week menu-plan
    </h1>

    <div class="mt-10 flex flex-col gap-2">
      <div v-for="date in dates">
        <h5 class="text-neutral-500 ps-5 mb-2">{{ dayjs(date.date).format('dddd') }}</h5>
        <div
          v-for="(meal, i) in date.meals"
          class="bg-neutral-200 rounded-3xl p-2 flex flex-row gap-2"
          :class="{
            'mb-4': i !== date.meals.length - 1,
            'bg-red-200 outline-4 outline-red-500 attention-pulse': dayjs(date.date).isSame(
              dayjs(),
              'date',
            ),
          }"
        >
          <img
            :src="meal.image"
            :alt="`${meal.name} picture`"
            class="w-24 h-24 bg-black text-neutral-400 px-2 rounded-2xl"
          />
          <div class="flex flex-col">
            <h5 class="font-bold">{{ meal.name }}</h5>
            <p>
              <span v-for="(ingredient, i) in meal.ingredients"
                >{{ ingredient }}<span v-if="i !== meal.ingredients.length - 1">, </span></span
              >
            </p>

            <p v-if="meal.allergies.length > 0" class="mt-auto text-neutral-500">
              <i class="ti ti-wheat-off"></i>
              <span v-for="(allergy, i) in meal.allergies"
                >{{ allergy }}<span v-if="i !== meal.allergies.length - 1">, </span></span
              >
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.attention-pulse {
  position: relative;
}

/* Expanding, fading ring outside the rounded card */
.attention-pulse::after {
  content: '';
  position: absolute;
  inset: -2px; /* start just outside */
  border-radius: 1.5rem; /* match rounded-3xl */
  border: 2px solid #ef4444; /* Tailwind red-500 */
  pointer-events: none;
  animation: attention-ring 1.5s ease-out infinite;
}

@keyframes attention-ring {
  0% {
    opacity: 0.85;
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  60% {
    opacity: 0.2;
    transform: scaleX(1.015) scaleY(1.10) scaleZ(1.01);
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
  100% {
    opacity: 0;
    transform: scaleX(1.02) scaleY(1.15) scaleZ(1.02);
    box-shadow: 0 0 0 14px rgba(239, 68, 68, 0);
  }
}
</style>
