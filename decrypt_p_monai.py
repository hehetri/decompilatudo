#!/usr/bin/env python3
"""Decrypt p_monai.bin by inverting all bytes (XOR 0xFF)."""
from __future__ import annotations

import argparse
from pathlib import Path


def invert_bytes(data: bytes) -> bytes:
    return bytes(b ^ 0xFF for b in data)


def detect_encoding(data: bytes, fallback: str) -> str:
    if data.startswith(b"\xff\xfe"):
        return "utf-16le"
    if data.startswith(b"\xfe\xff"):
        return "utf-16be"
    if data.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    return fallback


def main() -> None:
    parser = argparse.ArgumentParser(description="Decrypt p_monai.bin (XOR 0xFF).")
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
        help="Output decrypted file (default: p_monai.txt)",
    )
    parser.add_argument(
        "--encoding",
        default="cp949",
        help="Fallback text encoding (default: cp949).",
    )
    parser.add_argument(
        "--errors",
        default="replace",
        help="Decoding error handling (default: replace).",
    )
    parser.add_argument(
        "--binary",
        action="store_true",
        help="Write raw decrypted bytes instead of text.",
    )
    parser.add_argument(
        "--compare",
        dest="compare",
        help="Optional reference file to compare the decrypted output against.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = input_path.read_bytes()
    decrypted = invert_bytes(data)

    if args.binary:
        output_path.write_bytes(decrypted)
    else:
        encoding = detect_encoding(decrypted, args.encoding)
        text = decrypted.decode(encoding, errors=args.errors)
        output_path.write_text(text, encoding=encoding, newline="")

    if args.compare:
        reference = Path(args.compare).read_bytes()
        if decrypted != reference:
            raise SystemExit("Decrypted output does not match reference file.")


if __name__ == "__main__":
    main()
