import { defineStore } from 'pinia'
import { useCookies } from '@vueuse/integrations/useCookies'
import dayjs from 'dayjs'
import objectSupport from 'dayjs/plugin/objectSupport'
import gravatarUrl from 'gravatar-url'

dayjs.extend(objectSupport)

type JwtPayload = {
  nameid: string
  unique_name: string
  email: string
  household: string
  householdKey: string
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

type User = { username?: string; email?: string, household: string, householdKey: string };

function getUserFromPayload(payload: JwtPayload | null): User {
  return {
    username: (payload?.unique_name as string) || (payload?.nameid as string),
    email: payload?.email,
    household: payload?.household as string,
    householdKey: payload?.householdKey as string,
  };
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as User | null
  }),
  getters: {
    isAuthenticated: (session) => !!session.token,
    username: (session) => session.user?.username,
    email: (session) => session.user?.email,
    householdKey: (session) => session.user?.householdKey,
    householdName: (session) => session.user?.household,
    getGravatarUrl: (session) => {
      const email = session.user?.email?.trim().toLowerCase();
      if (!email) return null;
      return gravatarUrl(email, { size: 200 });
    }
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
      this.user = getUserFromPayload(payload);
    },
    loginWithToken(token: string) {
      this.token = token
      const payload = parseJwt(token)
      this.user = getUserFromPayload(payload);
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
