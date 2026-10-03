import { useState } from "react"
import UploadArea from "./UploadArea"
import ChatArea from "./ChatArea"
import ChatInput from "./ChatInput"

function ContentArea() {
  const [messages, setMessages] = useState([])

  function addMessage(message) {
    setMessages((currentMessages) => [
      ...currentMessages,
      message,
    ])
  }

  return (
    <div className="relative h-full min-h-0 min-w-0 bg-[#fff8d5] border-2 border-black rounded-l-2xl overflow-hidden flex flex-col">

      <UploadArea />

      <ChatArea messages={messages} />

      <ChatInput addMessage={addMessage} />

    </div>
  )
}

export default ContentArea