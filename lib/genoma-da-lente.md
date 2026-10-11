# Genoma da lente

Toda lente nasce daqui. A lente não é escolhida de uma lista: ela é **composta** a partir de três
leituras do objeto, e muda quando a leitura muda.

> **Lente = natureza × área × intenção**

- A **natureza** diz o que o objeto é, e por isso em que eixos ele se desmonta.
- A **área** diz que disciplina estuda aquilo, e por isso o que conta como prova ali.
- A **intenção** diz o que a pessoa quer levar, e por isso a forma da entrega.

## Os sete genes (seções obrigatórias de toda lente)

| Gene | Pergunta que responde |
|---|---|
| Eixos de desmontagem | Em que partes este tipo de coisa se separa? |
| Padrão de evidência | O que conta como prova nesta área, do mais forte ao mais fraco? |
| Fontes canônicas | Onde a área guarda o conhecimento conferível? |
| Perguntas de desmontagem | O que um especialista perguntaria primeiro? |
| Armadilhas | Como esta área costuma errar, e como o leigo costuma se enganar? |
| Portões de risco | Onde a análise pode causar dano e precisa parar? (ids de `lib/riscos.md`) |
| Entrega | Que forma tem o resultado útil para esta intenção? |

## Natureza: os eixos de cada tipo de coisa

Cada natureza se apoia num modelo clássico de explicação, para os eixos não serem inventados na hora.

| Natureza | Sinais de que é ela | Modelo | Eixos |
|---|---|---|---|
| `ser-vivo` | nome científico, foto de planta, fungo ou animal, "que espécie é" | as quatro perguntas de Tinbergen + taxonomia | identidade, morfologia diagnóstica, mecanismo, desenvolvimento, função ecológica, evolução e distribuição |
| `artefato` | objeto físico, máquina, construção, "como funciona este aparelho" | as quatro causas de Aristóteles + mecanismo | material, forma e estrutura, origem e fabricação, finalidade, mecanismo, modos de falha |
| `sistema-digital` | link, app, binário, API, código, "como este software faz X" | os três níveis de Marr | o que resolve, como resolve, onde roda, estado e dados, interfaces, fronteiras |
| `texto-argumento` | artigo, DOI, contrato, lei, post, laudo | o modelo de Toulmin + desenho do estudo | tese, dados, garantia, ressalvas, refutações, desenho e método |
| `ideia` | termo, teoria, viés, framework, "o que é X" | análise conceitual + genealogia | definição, premissas, genealogia, mecanismo, usos, fronteiras, confusões |
| `processo` | empresa, campanha, funil, mercado, política pública | cadeia causal + incentivos | objetivo, atores, etapas, incentivos, gargalos, métricas, efeitos colaterais |
| `obra` | estilo visual, tipografia, música, line art, texto literário | elementos + regras de composição | elementos, gramática (regras), técnica e ferramenta, variações, referências, assinatura do autor |

Objeto que mistura duas naturezas (um artigo sobre uma planta, um app que é também uma obra)
recebe **lente híbrida**:
- **eixos:** a união dos eixos úteis;
- **padrão de evidência:** o mais exigente dos dois;
- **portões:** a união dos dois.

O dossiê declara a mistura.

## Área: o padrão de prova

A área decide o gene "Padrão de evidência". Três perguntas montam esse gene quando não há lente pronta:

1. Qual é a evidência mais forte que esta área aceita? Exemplos: ensaio clínico em medicina, exsicata de herbário em botânica, obra original em filosofia, execução observada em software.
2. Qual é a mais fraca que ainda circula como se fosse prova? Post, app de identificação, resumo sem método.
3. Onde a área guarda o conhecimento conferível? Base oficial, periódico, flora, repositório, documentação. Use `lib/fontes-abertas.md` quando a área estiver lá.

## Intenção: a forma da entrega

| Intenção | Entrega |
|---|---|
| `entender` (padrão) | mapa das partes e de como se ligam |
| `verificar` | veredito por afirmação: sustentada, sustentada em parte, não sustentada, sem evidência |
| `reproduzir` | passo a passo, materiais, onde costuma dar errado |
| `criar-projeto` | a planta de um projeto novo (seção "Da desmontagem ao projeto" do dossiê) |

## Teste de especialista (antes de usar a lente)

Responda por escrito, no dossiê, em "Lente usada":
1. Que evidência um especialista desta área exigiria que a lente ainda não pede?
2. Que confusão clássica da área a lente não previne?
3. Que fonte canônica está faltando?

Corrija a lente antes de seguir. Se as três respostas forem "nenhuma", diga por quê.

## Compor uma lente do zero (área sem lente)

1. Copie `templates/lente.md`.
2. Preencha os sete genes a partir da natureza (eixos) e da área (as três perguntas acima).
3. Fontes canônicas só entram depois de abertas e conferidas: `desmontar lentes checar` testa os links.
4. Marque `origem: genoma`, `versao: 0` (rascunho) e use. Ela só vira versão 1 em `desmontar lentes gravar`,
   depois de um dossiê aprovado.
