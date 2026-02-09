#!/usr/bin/env python3
"""Pack p_monai text back into p_monai.bin (restore header + XOR 0xFF)."""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_HEADER_SIZE = 8
DEFAULT_HEADER_PLAIN = bytes.fromhex("FE FF FF FF 13 BA FD FF")


def invert_bytes(data: bytes) -> bytes:
    return bytes(b ^ 0xFF for b in data)


def header_from_encrypted(path: Path, size: int) -> bytes:
    encrypted = path.read_bytes()
    decrypted = invert_bytes(encrypted)
    return decrypted[:size]


def header_from_hex(hex_string: str) -> bytes:
    cleaned = hex_string.replace(" ", "").replace("0x", "")
    return bytes.fromhex(cleaned)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pack p_monai text into p_monai.bin by restoring header and XOR 0xFF.")
    parser.add_argument(
        "input",
        nargs="?",
        default="p_monai.txt",
        help="Input text file (default: p_monai.txt)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="p_monai.bin",
        help="Output encrypted file (default: p_monai.bin)",
    )
    parser.add_argument(
        "--encoding",
        default="cp949",
        help="Text encoding for input file (default: cp949).",
    )
    parser.add_argument(
        "--errors",
        default="replace",
        help="Encoding error handling (default: replace).",
    )
    parser.add_argument(
        "--header-from",
        help="Encrypted file to copy header from (default: p_monai.bin if exists).",
    )
    parser.add_argument(
        "--header-hex",
        help="Header bytes in hex (overrides --header-from).",
    )
    parser.add_argument(
        "--header-size",
        type=int,
        default=DEFAULT_HEADER_SIZE,
        help="Header size to use (default: 8).",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.header_hex:
        header = header_from_hex(args.header_hex)
    else:
        header_source = Path(args.header_from) if args.header_from else Path("p_monai.bin")
        if header_source.exists():
            header = header_from_encrypted(header_source, args.header_size)
        else:
            header = DEFAULT_HEADER_PLAIN

    text = input_path.read_text(encoding=args.encoding, errors=args.errors)
    body = text.encode(args.encoding, errors=args.errors)
    decrypted = header + body
    encrypted = invert_bytes(decrypted)
    output_path.write_bytes(encrypted)


if __name__ == "__main__":
    main()
