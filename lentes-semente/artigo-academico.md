---
id: texto-argumento/artigo-academico
natureza: texto-argumento
area: artigo-academico
versao: 1
origem: semente
rigor: alto
portoes:
criada: 2026-10-10
atualizada: 2026-10-10
---
# Lente: texto-argumento × artigo acadêmico

## Eixos de desmontagem
- **Pergunta e hipótese:** o que o artigo quer saber, nas palavras dele.
- **Desenho:** experimento, ensaio clínico, coorte, caso-controle, transversal, qualitativo, revisão, teórico ou simulação.
- **Amostra:** tamanho (n), como foi recrutada, que população representa.
- **Medidas e análise:** variáveis, instrumentos, testes, correção para múltiplas comparações, pré-registro.
- **Resultados:** tamanho do efeito com intervalo, e não só o valor de p.
- **Tese × dados (a garantia, no modelo de Toulmin):** o que a conclusão afirma e o que os dados de fato sustentam.
- **Ressalvas e refutações:** limitações declaradas, réplicas, correções, retratação.

## Padrão de evidência
1. Revisão sistemática ou meta-análise de boa qualidade.
2. Ensaio clínico randomizado, ou experimento controlado com replicação independente.
3. Coorte, depois caso-controle, depois transversal.
4. Série de casos, opinião de especialista.

Ajustes da área:
- em computação e física, dados e código abertos e replicação independente pesam mais que o tipo de desenho;
- pré-registro sobe a confiança;
- preprint vale como hipótese ainda não revisada;
- **artigo retratado não é evidência de nada**, só objeto de análise.

## Fontes canônicas
- Crossref, que traz a retratação pela base Retraction Watch: https://api.crossref.org/
- OpenAlex, com o campo `is_retracted` e as citações: https://api.openalex.org/
- PubMed, para biomedicina: https://pubmed.ncbi.nlm.nih.gov/
- arXiv, para preprints: https://arxiv.org/

## Perguntas de desmontagem
1. Qual é a pergunta exata e que resposta o artigo dá?
2. O desenho permite a conclusão causal que o título e o resumo sugerem?
3. Qual o n e o tamanho do efeito, com intervalo?
4. Houve pré-registro? Os dados e o código estão abertos?
5. Quem financiou, e há conflito de interesse declarado?
6. Foi replicado, contestado, corrigido ou retratado?
7. O que a conclusão afirma além do que os dados mostram?

## Armadilhas
- Título e resumo prometem mais que os resultados (spin).
- P-hacking e múltiplas comparações sem correção.
- Amostra pequena ou de uma população só, generalizada para todos.
- Correlação apresentada como causa.
- Preprint citado como se tivesse sido revisado.
- Artigo retratado que continua sendo citado.
- Revista predatória.
- Citar o resumo sem ler o método.

## Portões de risco
`saude` quando o artigo for biomédico ou de nutrição: o dossiê nunca recomenda tratamento, dieta ou dose.

## Entrega
- **Ficha do artigo:** pergunta, desenho, n, efeito, conclusão e status (revisado, preprint, corrigido ou retratado).
- **Tabela "o que o artigo afirma × o que os dados sustentam".**
- **Veredito por afirmação:** sustentada, sustentada em parte, não sustentada ou sem evidência.
