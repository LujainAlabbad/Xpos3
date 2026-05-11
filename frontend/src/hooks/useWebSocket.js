/**
 * useWebSocket — polls the scan status endpoint until the scan finishes.
 *
 * Named "useWebSocket" to match the project structure, but implemented as
 * HTTP polling (every 2 s) because the current backend is Flask without
 * Socket.IO. This gives the same real-time feel without extra infrastructure.
 *
 * Usage:
 *   const { status, error } = useWebSocket(scanId, (finalStatus) => {
 *     if (finalStatus === 'completed') navigate(`/report/${scanId}`);
 *   });
 */
import { useState, useEffect, useRef } from 'react';
import { scanAPI } from '../api/scanApi';

const POLL_INTERVAL_MS = 2000;

export const useWebSocket = (scanId, onComplete) => {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!scanId) return;

    const poll = async () => {
      try {
        const data = await scanAPI.getScanStatus(scanId);
        setStatus(data.status);

        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(intervalRef.current);
          if (onComplete) onComplete(data.status);
        }
      } catch (err) {
        const message = err.response?.data?.error || err.message || 'Polling failed';
        setError(message);
        clearInterval(intervalRef.current);
      }
    };

    // Immediate first check, then poll on interval
    poll();
    intervalRef.current = setInterval(poll, POLL_INTERVAL_MS);

    return () => clearInterval(intervalRef.current);
  }, [scanId]); // eslint-disable-line react-hooks/exhaustive-deps

  const stopPolling = () => clearInterval(intervalRef.current);

  return { status, error, stopPolling };
};
