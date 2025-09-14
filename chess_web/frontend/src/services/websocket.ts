import { io, Socket } from "socket.io-client";
import {
  WebSocketMessage,
  GameUpdateMessage,
  AnalysisUpdateMessage,
  GameState,
  PositionAnalysis,
} from "@types/index";

// WebSocket Configuration
const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8000";

export type WebSocketEventHandler = (data: any) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private clientId: string | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private eventHandlers: Map<string, Set<WebSocketEventHandler>> = new Map();

  constructor() {
    this.generateClientId();
  }

  private generateClientId(): void {
    this.clientId = `client_${Date.now()}_${Math.random()
      .toString(36)
      .substr(2, 9)}`;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket?.connected) {
        resolve();
        return;
      }

      console.log("Connecting to WebSocket server...");

      this.socket = io(WS_BASE_URL, {
        transports: ["websocket"],
        upgrade: false,
        rememberUpgrade: false,
        timeout: 10000,
        query: {
          clientId: this.clientId,
        },
      });

      this.socket.on("connect", () => {
        console.log("WebSocket connected:", this.socket?.id);
        this.reconnectAttempts = 0;
        this.setupEventHandlers();
        resolve();
      });

      this.socket.on("connect_error", (error) => {
        console.error("WebSocket connection error:", error);
        reject(error);
      });

      this.socket.on("disconnect", (reason) => {
        console.log("WebSocket disconnected:", reason);
        this.handleDisconnect();
      });

      // Set connection timeout
      setTimeout(() => {
        if (!this.socket?.connected) {
          reject(new Error("WebSocket connection timeout"));
        }
      }, 10000);
    });
  }

  private setupEventHandlers(): void {
    if (!this.socket) return;

    // Handle connection established
    this.socket.on("connection_established", (data) => {
      console.log("WebSocket connection established:", data);
      this.emit("connection_established", data);
    });

    // Handle game updates
    this.socket.on("game_update", (data: GameUpdateMessage["data"]) => {
      console.log("Game update received:", data);
      this.emit("game_update", data);
    });

    // Handle analysis updates
    this.socket.on("analysis_update", (data: AnalysisUpdateMessage["data"]) => {
      console.log("Analysis update received:", data);
      this.emit("analysis_update", data);
    });

    // Handle move made
    this.socket.on("move_made", (data) => {
      console.log("Move made:", data);
      this.emit("move_made", data);
    });

    // Handle analysis result
    this.socket.on("analysis_result", (data) => {
      console.log("Analysis result:", data);
      this.emit("analysis_result", data);
    });

    // Handle subscription confirmation
    this.socket.on("subscription_confirmed", (data) => {
      console.log("Subscription confirmed:", data);
      this.emit("subscription_confirmed", data);
    });

    // Handle unsubscription confirmation
    this.socket.on("unsubscription_confirmed", (data) => {
      console.log("Unsubscription confirmed:", data);
      this.emit("unsubscription_confirmed", data);
    });

    // Handle ping/pong
    this.socket.on("ping", () => {
      this.socket?.emit("pong", { timestamp: new Date().toISOString() });
    });

    // Handle errors
    this.socket.on("error", (error) => {
      console.error("WebSocket error:", error);
      this.emit("error", error);
    });
  }

  private handleDisconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay =
        this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

      console.log(
        `Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms...`
      );

      setTimeout(() => {
        this.connect().catch((error) => {
          console.error("Reconnection failed:", error);
        });
      }, delay);
    } else {
      console.error("Max reconnection attempts reached");
      this.emit("connection_failed", {
        reason: "Max reconnection attempts reached",
      });
    }
  }

  disconnect(): void {
    if (this.socket) {
      console.log("Disconnecting WebSocket...");
      this.socket.disconnect();
      this.socket = null;
    }
    this.eventHandlers.clear();
  }

  // Event handling
  on(event: string, handler: WebSocketEventHandler): void {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, new Set());
    }
    this.eventHandlers.get(event)!.add(handler);
  }

  off(event: string, handler: WebSocketEventHandler): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.delete(handler);
      if (handlers.size === 0) {
        this.eventHandlers.delete(event);
      }
    }
  }

  private emit(event: string, data: any): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.forEach((handler) => {
        try {
          handler(data);
        } catch (error) {
          console.error(
            `Error in WebSocket event handler for ${event}:`,
            error
          );
        }
      });
    }
  }

  // Message sending
  send(message: WebSocketMessage): void {
    if (this.socket?.connected) {
      this.socket.emit("message", message);
    } else {
      console.warn("WebSocket not connected, message not sent:", message);
    }
  }

  // Game-specific methods
  subscribeToGame(gameId: string): void {
    this.send({
      type: "subscribe_game",
      data: { game_id: gameId },
    });
  }

  unsubscribeFromGame(): void {
    this.send({
      type: "unsubscribe_game",
    });
  }

  requestAnalysis(fen: string, depth: number = 4): void {
    this.send({
      type: "analysis_request",
      data: { fen, depth },
    });
  }

  requestMove(gameId: string, move: string): void {
    this.send({
      type: "move_request",
      data: { game_id: gameId, move },
    });
  }

  // Connection status
  get isConnected(): boolean {
    return this.socket?.connected || false;
  }

  get connectionId(): string | undefined {
    return this.socket?.id;
  }

  get clientIdValue(): string | null {
    return this.clientId;
  }
}

// Create singleton instance
export const websocketService = new WebSocketService();

// React hook for WebSocket
import { useEffect, useRef, useCallback } from "react";

export function useWebSocket() {
  const serviceRef = useRef(websocketService);

  const connect = useCallback(async () => {
    try {
      await serviceRef.current.connect();
    } catch (error) {
      console.error("Failed to connect WebSocket:", error);
      throw error;
    }
  }, []);

  const disconnect = useCallback(() => {
    serviceRef.current.disconnect();
  }, []);

  const subscribe = useCallback(
    (event: string, handler: WebSocketEventHandler) => {
      serviceRef.current.on(event, handler);

      // Return cleanup function
      return () => {
        serviceRef.current.off(event, handler);
      };
    },
    []
  );

  const send = useCallback((message: WebSocketMessage) => {
    serviceRef.current.send(message);
  }, []);

  const subscribeToGame = useCallback((gameId: string) => {
    serviceRef.current.subscribeToGame(gameId);
  }, []);

  const unsubscribeFromGame = useCallback(() => {
    serviceRef.current.unsubscribeFromGame();
  }, []);

  const requestAnalysis = useCallback((fen: string, depth?: number) => {
    serviceRef.current.requestAnalysis(fen, depth);
  }, []);

  const requestMove = useCallback((gameId: string, move: string) => {
    serviceRef.current.requestMove(gameId, move);
  }, []);

  // Auto-cleanup on unmount
  useEffect(() => {
    return () => {
      serviceRef.current.disconnect();
    };
  }, []);

  return {
    connect,
    disconnect,
    subscribe,
    send,
    subscribeToGame,
    unsubscribeFromGame,
    requestAnalysis,
    requestMove,
    isConnected: serviceRef.current.isConnected,
    connectionId: serviceRef.current.connectionId,
    clientId: serviceRef.current.clientIdValue,
  };
}

export default websocketService;
