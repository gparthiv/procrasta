import { useState } from "react"
import { sendChat, getJobStatus } from "../api"

function ChatInput({ addMessage }) {
  const [query, setQuery] = useState("")
  const [status, setStatus] = useState("")

  async function handleSubmit(event) {
    event.preventDefault()

    if (!query.trim()) {
      return
    }

    const userMessage = query.trim()

    addMessage({
      role: "user",
      content: userMessage,
    })

    setQuery("")
    setStatus("Thinking...")

    try {
      const chatResult = await sendChat(userMessage)

      console.log("Chat queued:", chatResult)

      const result = await waitForJob(chatResult.job_id)

      console.log("Chat completed:", result)
      console.log("Answer:", result.result.answer)

      addMessage({
        role: "assistant",
        content: result.result.answer,
      })

      setStatus("")
    } catch (error) {
      console.error("Chat failed:", error)
      setStatus("Something went wrong.")
    }
  }

  async function waitForJob(jobId) {
    while (true) {
      const result = await getJobStatus(jobId)

      console.log("Chat job:", result)

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
    <div className="shrink-0 p-6">

      {status && (
        <p className="max-w-3xl mx-auto mb-2 text-sm font-semibold text-[#444444]">
          {status}
        </p>
      )}

      <form
        onSubmit={handleSubmit}
        className="max-w-3xl mx-auto flex gap-3"
      >
        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Ask something about this document..."
          className="flex-1 bg-[#FFE772] border-2 border-black rounded-3xl px-5 py-4 outline-none placeholder-[#444444]/60"
        />

        <button
          type="submit"
          className="bg-[#FF9849] border-2 border-black text-white px-6 rounded-full font-semibold"
        >
          SEND
        </button>
      </form>
    </div>
  )
}

export default ChatInput