import React from 'react'
import { Button } from '@/components/ui/button'
import { reprocessAllExisting } from '@/lib/reprocess'
import { toast } from 'sonner'

export function ReprocessButtons() {
  const [busy, setBusy] = React.useState(false)
  const [progress, setProgress] = React.useState<{ processed: number; total: number } | null>(null)
  const abortRef = React.useRef<AbortController | null>(null)

  const run = async (failedOnly: boolean) => {
    if (busy) return
    setBusy(true)
    setProgress({ processed: 0, total: 0 })

    const ac = new AbortController()
    abortRef.current = ac

    try {
      const res = await reprocessAllExisting({
        failedOnly,
        concurrency: 3,
        signal: ac.signal,
        onProgress: (p) => setProgress({ processed: p.processed, total: p.total }),
      })
      if (res.cancelled) {
        toast('Reprocess cancelled', {
          description: `${res.processed}/${res.total} processed before cancel.`,
        })
      } else {
        toast.success('Reprocess complete', {
          description: `${res.updated} updated, ${res.failed} failed, ${res.skipped} skipped.`,
        })
      }
    } catch (e) {
      toast.error('Reprocess failed')
      console.error(e)
    } finally {
      setBusy(false)
      abortRef.current = null
    }
  }

  const cancel = () => {
    abortRef.current?.abort()
  }

  return (
    <div className="flex items-center gap-2">
      <Button variant="secondary" disabled={busy} onClick={() => run(true)}>
        {busy ? 'Reprocessing…' : 'Reprocess All (failed only)'}
      </Button>
      <Button variant="outline" disabled={busy} onClick={() => run(false)}>
        Reprocess All (everything)
      </Button>
      {busy && (
        <>
          <span className="text-sm text-muted-foreground">
            {progress ? `${progress.processed}/${progress.total}` : ''}
          </span>
          <Button variant="ghost" size="sm" onClick={cancel}>
            Cancel
          </Button>
        </>
      )}
    </div>
  )
}
