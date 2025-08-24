import { z } from 'zod'


export const calendarMenusSchema = z.object({
  monday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  tuesday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  wednesday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  thursday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  friday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  saturday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  sunday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
})
