# Rótulos de evidência

Toda afirmação do dossiê começa com um destes quatro rótulos. São os mesmos registros que já
aparecem em outros lugares:
- o REA separa observação, inferência e desconhecido;
- o curso-45 separa o objeto, os especialistas e a minha inferência;
- as pesquisas do Nei marcam "não verificado".

| Rótulo | Quando usar | Formato obrigatório |
|---|---|---|
| `[observado]` | está no próprio objeto: no texto, na foto, no código ou na página | `[observado] ... (onde: p. 4, 2º parágrafo)` |
| `[citado]` | vem de fonte externa da lista "Fontes", que passou em `desmontar conferir` | `[citado] ... [F2]` |
| `[inferido]` | raciocínio a partir de observados e citados | `[inferido] ... (de: A1 + F2)` |
| `[desconhecido]` | não dá para afirmar com o que existe | `[desconhecido] ... (resolveria: ...)` |

## Regras

1. **Rótulo não sobe sozinho.** Um [inferido] só vira [citado] quando aparece a fonte que diz aquilo.
2. **Fonte que falhou derruba o rótulo.** Se `desmontar conferir` reprovou a [F2], toda afirmação que dependia dela
   vira [inferido] (com a cadeia) ou [desconhecido]. Nunca fica [citado] apontando para fonte quebrada.
3. **Memória não é citação.** "Lembro que o estudo dizia" é [inferido], no máximo. Citado é o que foi aberto e lido.
4. **Observar é olhar, não supor.** "A folha tem margem serrilhada" é [observado]. "Então é da família X" é
   [inferido], com `(de: ...)`.
5. **Estático não prova execução.** Ler o código mostra o que ele pode fazer ([observado] no código). O que
   ele faz quando roda só é [observado] com execução ou captura.
6. **Conclusão no modo publicar só usa [observado] e [citado].** Inferência entra no corpo, marcada, e nunca
   como conclusão.

## Numeração

- Afirmações: A1, A2... (para a cadeia do [inferido] apontar).
- Fontes: F1, F2... na seção "Fontes", cada uma com DOI, arXiv ou link, e a data de conferência.
- Artigo retratado: a linha da fonte diz **RETRATADO**, e ele só serve como objeto, nunca como prova.
