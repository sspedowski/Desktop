import { keys, get, set } from 'idb-keyval'
import { analyzeDocument } from '@/lib/ai'
import { extractText } from '@/lib/extractText'
import { logError } from '@/lib/log'

export type ProgressInfo = {
  total: number
  processed: number
  updated: number
  skipped: number
  failed: number
  currentId?: string
}

export type ReprocessOptions = {
  failedOnly?: boolean
  concurrency?: number
  onProgress?: (info: ProgressInfo) => void
  signal?: AbortSignal
}

function isFailedDoc(doc: any): boolean {
  if (!doc) return true
  const textLen = (doc.text?.length ?? 0)
  const hasSummary = !!doc.summary
  return !!doc.needsReview || !hasSummary || textLen < 100
}

export async function reprocessAllExisting(opts: ReprocessOptions = {}) {
  const {
    failedOnly = true,
    concurrency = 3,
    onProgress,
    signal,
  } = opts

  const allKeys = (await keys()) as any[]
  const candidateIds: string[] = []

  for (const k of allKeys) {
    if (typeof k !== 'string') continue
    try {
      const doc: any = await get(k)
      if (!doc) continue
      if (failedOnly) {
        if (isFailedDoc(doc)) candidateIds.push(k)
      } else {
        candidateIds.push(k)
      }
    } catch (e) {
      // Skip bad entries
      continue
    }
  }

  const progress: ProgressInfo = {
    total: candidateIds.length,
    processed: 0,
    updated: 0,
    skipped: 0,
    failed: 0,
  }

  let index = 0
  const next = () => candidateIds[index++]

  const report = (currentId?: string) => {
    onProgress?.({ ...progress, currentId })
  }

  report()

  const workers = Array.from({ length: Math.max(1, concurrency) }).map(async () => {
    while (true) {
      if (signal?.aborted) return
      const id = next()
      if (!id) return

      try {
        const doc: any = await get(id)
        if (!doc) {
          progress.skipped++
          progress.processed++
          report(id)
          continue
        }

        let text: string = typeof doc.text === 'string' ? doc.text : ''
        const textTooShort = !text || text.length < 100

        if ((textTooShort || failedOnly) && doc.rawArrayBuffer) {
          try {
            const file = new File([doc.rawArrayBuffer], doc.name || `${id}.pdf`, { type: doc.mimeType || 'application/pdf' })
            text = await extractText(file)
          } catch (ex) {
            // Keep going; mark needsReview if we can't extract
          }
        }

        // Analyze with current or refreshed text
        let analysis: any = undefined
        try {
          analysis = await analyzeDocument(text || doc.text || '', doc)
        } catch (ex) {
          // AI may fail; we'll still persist text/flags
        }

        const needsReview = !text || text.length < 100 || !analysis?.summary

        const updatedDoc = {
          ...doc,
          text,
          needsReview,
          severity: analysis?.severity ?? doc.severity ?? 'Medium',
          entities: analysis?.entities ?? doc.entities ?? [],
          legalCodes: analysis?.legalCodes ?? doc.legalCodes ?? [],
          violations: analysis?.violations ?? doc.violations ?? [],
          contradictions: analysis?.contradictions ?? doc.contradictions ?? [],
          summary: analysis?.summary ?? doc.summary ?? '',
          lastModified: new Date().toISOString(),
        }

        await set(id, updatedDoc)
        progress.updated++
      } catch (e: any) {
        progress.failed++
        logError('reprocess-failed', { error: e?.message || String(e) })
      } finally {
        progress.processed++
        report(id)
      }
    }
  })

  await Promise.all(workers)

  const cancelled = !!signal?.aborted
  return { ...progress, cancelled }
}
