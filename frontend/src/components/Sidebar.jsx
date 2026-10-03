import { useEffect, useState } from "react"
import { getUserFiles } from "../api"

function Sidebar() {
  const [files, setFiles] = useState([])

  useEffect(() => {
    loadFiles()

    window.addEventListener("filesUpdated", loadFiles)

    return () => {
      window.removeEventListener("filesUpdated", loadFiles)
    }
  }, [])

  async function loadFiles() {
    try {
      const result = await getUserFiles()
      setFiles(result.files)
    } catch (error) {
      console.error("Failed to load files:", error)
    }
  }

  return (
    <aside className="w-64 min-h-0 overflow-y-auto bg-[#FFC533] p-5">
      <h2 className="text-[#FF9849] text-outline-thick">
        DOCUMENTS
      </h2>

      {files.length === 0 ? (
        <div className="bg-[#FF9849] border-2 border-black rounded-lg p-4">
          <p className="font-semibold text-black/60">
            No documents yet
          </p>

          <p className="text-xs text-black/60 mt-1">
            Upload a file to get started
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {files.map((file) => (
            <div
              key={file}
              className="bg-[#FF9849] border-2 border-black rounded-lg p-3"
            >
              <p className="font-semibold text-black/60 text-sm wrap-break-words">
                {file}
              </p>
            </div>
          ))}
        </div>
      )}
    </aside>
  )
}

export default Sidebar