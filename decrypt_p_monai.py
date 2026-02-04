#!/usr/bin/env python3
"""Decrypt p_monai.bin with XOR 0xFF.

Usage:
  python decrypt_p_monai.py --input p_monai.bin --output p_monai.dec.bin
  python decrypt_p_monai.py --input p_monai.bin --output p_monai.txt --text
"""
from __future__ import annotations

import argparse
from pathlib import Path


def xor_bytes(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decrypt p_monai.bin with XOR 0xFF.")
    parser.add_argument("--input", required=True, help="Input file path.")
    parser.add_argument("--output", required=True, help="Output file path.")
    parser.add_argument("--key", default="0xFF", help="XOR key (hex or int).")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Decode output as cp949 text instead of writing raw bytes.",
    )
    args = parser.parse_args()

    key = int(args.key, 0)
    input_path = Path(args.input)
    output_path = Path(args.output)

    data = input_path.read_bytes()
    decrypted = xor_bytes(data, key)

    if args.text:
        output_path.write_text(decrypted.decode("cp949", errors="replace"), encoding="utf-8")
    else:
        output_path.write_bytes(decrypted)


if __name__ == "__main__":
    main()
