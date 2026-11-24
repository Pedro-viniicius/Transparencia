# Kickoff — Atendimento das duas lojas (WhatsApp + Instagram)

Data: 24/11/2026. Decisão do PO: construir já, rodando neste computador; o servidor pago fica
para depois.

## Briefing (do áudio e das mensagens do cliente, 24/11)

- 2 números de WhatsApp, um por loja: **Loja de Baixo** e **Loja da Praça**, "dois muito separados".
- 1 Instagram.
- 6 pessoas: 4 funcionárias (2 por loja) + o dono e a esposa, que acompanham tudo.
- Custo mensal baixo é requisito (por isso nada de licença por atendente).

## Premissas adotadas (confirmar com o cliente)

1. Cada funcionária só vê as conversas do número da loja dela.
2. Dono e esposa são administradores: veem as duas lojas, o Instagram e os relatórios.
3. Instagram é compartilhado: as 6 pessoas veem; uma resposta automática pergunta a loja e
   manda a conversa para a equipe certa.
4. Nomes e e-mails reais das 6 pessoas ainda não vieram: usamos e-mails provisórios
   `@lojas.local` (trocar antes de entregar).
5. Horário de atendimento ainda não veio: mensagem de boas-vindas sem horário.

## Equipe

**🏛️ Arq:** Chatwoot (painel de atendimento, código aberto, sem cobrança por atendente) +
Evolution API (liga o WhatsApp pelo QR Code, como o WhatsApp Web, e já tem integração nativa
com o Chatwoot). Um Postgres e um Redis para os dois. Nada de código próprio no caminho
crítico: separação por loja = **caixa de entrada por número + membros da caixa**; roteamento =
**equipes + regras de automação** nativas. Reversível: o mesmo `docker-compose.yml` sobe num VPS.

**🎨 UX:** a funcionária abre o navegador, entra, e só vê a caixa da loja dela. Nada para
instalar. O casal vê tudo. Mensagem de boas-vindas curta, com o nome da loja. No Instagram,
menu de 2 opções (1 Loja de Baixo, 2 Loja da Praça), porque quem escreve ali não sabe qual
número cuida de quê.

**💻 Dev:** tudo por script idempotente (`scripts/`): subir, preparar o banco, criar conta,
pessoas, equipes, caixas e automações pela API do Chatwoot, criar as instâncias no Evolution
com a integração já apontada. Segredos gerados no `.env` (fora do Git).

**⚙️ DevOps:** local agora (custo R$ 0), portas só em 127.0.0.1. Imagens com versão fixa
(Chatwoot v4.19.1-ce, Evolution v2.3.8). Para migrar: copiar a pasta, trocar `FRONTEND_URL`
por um domínio com HTTPS e restaurar o backup do Postgres. VPS estimado: 2 vCPU / 4 GB.

**🧪 QA:** o WhatsApp real depende dos chips do cliente (QR Code). Para testar ponta a ponta
sem eles, simulamos mensagens recebidas nas mesmas caixas pela API do Chatwoot e conferimos:
boas-vindas, equipe atribuída, quem enxerga a conversa. O Instagram não pode ser ligado
localmente: precisa de HTTPS público e do login do cliente na Meta.

### Pontos de discordância

- **DevOps × Arq:** a conexão por QR Code (não oficial) pode ser bloqueada se houver envio em
  massa. Mitigação: chips só para atendimento, sem disparos (regra de uso combinada com a loja).
- **QA × UX:** o menu do Instagram pode reatribuir se o cliente digitar "1" no meio da conversa.
  Mitigação: a regra só age em conversa ainda sem equipe.

## Definition of Done

- [ ] `scripts/subir.sh` sobe tudo do zero e é idempotente.
- [ ] 6 pessoas criadas com o papel certo; funcionária de uma loja não vê a outra.
- [ ] 2 caixas de WhatsApp ligadas a instâncias do Evolution (QR pronto para escanear).
- [ ] Boas-vindas e atribuição de equipe funcionando nas mensagens recebidas (teste simulado).
- [ ] Menu do Instagram pronto e testado numa caixa de simulação.
- [ ] Passo a passo para escanear o QR, ligar o Instagram e migrar para servidor.
