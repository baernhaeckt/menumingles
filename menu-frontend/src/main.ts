import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import Particles from '@tsparticles/vue3'
import { loadFull } from 'tsparticles'

import ToastPlugin from 'vue-toast-notification'

import App from './App.vue'
import router from './router'
import { createHead } from '@unhead/vue/client'

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

app.mount('#app')
