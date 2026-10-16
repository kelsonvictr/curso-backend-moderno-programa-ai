#!/usr/bin/env python3
"""Empacota a Loja Café (Cap 03) a partir do repositório git de referência.

Uso:  python3 tooling/build-loja-cafe.py [repo-ou-bundle]

Sem argumento, usa tooling/cap03-kafka/loja-cafe.bundle. Para cada tag (inicio, ato1..ato4)
gera capitulos/03-pedidos-kafka/apoio/loja-cafe-<tag>.zip com a pasta loja-cafe/ e o
COMO-RODAR.md, e atualiza apoio/checkpoints.json. ZIPs determinísticos (datas fixas).
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ORIGEM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "cap03-kafka", "loja-cafe.bundle")
APOIO = os.path.join(RAIZ, "capitulos", "03-pedidos-kafka", "apoio")
COMO_RODAR = os.path.join(AQUI, "cap03-kafka", "loja-cafe-extras", "COMO-RODAR.md")
TAGS = ["inicio", "ato1", "ato2", "ato3", "ato4"]
DATA = (2026, 10, 17, 13, 30, 0)

repo = ORIGEM
if ORIGEM.endswith(".bundle"):
    repo = tempfile.mkdtemp(prefix="loja-cafe-")
    subprocess.run(["git", "clone", "-q", ORIGEM, repo], check=True)
    subprocess.run(["git", "-C", repo, "fetch", "-q", "--tags", ORIGEM], check=True)

checkpoints = []
for tag in TAGS:
    tar = subprocess.run(["git", "-C", repo, "archive", "--format=tar", tag], capture_output=True, check=True).stdout
    arquivos = {}
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t.getmembers():
            if m.isfile():
                arquivos[m.name] = (t.extractfile(m).read(), m.mode)
    arquivos["COMO-RODAR.md"] = (open(COMO_RODAR, "rb").read(), 0o644)
    destino = os.path.join(APOIO, f"loja-cafe-{tag}.zip")
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for nome in sorted(arquivos):
            dados, modo = arquivos[nome]
            info = zipfile.ZipInfo("loja-cafe/" + nome, DATA)
            info.external_attr = (modo & 0o777 | 0o100000) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, dados)
    bruto = open(destino, "rb").read()
    checkpoints.append({"file": os.path.basename(destino), "tag": tag, "files": len(arquivos),
                        "sha256": hashlib.sha256(bruto).hexdigest(), "bytes": len(bruto)})
    print(f"{destino}  {len(arquivos)} arquivos  {len(bruto)} bytes")

json.dump(checkpoints, open(os.path.join(APOIO, "checkpoints.json"), "w"), indent=2)
