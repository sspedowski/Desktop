import { useEffect, useMemo, useState } from "react";
import { exhibits } from "../data/exhibits";
import { useConfirmation } from "../contexts/ConfirmationContext";
function useHashParam(){ const [id,setId]=useState<string|null>(null); useEffect(()=>{ const parse=()=>{ const m=location.hash.match(/#\/viewer\/(.+)$/); setId(m?decodeURIComponent(m[1]):null)}; parse(); addEventListener("hashchange",parse); return ()=>removeEventListener("hashchange",parse)},[]); return id }
export default function Viewer(){
  const id=useHashParam(); const exhibit=useMemo(()=>exhibits.find(e=>e.id===id),[id]);
  const { showConfirmation } = useConfirmation();
  if(!id) return <div className="p-6"><p className="text-sm">No exhibit selected. <a className="underline" href="#/exhibits">Back to list</a></p></div>;
  if(id==="README") return (<div className="max-w-3xl mx-auto p-6"><h1 className="text-2xl font-semibold mb-2">How to Use</h1>
    <ol className="list-decimal pl-5 space-y-2 text-sm"><li>Open an exhibit and review the PDF on the left.</li><li>Use the Notes panel to jump to highlighted pages (p./¶).</li><li>For context, see the Cover Letter & Executive Summary in your packet.</li></ol>
    <div className="mt-4"><a className="underline" href="#/exhibits">Back to Exhibits</a></div></div>);
  if(!exhibit) return <div className="p-6"><p className="text-sm">Exhibit not found: {id}. <a className="underline" href="#/exhibits">Back to list</a></p></div>;
  return (<div className="grid lg:grid-cols-[1fr_380px] min-h-screen">
    <div className="bg-neutral-50"><div className="flex items-center justify-between p-3 border-b bg-white">
      <div className="text-sm text-neutral-500">{exhibit.id}</div><a className="underline" href="#/exhibits">Back to Exhibits</a></div>
      <div className="h-[calc(100vh-48px)]"><iframe title={exhibit.title} src={exhibit.url} className="w-full h-full" /></div></div>
    <aside className="border-l bg-white p-4 overflow-auto">
      <div className="text-xs text-neutral-500">{exhibit.id}</div><h2 className="text-lg font-semibold mb-2">{exhibit.title}</h2>
      <p className="text-sm text-neutral-700 mb-3">{exhibit.description}</p>
      {exhibit.notes?.length?(<><h3 className="font-medium mb-2">Highlight Notes</h3><ul className="list-disc pl-5 space-y-2 text-sm">
        {exhibit.notes.map((n,i)=><li key={i}>{n}</li>)}</ul></>):(<p className="text-sm text-neutral-500">No notes for this exhibit.</p>)}
      <div className="mt-4">
        <button 
          className="rounded-xl bg-black text-white px-3 py-2 text-sm" 
          onClick={async () => {
            const confirmed = await showConfirmation(
              "Open PDF",
              "Are you sure you want to open this PDF in a new tab?"
            );
            if (confirmed) {
              window.open(exhibit.url, '_blank');
            }
          }}
        >
          Open PDF in New Tab
        </button>
      </div>
    </aside></div>)
}
