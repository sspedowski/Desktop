export interface Agency {
  id: string;
  name: string;
  code: string; // short code agencies will enter
  passphrase: string; // set a strong shared secret per agency
}

// Example agencies - replace with your real agency codes & secrets before sharing
export const agencies: Agency[] = [
  { id: "agency-1", name: "Oversight Agency A", code: "OVR-A", passphrase: "OVR-A-2025" },
  { id: "agency-2", name: "Media Contact", code: "MEDIA-1", passphrase: "MEDIA-1-2025" },
  { id: "agency-3", name: "Internal Reviewer", code: "INTERNAL", passphrase: "INTERNAL-2025" },
];

export function findAgencyByCode(code: string) {
  return agencies.find(a => a.code.toLowerCase() === code.trim().toLowerCase());
}
