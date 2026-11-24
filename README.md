# Atendimento das lojas — WhatsApp + Instagram num painel só

Duas lojas (**Loja de Baixo** e **Loja da Praça**), um número de WhatsApp para cada, um Instagram,
6 pessoas. Cada funcionária vê só a loja dela; o dono e a esposa veem tudo.

Roda neste computador com Docker (custo R$ 0). O servidor pago fica para depois: a mesma pasta
sobe num VPS (ver `docs/OPERACAO.md`).

| O quê | Onde |
|---|---|
| **Central do Atendimento** (página da equipe) | http://127.0.0.1:8090 |
| Painel (Chatwoot 4.19.1) | http://chatwoot.localhost:3000 |
| Conectar números (Evolution API 2.3.8) | http://127.0.0.1:8080/manager |
| Senhas | `credenciais.txt` (gerado; fora do Git) |
| Segredos | `.env` (gerado; fora do Git) |

## Comandos

```bash
scripts/subir.sh     # sobe tudo, aplica a configuração e roda o teste (idempotente)
scripts/testar.py    # só o teste ponta a ponta (30 verificações, apaga o que cria)
scripts/backup.sh    # bancos + sessões do WhatsApp + anexos, em backups/
docker compose down  # desliga (os dados ficam nos volumes)
```

## Como está configurado

| | WhatsApp · Loja de Baixo | WhatsApp · Loja da Praça | Instagram |
|---|---|---|---|
| Quem vê | dono, esposa, 2 atendentes da loja | dono, esposa, 2 atendentes da loja | as 6 pessoas |
| Resposta automática | "Olá! 😊 Obrigado por falar com a Loja de Baixo…" | idem, Loja da Praça | menu: 1 Loja de Baixo · 2 Loja da Praça |
| Equipe | Loja de Baixo | Loja da Praça | a que o cliente escolher |

- A separação é feita pelos **membros de cada caixa de entrada**: atendente que não é membro não
  enxerga a conversa (conferido pelo teste, pessoa por pessoa).
- A distribuição automática só entrega conversa para quem está **online** no painel.
- As respostas saem no WhatsApp assinadas com o nome de quem respondeu.
- O Instagram ainda não está ligado (precisa de servidor com HTTPS). Até lá existe a caixa
  **"Teste · Instagram (simulação)"**, usada só para testar o menu.

## Central do Atendimento e identidade visual

A Central é a porta de entrada da equipe: botão do painel, situação de cada número
(atualiza a cada 15 s), guia rápido para as atendentes e uma área técnica que gera o QR Code
de conexão (pede a chave; o QR se renova sozinho). O painel usa o nome **Atendimento das
Lojas**, com a logo da Central, e cada caixa tem um avatar na cor da loja (verde-azulado para a
Loja de Baixo, âmbar para a Loja da Praça). O painel de conversas também ganhou as cores da
Central (azul da marca nos botões, abas, links e balões, fundo claro azulado, foco visível), por
CSS injetado, sem mexer no código do Chatwoot. Nada do funcionamento mudou. Detalhes e tokens de
design em `docs/DESIGN.md`.

## Teste com WhatsApp real (24/11, chip de teste)

Nas duas lojas: mensagem chega na caixa certa, saudação única entregue e lida, equipe atribuída,
resposta do painel entregue e lida, a outra loja não acessa a conversa (HTTP 401). Nenhuma
conversa de grupo entrou depois de ligado o `groupsIgnore` (não houve teste dedicado com
mensagem de grupo).
O chip de teste ficou conectado na **Loja da Praça**; a Loja de Baixo está desconectada.

## Pendências (dependem do cliente ou do servidor)

1. **Nomes e e-mails reais** das 6 pessoas: hoje são provisórios (`@lojas.local`). Trocar em
   `scripts/configurar.py` (lista `PESSOAS`) e rodar `scripts/subir.sh`.
2. **Escanear o QR Code** de cada número com o chip da loja (passo a passo em `docs/OPERACAO.md`).
3. **Instagram**: só no servidor (HTTPS público + app da Meta).
4. Horário de atendimento e textos finais das mensagens automáticas.

Decisões técnicas: `docs/DECISOES.md`. Kickoff da equipe: `docs/KICKOFF.md`. Design: `docs/DESIGN.md`.
