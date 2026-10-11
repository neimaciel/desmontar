# 5. Aprender

A lente melhora a cada uso, sozinha e com travas. A biblioteca fica fora da skill, em
`~/Documents/desmontar/lentes/<natureza>/<area>/`: `lente.md`, `historico/` e `usos.jsonl`.

## Passos

1. **Pergunte o que a lente não previa neste uso:**
   - uma armadilha nova;
   - uma fonte canônica que funcionou;
   - uma pergunta que faltou;
   - um portão que apareceu;
   - um eixo que precisou ser criado.
2. **Escreva a versão nova** a partir da atual (ou do rascunho, se a lente nasceu agora). Ela tem que seguir três regras:
   - **só acrescenta ou refina**, e nunca remove portão nem rebaixa o rigor;
   - **nunca copia texto do objeto analisado:** a lente fala da área, nunca do caso;
   - **só traz fonte cujo link foi aberto.**
3. **Grave:**
   ```bash
   desmontar lentes gravar <lente-nova.md> --dossie <dossie>
   ```
   As travas rodam lá:
   - o dossiê precisa passar no validador e usar esta lente;
   - os portões não podem diminuir;
   - o rigor não pode baixar;
   - as listas de armadilhas, evidências, fontes e perguntas não podem encolher;
   - padrões de injeção e segredos são recusados;
   - os links são abertos.
4. **Se recusar:** leia o motivo e corrija. A versão anterior continua valendo.

## Voltar atrás

```bash
desmontar lentes historico <natureza>/<area>
desmontar lentes voltar <natureza>/<area> <versao>
```

A volta vira uma versão nova, registrada em `usos.jsonl`. Nada se apaga.

Siga para `workflows/encaminhar.md` quando a intenção for publicar ou criar projeto.
