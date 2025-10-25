import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useChatStream } from "./roadmap.hooks";
import { useSessionMessagesQuery } from "./roadmap.query";
import { Send, Bot, User, Loader2, CheckCircle, Sparkles } from "lucide-react";
import type { IMessage } from "./roadmap.types";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
  toolCalls?: Array<{
    tool_name: string;
    arguments: Record<string, any>;
    call_id: string;
  }>;
  toolResults?: Array<{
    operation: string;
    success: boolean;
    message: string;
    data?: any;
  }>;
}

interface ChatPaneProps {
  sessionId: number;
}

export default function ChatPane({ sessionId }: ChatPaneProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isStreaming, currentMessage, error, sendMessage, resetMessage } =
    useChatStream(sessionId);

  // Load old messages
  const { data: oldMessages, isLoading: isLoadingMessages } =
    useSessionMessagesQuery(sessionId);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentMessage]);

  // Convert API messages to chat messages
  const convertApiMessageToChatMessage = (
    apiMessage: IMessage
  ): ChatMessage => {
    const chatMessage: ChatMessage = {
      id: `${apiMessage.timestamp}-${apiMessage.role}`,
      role: apiMessage.role,
      content: apiMessage.content,
      timestamp: new Date(apiMessage.timestamp),
    };

    // Parse tool calls from metadata if available
    if (apiMessage.metadata?.has_tool_calls && apiMessage.metadata.tool_calls) {
      chatMessage.toolCalls = apiMessage.metadata.tool_calls.map((tc) => ({
        tool_name: tc.tool_name,
        arguments: tc.arguments,
        call_id: tc.call_id,
      }));
    }

    return chatMessage;
  };

  // Combined effect to handle session changes and message loading
  useEffect(() => {
    console.log(`ChatPane: Session ${sessionId} - Loading messages`, {
      oldMessages: oldMessages?.length,
      isLoading: isLoadingMessages,
    });

    // Clear input and reset stream when session changes
    setInputValue("");
    resetMessage();

    // Load messages for the current session
    if (oldMessages !== undefined) {
      if (oldMessages.length > 0) {
        const convertedMessages = oldMessages.map(
          convertApiMessageToChatMessage
        );
        console.log(
          `ChatPane: Setting ${convertedMessages.length} messages for session ${sessionId}`
        );
        setMessages(convertedMessages);
      } else {
        // No old messages for this session
        console.log(`ChatPane: No messages for session ${sessionId}`);
        setMessages([]);
      }
    } else if (!isLoadingMessages) {
      // Messages finished loading but are undefined - likely an error
      console.log(
        `ChatPane: Messages undefined for session ${sessionId}, not loading`
      );
      setMessages([]);
    }
    // If isLoadingMessages is true, don't clear messages yet
  }, [sessionId, oldMessages, isLoadingMessages, resetMessage]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isStreaming) return;

    const userMessage: ChatMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    resetMessage();

    // Create assistant message placeholder
    const assistantMessage: ChatMessage = {
      id: `${Date.now()}-assistant`,
      role: "assistant",
      content: "",
      timestamp: new Date(),
      isStreaming: true,
    };

    setMessages((prev) => [...prev, assistantMessage]);

    // Start streaming
    await sendMessage(userMessage.content);
  };

  // Update streaming message
  useEffect(() => {
    if (currentMessage && messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.role === "assistant" && lastMessage.isStreaming) {
        // Parse SSE format: event:type\ndata:json
        const lines = currentMessage.split("\n").filter((line) => line.trim());
        let accumulatedContent = "";
        let toolCalls: any[] = [];
        let toolResults: any[] = [];

        let currentEvent = "";
        for (const line of lines) {
          if (line.startsWith("event:")) {
            currentEvent = line.substring(6).trim();
          } else if (line.startsWith("data:")) {
            const dataContent = line.substring(5).trim();

            try {
              const parsed = JSON.parse(dataContent);

              if (currentEvent === "master_prompt" || currentEvent === "") {
                if (parsed.response) {
                  accumulatedContent += parsed.response;
                }

                if (parsed.tool_calls && parsed.tool_calls.length > 0) {
                  toolCalls = [...toolCalls, ...parsed.tool_calls];
                }
              } else if (currentEvent === "learning_materials") {
                if (parsed.operation && parsed.success !== undefined) {
                  toolResults.push({
                    operation: parsed.operation,
                    success: parsed.success,
                    message: parsed.message,
                    data: parsed.data,
                  });
                }
              } else if (currentEvent === "done") {
                // Handle completion message if needed
                console.log("Stream completed:", parsed.message);
              }
            } catch (e) {
              // If not JSON, treat as plain text
              if (dataContent && dataContent !== "") {
                accumulatedContent += dataContent;
              }
            }
          }
        }

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === lastMessage.id
              ? {
                  ...msg,
                  content: accumulatedContent,
                  toolCalls: toolCalls.length > 0 ? toolCalls : undefined,
                  toolResults: toolResults.length > 0 ? toolResults : undefined,
                }
              : msg
          )
        );
      }
    }
  }, [currentMessage, messages]);

  // Mark streaming as complete
  useEffect(() => {
    if (!isStreaming && messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.role === "assistant" && lastMessage.isStreaming) {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === lastMessage.id ? { ...msg, isStreaming: false } : msg
          )
        );
      }
    }
  }, [isStreaming, messages]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getToolDesc = (tool: string) => {
    switch (tool) {
      case "createLearningMaterials":
        return "Generated materials";
      case "createRoadmapSkeleton":
        return "Created roadmap";
    }
  };

  const renderToolCalls = (toolCalls: ChatMessage["toolCalls"]) => {
    if (!toolCalls || toolCalls.length === 0) return null;

    return (
      <div className="mt-3 space-y-2">
        {toolCalls.map((call) => (
          <div
            key={call.call_id}
            className="flex items-center gap-2 text-sm dark:bg-blue-900/20 p-2 rounded-lg bg-primary/10 text-primary border border-primary/50"
          >
            <Sparkles className="w-4 h-4 " />
            {getToolDesc(call.tool_name)}
          </div>
        ))}
      </div>
    );
  };

  const renderToolResults = (toolResults: ChatMessage["toolResults"]) => {
    if (!toolResults || toolResults.length === 0) return null;

    return (
      <div className="mt-3 space-y-2">
        {toolResults.map((result, index) => (
          <div
            key={index}
            className={`flex items-center gap-2 text-sm p-2 rounded ${
              result.success
                ? "bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300"
                : "bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300"
            }`}
          >
            <CheckCircle className="w-4 h-4" />
            <span className="font-medium">{result.operation}:</span>
            <span>{result.message}</span>
            {result.data?.title && (
              <Badge variant="outline" className="ml-2">
                {result.data.title}
              </Badge>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="w-108 border-l bg-card flex flex-col h-full rounded-xl border drop-shadow-lg drop-shadow-black/5">
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          <h3 className="font-semibold">Roadmap Assistant</h3>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          Describe your learning goals to generate a tailored roadmap and study
          materials.
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden p-4 space-y-4">
        {isLoadingMessages && (
          <div className="text-center py-8">
            <Loader2 className="w-8 h-8 text-muted-foreground mx-auto mb-4 animate-spin" />
            <p className="text-muted-foreground text-sm">Loading messages...</p>
          </div>
        )}

        {!isLoadingMessages && messages.length === 0 && (
          <div className="text-center py-8">
            <Bot className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground text-sm">
              Start a conversation to get help with your learning journey
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`flex gap-3 max-w-[85%] ${
                message.role === "user" ? "flex-row-reverse" : "flex-row"
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  message.role === "user"
                    ? "bg-primary text-primary-foreground hidden"
                    : "bg-muted"
                }`}
              >
                {message.role === "user" ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>

              <div
                className={`rounded-xl border p-3 drop-shadow-sm drop-shadow-black/5 ${
                  message.role === "user"
                    ? "bg-primary border-primary text-primary-foreground"
                    : "bg-muted"
                }`}
              >
                {message.content && (
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.content}
                    </ReactMarkdown>
                  </div>
                )}

                {message.isStreaming && (
                  <div className="flex items-center gap-2 animate-pulse mt-2 text-sm text-muted-foreground">
                    <span>Working on it...</span>
                  </div>
                )}

                {renderToolCalls(message.toolCalls)}
                {renderToolResults(message.toolResults)}
              </div>
            </div>
          </div>
        ))}

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 p-3 rounded-lg text-sm">
            Error: {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about your learning goals..."
            disabled={isStreaming}
            className="flex-1"
          />
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isStreaming}
            size="icon"
          >
            {isStreaming ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
