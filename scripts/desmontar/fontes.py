"""Conferência de fontes: DOI, retratação, título, links e peso por domínio.

Herda do motor do Conclave (mairs/extract.py e mairs/websearch.py) a regra de paywall, o corpo
mínimo e a autoridade por domínio. A rede entra por uma função injetável, para os testes não
dependerem dela.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable

from .comum import Achado, limiares, normal
from .dossie import RE_ARXIV, RE_URL, doi_de, fontes


@dataclass
class Resposta:
    status: int  # 0 = não conectou
    texto: str
    url_final: str = ""


Buscador = Callable[[str], Resposta]

PAYWALL = re.compile(
    r"(member[- ]only|sign in to (read|continue)|subscribe to (read|continue|keep reading)|"
    r"assine para (continuar|ler)|conte[úu]do exclusivo para assinantes|"
    r"create a free account to|you'?ve reached your (free )?(article|monthly) limit|"
    r"metered paywall|please (log|sign) in to (view|read)|faça login para (ler|continuar))",
    re.I)
DESAFIO = re.compile(r"<title>\s*(just a moment|attention required|access denied)", re.I)
ACADEMICO = ("arxiv.org", "doi.org", "ncbi.nlm.nih.gov", "pubmed", "semanticscholar.org",
             "springer", "sciencedirect", "nature.com", "jstor.org", "ssrn.com", "scielo",
             "openalex.org", "crossref.org", "acm.org", "ieee.org", "plos.org", "mdpi.com",
             "wiley.com", "tandfonline.com", "sagepub.com", "cambridge.org", "oup.com",
             "frontiersin.org", "plato.stanford.edu", ".edu")
INSTITUCIONAL = (".gov", ".gob", ".int", "europa.eu", "who.int", "oecd.org", "worldbank.org",
                 "un.org", "iso.org", "gbif.org", "kew.org", "jbrj.gov.br")


def autoridade(url: str) -> int:
    """0 acadêmico, 1 institucional, 2 o resto. Menor é mais forte."""
    host = urllib.parse.urlparse(url if url.startswith("http") else "https://" + url).netloc.lower()
    if any(k in host for k in ACADEMICO):
        return 0
    if any(k in host for k in INSTITUCIONAL):
        return 1
    return 2


def buscador_padrao() -> Buscador:
    rede = limiares()["rede"]

    def buscar(url: str) -> Resposta:
        ultimo = Resposta(0, "")
        for _ in range(max(1, int(rede["tentativas"]))):
            req = urllib.request.Request(url, headers={"User-Agent": rede["user_agent"],
                                                       "Accept": "*/*"})
            try:
                with urllib.request.urlopen(req, timeout=rede["timeout_s"]) as r:
                    corpo = r.read(400_000).decode("utf-8", errors="replace")
                    return Resposta(r.status, corpo, r.geturl())
            except urllib.error.HTTPError as e:
                corpo = e.read(50_000).decode("utf-8", errors="replace") if e.fp else ""
                return Resposta(e.code, corpo, url)
            except (urllib.error.URLError, TimeoutError, OSError):
                ultimo = Resposta(0, "")
        return ultimo
    return buscar


def _palavras(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", normal(s)) if len(w) > 3}


def semelhanca(titulo: str, linha: str) -> float:
    t = _palavras(titulo)
    return len(t & _palavras(linha)) / len(t) if t else 1.0


def _json(r: Resposta) -> dict | None:
    try:
        return json.loads(r.texto)
    except ValueError:
        return None


def conferir_doi(doi: str, linha: str, ref: str, buscar: Buscador) -> list[Achado]:
    a: list[Achado] = []
    cr = buscar(f"https://api.crossref.org/v1/works/{urllib.parse.quote(doi, safe='/')}")
    dados = (_json(cr) or {}).get("message") if cr.status == 200 else None
    if not dados:
        if cr.status == 0:
            a.append(Achado("aviso", ref, f"sem conexão para conferir o DOI {doi}"))
        else:
            a.append(Achado("erro", ref, f"DOI {doi} não resolve no Crossref (HTTP {cr.status})"))
        return a
    titulo = (dados.get("title") or [""])[0]
    retratado = any("retract" in normal(str(u.get("type", "")) + str(u.get("label", "")))
                    for u in dados.get("updated-by") or [])
    oa = buscar(f"https://api.openalex.org/works/doi:{doi}?select=is_retracted,title,type")
    # a própria nota de retratação vem marcada is_retracted na OpenAlex; ela não é o artigo retratado
    if oa.status == 200 and (_json(oa) or {}).get("is_retracted") and (_json(oa) or {}).get("type") != "retraction":
        retratado = True
    if retratado and "retratad" not in normal(linha):
        a.append(Achado("erro", ref, f"artigo RETRATADO e o dossiê não marca: {titulo[:70]}"))
    elif retratado:
        a.append(Achado("info", ref, "retratado, e o dossiê marca"))
    limite = limiares()["fontes"]["titulo_semelhanca_minima"]
    if titulo and semelhanca(titulo, linha) < limite:
        a.append(Achado("aviso", ref, f"título não confere com o DOI: '{titulo[:70]}'"))
    return a


def conferir_arxiv(ident: str, linha: str, ref: str, buscar: Buscador) -> list[Achado]:
    r = buscar(f"https://export.arxiv.org/api/query?id_list={ident}")
    titulos = re.findall(r"<title>([^<]+)</title>", r.texto or "")
    if r.status == 0:
        return [Achado("aviso", ref, f"sem conexão para conferir arXiv:{ident}")]
    if r.status != 200 or len(titulos) < 2:
        return [Achado("erro", ref, f"arXiv:{ident} não encontrado")]
    a = []
    titulo = titulos[1].strip()
    if semelhanca(titulo, linha) < limiares()["fontes"]["titulo_semelhanca_minima"]:
        a.append(Achado("aviso", ref, f"título não confere com o arXiv: '{titulo[:70]}'"))
    if "preprint" not in normal(linha):
        a.append(Achado("aviso", ref, "preprint sem revisão por pares: diga isso na linha da fonte"))
    return a


def conferir_link(url: str, ref: str, modo: str, buscar: Buscador) -> list[Achado]:
    lim = limiares()["fontes"]
    r = buscar(url)
    grave = "erro" if modo == "publicar" else "aviso"
    if r.status == 0:
        return [Achado(grave, ref, f"link não abriu: {url}")]
    if r.status in lim["status_quebrado"] and not DESAFIO.search(r.texto or ""):
        return [Achado(grave, ref, f"link quebrado (HTTP {r.status}): {url}")]
    if DESAFIO.search(r.texto or ""):
        return [Achado("aviso", ref, f"página bloqueia robôs; conferir à mão: {url}")]
    a = []
    if PAYWALL.search(r.texto or ""):
        a.append(Achado("aviso", ref, f"paywall: a página não conta como lida: {url}"))
    elif len(re.sub(r"<[^>]+>", " ", r.texto or "").strip()) < lim["corpo_minimo_chars"]:
        a.append(Achado("aviso", ref, f"página quase vazia: {url}"))
    return a


def conferir(txt: str, modo: str = "pessoal", buscar: Buscador | None = None,
             offline: bool = False) -> tuple[list[Achado], list[dict]]:
    """Confere cada fonte da seção Fontes. Devolve (achados, tabela das fontes)."""
    achados: list[Achado] = []
    tabela: list[dict] = []
    buscar = buscar or buscador_padrao()
    for n, linha in fontes(txt).items():
        ref = f"F{n}"
        doi = doi_de(linha)
        arx = RE_ARXIV.search(linha)
        urls = [u.rstrip(".,;") for u in RE_URL.findall(linha)]
        alvo = (f"https://doi.org/{doi}" if doi else
                f"https://arxiv.org/abs/{arx.group(1)}" if arx else (urls[0] if urls else ""))
        tabela.append({"ref": ref, "alvo": alvo, "autoridade": autoridade(alvo) if alvo else None})
        if offline:
            continue
        if doi:
            achados += conferir_doi(doi, linha, ref, buscar)
        elif arx:
            achados += conferir_arxiv(arx.group(1), linha, ref, buscar)
        elif urls:
            achados += conferir_link(urls[0], ref, modo, buscar)
    if offline:
        achados.append(Achado("aviso", "rede", "modo offline: nenhuma fonte foi aberta"))
    return achados, tabela
