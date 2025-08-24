import { z } from 'zod'

/**
 * Zod schema for chat messages.
 * Corresponds to the Pydantic ChatMessage model.
 */
export const ChatMessageSchema = z.object({
  type: z.enum(['chat', 'fridge', "planning", 'planning_finished']),
  name: z.string(),
  message: z.string(),
  timestamp: z.number().optional()
})

export type ChatMessage = z.infer<typeof ChatMessageSchema>
