"""Validador do dossiê: estrutura, rótulos e regras de cada modo de uso.

O formato do achado (erro, aviso) segue o da random-video-editor-ultra.
"""
from __future__ import annotations

import re

from .comum import Achado, frontmatter, itens, normal, secao, secoes

ROTULOS = ("observado", "citado", "inferido", "desconhecido")
MODOS = ("pessoal", "publicar", "cliente", "projeto")
INTENCOES = ("entender", "verificar", "reproduzir", "criar-projeto")
CAMPOS = ("objeto", "data", "modo", "intencao", "lente")
SECOES = ("Ficha de área", "Lente usada", "Partes", "Afirmações", "Conclusão",
          "Limites e riscos", "Próximas perguntas", "Fontes")
PROJETO = "Da desmontagem ao projeto"
PARTES_DO_PROJETO = ("Reproduzir", "Fazer diferente", "Não copiar", "Licenças", "Primeiros passos")

RE_ROTULO = re.compile(r"\[(observado|citado|inferido|desconhecido)\]", re.I)
RE_AFIRMACAO = re.compile(
    r"^(?:\*\*)?(?:A\d+)?(?:\*\*)?[.:)]?\s*\[(observado|citado|inferido|desconhecido)\]", re.I)
RE_REF = re.compile(r"\[F(\d+)\]")
RE_FONTE = re.compile(r"^\[F(\d+)\]\s*(.*)$")
RE_DOI = re.compile(r"\b10\.\d{4,9}/\S+")
RE_ARXIV = re.compile(r"(?:arXiv:\s*|arxiv\.org/abs/)(\d{4}\.\d{4,5})", re.I)
RE_URL = re.compile(r"https?://[^\s\)\]>]+")
RE_TRAVESSAO = re.compile(r"—|\s–\s")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
RE_TELEFONE = re.compile(r"(?:\+?55\s?)?\(?\b\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b")
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")


def doi_de(linha: str) -> str | None:
    """O DOI da linha, sem a pontuação do texto em volta. DOI pode ter parênteses: 10.1016/S0140-6736(97)11096-0."""
    m = RE_DOI.search(linha or "")
    if not m:
        return None
    doi = m.group(0).rstrip(".,;:]>\"'")
    while doi.endswith(")") and doi.count("(") < doi.count(")"):
        doi = doi[:-1].rstrip(".,;:]>\"'")
    return doi


