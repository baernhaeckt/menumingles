import './assets/main.css'

import { createPinia } from 'pinia'
import { createApp } from 'vue'

import Particles from '@tsparticles/vue3'
import { loadFull } from 'tsparticles'

import ToastPlugin from 'vue-toast-notification'

import { createHead } from '@unhead/vue/client'
import App from './App.vue'
import router from './router'
import { useSessionKeyStore } from './stores/sessionKey'

const app = createApp(App)
  .use(Particles, {
    init: async (engine) => {
      await loadFull(engine)
    },
  })
  .use(ToastPlugin)
  .use(createHead())

app.use(createPinia())
app.use(router)

// Initialize session key store from localStorage
const sessionKeyStore = useSessionKeyStore()
sessionKeyStore.initFromStorage()

app.mount('#app')
