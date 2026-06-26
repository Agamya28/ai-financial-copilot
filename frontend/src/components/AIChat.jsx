import { useState, useEffect } from "react";
import api from "../services/api";

function AIChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
    useEffect(() => {
        loadHistory();
    }, []);
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
      setLoading(true);
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
    } 
    catch (error) {
      console.error(error);
      setMessages((prev) => [
    ...prev,
    {
      role: "assistant",
      text: "Sorry, something went wrong.",
    },
  ]);
    }
    finally {
    setLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
        const response = await api.get("/ai/history");

        const formatted = [];

        response.data.reverse().forEach((chat) => {
            formatted.push({
                role: "user",
                text: chat.question,
            });

            formatted.push({
                role: "assistant",
                text: chat.response,
            });
        });

        setMessages(formatted);

    } catch (error) {
        console.error(error);
    }
};

  return (
    <div className="bg-white p-6 rounded-xl shadow mt-8">

      <h2 className="text-2xl font-semibold mb-4">
        AI Financial Assistant
      </h2>

      <div className="h-[500px] overflow-y-auto border rounded-xl p-4 mb-4 bg-gray-50 space-y-3">

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
              className={`
                inline-block
                max-w-[75%]
                px-4
                py-3
                rounded-2xl
                shadow-sm
                ${
                    message.role === "user"
                    ? "bg-blue-500 text-white rounded-br-md"
                    : "bg-gray-100 text-gray-800 rounded-bl-md"
                }
            `}
            >
              {message.text}
            </div>
          </div>
        ))}
        {loading && (
    <div className="text-left">
        <div
            className="
                inline-block
                bg-gray-200
                rounded-2xl
                px-4
                py-3
                animate-pulse
            "
        >
            AI is typing...
        </div>
    </div>
)}

      </div>

      <div className="flex gap-3 items-center">

        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask about your finances..."
          className="flex-1 border rounded-full px-5 py-3 focus:outline-none focus:ring-2 focus:ring-blue-400" />

        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-6 py-3 rounded-full hover:bg-blue-600"
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default AIChat;