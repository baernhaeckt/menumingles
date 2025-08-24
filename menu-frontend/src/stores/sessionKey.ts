import { defineStore } from 'pinia'

const SESSION_KEY_STORAGE_KEY = 'menu-session-key'

export const useSessionKeyStore = defineStore('sessionKey', {
  state: () => ({
    sessionKey: null as string | null,
  }),
  getters: {
    hasSessionKey: (state) => !!state.sessionKey,
    getSessionKey: (state) => state.sessionKey,
  },
  actions: {
    /**
     * Initialize the store from localStorage
     */
    initFromStorage() {
      try {
        const storedKey = localStorage.getItem(SESSION_KEY_STORAGE_KEY)
        if (storedKey) {
          this.sessionKey = storedKey
        }
      } catch (error) {
        console.warn('Failed to load session key from localStorage:', error)
        this.sessionKey = null
      }
    },

    /**
     * Set a new session key and store it in localStorage
     * @param sessionKey - The new session key to set
     */
    setSessionKey(sessionKey: string) {
      if (!sessionKey || sessionKey.trim() === '') {
        console.warn('Attempted to set empty session key')
        return
      }

      this.sessionKey = sessionKey
      try {
        localStorage.setItem(SESSION_KEY_STORAGE_KEY, sessionKey)
      } catch (error) {
        console.warn('Failed to save session key to localStorage:', error)
      }
    },

    /**
     * Clear the session key and remove it from localStorage
     */
    clearSessionKey() {
      this.sessionKey = null
      try {
        localStorage.removeItem(SESSION_KEY_STORAGE_KEY)
      } catch (error) {
        console.warn('Failed to remove session key from localStorage:', error)
      }
    },
  },
})
