export const logError = (scope: string, err: unknown) => {
  console.error(`[${scope}]`, err)
}
