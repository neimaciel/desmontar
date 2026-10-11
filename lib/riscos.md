# Portões de risco

Cada lente lista, no cabeçalho, os portões que se aplicam (`portoes: saude, pi`). Quando um portão
dispara, a skill faz o que a coluna "O que fazer" manda, mesmo que o pedido diga outra coisa.
Uma lente nunca perde um portão ao ganhar versão nova.

| Id | Dispara quando | O que fazer | O que devolver |
|---|---|---|---|
| `saude` | comer, beber, chá, remédio, dose, toxicidade, sintoma, tratamento | nunca certificar comestível, seguro, tóxico ou eficaz; listar as espécies parecidas perigosas quando houver | "Identificação não substitui especialista" e quem procurar: micólogo, botânico, médico, centro de toxicologia (CIATox) |
| `juridico` | contrato, lei, processo, direito, obrigação | informar o que o texto diz, com rótulos; não decidir nem recomendar conduta | a pergunta jurídica em aberto, para um advogado |
| `financeiro` | investimento, compra ou venda de ativo, crédito, preço justo | informar o mecanismo e os números conferidos; não recomendar operação | as premissas que mudam a decisão, para quem decide |
| `seguranca` | software ou sistema de terceiros, acesso, proteção, licença, DRM | só o que é público ou próprio, ou com autorização expressa; nunca contornar proteção | o que daria para saber com autorização, e de quem pedir |
| `dados-pessoais` | nome, CPF, e-mail, telefone, foto de pessoa, dado de cliente | minimizar; no modo cliente, o dossiê fica só na máquina; não publicar | o dossiê sem os dados ou com eles mascarados |
| `pi` | criar projeto a partir de algo de terceiros | reimplementar a partir do entendimento; não copiar marca, código, texto ou imagem protegidos; checar a licença | a seção "Não copiar" e a licença de cada parte |

## Regra de desempate

Na dúvida entre dois portões, valem os dois. Na dúvida se um portão se aplica, ele se aplica.
Se a área foi reconhecida com confiança abaixo de `classificacao.confianca_minima` (`lib/limiares.json`)
e há qualquer portão, a skill faz uma pergunta antes de seguir.
