const frontMatter = [
  {
    title: "Cover Letter",
    filename: "Front_Cover_Letter.pdf"
  },
  {
    title: "Executive Summary",
    filename: "Front_Executive_Summary.pdf"
  },
  {
    title: "Contradictions Table",
    filename: "Front_Contradictions_Table.pdf"
  }
];

export default function Front() {
  return (
    <div className="max-w-2xl mx-auto py-10 px-4">
      <div className="mb-6">
        <a href="/justice_project_chat_map.png" target="_blank" rel="noopener noreferrer">
          <img src="/justice_project_chat_map.png" alt="Justice project map" className="w-full rounded-lg shadow-sm mb-2" />
        </a>
        <div className="text-sm text-neutral-500">Project map — click to open full-size</div>
      </div>
      <h1 className="text-3xl font-bold mb-6">Front Matter</h1>
      <ul className="space-y-4">
        {frontMatter.map((item) => (
          <li key={item.filename} className="bg-white rounded shadow p-4 flex items-center justify-between">
            <span className="font-medium">{item.title}</span>
            <a
              href={`/pdfs/${item.filename}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Open PDF
            </a>
          </li>
        ))}
      </ul>
      <div className="mt-8 text-center">
        <a href="#/exhibits" className="inline-block bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition">Go to Exhibits</a>
      </div>
    </div>
  );
}
