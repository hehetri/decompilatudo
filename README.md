# p_monai.bin encrypt/decrypt

O arquivo `p_monai.bin` usa uma criptografia simples: cada byte é invertido (XOR `0xFF`).
Os scripts abaixo fazem a conversão nos dois sentidos, mantendo a mesma criptografia do arquivo original.

## Requisitos

- Python 3

## Descriptografar

Por padrão, o script gera texto automaticamente detectando BOM (UTF-16/UTF-8) e usando `cp949`
como fallback:

```bash
python decrypt_p_monai.py p_monai.bin p_monai.txt
```

Se quiser gravar o resultado como bytes crus (sem decodificar texto):

```bash
python decrypt_p_monai.py p_monai.bin p_monai.txt --binary
```

Também é possível ajustar a codificação e o tratamento de erros:

```bash
python decrypt_p_monai.py p_monai.bin p_monai.txt --encoding cp949 --errors replace
```

Para validar contra um arquivo de referência:

```bash
python decrypt_p_monai.py p_monai.bin p_monai.txt --compare caminho/para/referencia.bin
```

## Criptografar

Se você editou o arquivo como texto, use a mesma codificação:

```bash
python encrypt_p_monai.py p_monai.txt p_monai.bin --encoding cp949
```

Se o arquivo de entrada for binário (bytes crus), use:

```bash
python encrypt_p_monai.py p_monai.txt p_monai.bin --binary
```

Para garantir que a criptografia bate exatamente com um `.bin` original:

```bash
python encrypt_p_monai.py p_monai.txt p_monai.bin --compare caminho/para/p_monai.bin
```

## Observações

- Esse arquivo costuma conter bytes que não são válidos em UTF-8; por isso há fallback para `cp949`.
- Use `--binary` se você precisa manter 100% dos bytes sem nenhuma mudança.
