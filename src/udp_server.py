from typing import Callable
import socket
import threading


class UDPServer:
    """Simple UDP server that calls a callback with (data: bytes, addr).

    Runs in its own thread and can be stopped.
    """

    def __init__(self, host: str, port: int, on_packet: Callable[[bytes, tuple], None]):
        self.host = host
        self.port = port
        self.on_packet = on_packet
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._thread: threading.Thread | None = None
        self._running = threading.Event()

    def start(self) -> None:
        self._sock.bind((self.host, self.port))
        self._running.set()
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()

    def _recv_loop(self) -> None:
        while self._running.is_set():
            try:
                data, addr = self._sock.recvfrom(2048)
            except OSError:
                break
            try:
                self.on_packet(data, addr)
            except Exception:
                # keep server alive even if callback fails
                import traceback

                traceback.print_exc()

    def stop(self) -> None:
        self._running.clear()
        try:
            self._sock.close()
        except Exception:
            pass
        if self._thread:
            self._thread.join(timeout=1.0)
