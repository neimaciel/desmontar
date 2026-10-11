# 2. Transmutar a lente

A lente se adapta ao que foi reconhecido. Ninguém escolhe domínio numa lista.

## Passos

1. **Busque a lente mais específica:**
   ```bash
   desmontar lentes escolher <natureza> <area>
   ```
   A ordem é:
   - lente aprendida, da biblioteca em `~/Documents/desmontar/lentes/`;
   - lente-semente, em `lentes-semente/`;
   - o modelo em branco, `templates/lente.md`.

   O comando diz qual veio e de onde.
2. **Se veio o modelo:** componha a lente nova pelos sete genes de `lib/genoma-da-lente.md`.
   - Os eixos saem da natureza, e o padrão de evidência sai da área.
   - Fontes canônicas só entram depois de abertas: `desmontar lentes checar <arquivo> --links`.
3. **Se a lente é híbrida:**
   - **eixos:** a união dos eixos úteis;
   - **padrão de evidência:** o mais exigente dos dois;
   - **portões:** todos os das duas.
4. **Ajuste à intenção:** a entrega muda conforme a intenção (tabela do genoma), e os eixos não mudam.
5. **Teste de especialista:** as três perguntas do genoma. Corrija a lente antes de usar.

## Portão para seguir

A lente tem os sete genes preenchidos e passa em `desmontar lentes checar`.

## Saída

A seção "Lente usada" do dossiê precisa trazer:
- id, versão e origem;
- os eixos em uma linha;
- as respostas do teste de especialista.

Guarde o rascunho da lente nova junto do dossiê. Ele vira versão na etapa `workflows/aprender.md`.
Siga para `workflows/desmontar.md`.
