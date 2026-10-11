# Desmontar

Engenharia reversa de qualquer coisa, com evidência: um conceito, um artigo acadêmico, uma planta,
um software, um processo, uma obra.

## O que você recebe

- **Uma lente que se transforma sozinha.** A skill lê o objeto e reconhece a área, e só então monta a
  lente: os eixos de desmontagem, o que conta como prova naquela área, as fontes canônicas, as
  armadilhas e os riscos.
- **Um dossiê em que nada fica sem origem.** Toda afirmação diz se foi observada no objeto, citada de
  uma fonte conferida por programa, inferida (com a cadeia) ou se é desconhecida.
- **Fontes conferidas de verdade.** DOI resolvido no Crossref e no OpenAlex, artigo retratado
  marcado, link aberto, paywall e página bloqueada sinalizados.
- **Lentes que aprendem.** Cada desmontagem aprovada pode refinar a lente da área. As travas impedem
  que ela exija menos ou que um texto analisado vire instrução.
- **Ponte para construir.** No modo projeto, o dossiê vira a planta de um projeto novo e segue para a
  skill construtora certa.

## Como a lente se transforma

> **Lente = natureza × área × intenção**

| Leitura | Decide | Exemplo |
|---|---|---|
| Natureza | os eixos de desmontagem | ser vivo: as quatro perguntas de Tinbergen |
| Área | o padrão de prova | botânica: exsicata e flora oficial valem mais que app de foto |
| Intenção | a forma da entrega | verificar: veredito por afirmação |

Quatro lentes já vêm prontas: conceito, artigo acadêmico, botânica e software. As outras nascem
na hora, a partir do genoma, e ficam guardadas em `~/Documents/desmontar/lentes/`.

## Instalação por modelo de IA

| Modelo | Como instalar |
|---|---|
| Claude Code | copie a pasta para `~/.claude/skills/desmontar`, rode `pip install -e ~/.claude/skills/desmontar/scripts` e acione `/desmontar <objeto>` |
| Claude.ai e Claude Desktop | crie um Projeto e envie `SKILL.md`, `lib/`, `workflows/`, `lentes-semente/` e `templates/` como conhecimento |
| Cursor e Windsurf | `.cursor/rules/desmontar.mdc` com o conteúdo do `SKILL.md`, e a pasta no repositório |
| Codex CLI | referencie o `SKILL.md` no `AGENTS.md` do projeto |
| Gemini CLI | referencie o `SKILL.md` no `GEMINI.md` |
| ChatGPT | GPT personalizado: `SKILL.md` nas instruções, as pastas como conhecimento e o `scripts/` no interpretador de código |

Fora do Claude Code, os comandos rodam com `python3 -m desmontar.cli` dentro de `scripts/`.

## Linha de comando

```bash
desmontar novo "efeito Dunning-Kruger" --intencao verificar --lente ideia/conceito
desmontar conferir ~/Documents/desmontar/dossies/<arquivo>.md --modo publicar
desmontar validar  ~/Documents/desmontar/dossies/<arquivo>.md
desmontar lentes listar
desmontar lentes gravar lente-nova.md --dossie <dossie-aprovado>.md
desmontar lentes voltar ser-vivo/micologia 1
```

## Testes

```bash
pip install -e "scripts[dev]" && pytest -q scripts/tests
```

Só biblioteca padrão do Python. Os testes usam dados gerados e uma rede de mentira.

## Licença

MIT.
