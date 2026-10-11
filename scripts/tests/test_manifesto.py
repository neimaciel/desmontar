"""O skill.json não pode mentir: todo caminho citado existe e a versão é a mesma em todo lugar."""
from __future__ import annotations

import contextlib
import io
import json
import re
from pathlib import Path

import desmontar
from desmontar import cli

RAIZ = Path(__file__).resolve().parents[2]
MANIFESTO = json.loads((RAIZ / "skill.json").read_text(encoding="utf-8"))


def _caminhos(m: dict) -> list[str]:
    return ([m["entrypoint"], m["limiares"]] + m["workflows"] + m["lib"] + m["templates"]
            + list(m["lentes_semente"].values()))


def test_todo_caminho_do_manifesto_existe():
    faltando = [c for c in _caminhos(MANIFESTO) if not (RAIZ / c).is_file()]
    assert faltando == []


def test_todo_caminho_citado_no_skill_md_existe():
    txt = (RAIZ / "SKILL.md").read_text(encoding="utf-8")
    citados = [t for t in re.findall(r"`([^`\s]+\.(?:md|json))`", txt)]
    assert citados and [c for c in citados if not (RAIZ / c).is_file()] == []


def test_versao_e_a_mesma_em_todo_lugar():
    pyproject = re.search(r'^version = "([^"]+)"', (RAIZ / "scripts" / "pyproject.toml").read_text(encoding="utf-8"), re.M)
    rodape = re.findall(r"\bv(\d+\.\d+\.\d+)\b", (RAIZ / "SKILL.md").read_text(encoding="utf-8"))
    changelog = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (RAIZ / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    versoes = {MANIFESTO["version"], desmontar.__version__, pyproject.group(1), rodape[-1], changelog.group(1)}
    assert len(versoes) == 1, versoes


def test_comandos_do_manifesto_existem_na_linha_de_comando():
    ajuda = io.StringIO()
    with contextlib.redirect_stdout(ajuda):
        try:
            cli.main(["--help"])
        except SystemExit:
            pass
    for comando in MANIFESTO["comandos"]:
        assert comando in ajuda.getvalue(), comando


def test_sementes_do_manifesto_batem_com_o_id_de_cada_arquivo():
    from desmontar.comum import frontmatter
    for lente_id, caminho in MANIFESTO["lentes_semente"].items():
        fm = frontmatter((RAIZ / caminho).read_text(encoding="utf-8"))
        assert fm["id"] == lente_id
