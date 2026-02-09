# p_monai.bin encrypt/decrypt

O arquivo `p_monai.bin` usa uma criptografia simples: cada byte é invertido (XOR `0xFF`).
Os scripts abaixo fazem a conversão nos dois sentidos, mantendo a mesma criptografia do arquivo original.

## Requisitos

- Python 3

## Extração (modo recomendado)

O arquivo possui um cabeçalho de 8 bytes antes do texto. Use o script de extração para
remover o cabeçalho e gerar um `.txt` legível:

```bash
python extract_p_monai.py p_monai.bin p_monai.txt
```

Se precisar alterar codificação ou erros:

```bash
python extract_p_monai.py p_monai.bin p_monai.txt --encoding cp949 --errors replace
```

## Reempacotar (modo recomendado)

Depois de editar o texto, reempacote o arquivo usando o mesmo cabeçalho:

```bash
python pack_p_monai.py p_monai.txt p_monai.bin
```

Você também pode apontar para um `.bin` de referência para copiar o cabeçalho:

```bash
python pack_p_monai.py p_monai.txt p_monai.bin --header-from p_monai.bin
```

## Scripts básicos (binário completo)

Se você quiser trabalhar com o arquivo inteiro (sem remover cabeçalho), use os scripts
`decrypt_p_monai.py` e `encrypt_p_monai.py`:

```bash
python decrypt_p_monai.py p_monai.bin p_monai_full.bin --binary
python encrypt_p_monai.py p_monai_full.bin p_monai.bin --binary
```

## Observações

- A codificação mais comum do texto é `cp949`.
- Se você precisa preservar todos os bytes sem mudanças, use os modos binários.
