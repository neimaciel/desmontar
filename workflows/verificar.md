# 4. Verificar

O dossiê só está pronto quando as fontes foram abertas por um programa, e não só pela memória de quem escreveu.

## Passos

1. **Confira as fontes:**
   ```bash
   desmontar conferir <dossie> --modo <modo>
   ```
   O comando:
   - resolve cada DOI no Crossref e no OpenAlex;
   - confere o título e a retratação;
   - abre os links e marca página quebrada, paywall ou página fina;
   - mostra o peso de cada domínio.
2. **Fonte que falhou:**
   - troque por outra fonte conferida, ou
   - rebaixe as afirmações que dependiam dela para [inferido] ou [desconhecido] (`lib/rotulos.md`, regra 2).
3. **Artigo retratado:** a linha da fonte precisa dizer RETRATADO. Afirmação que dependia dele como prova cai.
4. **Valide a estrutura:**
   ```bash
   desmontar validar <dossie> --modo <modo>
   ```
   Repita até zero erros. Avisos se leem um a um: cada um ou se corrige, ou se explica em "Limites e riscos".
5. **Modo publicar:** passe o texto que vai sair pela skill `nei` e rode `desmontar validar` de novo. A voz não pode trazer travessão nem transformar inferência em fato.

## Portão para seguir

`conferir` e `validar` sem erro. Siga para `workflows/aprender.md`.
