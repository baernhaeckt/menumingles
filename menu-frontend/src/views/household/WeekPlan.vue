<script setup lang="ts">
import { useHead } from '@unhead/vue'
import dayjs from 'dayjs'
import ShoppingList from '@/components/ShoppingList.vue'
import CustomImage from '@/components/CustomImage.vue'
import { ref } from 'vue'

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
        name: 'Vegetarian Lasagna',
        ingredients: ['Italian', 'Cheese', 'Tomatoes'],
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
        image: 'https://example.com/spaghetti-carbonara.jpg',
      },
    ],
  },
]

const collapsed = ref(true);
const toggleCollapse = () => {
  collapsed.value = !collapsed.value;
}
</script>

<template>
  <div class="block bg-white mt-10! p-5 mx-4 rounded-3xl">
    <h1 class="text-5xl font-poetsen-one text-red-600 text-center">
      <i class="ti ti-calendar-week"></i>
      Menu Plan
    </h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-10 mt-3">
      <div class="flex flex-col gap-2 row-2 md:row-1">
        <div v-for="date in dates">
          <h5 class="text-neutral-500 ps-5 mb-2">{{ dayjs(date.date).format('dddd') }}</h5>
          <div
            v-for="(meal, i) in date.meals"
            class="bg-neutral-200 rounded-3xl p-2 flex flex-row items-center gap-2"
            :class="{
              'mb-4': i !== date.meals.length - 1,
              'bg-red-200 outline-4 outline-red-500 attention-pulse': dayjs(date.date).isSame(
                dayjs(),
                'date',
              ),
            }"
          >
            <div class="w-24 h-16 min-w-24 rounded-2xl">
              <CustomImage :src="meal.image" />
            </div>

            <div class="flex flex-col">
              <h5 class="font-bold">{{ meal.name }}</h5>
              <p class="text-xs text-neutral-500">
                <span v-for="(ingredient, i) in meal.ingredients"
                  >{{ ingredient }}<span v-if="i !== meal.ingredients.length - 1">, </span></span
                >
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-emerald-600 p-5 px-7 rounded-3xl mt-4">
        <div class="flex flex-row items-center gap-5 md:justify-center">
          <h2 class="text-white font-poetsen-one text-3xl">Shopping list</h2>
          <i @click="toggleCollapse" v-if="collapsed" class="block md:hidden ti ti-chevron-down text-white text-3xl ms-auto cursor-pointer"></i>
          <i @click="toggleCollapse" v-else-if="!collapsed" class="block md:hidden ti ti-chevron-up text-white text-3xl ms-auto cursor-pointer"></i>
        </div>

        <div :class="{ 'hidden md:block': collapsed }">
          <ShoppingList />
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
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 1);
  }
  60% {
    opacity: 0.2;
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0.5);
  }
  100% {
    opacity: 0;
    box-shadow: 0 0 0 14px rgba(239, 68, 68, 0);
  }
}
</style>
