import { useRef, useState } from "react"
import { uploadFile, getJobStatus } from "../api"

function UploadArea() {
  const fileInputRef = useRef(null)
  const [status, setStatus] = useState("")

  function chooseFile() {
    fileInputRef.current.click()
  }

  async function handleFileChange(event) {
    const file = event.target.files[0]

    if (!file) {
      return
    }

    try {
      setStatus("Uploading...")

      const uploadResult = await uploadFile(file)

      console.log("Upload queued:", uploadResult)

      setStatus("Processing...")

      const result = await waitForJob(uploadResult.job_id)

      console.log("Upload completed:", result)

      window.dispatchEvent(new Event("filesUpdated"))

      setStatus("Uploaded!")

      setTimeout(() => {
        setStatus("")
      }, 2000)

    } catch (error) {
      console.error("Upload failed:", error)
      setStatus("Upload failed.")

      setTimeout(() => {
        setStatus("")
      }, 3000)
    }

    event.target.value = ""
  }

  async function waitForJob(jobId) {
    while (true) {
      const result = await getJobStatus(jobId)

      console.log("Job status:", result)

      if (result.status === "completed") {
        return result
      }

      if (result.status === "failed") {
        throw new Error(result.error)
      }

      await new Promise((resolve) => setTimeout(resolve, 1000))
    }
  }

  return (
    <div className="absolute top-5 right-6 z-10 flex items-center gap-3">

      {status && (
        <p className="text-sm font-semibold text-[#444444]">
          {status}
        </p>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.pptx,.png,.jpg,.jpeg"
        onChange={handleFileChange}
        className="hidden"
      />

      <button
        onClick={chooseFile}
        className="bg-[#FF9849] border-2 border-black text-black/60 px-4 py-2 rounded-lg font-semibold"
      >
        + Upload
      </button>

    </div>
  )
}

export default UploadArea