import json

import pytest
from conftest import dossie

from desmontar.fontes import Resposta, autoridade, conferir


class Rede:
    """Rede de mentira: cada trecho de URL devolve uma resposta pronta."""

    def __init__(self, respostas):
        self.respostas = respostas
        self.chamadas = []

    def __call__(self, url):
        self.chamadas.append(url)
        for trecho, r in self.respostas.items():
            if trecho in url:
                return r
        return Resposta(404, "")


CROSSREF_OK = Resposta(200, json.dumps({"message": {"title": ["Um título sobre Amanita muscaria"]}}))
CROSSREF_RETRATADO = Resposta(200, json.dumps({"message": {
    "title": ["Um título sobre Amanita muscaria"],
    "updated-by": [{"type": "retraction", "label": "Retraction", "source": "retraction-watch"}]}}))
OPENALEX_LIMPO = Resposta(200, json.dumps({"is_retracted": False}))


def _erros(achados):
    return [a.achado for a in achados if a.nivel == "erro"]


def test_doi_conferido_passa():
    rede = Rede({"api.crossref.org": CROSSREF_OK, "api.openalex.org": OPENALEX_LIMPO})
    achados, tabela = conferir(dossie(), buscar=rede)
    assert _erros(achados) == []
    assert tabela[0]["autoridade"] == 0


def test_retratado_nao_marcado_e_erro():
    rede = Rede({"api.crossref.org": CROSSREF_RETRATADO, "api.openalex.org": OPENALEX_LIMPO})
    achados, _ = conferir(dossie(), buscar=rede)
    assert any("RETRATADO" in e for e in _erros(achados))


def test_retratado_marcado_passa():
    fonte = ["[F1] Autor X, 2020. Um título sobre Amanita muscaria. RETRATADO. https://doi.org/10.1234/abc.567"]
    rede = Rede({"api.crossref.org": CROSSREF_RETRATADO, "api.openalex.org": OPENALEX_LIMPO})
    achados, _ = conferir(dossie(fontes=fonte), buscar=rede)
    assert _erros(achados) == []


def test_openalex_sozinho_tambem_acusa_retratacao():
    rede = Rede({"api.crossref.org": CROSSREF_OK, "api.openalex.org": Resposta(200, '{"is_retracted": true}')})
    achados, _ = conferir(dossie(), buscar=rede)
    assert any("RETRATADO" in e for e in _erros(achados))


def test_nota_de_retratacao_nao_e_artigo_retratado():
    # a OpenAlex marca a própria nota (type "retraction") como is_retracted; a nota não é o artigo retratado
    nota = Resposta(200, '{"is_retracted": true, "type": "retraction"}')
    rede = Rede({"api.crossref.org": CROSSREF_OK, "api.openalex.org": nota})
    achados, _ = conferir(dossie(), buscar=rede)
    assert _erros(achados) == []


def test_doi_que_nao_resolve_e_erro():
    achados, _ = conferir(dossie(), buscar=Rede({}))
    assert any("não resolve" in e for e in _erros(achados))


def test_titulo_que_nao_confere_avisa():
    outro = Resposta(200, json.dumps({"message": {"title": ["Quantum chromodynamics lattice simulations"]}}))
    achados, _ = conferir(dossie(), buscar=Rede({"api.crossref.org": outro, "api.openalex.org": OPENALEX_LIMPO}))
    assert any("título não confere" in a.achado for a in achados if a.nivel == "aviso")


@pytest.mark.parametrize("modo,nivel", [("publicar", "erro"), ("pessoal", "aviso")])
def test_link_quebrado_pesa_conforme_o_modo(modo, nivel):
    txt = dossie(fontes=["[F1] Página. https://exemplo.com.br/sumiu"])
    achados, _ = conferir(txt, modo=modo, buscar=Rede({"exemplo.com.br": Resposta(404, "")}))
    assert any(a.nivel == nivel and "quebrado" in a.achado for a in achados)


def test_paywall_e_desafio_viram_aviso():
    pay = Resposta(200, "<html>" + "x" * 300 + " Subscribe to continue reading</html>")
    desafio = Resposta(403, "<html><title>Just a moment...</title></html>")
    txt = dossie(fontes=["[F1] Jornal. https://jornal.exemplo/a", "[F2] Base. https://base.exemplo/b"])
    achados, _ = conferir(txt, buscar=Rede({"jornal.exemplo": pay, "base.exemplo": desafio}))
    textos = " ".join(a.achado for a in achados if a.nivel == "aviso")
    assert "paywall" in textos and "bloqueia robôs" in textos
    assert _erros(achados) == []


def test_arxiv_sem_a_palavra_preprint_avisa():
    feed = Resposta(200, "<feed><title>ArXiv Query</title><entry><title>Attention Is All You Need</title></entry></feed>")
    txt = dossie(fontes=["[F1] Vaswani et al., 2017. Attention Is All You Need. arXiv:1706.03762"])
    achados, _ = conferir(txt, buscar=Rede({"export.arxiv.org": feed}))
    assert any("preprint" in a.achado for a in achados)


def test_offline_nao_abre_nada():
    def proibida(url):
        raise AssertionError("abriu a rede no modo offline")
    achados, tabela = conferir(dossie(), buscar=proibida, offline=True)
    assert tabela and any("offline" in a.achado for a in achados)


def test_autoridade_por_dominio():
    assert autoridade("https://doi.org/10.1/x") == 0
    assert autoridade("https://servicos.jbrj.gov.br/v2/flora/taxon/x") == 1
    assert autoridade("https://medium.com/post") == 2
    # observação cidadã é plataforma, não instituição: peso baixo, como blog
    assert autoridade("https://api.inaturalist.org/v1/taxa?q=x") == 2
