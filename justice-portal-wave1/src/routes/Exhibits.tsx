import { exhibits } from "../data/exhibits";
export default function Exhibits(){
  return(<div className="p-6 max-w-6xl mx-auto">
    <div className="flex items-center justify-between mb-4">
      <h1 className="text-2xl font-semibold">Exhibits (Wave 1)</h1>
      <div className="flex gap-4">
        <a className="underline" href="#/front">Front Matter</a>
        <a className="underline" href="#/viewer/README">How to Use</a>
      </div>
    </div>
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      {exhibits.map(ex=>(<div key={ex.id} className="rounded-2xl border shadow-sm p-4 bg-white">
        <div className="text-sm text-neutral-500 mb-1">{ex.id}</div>
        <div className="font-medium mb-2">{ex.title}</div>
        <p className="text-sm text-neutral-600 line-clamp-3">{ex.description}</p>
        <div className="mt-3 flex items-center gap-2">
          <a className="rounded-xl bg-black text-white px-3 py-1 text-sm" href={`#/viewer/${encodeURIComponent(ex.id)}`}>Open</a>
          <a className="rounded-xl border px-3 py-1 text-sm" href={ex.url} target="_blank" rel="noreferrer">View PDF</a>
        </div>
      </div>))}
    </div></div>)
}
