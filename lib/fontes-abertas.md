# Fontes abertas (gratuitas, sem chave)

Testadas em 10/10/2026. A coluna "Devolve" diz o que serve como evidência. Fonte fora desta lista
pode ser usada, mas passa por `desmontar conferir` como qualquer link.

## Artigos e ciência

| Fonte | Chamada | Devolve |
|---|---|---|
| Crossref | `https://api.crossref.org/v1/works/<DOI>` | título, ano, revista; em `updated-by`, correções e **retratações** da base Retraction Watch |
| OpenAlex | `https://api.openalex.org/works/doi:<DOI>` | `is_retracted`, citações, acesso aberto, autores |
| arXiv | `https://export.arxiv.org/api/query?id_list=<id>` | título e resumo do preprint (sem revisão por pares) |
| PubMed | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<termos>&retmode=json` | PMIDs da biomedicina |
| Semantic Scholar | `https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>` | citações e contexto; **sem chave devolve 429**, por isso é opcional |

## Botânica e seres vivos

| Fonte | Chamada | Devolve |
|---|---|---|
| Flora e Funga do Brasil (JBRJ) | `https://servicos.jbrj.gov.br/v2/flora/taxon/<nome científico>` | nome correto, status (aceito, sinônimo), família, ocorrência no Brasil |
| GBIF | `https://api.gbif.org/v1/species/match?name=<nome>` | nome aceito no mundo, família, `confidence` do casamento |
| iNaturalist | `https://api.inaturalist.org/v1/taxa?q=<nome>` | nome popular, número de observações, fotos de referência |
| POWO (Kew) | `https://powo.science.kew.org/` | **bloqueado por desafio da Cloudflare para robôs**: só como link aberto à mão |

## Conceitos e conhecimento geral

| Fonte | Chamada | Devolve |
|---|---|---|
| Wikidata | `https://www.wikidata.org/w/api.php?action=wbsearchentities&search=<termo>&language=pt&format=json` | entidade, descrição curta, ligações com outras entidades |
| Wikipedia | `https://pt.wikipedia.org/api/rest_v1/page/summary/<Título>` | resumo; serve de **mapa** para achar a fonte primária, nunca como prova final |
| Stanford Encyclopedia of Philosophy | `https://plato.stanford.edu/entries/<verbete>/` | verbete revisado por pares (sem API; link estável) |

## Software

| Fonte | Como | Devolve |
|---|---|---|
| O próprio artefato | leitura do código, do pacote ou da página | o que está lá ([observado]) |
| REA | ferramentas do REA, se estiverem conectadas na sessão | evidência de binário, APK, firmware, Electron |
| Navegador | só leitura, só o que a página entrega ao público | estrutura, scripts, chamadas de rede |
| Documentação e changelog oficiais | link | o que o fabricante promete (a comparar com o observado) |

## Peso por domínio (autoridade)

Herdado do motor do Conclave (`authority_rank`). Menor é mais forte.
- **0, acadêmico:** doi.org, arXiv, PubMed, OpenAlex, Semantic Scholar, SciELO, periódicos e `.edu`.
- **1, institucional:** `.gov`, `.int`, organismos multilaterais, e as bases oficiais de flora (JBRJ, GBIF).
- **2, o resto:** imprensa, blog, rede social. Serve como objeto ou pista, raramente como prova.
