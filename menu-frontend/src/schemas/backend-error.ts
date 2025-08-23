import { z } from 'zod'

const errorSchema = z.object({
  response: z.object({
    data: z
      .object({
        message: z.string(),
      })
      .or(z.string())
      .optional(),
    status: z.number().min(0),
  }),
})

export const getErrorMessage = (error: unknown) => {
  const safeParse = errorSchema.safeParse(error)
  if (safeParse.success) {
    if (safeParse.data.response.data && typeof safeParse.data.response.data !== 'string') {
      return safeParse.data.response.data.message
    }

    if (safeParse.data.response.status === 401) {
      return 'Your session has expired or your login attempt was not successful. Please try again.'
    }
  }
  return 'Unknown error. Please try again later.'
}
