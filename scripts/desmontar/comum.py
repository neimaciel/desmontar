"""Peças comuns: onde a skill mora, os limiares, o cabeçalho e as seções de um Markdown.

`frontmatter` e `secao` vêm do validador da matriz (meta-skill/scripts/validar.py), adaptados.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def raiz() -> Path:
    """A pasta da skill: a variável DESMONTAR_RAIZ, ou a pasta acima de scripts/."""
    env = os.environ.get("DESMONTAR_RAIZ")
    if env:
        return Path(env).expanduser()
    if (RAIZ / "lib" / "limiares.json").is_file():
        return RAIZ
    return Path("~/.claude/skills/desmontar").expanduser()


def casa() -> Path:
    """Onde ficam os dossiês e a biblioteca de lentes (fora da skill)."""
    return Path(os.environ.get("DESMONTAR_HOME", "~/Documents/desmontar")).expanduser()


def limiares() -> dict:
    return json.loads((raiz() / "lib" / "limiares.json").read_text(encoding="utf-8"))


@dataclass
class Achado:
    nivel: str  # "erro" | "aviso" | "info"
    item: str
    achado: str

    def dict(self) -> dict:
        return asdict(self)


def erros(achados: list[Achado]) -> list[Achado]:
    return [a for a in achados if a.nivel == "erro"]


def frontmatter(txt: str) -> dict | None:
    """Cabeçalho YAML simples (chave: valor)."""
    if not txt.startswith("---"):
        return None
    fim = txt.find("\n---", 3)
    if fim < 0:
        return None
    fm = {}
    for linha in txt[3:fim].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", linha)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def corpo(txt: str) -> str:
    """O texto sem o cabeçalho."""
    if txt.startswith("---"):
        fim = txt.find("\n---", 3)
        if fim >= 0:
            return txt[fim + 4:]
    return txt


def lista(valor: str | None) -> list[str]:
    """'saude, pi' -> ['saude', 'pi']."""
    return [v.strip() for v in (valor or "").split(",") if v.strip()]


def normal(s: str) -> str:
    """Minúsculas e sem acento, para comparar títulos."""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def secoes(txt: str) -> dict[str, str]:
    """Seções de nível 2 ('## Título') -> texto até a próxima seção de nível 2."""
    out: dict[str, str] = {}
    partes = re.split(r"^##\s+(.+?)\s*$", corpo(txt), flags=re.M)
    for i in range(1, len(partes), 2):
        out[normal(partes[i])] = partes[i + 1]
    return out


def secao(txt: str, titulo: str) -> str | None:
    return secoes(txt).get(normal(titulo))


def itens(texto: str | None) -> list[str]:
    """Linhas de lista ('- x', '* x', '1. x') de um trecho."""
    return [m.group(1).strip() for m in re.finditer(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$", texto or "", flags=re.M)]


def slug(texto: str, maximo: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", normal(texto)).strip("-")
    return (s[:maximo].rstrip("-")) or "objeto"
