"""Biblioteca de lentes: escolher, checar, gravar com travas, histórico e volta.

A biblioteca fica fora da skill, em ~/Documents/desmontar/lentes/<natureza>/<area>/:
lente.md (versão atual), historico/v<N>.md e usos.jsonl. As lentes-semente vêm com a skill.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import shutil
from pathlib import Path

from .comum import Achado, casa, erros, frontmatter, itens, lista, limiares, normal, raiz, secao
from .dossie import validar as validar_dossie

NATUREZAS = ("ser-vivo", "artefato", "sistema-digital", "texto-argumento", "ideia", "processo", "obra")
PORTOES = ("saude", "juridico", "financeiro", "seguranca", "dados-pessoais", "pi")
GENES = ("Eixos de desmontagem", "Padrão de evidência", "Fontes canônicas", "Perguntas de desmontagem",
         "Armadilhas", "Portões de risco", "Entrega")
CAMPOS = ("id", "natureza", "area", "versao", "origem", "rigor")
# o que um objeto analisado não pode enfiar numa lente
INJECAO = re.compile(
    r"(ignore (all |the |as |todas as )?(previous|prior|above|anteriores|instru)|disregard (all|the|previous)|"
    r"system prompt|prompt do sistema|you are now|voc[eê] agora [eé] |new instructions|novas instru[cç][oõ]es|"
    r"desconsidere (as|todas)|\brm\s+-rf\b|curl[^\n]*\|\s*(ba|z)?sh|<script|\beval\(|base64\s+-d)", re.I)
SEGREDO = re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}|AIza[0-9A-Za-z_-]{30,}|gh[op]_[A-Za-z0-9]{20,}|"
                     r"rpa_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
RE_URL = re.compile(r"https?://[^\s\)\]>]+")


def sementes() -> dict[str, Path]:
    out = {}
    for p in sorted((raiz() / "lentes-semente").glob("*.md")):
        fm = frontmatter(p.read_text(encoding="utf-8")) or {}
        if fm.get("id"):
            out[fm["id"]] = p
    return out


def pasta(lente_id: str) -> Path:
    natureza, _, area = lente_id.partition("/")
    return casa() / "lentes" / natureza / area


def escolher(natureza: str, area: str) -> tuple[Path, str]:
    """A lente mais específica: aprendida, depois semente, depois o modelo em branco."""
    lente_id = f"{natureza}/{area}"
    aprendida = pasta(lente_id) / "lente.md"
    if aprendida.is_file():
        return aprendida, "aprendida"
    sem = sementes()
    if lente_id in sem:
        return sem[lente_id], "semente"
    return raiz() / "templates" / "lente.md", "modelo"


def listar() -> list[dict]:
    out = [{"id": i, "versao": (frontmatter(p.read_text(encoding="utf-8")) or {}).get("versao"),
            "origem": "semente", "caminho": str(p)} for i, p in sementes().items()]
    base = casa() / "lentes"
    for p in sorted(base.glob("*/*/lente.md")) if base.is_dir() else []:
        fm = frontmatter(p.read_text(encoding="utf-8")) or {}
        out.append({"id": fm.get("id"), "versao": fm.get("versao"), "origem": "aprendida", "caminho": str(p)})
    return out


def _contagem(txt: str, gene: str) -> int:
    return len(itens(secao(txt, gene)))


def checar(txt: str, links: bool = False, buscar=None) -> list[Achado]:
    """Estrutura, cabeçalho, portões conhecidos, tamanho, injeção, segredo e (opcional) links."""
    a: list[Achado] = []
    fm = frontmatter(txt) or {}
    for c in CAMPOS:
        if not fm.get(c) or "<" in fm.get(c, ""):
            a.append(Achado("erro", "cabeçalho", f"falta o campo '{c}'"))
    if fm.get("natureza") and fm["natureza"] not in NATUREZAS:
        a.append(Achado("erro", "cabeçalho", f"natureza '{fm['natureza']}' fora de {', '.join(NATUREZAS)}"))
    if fm.get("id") and fm.get("natureza") and fm.get("area") and fm["id"] != f"{fm['natureza']}/{fm['area']}":
        a.append(Achado("erro", "cabeçalho", "id precisa ser <natureza>/<area>"))
    ordem = limiares()["lentes"]["rigor_ordem"]
    if fm.get("rigor") and fm["rigor"] not in ordem:
        a.append(Achado("erro", "cabeçalho", f"rigor '{fm['rigor']}' fora de {', '.join(ordem)}"))
    for p in lista(fm.get("portoes")):
        if p not in PORTOES:
            a.append(Achado("erro", "portões", f"portão '{p}' não existe em lib/riscos.md"))
    for gene in GENES:
        s = secao(txt, gene)
        if s is None or not s.strip():
            a.append(Achado("erro", "genes", f"falta o gene '{gene}'"))
    if len(txt.encode("utf-8")) > limiares()["lentes"]["tamanho_maximo_kb"] * 1024:
        a.append(Achado("erro", "tamanho", "lente acima do tamanho máximo (lib/limiares.json)"))
    if INJECAO.search(txt):
        a.append(Achado("erro", "injeção", f"padrão de instrução embutida: '{INJECAO.search(txt).group(0)}'"))
    if SEGREDO.search(txt):
        a.append(Achado("erro", "segredo", "chave ou segredo dentro da lente"))
    for url in RE_URL.findall(txt):
        if url.startswith("http://"):
            a.append(Achado("aviso", "fontes", f"link sem https: {url}"))
    if links:
        from .fontes import buscador_padrao
        buscar = buscar or buscador_padrao()
        for url in sorted(set(u.rstrip(".,;") for u in RE_URL.findall(secao(txt, "Fontes canônicas") or ""))):
            r = buscar(url)
            if r.status == 0 or r.status in limiares()["lentes"]["status_fonte_morta"]:
                a.append(Achado("erro", "fontes", f"fonte canônica não abre (HTTP {r.status}): {url}"))
    return a


def _travas(nova: str, atual: str) -> list[Achado]:
    """A lente aprende a exigir mais, nunca menos."""
    a: list[Achado] = []
    fn, fa = frontmatter(nova) or {}, frontmatter(atual) or {}
    perdidos = set(lista(fa.get("portoes"))) - set(lista(fn.get("portoes")))
    if perdidos:
        a.append(Achado("erro", "trava", f"a versão nova perde portões: {', '.join(sorted(perdidos))}"))
    ordem = limiares()["lentes"]["rigor_ordem"]
    if fa.get("rigor") in ordem and fn.get("rigor") in ordem and ordem.index(fn["rigor"]) < ordem.index(fa["rigor"]):
        a.append(Achado("erro", "trava", f"o rigor baixaria de '{fa['rigor']}' para '{fn['rigor']}'"))
    for gene in ("Padrão de evidência", "Fontes canônicas", "Perguntas de desmontagem", "Armadilhas"):
        if _contagem(nova, gene) < _contagem(atual, gene):
            a.append(Achado("erro", "trava", f"'{gene}' encolheria ({_contagem(atual, gene)} -> {_contagem(nova, gene)})"))
    return a


def _versao(fm: dict) -> int:
    try:
        return int(fm.get("versao") or 0)
    except ValueError:
        return 0


def _com_cabecalho(txt: str, **campos) -> str:
    fim = txt.find("\n---", 3)
    cab, resto = txt[3:fim], txt[fim:]
    for k, v in campos.items():
        if re.search(rf"^{k}:", cab, flags=re.M):
            cab = re.sub(rf"^{k}:.*$", f"{k}: {v}", cab, flags=re.M)
        else:
            cab += f"\n{k}: {v}"
    return "---" + cab + resto


def _registrar(lente_id: str, registro: dict) -> None:
    with (pasta(lente_id) / "usos.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def gravar(arquivo: Path, dossie: Path, links: bool = True, buscar=None,
           hoje: str | None = None) -> tuple[list[Achado], Path | None]:
    """Grava a versão nova da lente, se o dossiê passou e as travas deixam."""
    nova = arquivo.read_text(encoding="utf-8")
    a = checar(nova, links=links, buscar=buscar)
    texto_dossie = dossie.read_text(encoding="utf-8")
    erros_dossie = erros(validar_dossie(texto_dossie))
    if erros_dossie:
        a.append(Achado("erro", "dossiê", f"o dossiê tem {len(erros_dossie)} erro(s) no validador"))
    fm = frontmatter(nova) or {}
    lente_id = fm.get("id", "")
    usada = normal((frontmatter(texto_dossie) or {}).get("lente", ""))
    if lente_id and not usada.startswith(normal(lente_id)):
        a.append(Achado("erro", "dossiê", f"o dossiê não usou a lente {lente_id}"))
    destino = pasta(lente_id) / "lente.md" if lente_id else None
    atual_txt = destino.read_text(encoding="utf-8") if destino and destino.is_file() else None
    if atual_txt is None and lente_id in sementes():
        atual_txt = sementes()[lente_id].read_text(encoding="utf-8")
    if atual_txt:
        a += _travas(nova, atual_txt)
    if erros(a) or destino is None:
        return a, None
    versao = (_versao(frontmatter(atual_txt) or {}) if atual_txt else 0) + 1
    hoje = hoje or _dt.date.today().isoformat()
    destino.parent.mkdir(parents=True, exist_ok=True)
    (destino.parent / "historico").mkdir(exist_ok=True)
    if destino.is_file():
        anterior = _versao(frontmatter(destino.read_text(encoding="utf-8")) or {})
        shutil.copy2(destino, destino.parent / "historico" / f"v{anterior}.md")
    elif atual_txt is not None:
        # primeira vez que a lente aprende: a semente vira a versão de partida do histórico
        anterior = _versao(frontmatter(atual_txt) or {})
        (destino.parent / "historico" / f"v{anterior}.md").write_text(atual_txt, encoding="utf-8")
    destino.write_text(_com_cabecalho(nova, versao=versao, origem="aprendida", atualizada=hoje),
                       encoding="utf-8")
    shutil.copy2(destino, destino.parent / "historico" / f"v{versao}.md")
    _registrar(lente_id, {"data": hoje, "acao": "gravar", "versao": versao, "dossie": str(dossie)})
    return a, destino


def historico(lente_id: str) -> list[dict]:
    arq = pasta(lente_id) / "usos.jsonl"
    if not arq.is_file():
        return []
    return [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]


def voltar(lente_id: str, versao: int, hoje: str | None = None) -> tuple[list[Achado], Path | None]:
    """Volta a uma versão do histórico. A volta vira uma versão nova; nada se apaga."""
    p = pasta(lente_id)
    origem = p / "historico" / f"v{versao}.md"
    if not origem.is_file():
        return [Achado("erro", "voltar", f"não existe a versão {versao} de {lente_id}")], None
    atual = _versao(frontmatter((p / "lente.md").read_text(encoding="utf-8")) or {})
    nova = atual + 1
    hoje = hoje or _dt.date.today().isoformat()
    txt = _com_cabecalho(origem.read_text(encoding="utf-8"), versao=nova, atualizada=hoje)
    (p / "lente.md").write_text(txt, encoding="utf-8")
    shutil.copy2(p / "lente.md", p / "historico" / f"v{nova}.md")
    _registrar(lente_id, {"data": hoje, "acao": "voltar", "versao": nova, "de": versao})
    return [], p / "lente.md"
