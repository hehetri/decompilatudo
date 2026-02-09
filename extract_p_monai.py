#!/usr/bin/env python3
"""Extract p_monai.bin into readable text (XOR 0xFF + header skip)."""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_HEADER_SIZE = 8


def invert_bytes(data: bytes) -> bytes:
    return bytes(b ^ 0xFF for b in data)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract p_monai.bin into text by XOR 0xFF and skipping header.")
    parser.add_argument(
        "input",
        nargs="?",
        default="p_monai.bin",
        help="Input encrypted file (default: p_monai.bin)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="p_monai.txt",
        help="Output text file (default: p_monai.txt)",
    )
    parser.add_argument(
        "--encoding",
        default="cp949",
        help="Text encoding for output (default: cp949).",
    )
    parser.add_argument(
        "--errors",
        default="replace",
        help="Decoding error handling (default: replace).",
    )
    parser.add_argument(
        "--header-size",
        type=int,
        default=DEFAULT_HEADER_SIZE,
        help="Header size to skip before text (default: 8).",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    encrypted = input_path.read_bytes()
    decrypted = invert_bytes(encrypted)
    body = decrypted[args.header_size :]
    text = body.decode(args.encoding, errors=args.errors)
    output_path.write_text(
        text,
        encoding=args.encoding,
        errors=args.errors,
        newline="",
    )


if __name__ == "__main__":
    main()
