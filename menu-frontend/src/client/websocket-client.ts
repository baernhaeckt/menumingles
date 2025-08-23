export interface WebSocketMessage {
  data: any;
  type: string;
  timestamp: number;
}

export interface WebSocketClientOptions {
  serverAddress?: string;
  onMessageReceived?: (message: WebSocketMessage) => void;
  onOpen?: () => void;
  onClose?: (event: CloseEvent) => void;
  onError?: (event: Event) => void;
  autoReconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  pingInterval?: number;
  pingTimeout?: number;
}

export class WebSocketClient {
  private socket: WebSocket | null = null;
  private serverAddress: string;
  private onMessageReceived: ((message: WebSocketMessage) => void) | undefined;
  private onOpen: (() => void) | undefined;
  private onClose: ((event: CloseEvent) => void) | undefined;
  private onError: ((event: Event) => void) | undefined;
  private autoReconnect: boolean;
  private reconnectInterval: number;
  private maxReconnectAttempts: number;
  private reconnectAttempts: number = 0;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private isConnecting: boolean = false;
  private pingInterval: number;
  private pingTimeout: number;
  private pingTimer: NodeJS.Timeout | null = null;
  private pongTimer: NodeJS.Timeout | null = null;
  private lastPongTime: number = 0;
  private isManuallyDisconnected: boolean = false;

  constructor(options: WebSocketClientOptions = {}) {
    this.serverAddress = options.serverAddress || 'ws://localhost:8765/ws';
    this.onMessageReceived = options.onMessageReceived;
    this.onOpen = options.onOpen;
    this.onClose = options.onClose;
    this.onError = options.onError;
    this.autoReconnect = options.autoReconnect ?? true;
    this.reconnectInterval = options.reconnectInterval || 5000;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
    this.pingInterval = options.pingInterval || 30000; // 30 seconds
    this.pingTimeout = options.pingTimeout || 10000; // 10 seconds
  }

