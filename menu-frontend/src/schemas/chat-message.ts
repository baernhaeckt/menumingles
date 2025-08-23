import { z } from 'zod'

/**
 * Zod schema for chat messages.
 * Corresponds to the Pydantic ChatMessage model.
 */
export const ChatMessageSchema = z.object({
  type: z.enum(['chat', 'fridge']),
  name: z.string(),
  message: z.string(),
  timestamp: z.number().optional()
})

export type ChatMessage = z.infer<typeof ChatMessageSchema>
