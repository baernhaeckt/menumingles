import { z } from 'zod'

export const calendarMenusSchema = z.object({
  results: z.record(z.string(), z.object({ name: z.string(), ingredients: z.array(z.string()) })),
})
