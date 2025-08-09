import React from 'react'
import { Button } from '@/components/ui/button'
import { extractText } from '@/lib/extractText'
import { analyzeDocument } from '@/lib/ai'
import { get, set } from 'idb-keyval'
import { toast } from 'sonner'

export function ReprocessOne({ docId }: { docId: string }) {
  const [busy, setBusy] = React.useState(false)

  const run = async () => {
    setBusy(true)
    try {
      const doc: any = await get(docId)
      if (!doc) return toast.error('Document not found')

      let text = doc.text || ''
      if ((!text || text.length < 100) && doc.rawArrayBuffer) {
        const file = new File([doc.rawArrayBuffer], doc.name, { type: doc.mimeType || 'application/pdf' })
        text = await extractText(file)
      }
      const analysis = await analyzeDocument(text, doc)
      await set(docId, {
        ...doc,
        text,
        needsReview: !text || text.length < 100 || !analysis?.summary,
        severity: analysis?.severity ?? doc.severity ?? 'Medium',
        entities: analysis?.entities ?? doc.entities ?? [],
        legalCodes: analysis?.legalCodes ?? doc.legalCodes ?? [],
        violations: analysis?.violations ?? doc.violations ?? [],
        contradictions: analysis?.contradictions ?? doc.contradictions ?? [],
        lastModified: new Date().toISOString()
      })
      toast.success('Reprocessed')
    } catch (e) {
      toast.error('Failed to reprocess this document')
      console.error(e)
    } finally {
      setBusy(false)
    }
  }

  return (
    <Button size="sm" variant="outline" disabled={busy} onClick={run}>
      {busy ? 'Reprocessing…' : 'Reprocess This'}
    </Button>
  )
}
