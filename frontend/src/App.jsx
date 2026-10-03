import { useEffect, useRef } from "react"
import Header from "./components/Header"
import Sidebar from "./components/Sidebar"
import ContentArea from "./components/ContentArea"
import api from "./api"

function App() {
  const sessionStarted = useRef(false)
  useEffect(() => {
    if (sessionStarted.current) return
    sessionStarted.current = true
    createSession()
  }, [])

  async function createSession() {
    try {
      const response = await api.post("/session")

      localStorage.setItem("user_id", response.data.user_id)

      console.log("New session:", response.data.user_id)
    } catch (error) {
      console.error("Session creation failed:", error)
    }
  }

  return (
    <div className="h-screen overflow-hidden flex flex-col bg-[#FFC533]">
      <Header />

      <div className="flex flex-1 min-h-0 overflow-hidden">
        <Sidebar />

        <main className="flex-1 min-w-0 bg-[#FFC533]">
          <ContentArea />
        </main>
      </div>
    </div>
  )
}

export default App