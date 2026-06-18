import { useState } from "react";
import api from "../services/api";

function AIChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    try {
      const response = await api.post(
        "/ai/chat",
        {
          question,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: response.data.response,
        },
      ]);

      setQuestion("");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow mt-8">

      <h2 className="text-2xl font-semibold mb-4">
        AI Financial Assistant
      </h2>

      <div className="h-96 overflow-y-auto border rounded p-4 mb-4">

        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-3 ${
              message.role === "user"
                ? "text-right"
                : "text-left"
            }`}
          >
            <div
              className={`inline-block p-3 rounded-lg ${
                message.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200"
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}

      </div>

      <div className="flex gap-3">

        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask about your finances..."
          className="flex-1 border rounded p-3"
        />

        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 rounded"
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default AIChat;