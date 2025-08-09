import { get, set, keys } from 'idb-keyval'
import { extractText } from './extractText'
import { analyzeDocument } from './ai'
import { logError } from './log'

export type ReprocessSummary = { total:number; fixed:number; unchanged:number; errors:number }

type ProgressFn = (n:number, total:number, name:string) => void

export async function reprocessAllExisting(
  opts: { onlyFailed?: boolean; onProgress?: ProgressFn; signal?: AbortSignal } = {}
): Promise<ReprocessSummary> {
  const { onlyFailed = true, onProgress, signal } = opts
  const allKeys = await keys()
  const docIds = allKeys.filter(k => String(k).startsWith('doc-')) as string[]
  const total = docIds.length
  let done = 0, fixed = 0, unchanged = 0, errors = 0

  const queue = [...docIds]
  const workers = 3

  const work = async () => {
    while (queue.length) {
      if (signal?.aborted) return
      const id = queue.shift()!
      const doc: any = await get(id)
      if (!doc) { done++; onProgress?.(done, total, ''); continue }

      const needs = !doc.text || doc.text.length < 100 || doc.needsReview === true
      if (onlyFailed && !needs) { unchanged++; done++; onProgress?.(done, total, doc.name); continue }

      onProgress?.(done, total, doc.name)
      try {
        let text: string = doc.text || ''
        if ((!text || text.length < 100) && doc.rawArrayBuffer) {
          const file = new File([doc.rawArrayBuffer], doc.name, { type: doc.mimeType || 'application/pdf' })
          text = await extractText(file, { signal })
        }
        if (!text) text = doc.text || ''

        const analysis = await analyzeDocument(text, doc)
        const updated = {
          ...doc,
          text,
          needsReview: !text || text.length < 100 || !analysis?.summary,
          severity: analysis?.severity ?? doc.severity ?? 'Medium',
          entities: analysis?.entities ?? doc.entities ?? [],
          legalCodes: analysis?.legalCodes ?? doc.legalCodes ?? [],
          violations: analysis?.violations ?? doc.violations ?? [],
          contradictions: analysis?.contradictions ?? doc.contradictions ?? [],
          lastModified: new Date().toISOString()
        }
        await set(id, updated)
        fixed += needs ? 1 : 0
      } catch (err) {
        errors++
        logError('reprocess', err)
      } finally {
        done++
        onProgress?.(done, total, doc.name)
      }
    }
  }

  await Promise.all(Array.from({ length: workers }, work))
  return { total, fixed, unchanged, errors }
}
