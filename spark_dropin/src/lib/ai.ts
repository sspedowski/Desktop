export async function analyzeDocument(text: string, doc?: any) {
  // TODO: call your spark.llm wrapper; return a normalized shape
  return {
    summary: doc?.summary ?? (text?.slice(0, 200) ? `Auto-summary: ${text.slice(0, 200)}…` : ''),
    entities: doc?.entities ?? [],
    legalCodes: doc?.legalCodes ?? [],
    violations: doc?.violations ?? [],
    contradictions: doc?.contradictions ?? [],
    severity: doc?.severity ?? 'Medium',
  }
}
