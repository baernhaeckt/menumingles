<script setup lang="ts"></script>

<template>
  <div class="block bg-white mt-10! p-5 py-24 mx-4 rounded-3xl">
    <img
      src="@/assets/illustrations/undraw_group-project_kow1.svg"
      alt="illustration"
      class="h-36 w-auto mx-auto mb-16"
    />

    <h1 class="text-center text-red-600 font-poetsen-one text-5xl mb-2">"WG Bern"</h1>
    <h2 class="mb-12! text-center text-2xl text-neutral-500">
      You have been invited to this household.<br />Register an account to accept the invitation.
    </h2>

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
</template>

<style scoped></style>
