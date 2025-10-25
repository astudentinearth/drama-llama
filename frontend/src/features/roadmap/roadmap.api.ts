import axios from "axios";
import type {
  FullSessionResponse,
  IMessage,
  ISession,
  RoadmapResponse,
  SessionProgress,
} from "./roadmap.types";

const ROADMAP_BASEURL = "/api/roadmap";
const SESSIONS = "/api/roadmap/sessions";

export function Session(id: number) {
  const baseurl = SESSIONS + "/" + id;
  async function get() {
    const result = await axios.get(baseurl);
    return result.data as ISession;
  }
  async function getFull() {
    const result = await axios.get(baseurl + "/full");
    return result.data as FullSessionResponse;
  }
  async function getProgress() {
    const result = await axios.get(baseurl + "/progress");
    return result.data as SessionProgress;
  }
  async function complete() {
    const result = await axios.post(SESSIONS + "/complete?sessionId=" + id);
    return result.data as ISession;
  }
  async function archive() {
    const result = await axios.post(SESSIONS + "/archive?sessionId=" + id);
    return result.data as ISession;
  }
  async function getMessages() {
    const result = await axios.get(baseurl + "/messages");
    return result.data.messages as IMessage[];
  }
  async function getRecentMessages() {
    const result = await axios.get(baseurl + "/messages/recent");
    return result.data.messages as IMessage[];
  }
  async function chat(
    message: string,
    onMessage: (data: string) => void,
    onError?: (error: Error) => void,
    onComplete?: () => void
  ) {
    try {
      const response = await fetch(
        `${ROADMAP_BASEURL}/ai/sessions/${id}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ message }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("No response body reader available");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      try {
        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            onComplete?.();
            break;
          }

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || ""; // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.trim() === "") continue;

            // Handle SSE format: "data: {content}" or just plain content
            let data = line;
            if (line.startsWith("data: ")) {
              data = line.slice(6);
            }

            // Skip SSE control messages
            if (data.trim() === "[DONE]" || data.trim() === "") {
              continue;
            }

            if (data.trim()) {
              onMessage(data.trim());
            }
          }
        }
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      onError?.(
        error instanceof Error ? error : new Error("Unknown error occurred")
      );
    }
  }
  async function getRoadmap() {
    const result = await axios.get(
      `${ROADMAP_BASEURL}/ai/sessions/${id}/roadmap`
    );
    return result.data as RoadmapResponse;
  }
  return {
    get,
    getFull,
    getProgress,
    complete,
    archive,
    getMessages,
    getRecentMessages,
    chat,
    getRoadmap,
  };
}

export async function getSessions() {
  const result = await axios.get("/api/roadmap/sessions");
  return result.data.sessions as ISession[];
}

export async function createSession(sessionName: string, description: string) {
  const result = await axios.post("/api/roadmap/sessions", {
    session_name: sessionName,
    description: description,
  });
  return result.data as ISession;
}
