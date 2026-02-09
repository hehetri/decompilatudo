#!/usr/bin/env python3
"""Encrypt p_monai plaintext by inverting all bytes (XOR 0xFF)."""
from __future__ import annotations

import argparse
from pathlib import Path


def invert_bytes(data: bytes) -> bytes:
    return bytes(b ^ 0xFF for b in data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt p_monai text (XOR 0xFF).")
    parser.add_argument(
        "input",
        nargs="?",
        default="p_monai.txt",
        help="Input decrypted file (default: p_monai.txt)",
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
        "--binary",
        action="store_true",
        help="Read raw bytes from input instead of decoding text.",
    )
    parser.add_argument(
        "--compare",
        dest="compare",
        help="Optional reference file to compare the encrypted output against.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.binary:
        data = input_path.read_bytes()
    else:
        text = input_path.read_text(encoding=args.encoding, errors=args.errors)
        data = text.encode(args.encoding, errors=args.errors)

    encrypted = invert_bytes(data)
    output_path.write_bytes(encrypted)

    if args.compare:
        reference = Path(args.compare).read_bytes()
        if encrypted != reference:
            raise SystemExit("Encrypted output does not match reference file.")


if __name__ == "__main__":
    main()
