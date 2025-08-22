<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const hasInvite = computed(() => !!route.query.householdInviteCode)

const particleConfig = {
  fullScreen: {
    zIndex: 1,
  },
  emitters: [
    {
      position: {
        x: 0,
        y: 30,
      },
      rate: {
        quantity: 5,
        delay: 0.15,
      },
      life: {
        count: 1,
        duration: 1.5
      },
      particles: {
        move: {
          direction: 'top-right',
          outModes: {
            top: 'none',
            left: 'none',
            default: 'destroy',
          },
        },
      },
    },
    {
      position: {
        x: 100,
        y: 30,
      },
      rate: {
        quantity: 5,
        delay: 0.15,
      },
      life: {
        count: 1,
        duration: 1.5
      },
      particles: {
        move: {
          direction: 'top-left',
          outModes: {
            top: 'none',
            right: 'none',
            default: 'destroy',
          },
        },
      },
    },
  ],
  particles: {
    color: {
      value: ['#ffffff', '#FF0000'],
    },
    move: {
      decay: 0.05,
      direction: 'top',
      enable: true,
      gravity: {
        enable: true,
      },
      outModes: {
        top: 'none',
        default: 'destroy',
      },
      speed: {
        min: 10,
        max: 50,
      },
    },
    number: {
      value: 0,
    },
    opacity: {
      value: 1,
    },
    rotate: {
      value: {
        min: 0,
        max: 360,
      },
      direction: 'random',
      animation: {
        enable: true,
        speed: 30,
      },
    },
    tilt: {
      direction: 'random',
      enable: true,
      value: {
        min: 0,
        max: 360,
      },
      animation: {
        enable: true,
        speed: 30,
      },
    },
    size: {
      value: {
        min: 4,
        max: 7,
      },
      animation: {
        enable: true,
        startValue: 'min',
        count: 1,
        speed: 16,
        sync: true,
      },
    },
    roll: {
      darken: {
        enable: true,
        value: 25,
      },
      enable: true,
      speed: {
        min: 5,
        max: 15,
      },
    },
    wobble: {
      distance: 30,
      enable: true,
      speed: {
        min: -7,
        max: 7,
      },
    },
    shape: {
      type: ['circle', 'square'],
      options: {},
    },
  },
}
</script>

<template>
  <div class="block bg-white mt-10! p-5 py-24 mx-4 rounded-3xl">
    <img
      v-if="hasInvite"
      src="@/assets/illustrations/undraw_group-project_kow1.svg"
      alt="illustration"
      class="h-36 w-auto mx-auto mb-16"
    />
    <img
        v-else
        src="@/assets/illustrations/undraw_enter_nwx3.svg"
        alt="illustration"
        class="h-36 w-auto mx-auto mb-16"
    />

    <div v-if="hasInvite">
      <h1 class="text-center text-red-600 font-poetsen-one text-5xl mb-2">"WG Bern"</h1>
      <h2 class="mb-12! text-center text-2xl text-neutral-500">
        You have been invited to this household.<br />Register an account to accept the invitation.
      </h2>
    </div>
    <div v-else>
      <h1 class="text-center text-red-600 font-poetsen-one text-5xl mb-2">Register</h1>
      <h2 class="mb-12! text-center text-2xl text-neutral-500">
        You are creating a new household.<br />Register an account to start.
      </h2>
    </div>

    <div class="w-1/2! mx-auto mb-5">
      <label class="text-neutral-600" for="account-email"
        >Email <span class="text-orange-500">*</span></label
      >
      <input
        id="account-email"
        type="email"
        placeholder="dan@mingle.xyz"
        class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
      />
    </div>

    <div class="w-1/2! mx-auto mb-5">
      <label class="text-neutral-600" for="account-password"
        >Password <span class="text-orange-500">*</span></label
      >
      <input
        id="account-password"
        type="password"
        placeholder="●●●●●●●●●●●●"
        class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
      />
    </div>

    <div class="w-1/2! mx-auto mb-10">
      <label class="text-neutral-600" for="confirm-account-password"
        >Confirm password <span class="text-orange-500">*</span></label
      >
      <input
        id="confirm-account-password"
        type="password"
        placeholder="●●●●●●●●●●●●"
        class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
      />
    </div>

    <div class="w-1/2! mx-auto">
      <button
        class="rounded-2xl bg-red-600 hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
      >
        Register
      </button>
    </div>
  </div>

  <vue-particles v-if="hasInvite" id="tsparticles" :options="particleConfig" />
</template>

<style scoped></style>
