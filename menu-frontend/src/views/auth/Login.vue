<script setup lang="ts">
import { IconLogin2 } from '@tabler/icons-vue'
import { useHead } from '@unhead/vue'
import { z } from 'zod'
import { reactive, ref } from 'vue'
import { validate } from '@/forms/validation.ts'
import { httpClient } from '@/client/http-client.ts'
import { getErrorMessage } from '@/schemas/backend-error.ts'
import { useCookies } from '@vueuse/integrations/useCookies'
import { useToast } from 'vue-toast-notification'
import { useRouter } from 'vue-router'

useHead({
  title: 'Login • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Login to your account',
    },
  ],
  link: [
    {
      rel: 'icon',
    },
  ],
});

const cookies = useCookies(['menu-session']);
const router = useRouter();

const loginSchema = z.object({
  username: z.string().trim().min(1, 'Username is required'),
  password: z.string().trim().min(1, 'Password is required'),
})

type RegisterForm = z.infer<typeof loginSchema>

const form = reactive<RegisterForm>({
  username: '',
  password: '',
})

const apiError = ref<string | null>(null)
const fieldErrors = ref<{
  username?: string
  password?: string
}>({})
const submitting = ref(false)

function validateForm(): boolean {
  return validate<RegisterForm>(loginSchema, form, fieldErrors)
}

async function onSubmit() {
  if (!validateForm()) return
  submitting.value = true
  apiError.value = null
  try {
    const payload: Record<string, unknown> = {
      username: form.username.trim(),
      password: form.password,
    }
    const toast = useToast();

    const response = await httpClient.post<string>('/v1/auth/login', payload);
    cookies.set('menu-session', response.data, {
      sameSite: 'lax'
    });
    toast.success('Logged in successfully');
    await router.push({ name: 'home' });
  } catch (error) {
    apiError.value = getErrorMessage(error);
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="block bg-white mt-10! p-5 py-12 md:py-24 mx-4 rounded-3xl">
    <img
      src="@/assets/illustrations/undraw_enter_nwx3.svg"
      alt="illustraregistertion"
      class="h-36 w-auto mx-auto mb-16"
    />
    <h1 class="text-center text-red-600 font-poetsen-one text-3xl md:text-5xl mb-2">Login</h1>
    <h2 class="mb-12! text-center text-lg md:text-2xl text-gray-700">Welcome back!</h2>

    <form @submit.prevent="onSubmit" novalidate>
      <div class="md:w-1/2! mx-auto mb-5">
        <label class="text-neutral-600" for="account-username"
          >Username <span class="text-orange-500">*</span></label
        >
        <input
          id="account-username"
          type="text"
          placeholder="Dan"
          v-model="form.username"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />
        <p v-if="fieldErrors.username" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.username }}
        </p>
      </div>

      <div class="md:w-1/2! mx-auto mb-10">
        <label class="text-neutral-600" for="account-password"
          >Password <span class="text-orange-500">*</span></label
        >
        <input
          id="account-password"
          type="password"
          placeholder="●●●●●●●●●●●●"
          v-model="form.password"
          class="w-full bg-neutral-100 p-2 rounded-2xl outline-4 outline-transparent focus:outline-rose-600"
        />
        <p v-if="fieldErrors.password" class="text-sm text-red-600 mt-1">
          <i class="ti ti-exclamation-circle-filled"></i>
          {{ fieldErrors.password }}
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
          class="rounded-2xl bg-red-600 disabled:bg-gray-700 disabled:hover:bg-gray-700 disabled:cursor-not-allowed hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200"
        >
          Login
          <IconLogin2 size="1.2rem" />
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped></style>
