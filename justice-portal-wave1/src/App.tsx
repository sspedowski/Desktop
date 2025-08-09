import AccessGate from "./routes/AccessGate"; import Exhibits from "./routes/Exhibits"; import Viewer from "./routes/Viewer";
import { useEffect, useState } from "react";
function useRoute(){ const [route,setRoute]=useState<string>(location.hash||"#/"); useEffect(()=>{ const on=()=>setRoute(location.hash||"#/"); addEventListener("hashchange",on); return ()=>removeEventListener("hashchange",on)},[]); return route }
function RouterView(){ const route=useRoute(); if(route.startsWith("#/viewer/")) return <Viewer />; if(route.startsWith("#/exhibits")) return <Exhibits />;
  return (<div className="min-h-screen bg-neutral-100"><div className="max-w-3xl mx-auto p-6"><div className="rounded-2xl bg-white shadow-sm p-6 space-y-4">
    <h1 className="text-2xl font-semibold">Justice Packet Portal (Wave 1)</h1>
    <p className="text-neutral-700">Secure guest access to exhibits for oversight agencies and media. Full packet includes Cover Letter, Executive Summary, and Contradictions Table.</p>
    <a className="inline-block rounded-xl bg-black text-white px-4 py-2" href="#/exhibits">Enter</a></div></div></div>) }
export default function App(){ return (<AccessGate><RouterView /></AccessGate>) }
