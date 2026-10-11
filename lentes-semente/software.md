---
id: sistema-digital/software
natureza: sistema-digital
area: software
versao: 1
origem: semente
rigor: padrao
portoes: seguranca, pi, dados-pessoais
criada: 2026-10-10
atualizada: 2026-10-10
---
# Lente: sistema digital × software

## Eixos de desmontagem
- **O que resolve:** problema, usuário, e o caminho da entrada até a saída.
- **Como resolve:** arquitetura, módulos, fluxo de dados, algoritmos, formatos, protocolos.
- **Onde roda:** plataforma, dependências, infraestrutura, terceiros chamados.
- **Estado e dados:** o que guarda, onde, por quanto tempo, e de quem.
- **Interfaces:** API, eventos, rotas, comunicação entre processos.
- **Fronteiras:** limites, tratamento de erro, segurança, o que muda entre versões.

## Padrão de evidência
1. Comportamento observado em execução: rede, logs, tela. Vale para o próprio sistema, ou para um analisado com autorização.
2. Artefato inspecionado: código-fonte, pacote, ou binário via REA.
3. Documentação oficial e changelog.
4. Issues e discussões do próprio projeto.
5. Post de terceiros: é hipótese.

A análise estática nunca prova execução: ler o código mostra o que ele pode fazer, e não o que fez.

## Fontes canônicas
- O próprio artefato: código, pacote, página. É evidência [observado].
- Repositório e documentação oficiais do projeto.
- REA, para binário, APK, firmware e Electron, quando as ferramentas dele estiverem conectadas: https://github.com/morluto/rea

## Perguntas de desmontagem
1. Qual é a feature, em uma frase, e qual o caminho dela da entrada até a saída?
2. Que chamadas de rede e que arquivos ela usa?
3. De que dependências e terceiros ela depende?
4. Onde guarda dados, e quais?
5. O que a documentação promete que o comportamento observado não confirma?
6. O que dá para observar sem contornar nenhuma proteção?

## Armadilhas
- Deduzir comportamento só por nome de arquivo, string ou estrutura de pastas.
- Tratar a leitura estática como se fosse execução.
- Analisar uma versão diferente da que está em produção.
- Código minificado ou ofuscado enganando a leitura.
- Atribuir ao site chamadas que são do navegador ou de uma extensão.

## Portões de risco
- **`seguranca`:** só o que é público, próprio ou autorizado; nunca contornar proteção, licença ou DRM.
- **`pi`:** no modo criar projeto, reimplementar a partir do entendimento, sem copiar código protegido.
- **`dados-pessoais`:** dado de usuário que aparecer fica fora do dossiê.

## Entrega
- **Mapa de arquitetura:** as partes e o fluxo entre elas.
- **A trilha de uma feature.**
- **A lista de terceiros e de dados.**
- **No modo criar projeto,** a planta de uma reimplementação limpa.
