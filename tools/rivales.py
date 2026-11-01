#!/usr/bin/env python3
"""Cifra y descifra las notas privadas de rivales.

Las notas se escriben en un JSON (notas.json) que NO se sube al repositorio.
Este script lo convierte en rivales.enc.json, que sí se sube y solo se puede
abrir con la contraseña. La página lo descifra en el navegador.

Uso (la contraseña va en una variable de entorno, no en la línea de comandos):

    RIVALES_PASS='...' python3 tools/rivales.py encrypt notas.json
    RIVALES_PASS='...' python3 tools/rivales.py decrypt > notas.json

Necesita:  pip install cryptography

Formato de notas.json:

    {
      "updated": "2026-11-01",
      "teams": {
        "København Futsal": {
          "Cómo juegan": "Texto libre. Las líneas que empiezan con '- ' forman una lista.",
          "Jugadores a marcar": ["Nombre 1", "Nombre 2"]
        }
      }
    }
"""
import base64
import json
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITER = 600_000
OUT = Path(__file__).resolve().parent.parent / "rivales.enc.json"


def key_from(password: str, salt: bytes, iterations: int) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    return kdf.derive(password.encode("utf-8"))


def b64(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def password() -> str:
    pw = os.environ.get("RIVALES_PASS", "")
    if len(pw) < 12:
        sys.exit("Falta RIVALES_PASS o es muy corta (mínimo 12 caracteres).")
    return pw


def encrypt(src: str) -> None:
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    plain = json.dumps(data, ensure_ascii=False).encode("utf-8")
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(key_from(password(), salt, ITER)).encrypt(iv, plain, None)
    blob = {"v": 1, "kdf": "PBKDF2-SHA256", "iter": ITER, "salt": b64(salt), "iv": b64(iv), "ct": b64(ct)}
    OUT.write_text(json.dumps(blob, indent=1) + "\n", encoding="utf-8")
    print(f"Escrito {OUT}")


def decrypt() -> None:
    blob = json.loads(OUT.read_text(encoding="utf-8"))
    salt, iv, ct = (base64.b64decode(blob[k]) for k in ("salt", "iv", "ct"))
    try:
        plain = AESGCM(key_from(password(), salt, blob["iter"])).decrypt(iv, ct, None)
    except Exception:
        sys.exit("Contraseña incorrecta.")
    print(json.dumps(json.loads(plain), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "encrypt":
        encrypt(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "decrypt":
        decrypt()
    else:
        sys.exit(__doc__)
