<script setup lang="ts">
import { QrcodeSvg } from 'qrcode.vue'
import { useToast } from 'vue-toast-notification'
import { useHead } from '@unhead/vue'

const copyInviteLink = async () => {
  await navigator.clipboard.writeText(
    'https://menu-mingles-frontend-cccnfba0ezc2dhbc.northeurope-01.azurewebsites.net/auth/register?householdInviteCode=23892',
  )

  const $toast = useToast()
  $toast.success('<i class="ti ti-circle-check-filled"></i> Invite link copied to clipboard')
}

useHead({
  title: 'Profile • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Manage your account and household settings',
    },
  ],
  link: [
    {
      rel: 'icon',
    }
  ]
})
</script>

<template>
  <div class="block bg-white mt-10! p-5 mx-4 rounded-3xl">
    <div class="flex flex-row items-center gap-5 flex-nowrap mb-12">
      <img
        src="@/assets/peter.jpg"
        alt="profile picture"
        class="w-24 h-24 rounded-full border-2 border-neutral-700"
      />
      <div>
        <h1 class="text-3xl font-poetsen-one text-red-600">peter@xyz.xyz</h1>
        <h1 class="text-lg text-neutral-600">
          You're part of <span class="text-red-600">"WG Bern"</span>
        </h1>
      </div>
    </div>

    <div class="bg-neutral-200 rounded-2xl p-5 mb-5">
      <h2 class="font-poetsen-one text-xl mb-3">Invite new people</h2>

      <div class="flex flex-row flex-nowrap gap-5">
        <!-- do not stretch button -->
        <div>
          <p class="text-neutral-500 mb-2">
            Add new people to your household by scanning the QR code or sending this invitation
            link. People in your household can vote what food they like and their allergies will be
            respected for menu planing.
          </p>
          <button
            @click="copyInviteLink"
            class="rounded-2xl bg-red-600 px-6 py-4 text-white font-bold cursor-pointer text-center"
          >
            Copy invite link
          </button>
        </div>

        <div class="p-3 bg-white rounded-2xl">
          <qrcode-svg
            value="https://menu-mingles-frontend-cccnfba0ezc2dhbc.northeurope-01.azurewebsites.net/auth/register?householdInviteCode=23892"
            level="H"
            :size="250"
          />
        </div>
      </div>
    </div>

    <a href="https://www.transgourmet.ch/de/pg" class="rounded-2xl">
      <div class="bg-red-500 rounded-2xl p-5">
        <div class="flex flex-nowrap items-center gap-5">
          <i class="ti ti-external-link text-white text-5xl"></i>
          <div>
            <h2 class="font-poetsen-one text-white text-2xl">
              Craving for fresh ingredients and foods?
            </h2>
            <p class="m-0 text-white">
              Click here to check out our online store with unbeatable variety and over 25'000+
              products
            </p>
          </div>
        </div>
      </div>
    </a>
  </div>
</template>

<style scoped></style>
