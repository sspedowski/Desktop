import { useEffect, useState } from "react";
import { findAgencyByCode } from "../data/agencies";

const SESSION_KEY = "justice_portal_agency_v1";

export default function AccessGate({children}:{children:React.ReactNode}){
  const [session, setSession] = useState<{ agencyId: string; agencyName: string } | null>(null);
  const [code, setCode] = useState("");
  const [pass, setPass] = useState("");

  useEffect(()=>{
    try {
      const raw = localStorage.getItem(SESSION_KEY);
      if (raw) setSession(JSON.parse(raw));
    } catch { /* ignore */ }
  },[]);

  function signOut(){
    localStorage.removeItem(SESSION_KEY);
    setSession(null);
    location.hash = "#/";
  }

  function submit(e:React.FormEvent){
    e.preventDefault();
    const agency = findAgencyByCode(code || "");
    if (!agency) return alert("Unknown agency code. Please check and try again.");
    if (pass.trim() !== agency.passphrase) return alert("Incorrect passphrase for agency.");
    const payload = { agencyId: agency.id, agencyName: agency.name };
    localStorage.setItem(SESSION_KEY, JSON.stringify(payload));
    setSession(payload);
    location.hash = "#/front";
  }

  if (session) {
    return (<div className="min-h-screen bg-neutral-100 p-6">
      <div className="max-w-3xl mx-auto">
        <div className="rounded-2xl bg-white shadow p-6 flex items-center justify-between">
          <div>
            <div className="text-sm text-neutral-500">Signed in as</div>
            <div className="font-medium">{session.agencyName}</div>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={signOut} className="rounded-xl border px-4 py-2">Sign out</button>
          </div>
        </div>
        <div className="mt-6">{children}</div>
      </div>
    </div>);
  }

  return(<div className="min-h-screen flex items-center justify-center p-6 bg-neutral-100">
    <div className="w-full max-w-md rounded-2xl shadow-lg bg-white p-6 space-y-4">
      <h1 className="text-xl font-semibold">Justice Packet Portal — Agency Login</h1>
      <p className="text-sm text-neutral-600">Enter your agency code and passphrase. Need access? Email
        <a className="underline" href="mailto:Godspathtojustice@gmail.com"> Godspathtojustice@gmail.com</a> or text (616) 333-0486.</p>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full rounded-xl border p-2 outline-none" type="text" placeholder="Agency code (e.g. OVR-A)" value={code} onChange={e=>setCode(e.target.value)} />
        <input className="w-full rounded-xl border p-2 outline-none" type="password" placeholder="Agency passphrase" value={pass} onChange={e=>setPass(e.target.value)} />
        <button className="w-full rounded-xl bg-black text-white py-2" type="submit">Continue</button>
      </form></div></div>)
}
