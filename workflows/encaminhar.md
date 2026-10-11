# 6. Encaminhar

A desmontagem termina no dossiê. Quando a intenção pede mais, a skill passa o dossiê para quem constrói.

## Para quem vai

| Intenção ou objeto | Skill | O que leva |
|---|---|---|
| modo publicar | `nei` | o dossiê; o texto sai na voz do Nei e volta para `desmontar validar` |
| criar uma skill | `meta-skill` | a seção "Da desmontagem ao projeto" como briefing |
| criar um mod do Claude Code | `plugin-authoring` | idem |
| criar uma landing page | `random-lp-ultra` | idem, mais as referências visuais conferidas |
| criar um plano de marketing | `random-planner-ultra` | idem, mais os números com rótulo |
| criar uma interface | `impeccable` ou `conclave-design` | idem |
| binário, APK, firmware | `reverse-engineer-anything` (REA), se instalado | o artefato e a pergunta |
| portão de risco disparado | decisão humana | o dossiê com a seção "Limites e riscos" |

## Regras do modo criar projeto

- **Reimplementar a partir do entendimento:** o projeto novo nasce do mapa das partes, nunca da cópia do objeto.
- **"Não copiar" é seção obrigatória:** marca, código, texto e imagem protegidos ficam listados ali.
- **Licença de cada parte reaproveitada:** MIT e Apache permitem com atribuição; licença própria ou sem licença
  exige ler o arquivo, e na dúvida não se usa.
- **Primeiros passos:** o menor projeto que prova a ideia. Sem cronograma inventado.

## Saída

O dossiê fica em `~/Documents/desmontar/dossies/`. A skill construtora recebe o caminho e a seção do projeto.
Nada é publicado, commitado ou enviado sem o OK do Nei.
