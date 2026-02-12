import { useEffect, useState, useRef, useCallback } from 'react';
import { useDispatch } from 'react-redux';
import { WS_BASE_URL } from '../utils/constants';
import { addNotification } from '../store/slices/uiSlice';

/**
 * Custom hook for WebSocket connection management
 * @param {string} url - WebSocket URL (if not provided, uses WS_BASE_URL)
 * @param {Object} options - Configuration options
 * @returns {Object} WebSocket state and methods
 */
export const useWebSocket = (url = null, options = {}) => {
  const dispatch = useDispatch();
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const wsRef = useRef(null);
  const messageHandlers = useRef({});
  const reconnectTimeoutRef = useRef(null);

  const wsUrl = url || WS_BASE_URL;
  const {
    autoConnect = true,
    reconnect = true,
    maxRetries = 5,
    retryDelay = 3000,
    messageQueueSize = 100,
  } = options;

  /**
   * Connect to WebSocket
   */
  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    try {
      const token = localStorage.getItem('accessToken');
      const connectUrl = token ? `${wsUrl}?token=${token}` : wsUrl;

      const ws = new WebSocket(connectUrl);

      ws.onopen = () => {
        console.debug('[WebSocket] Connected');
        setIsConnected(true);
        setError(null);
        setRetryCount(0);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.debug('[WebSocket] Received:', message.type);

          setData(message);

          // Call registered message handlers
          if (message.type && messageHandlers.current[message.type]) {
            messageHandlers.current[message.type](message);
          }

          // Call generic message handler
          if (messageHandlers.current['*']) {
            messageHandlers.current['*'](message);
          }
        } catch (err) {
          console.error('[WebSocket] Message parse error:', err);
        }
      };

      ws.onerror = (event) => {
        console.error('[WebSocket] Error:', event);
        const errorMsg = 'WebSocket connection error';
        setError(errorMsg);
        setIsConnected(false);

        dispatch(
          addNotification({
            type: 'error',
            message: errorMsg,
          })
        );
      };

      ws.onclose = () => {
        console.debug('[WebSocket] Disconnected');
        setIsConnected(false);

        // Attempt reconnection
        if (reconnect && retryCount < maxRetries) {
          reconnectTimeoutRef.current = setTimeout(() => {
            console.debug(`[WebSocket] Reconnecting... (attempt ${retryCount + 1}/${maxRetries})`);
            setRetryCount((prev) => prev + 1);
            connect();
          }, retryDelay);
        } else if (retryCount >= maxRetries) {
          const maxRetriesMsg = `Failed to connect after ${maxRetries} attempts`;
          setError(maxRetriesMsg);
          dispatch(
            addNotification({
              type: 'error',
              message: maxRetriesMsg,
            })
          );
        }
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('[WebSocket] Connection error:', err);
      setError(err.message);
    }
  }, [wsUrl, dispatch, reconnect, maxRetries, retryDelay, retryCount]);

  /**
   * Disconnect from WebSocket
   */
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setIsConnected(false);
  }, []);

  /**
   * Send message through WebSocket
   */
  const send = useCallback((message) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.warn('[WebSocket] Not connected, cannot send message');
      return false;
    }

    try {
      wsRef.current.send(JSON.stringify(message));
      console.debug('[WebSocket] Sent:', message.type);
      return true;
    } catch (err) {
      console.error('[WebSocket] Send error:', err);
      return false;
    }
  }, []);

  /**
   * Register a message handler for specific message type
   */
  const on = useCallback((messageType, handler) => {
    messageHandlers.current[messageType] = handler;

    return () => {
      delete messageHandlers.current[messageType];
    };
  }, []);

  /**
   * Unregister a message handler
   */
  const off = useCallback((messageType) => {
    delete messageHandlers.current[messageType];
  }, []);

  /**
   * Subscribe to a channel
   */
  const subscribe = useCallback(
    (channel) => {
      send({
        type: 'subscribe',
        channel,
      });
    },
    [send]
  );

  /**
   * Unsubscribe from a channel
   */
  const unsubscribe = useCallback(
    (channel) => {
      send({
        type: 'unsubscribe',
        channel,
      });
    },
    [send]
  );

  // Auto-connect on mount
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    isConnected,
    error,
    data,
    retryCount,
    connect,
    disconnect,
    send,
    on,
    off,
    subscribe,
    unsubscribe,
  };
};

export default useWebSocket;
