import { useEffect, useRef, useState } from 'react';

export default function useWebSocket(url) {
  const wsRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!url) return;
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (evt) => {
      try {
        const obj = JSON.parse(evt.data);
        setMessages(m => [obj, ...m].slice(0, 100));
      } catch (e) { }
    };
    return () => { try { ws.close(); } catch {} };
  }, [url]);

  const send = (obj) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(obj));
      return true;
    }
    return false;
  };

  return { connected, messages, send };
}
