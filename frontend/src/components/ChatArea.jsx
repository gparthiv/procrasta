import ReactMarkdown from "react-markdown"

function ChatArea({ messages }) {
  return (
    <div className="chat-scroll flex-1 min-h-0 overflow-y-auto px-8 py-8">

      <div className="max-w-3xl mx-auto space-y-6">

        {messages.map((message, index) => (
          <div
            key={index}
            className={
              message.role === "user"
                ? "flex justify-end"
                : "flex justify-start"
            }
          >
            <div
              className={
                message.role === "user"
                  ? "max-w-[75%] bg-[#FF9849] border-2 border-black rounded-2xl rounded-br-md p-4 text-black/70 "
                  : "max-w-[75%] bg-[#FFE772] border-2 border-black rounded-2xl rounded-bl-md p-5 text-[#444444]"
              }
            >
              {message.role === "user" ? (
                <p className="leading-7 whitespace-pre-wrap">
                  {message.content}
                </p>
              ) : (
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-2xl font-bold mb-3">
                        {children}
                      </h1>
                    ),

                    h2: ({ children }) => (
                      <h2 className="text-xl font-bold mb-2">
                        {children}
                      </h2>
                    ),

                    h3: ({ children }) => (
                      <h3 className="text-lg font-bold mb-2">
                        {children}
                      </h3>
                    ),

                    p: ({ children }) => (
                      <p className="mb-3 leading-7">
                        {children}
                      </p>
                    ),

                    ul: ({ children }) => (
                      <ul className="list-disc ml-6 mb-3 space-y-1">
                        {children}
                      </ul>
                    ),

                    ol: ({ children }) => (
                      <ol className="list-decimal ml-6 mb-3 space-y-1">
                        {children}
                      </ol>
                    ),

                    strong: ({ children }) => (
                      <strong className="font-bold">
                        {children}
                      </strong>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              )}
            </div>
          </div>
        ))}

      </div>
    </div>
  )
}

export default ChatArea