  /**
   * Connect to the WebSocket server
   */
  public connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        reject(new Error('Connection already in progress'));
        return;
      }

      this.isConnecting = true;
      this.isManuallyDisconnected = false;

      try {
        this.socket = new WebSocket(this.serverAddress);

        this.socket.onopen = (event) => {
          this.isConnecting = false;
          this.reconnectAttempts = 0;
          console.log('WebSocket connected to:', this.serverAddress);

          if (this.onOpen) {
            this.onOpen();
          }

          // Start ping/pong monitoring
          this.startPingPong();

          resolve();
        };

        this.socket.onmessage = (event) => {
          // Handle pong messages
          if (event.data === 'pong') {
            this.handlePong();
            return;
          }

          try {
            const message: WebSocketMessage = {
              data: JSON.parse(event.data),
              type: 'message',
              timestamp: Date.now()
            };

            if (this.onMessageReceived) {
              this.onMessageReceived(message);
            }
          } catch (error) {
            // If JSON parsing fails, treat as raw text
            const message: WebSocketMessage = {
              data: event.data,
              type: 'text',
              timestamp: Date.now()
            };

            if (this.onMessageReceived) {
              this.onMessageReceived(message);
            }
          }
        };

        this.socket.onclose = (event) => {
          this.isConnecting = false;
          this.stopPingPong();
          console.log('WebSocket disconnected:', event.code, event.reason, 'wasClean:', event.wasClean);

          if (this.onClose) {
            this.onClose(event);
          }

          // Handle reconnection - attempt to reconnect for any close reason except manual disconnect
          if (this.autoReconnect && !this.isManuallyDisconnected && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.scheduleReconnect();
          } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached. Giving up.');
          }
        };

        this.socket.onerror = (event) => {
          this.isConnecting = false;
          console.error('WebSocket error:', event);

          if (this.onError) {
            this.onError(event);
          }
          reject(new Error('WebSocket connection failed'));
        };

      } catch (error) {
        this.isConnecting = false;
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the WebSocket server
   */
  public disconnect(): void {
    this.isManuallyDisconnected = true;
    this.stopPingPong();

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.socket) {
      this.socket.close(1000, 'Client disconnect');
      this.socket = null;
    }

    this.reconnectAttempts = 0;
    this.isConnecting = false;
  }

  /**
   * Send a message to the server
   */
  public send(data: any): boolean {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected');
      return false;
    }

    try {
      const message = typeof data === 'string' ? data : JSON.stringify(data);
      this.socket.send(message);
      return true;
    } catch (error) {
      console.error('Failed to send message:', error);
      return false;
    }
  }

  /**
   * Get the current connection state
   */
  public getState(): number {
    return this.socket ? this.socket.readyState : WebSocket.CLOSED;
  }

  /**
   * Check if the connection is open
   */
  public isConnected(): boolean {
    return this.socket?.readyState === WebSocket.OPEN;
  }

  /**
   * Update the message handler
   */
  public setMessageHandler(handler: (message: WebSocketMessage) => void): void {
    this.onMessageReceived = handler;
  }

  /**
   * Get the current reconnection attempts count
   */
  public getReconnectAttempts(): number {
    return this.reconnectAttempts;
  }

  /**
   * Start ping/pong monitoring
   */
  private startPingPong(): void {
    this.stopPingPong();

    this.pingTimer = setInterval(() => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        try {
          this.socket.send('ping');

          // Set up pong timeout
          this.pongTimer = setTimeout(() => {
            console.warn('Ping timeout - connection may be stale');
            if (this.socket) {
              this.socket.close(1000, 'Ping timeout');
            }
          }, this.pingTimeout);
        } catch (error) {
          console.error('Failed to send ping:', error);
        }
      }
    }, this.pingInterval);
  }

  /**
   * Handle pong response
   */
  private handlePong(): void {
    this.lastPongTime = Date.now();
    if (this.pongTimer) {
      clearTimeout(this.pongTimer);
      this.pongTimer = null;
    }
  }

  /**
   * Stop ping/pong monitoring
   */
  private stopPingPong(): void {
    if (this.pingTimer) {
      clearInterval(this.pingTimer);
      this.pingTimer = null;
    }
    if (this.pongTimer) {
      clearTimeout(this.pongTimer);
      this.pongTimer = null;
    }
  }

  /**
   * Schedule a reconnection attempt
   */
  private scheduleReconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.reconnectAttempts++;
    const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1); // Exponential backoff

    console.log(`Scheduling reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`);

    this.reconnectTimer = setTimeout(() => {
      this.connect().catch((error) => {
        console.error('Reconnection failed:', error);
      });
    }, delay);
  }

  /**
   * Test if a WebSocket server is reachable
   */
  static async testConnection(serverAddress: string, timeout: number = 5000): Promise<boolean> {
    return new Promise((resolve) => {
      const testSocket = new WebSocket(serverAddress);
      const timeoutId = setTimeout(() => {
        testSocket.close();
        resolve(false);
      }, timeout);

      testSocket.onopen = () => {
        clearTimeout(timeoutId);
        testSocket.close();
        resolve(true);
      };

      testSocket.onerror = () => {
        clearTimeout(timeoutId);
        resolve(false);
      };
    });
  }
}

// Export a default instance for convenience
export const defaultWebSocketClient = new WebSocketClient();

// Singleton instance for shared use across components
let singletonInstance: WebSocketClient | null = null;

export function getWebSocketClient(options?: WebSocketClientOptions): WebSocketClient {
  if (!singletonInstance) {
    singletonInstance = new WebSocketClient(options);
  }
  return singletonInstance;
}

export function resetWebSocketClient(): void {
  if (singletonInstance) {
    singletonInstance.disconnect();
    singletonInstance = null;
  }
}

// Export connection state constants
export const WebSocketState = {
  CONNECTING: WebSocket.CONNECTING,
  OPEN: WebSocket.OPEN,
  CLOSING: WebSocket.CLOSING,
  CLOSED: WebSocket.CLOSED
} as const;
