import "./Assistant.css";
import { useState } from "react";
import PageHeader from "../components/PageHeader/PageHeader";
import { chatWithAssistant } from "../api/api";

export default function Assistant() {
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content:
                "👋 Hello! I'm your Face Attendance AI Assistant.\n\nYou can ask me things like:\n\n• Who attended today?\n•Who is absent today?\n• Show attendance analytics.\n• Show all registered users.\n• How do I register a new student?\n•How do I recognize a student?",
        },
    ]);

    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const question = input.trim();

        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                content: question,
            },
        ]);

        setInput("");
        setLoading(true);

        try {
            const data = await chatWithAssistant(question);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: data.reply || "I received your request.",
                },
            ]);
        } catch (error) {
            console.error(error);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        "❌ Unable to contact the assistant backend. Make sure FastAPI is running.",
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="container">
            <PageHeader
                icon="🤖"
                title="AI Attendance Assistant"
                subtitle="Ask questions about attendance using natural language."
            />

            <div className="assistant-card">
                <div className="chat-window">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`message ${message.role}`}
                        >
                            <div className="bubble">{message.content}</div>
                        </div>
                    ))}

                    {loading && (
                        <div className="message assistant">
                            <div className="bubble">Thinking...</div>
                        </div>
                    )}
                </div>

                <div className="chat-input">
                    <textarea
                        placeholder="Ask me anything..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        rows={2}
                        disabled={loading}
                    />

                    <button
                        className="btn-primary"
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
}