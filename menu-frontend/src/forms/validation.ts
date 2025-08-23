import { z, type ZodSchema } from 'zod'
import type { Ref } from 'vue'

export type FieldErrors<T extends object> = Partial<Record<keyof T, string>>

/**
 * Validate a form against a Zod schema.
 * - Writes first error per field into `fieldErrors`
 * - Returns true if valid, false otherwise
 */
export function validate<T extends object>(
  schema: ZodSchema<T>,
  form: unknown,
  fieldErrors: Ref<FieldErrors<T>>,
): form is T {
  const parsed = schema.safeParse(form)
  if (parsed.success) {
    fieldErrors.value = {}
    return true
  }

  const errs: FieldErrors<T> = {}
  for (const issue of parsed.error.issues) {
    const key = issue.path[0] as keyof T | undefined
    if (key && !errs[key]) {
      errs[key] = issue.message
    }
  }
  fieldErrors.value = errs
  return false
}
