#!/usr/bin/env python3
"""Encrypt a decrypted p_monai file with XOR 0xFF.

Usage:
  python encrypt_p_monai.py --input p_monai.dec.bin --output p_monai.bin
"""
from __future__ import annotations

import argparse
from pathlib import Path


def xor_bytes(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt p_monai data with XOR 0xFF.")
    parser.add_argument("--input", required=True, help="Input file path.")
    parser.add_argument("--output", required=True, help="Output file path.")
    parser.add_argument("--key", default="0xFF", help="XOR key (hex or int).")
    args = parser.parse_args()

    key = int(args.key, 0)
    input_path = Path(args.input)
    output_path = Path(args.output)

    data = input_path.read_bytes()
    encrypted = xor_bytes(data, key)
    output_path.write_bytes(encrypted)


if __name__ == "__main__":
    main()
