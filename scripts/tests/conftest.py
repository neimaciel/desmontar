"""Testes com dados gerados: nenhum dossiê real, nenhum CPF real, nenhuma rede."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))


@pytest.fixture(autouse=True)
def _ambiente(tmp_path, monkeypatch):
    monkeypatch.setenv("DESMONTAR_RAIZ", str(RAIZ))
    monkeypatch.setenv("DESMONTAR_HOME", str(tmp_path / "casa"))


def dossie(modo="pessoal", intencao="entender", lente="ser-vivo/micologia v1 (genoma)",
           afirmacoes=None, conclusao=None, limites="Não cobre toxicidade; portão saude devolvido.",
           fontes=None, extra=""):
    afirmacoes = afirmacoes or [
        "A1 [observado] O chapéu é vermelho com pintas brancas (onde: foto 1)",
        "A2 [citado] O nome aceito é Amanita muscaria [F1]",
        "A3 [inferido] O cogumelo da foto é compatível com Amanita muscaria (de: A1 + F1)",
        "A4 [desconhecido] A cor do esporo (resolveria: impressão de esporos)",
    ]
    conclusao = conclusao or "Compatível com Amanita muscaria [F1], sem certificar nada sobre consumo."
    fontes = fontes or ["[F1] Autor X, 2020. Um título sobre Amanita muscaria. https://doi.org/10.1234/abc.567 (conferida em 2026-10-10)"]
    linhas = "\n".join(f"- {a}" for a in afirmacoes)
    fts = "\n".join(f"- {f}" for f in fontes)
    return f"""---
objeto: cogumelo de teste
data: 2026-10-10
modo: {modo}
intencao: {intencao}
lente: {lente}
confianca_area: 0.8
---
# Desmontagem: cogumelo de teste

## Ficha de área
- **Natureza:** ser-vivo

## Lente usada
ser-vivo/micologia v1; teste de especialista: acrescentei impressão de esporos.

## Partes
| Parte | O que é | O que faz | Rótulo | Fonte |
|---|---|---|---|---|
| chapéu | píleo | protege as lamelas | observado | (onde: foto 1) |
| nome | táxon | identifica | citado | [F1] |

## Afirmações
{linhas}

## Conclusão
{conclusao}

## Limites e riscos
{limites}

## Próximas perguntas
- Fazer impressão de esporos.

## Fontes
{fts}
{extra}"""


def cpf_gerado() -> str:
    d = [int(c) for c in "5299" + "82247"]
    for n in (9, 10):
        d.append((sum(d[j] * (n + 1 - j) for j in range(n)) * 10) % 11 % 10)
    t = "".join(map(str, d))
    return f"{t[:3]}.{t[3:6]}.{t[6:9]}-{t[9:]}"
