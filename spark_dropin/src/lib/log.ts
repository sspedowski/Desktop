export function logError(event: string, data?: any) {
  // Minimal logger stub; integrate with your analytics if desired
  try {
    // eslint-disable-next-line no-console
    console.warn(`[${event}]`, data || {})
  } catch {
    // no-op
  }
}
