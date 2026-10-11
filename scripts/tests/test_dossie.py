from conftest import cpf_gerado, dossie

from desmontar.dossie import PARTES_DO_PROJETO, PROJETO, doi_de, validar


def _erros(achados):
    return [a.achado for a in achados if a.nivel == "erro"]


def _avisos(achados):
    return [a.achado for a in achados if a.nivel == "aviso"]


def test_dossie_completo_passa_sem_erro():
    assert _erros(validar(dossie())) == []


def test_falta_secao_e_erro():
    txt = dossie().replace("## Próximas perguntas", "## Outra coisa")
    assert any("Próximas perguntas" in e for e in _erros(validar(txt)))


def test_afirmacao_sem_rotulo_e_erro():
    txt = dossie(afirmacoes=["A1 O chapéu é vermelho"])
    assert any("sem rótulo" in e for e in _erros(validar(txt)))


def test_citado_sem_fonte_e_erro():
    txt = dossie(afirmacoes=["A1 [citado] O nome aceito é X"])
    assert any("[citado] sem [Fn]" in e for e in _erros(validar(txt)))


def test_citado_com_fonte_que_nao_existe_e_erro():
    txt = dossie(afirmacoes=["A1 [citado] O nome aceito é X [F9]"])
    assert any("[F9]" in e for e in _erros(validar(txt)))


def test_inferido_sem_cadeia_e_erro():
    txt = dossie(afirmacoes=["A1 [inferido] Deve ser venenoso"])
    assert any("cadeia" in e for e in _erros(validar(txt)))


def test_fonte_sem_doi_nem_link_e_erro():
    txt = dossie(fontes=["[F1] Um livro que eu li"])
    assert any("sem DOI" in e for e in _erros(validar(txt)))


def test_publicar_recusa_inferencia_na_conclusao():
    txt = dossie(modo="publicar", conclusao="[inferido] É Amanita (de: A1)")
    assert any("publicar" in e or "inferência" in e for e in _erros(validar(txt)))


def test_publicar_recusa_travessao_e_pessoal_so_avisa():
    txt = dossie(conclusao="Compatível com Amanita — sem certificar consumo [F1].")
    assert any("travessão" in e for e in _erros(validar(txt, "publicar")))
    assert _erros(validar(txt, "pessoal")) == []
    assert any("travessão" in w for w in _avisos(validar(txt, "pessoal")))


def test_cliente_avisa_cpf_e_exige_limites():
    cpf = cpf_gerado()
    txt = dossie(modo="cliente", limites=" ", extra=f"\nObservação: CPF {cpf}\n")
    achados = validar(txt)
    assert any("Limites e riscos" in e for e in _erros(achados))
    assert any("CPF" in w for w in _avisos(achados))


def test_projeto_exige_a_secao_com_as_cinco_partes():
    txt = dossie(intencao="criar-projeto")
    assert any(PROJETO in e for e in _erros(validar(txt)))
    completa = "\n## " + PROJETO + "\n" + "".join(f"\n### {p}\ntexto\n" for p in PARTES_DO_PROJETO)
    assert _erros(validar(dossie(intencao="criar-projeto", extra=completa))) == []


def test_sem_observado_avisa():
    txt = dossie(afirmacoes=["A1 [citado] O nome aceito é X [F1]"]).replace("| observado |", "| citado | [F1] |", 1)
    assert any("não olhou" in w for w in _avisos(validar(txt)))


def test_doi_com_parenteses_sai_inteiro():
    linha = "- [F1] Wakefield, 1998. https://doi.org/10.1016/S0140-6736(97)11096-0 (RETRATADO)"
    assert doi_de(linha) == "10.1016/S0140-6736(97)11096-0"
    assert doi_de("[x](https://doi.org/10.1016/S0140-6736(97)11096-0).") == "10.1016/S0140-6736(97)11096-0"
