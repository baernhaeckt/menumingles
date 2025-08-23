import { defineStore } from 'pinia'
import { useCookies } from '@vueuse/integrations/useCookies'
import dayjs from 'dayjs'
import objectSupport from 'dayjs/plugin/objectSupport'
dayjs.extend(objectSupport)

type JwtPayload = {
  nameid: string
  unique_name: string
  email: string
  nbf: number
  exp: number
  iat: number
  iss: string
  aud: string
  // [k: string]: unknown
}

function base64UrlDecode(input: string) {
  // Replace URL-safe chars and pad
  input = input.replace(/-/g, '+').replace(/_/g, '/')
  const pad = input.length % 4
  if (pad) input += '='.repeat(4 - pad)
  return decodeURIComponent(
    atob(input)
      .split('')
      .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join(''),
  )
}

function parseJwt<T extends object = JwtPayload>(token: string): T | null {
  try {
    const [, payload] = token.split('.')
    if (!payload) return null
    return JSON.parse(base64UrlDecode(payload)) as T
  } catch {
    return null
  }
}

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? decodeURIComponent(match[2]) : null
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as { username?: string; email?: string } | null,
  }),
  getters: {
    isAuthenticated: (session) => !!session.token,
    username: (session) => session.user?.username,
  },
  actions: {
    initFromCookie() {
      const cookies = useCookies(['menu-session'])
      const token = cookies.get('menu-session')

      if (!token) {
        this.token = null
        this.user = null
        return
      }
      this.token = token
      const payload = parseJwt(token)
      this.user = {
        username: (payload?.unique_name as string) || (payload?.nameid as string),
        email: payload?.email,
      }
    },
    loginWithToken(token: string) {
      this.token = token
      const payload = parseJwt(token)
      this.user = {
        username: (payload?.unique_name as string) || (payload?.nameid as string),
        email: payload?.email,
      }
      const cookies = useCookies(['menu-session'])
      cookies.set('menu-session', encodeURIComponent(token), {
        sameSite: 'lax',
        path: '/',
        expires: payload
          ? dayjs({ seconds: payload.exp }).toDate()
          : dayjs().add(1, 'day').toDate(),
      })
    },
    logout() {
      this.token = null
      this.user = null
      const cookies = useCookies(['menu-session'])
      cookies.remove('menu-session')
    },
  },
})
