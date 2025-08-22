import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import Particles from '@tsparticles/vue3'
import { loadFull } from 'tsparticles'

import App from './App.vue'
import router from './router'

const app = createApp(App).use(Particles, {
  init: async (engine) => {
    await loadFull(engine)
  },
})

app.use(createPinia())
app.use(router)

app.mount('#app')
