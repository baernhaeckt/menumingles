<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'
import { z } from 'zod'
import { httpClient } from '@/client/http-client.ts'
import { validate } from '@/forms/validation.ts'
import { useToast } from 'vue-toast-notification'
import router from '@/router'
import { getErrorMessage } from '@/schemas/backend-error.ts'

const route = useRoute()
const hasInvite = computed(() => !!route.query.householdInviteCode)

useHead({
  title: hasInvite.value ? 'Accept invitation • Menu Mingles' : 'Register • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: hasInvite.value
        ? 'Accept the invitation to join your household'
        : 'Create a new account to start your own household',
    },
  ],
  link: [],
})

const registerSchema = z
  .object({
    username: z.string().trim().min(1, 'Username is required'),
    email: z.email().trim().min(1, 'Email is required'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain an uppercase letter')
      .regex(/[a-z]/, 'Password must contain a lowercase letter')
      .regex(/[0-9]/, 'Password must contain a number')
      .regex(/[^A-Za-z0-9]/, 'Password must contain a symbol'),
    confirmPassword: z.string(),
    householdName: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords must match',
    path: ['confirmPassword'],
  })
  .refine((data) => data.householdName.length > 0 || hasInvite.value, {
    message: 'Household name is required',
    path: ['householdName'],
  })

type RegisterForm = z.infer<typeof registerSchema>

const form = reactive<RegisterForm>({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  householdName: '',
})

const apiError = ref<string | null>(null)

const fieldErrors = ref<{
  email?: string
  password?: string
  confirmPassword?: string
  username?: string,
  householdName?: string,
}>({})
const submitting = ref(false)

function validateForm(): boolean {
  return validate<RegisterForm>(registerSchema, form, fieldErrors)
}

async function onSubmit() {
  if (!validateForm()) return
  submitting.value = true
  apiError.value = null
  try {
    const toast = useToast()

    const payload: Record<string, unknown> = {
      email: form.email.trim(),
      username: form.username.trim(),
      password: form.password,
      household: !route.query.householdInviteCode ? form.householdName.trim() : null,
      householdKey: route.query.householdInviteCode ? (route.query.householdInviteCode as string) : null,
    }

    await httpClient.post('/v1/auth/register', payload);
    toast.success('<i class="ti ti-circle-check-filled"></i> Successfully registered. Please login to continue.');
    await router.push({ name: 'login' })
  } catch (e: any) {
    apiError.value = getErrorMessage(e);
  } finally {
    submitting.value = false
  }
}

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
        duration: 1.5,
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
        duration: 1.5,
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
  <div class="block bg-white mt-10! p-5 py-12 md:py-24 mx-4 rounded-3xl">
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
      <h1 class="text-center text-red-600 font-poetsen-one text-3xl md:text-5xl mb-2">"WG Bern"</h1>
      <h2 class="mb-12! text-center text-lg md:text-2xl text-gray-700">
        You have been invited to this household.<br />Register an account to accept the invitation.
      </h2>
    </div>
    <div v-else>
      <h1 class="text-center text-red-600 font-poetsen-one text-3xl md:text-5xl mb-2">Register</h1>
      <h2 class="mb-12! text-center text-lg md:text-2xl text-gray-700">
        You are creating a new household.<br />Register an account to start.
      </h2>
    </div>

    <form @submit.prevent="onSubmit" novalidate>
      <div class="md:w-1/2! mx-auto mb-5">
        <label class="text-neutral-600" for="account-username"
          >Username <span class="text-orange-500">*</span></label
        >
        <input
          id="account-username"
          type="email"
          placeholder="Dan"
          v-model="form.username"
          autocomplete="name"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />

        <p v-if="fieldErrors.username" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.username }}
        </p>
      </div>

      <div class="md:w-1/2! mx-auto mb-5">
        <label class="text-neutral-600" for="account-email"
          >E-Mail <span class="text-orange-500">*</span></label
        >
        <input
          id="account-email"
          type="email"
          v-model="form.email"
          autocomplete="email"
          placeholder="dan@mingle.xyz"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />
        <p v-if="fieldErrors.email" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.email }}
        </p>
      </div>

      <div class="md:w-1/2! mx-auto mb-5">
        <label class="text-neutral-600" for="account-password"
          >Password <span class="text-orange-500">*</span></label
        >
        <input
          id="account-password"
          type="password"
          v-model="form.password"
          autocomplete="password"
          placeholder="●●●●●●●●●●●●"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />

        <p v-if="fieldErrors.password" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.password }}
        </p>
      </div>

      <div class="md:w-1/2! mx-auto mb-5">
        <label class="text-neutral-600" for="confirm-account-password"
          >Confirm password <span class="text-orange-500">*</span></label
        >
        <input
          id="confirm-account-password"
          type="password"
          v-model="form.confirmPassword"
          autocomplete="password"
          placeholder="●●●●●●●●●●●●"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />
        <p v-if="fieldErrors.confirmPassword" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.confirmPassword }}
        </p>
      </div>

      <div v-if="!hasInvite" class="md:w-1/2! mx-auto mb-5">
        <label class="text-neutral-600" for="household-name"
          >Household name <span class="text-orange-500">*</span></label
        >
        <input
          id="household-name"
          type="text"
          placeholder="WG Bern"
          v-model="form.householdName"
          autocomplete="name"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />

        <p v-if="fieldErrors.householdName" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.householdName }}
        </p>
      </div>

      <div v-if="apiError" class="bg-red-300 rounded-3xl p-5 text-red-800 mb-8 md:w-1/2! mx-auto">
        <i class="ti ti-exclamation-circle-filled"></i>
        {{ apiError }}
      </div>

      <div class="md:w-1/2! mx-auto">
        <button
          type="submit"
          :disabled="submitting"
          class="rounded-2xl bg-red-600 hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
        >
          Register
        </button>
      </div>

      <div class="md:w-1/2! mx-auto mt-5">
        <RouterLink to="/auth/login">
          <div class="rounded-3xl p-5 bg-neutral-200 underline text-neutral-500">
            Already have an account? Click here to login
          </div>
        </RouterLink>
      </div>
    </form>
  </div>

  <vue-particles v-if="hasInvite" id="tsparticles" :options="particleConfig" />
</template>

<style scoped></style>
