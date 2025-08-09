import { useEffect, useState } from "react";
const STORAGE_KEY="justice_portal_access_v1"; const PASSPHRASE="JACE+JOSH2025"; // change before sharing
export default function AccessGate({children}:{children:React.ReactNode}){
  const [ok,setOk]=useState(false); const [input,setInput]=useState("");
  useEffect(()=>{ setOk(localStorage.getItem(STORAGE_KEY)==="ok") },[]);
  function submit(e:React.FormEvent){
    e.preventDefault();
    if(input.trim()===PASSPHRASE){
      localStorage.setItem(STORAGE_KEY,"ok");
      setOk(true);
    } else alert("Incorrect passphrase.");
  }

  useEffect(() => {
    if (ok && (!location.hash || location.hash === "#/")) {
      location.hash = "#/front";
    }
  }, [ok]);

  if(ok) return <>{children}</>;
  return(<div className="min-h-screen flex items-center justify-center p-6 bg-neutral-100">
    <div className="w-full max-w-md rounded-2xl shadow-lg bg-white p-6 space-y-4">
      <h1 className="text-xl font-semibold">Justice Packet Portal</h1>
      <p className="text-sm text-neutral-600">Enter the passphrase. Need access? Email
        <a className="underline" href="mailto:Godspathtojustice@gmail.com"> Godspathtojustice@gmail.com</a> or text (616) 333-0486.</p>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full rounded-xl border p-2 outline-none" type="password" placeholder="Passphrase" value={input} onChange={e=>setInput(e.target.value)} />
        <button className="w-full rounded-xl bg-black text-white py-2" type="submit">Continue</button>
      </form></div></div>)
}
