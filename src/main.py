from typing import Tuple
import argparse

from .udp_server import UDPServer
from .midi_handler import MidiHandler
from .audio_engine import AudioEngine
from .ui import MidiUI


def main(argv: Tuple[str, ...] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="UDP listen host")
    parser.add_argument("--port", type=int, default=6000, help="UDP listen port")
    args = parser.parse_args(argv)

    engine = AudioEngine()

    # UI will run in main thread; run UDP server in background thread
    ui = MidiUI(on_close=lambda: None)

    def note_on(note: int, velocity: int) -> None:
        engine.note_on(note, velocity)
        ui.show_note(note, velocity)

    def note_off(note: int) -> None:
        engine.note_off(note)

    midi = MidiHandler(note_on, note_off)

    server = UDPServer(args.host, args.port, lambda data, addr: midi.handle_packet(data))
    server.start()
    ui.set_status(f"Listening on {args.host}:{args.port}")

    try:
        ui.run()
    finally:
        server.stop()


if __name__ == "__main__":
    main()