def cpf_valido(cpf: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", cpf)]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for n in (9, 10):
        if (sum(d[j] * (n + 1 - j) for j in range(n)) * 10) % 11 % 10 != d[n]:
            return False
    return True


def fontes(txt: str) -> dict[str, str]:
    """{'1': 'linha da fonte F1', ...} a partir da seção Fontes."""
    out = {}
    for linha in itens(secao(txt, "Fontes")):
        m = RE_FONTE.match(linha)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def _linhas_da_tabela(texto: str | None) -> list[list[str]]:
    linhas = []
    for bruta in (texto or "").splitlines():
        b = bruta.strip()
        if not b.startswith("|") or re.match(r"^\|[\s:|-]+\|$", b):
            continue
        linhas.append([c.strip() for c in b.strip("|").split("|")])
    return linhas[1:]  # sem o cabeçalho


def validar(txt: str, modo: str | None = None) -> list[Achado]:
    a: list[Achado] = []
    fm = frontmatter(txt) or {}
    for campo in CAMPOS:
        if not fm.get(campo) or "<" in fm.get(campo, ""):
            a.append(Achado("erro", "cabeçalho", f"falta o campo '{campo}'"))
    modo = modo or fm.get("modo") or "pessoal"
    if modo not in MODOS:
        a.append(Achado("erro", "cabeçalho", f"modo '{modo}' não existe ({', '.join(MODOS)})"))
    intencao = fm.get("intencao", "entender")
    if fm.get("intencao") and intencao not in INTENCOES:
        a.append(Achado("erro", "cabeçalho", f"intenção '{intencao}' não existe ({', '.join(INTENCOES)})"))

    todas = secoes(txt)
    for titulo in SECOES:
        if normal(titulo) not in todas:
            a.append(Achado("erro", "estrutura", f"falta a seção '{titulo}'"))

    refs_definidas = fontes(txt)
    for n, linha in refs_definidas.items():
        if not (RE_DOI.search(linha) or RE_ARXIV.search(linha) or RE_URL.search(linha)):
            a.append(Achado("erro", f"F{n}", "fonte sem DOI, arXiv ou link"))

    def _refs(texto: str, onde: str) -> None:
        for n in RE_REF.findall(texto):
            if n not in refs_definidas:
                a.append(Achado("erro", onde, f"[F{n}] citada mas não está em Fontes"))

    afirmacoes = itens(secao(txt, "Afirmações"))
    if normal("Afirmações") in todas and not afirmacoes:
        a.append(Achado("erro", "Afirmações", "nenhuma afirmação"))
    for linha in afirmacoes:
        curta = linha[:70]
        m = RE_AFIRMACAO.match(linha)
        if not m:
            a.append(Achado("erro", "rótulo", f"afirmação sem rótulo: '{curta}'"))
            continue
        rot = m.group(1).lower()
        if rot == "citado" and not RE_REF.search(linha):
            a.append(Achado("erro", "rótulo", f"[citado] sem [Fn]: '{curta}'"))
        if rot == "inferido" and "(de:" not in linha:
            a.append(Achado("erro", "rótulo", f"[inferido] sem a cadeia '(de: ...)': '{curta}'"))
        if rot == "observado" and "(onde:" not in linha:
            a.append(Achado("aviso", "rótulo", f"[observado] sem '(onde: ...)': '{curta}'"))
        if rot == "desconhecido" and "(resolveria:" not in linha:
            a.append(Achado("aviso", "rótulo", f"[desconhecido] sem '(resolveria: ...)': '{curta}'"))
        _refs(linha, "Afirmações")

    for celulas in _linhas_da_tabela(secao(txt, "Partes")):
        if len(celulas) < 5:
            continue
        rot = normal(celulas[3]).strip("[]")
        if rot not in ROTULOS:
            a.append(Achado("erro", "Partes", f"parte '{celulas[0][:40]}' sem rótulo válido"))
        elif rot == "citado" and not RE_REF.search(celulas[4]):
            a.append(Achado("erro", "Partes", f"parte '{celulas[0][:40]}' citada sem [Fn]"))
        _refs(celulas[4], "Partes")

    if not re.search(r"\[observado\]|\|\s*observado\s*\|", txt, re.I):
        a.append(Achado("aviso", "método", "nenhum [observado]: o dossiê não olhou o próprio objeto"))

    conclusao = secao(txt, "Conclusão") or ""
    if normal("Conclusão") in todas and not conclusao.strip():
        a.append(Achado("erro", "Conclusão", "conclusão vazia"))
    _refs(conclusao, "Conclusão")
    limites = secao(txt, "Limites e riscos") or ""

    if modo == "publicar":
        for rot in ("inferido", "desconhecido"):
            if f"[{rot}]" in conclusao.lower():
                a.append(Achado("erro", "publicar", f"[{rot}] na conclusão: inferência não vira fato no modo publicar"))
        if RE_TRAVESSAO.search(txt):
            a.append(Achado("erro", "publicar", "travessão no texto"))
    elif RE_TRAVESSAO.search(txt):
        a.append(Achado("aviso", "estilo", "travessão no texto"))

    if modo == "cliente":
        if not limites.strip():
            a.append(Achado("erro", "cliente", "a seção 'Limites e riscos' é obrigatória no modo cliente"))
        if any(cpf_valido(c) for c in RE_CPF.findall(txt)):
            a.append(Achado("aviso", "dados-pessoais", "CPF válido no dossiê: mascarar antes de compartilhar"))
        if RE_EMAIL.search(corpo_sem_fontes(txt)):
            a.append(Achado("aviso", "dados-pessoais", "e-mail no dossiê: mascarar antes de compartilhar"))
        if RE_TELEFONE.search(corpo_sem_fontes(txt)):
            a.append(Achado("aviso", "dados-pessoais", "telefone no dossiê: mascarar antes de compartilhar"))

    if modo == "projeto" or intencao == "criar-projeto":
        projeto = secao(txt, PROJETO)
        if projeto is None:
            a.append(Achado("erro", "projeto", f"falta a seção '{PROJETO}'"))
        else:
            for parte in PARTES_DO_PROJETO:
                if normal(parte) not in normal(projeto):
                    a.append(Achado("erro", "projeto", f"falta '{parte}' em '{PROJETO}'"))
    return a


def corpo_sem_fontes(txt: str) -> str:
    """O texto sem a seção Fontes (links e DOIs lá não são dado pessoal)."""
    s = secao(txt, "Fontes")
    return txt.replace(s, "") if s else txt
