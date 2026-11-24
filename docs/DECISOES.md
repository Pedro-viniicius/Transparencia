# Decisões (ADRs)

## ADR-001 — Chatwoot + Evolution API, sem código próprio no caminho das mensagens
**Contexto:** 2 números, 1 Instagram, 6 pessoas, orçamento apertado (custo mensal baixo é requisito).
**Decisão:** Chatwoot (painel, sem cobrança por atendente) e Evolution API (WhatsApp por QR,
com integração nativa ao Chatwoot). Roteamento com recursos nativos: membros de caixa, equipes,
saudação da caixa e regras de automação. Nosso código só configura e testa.
**Consequências:** nada para manter no caminho crítico; atualização = trocar a tag da imagem.
A conexão por QR não é a API oficial: risco de bloqueio se houver disparo em massa.

## ADR-002 — Separação por loja = uma caixa de entrada por número
**Contexto:** "dois muito separados"; funcionária de uma loja não deve ver a outra.
**Decisão:** cada número é uma caixa; só as atendentes da loja (e os donos) são membros.
Equipes por loja servem para relatório e para o menu do Instagram.
**Consequências:** separação garantida pelo controle de acesso do Chatwoot, conferida no teste.

## ADR-003 — Liberar rede privada para os webhooks do Chatwoot
**Contexto:** o Chatwoot 4.19 recusa webhooks para IP privado ("no public ip addresses"), e o
Evolution fica na rede interna do Docker. Sem isso, as respostas do painel não saíam.
**Decisão:** `SAFE_FETCH_ALLOW_PRIVATE_NETWORK=true`.
**Consequências:** um administrador poderia apontar webhook para a rede interna. Aceitável:
só o responsável técnico e os donos são administradores, e as portas só escutam em 127.0.0.1.

## ADR-004 — Contato-robô do Evolution desligado
**Contexto:** com `CHATWOOT_BOT_CONTACT=true` o QR Code aparecia como conversa na caixa da loja,
visível às atendentes. Escanear com o celular pessoal ligaria o WhatsApp pessoal à loja.
**Decisão:** desligado; conectar/reconectar só com a apikey, pela Central do Atendimento
(ADR-009) ou pelo `/manager`.
**Consequências:** reconexão depende do responsável técnico ou do dono.

## ADR-005 — Menu do Instagram só age em conversa sem equipe
**Contexto:** cliente pode digitar "1" no meio de uma conversa.
**Decisão:** regras de `message_created` com `team_id is_not_present` + conteúdo exatamente "1"/"2".
**Consequências:** depois de escolhida a loja, números digitados não mudam nada (testado).
Se o cliente escrever outra coisa, a conversa fica sem equipe e os donos/atendentes atendem.

## ADR-006 — Endereço único `chatwoot.localhost:3000`
**Contexto:** o navegador usa 127.0.0.1 e o Evolution usa a rede do Docker; anexos enviados pelo
painel são baixados pelo Evolution pela URL do Chatwoot.
**Decisão:** `FRONTEND_URL=http://chatwoot.localhost:3000` e alias de rede com o mesmo nome.
**Consequências:** no servidor, `FRONTEND_URL` vira o domínio com HTTPS.

## ADR-007 — Saudação do WhatsApp pela automação, não pela saudação nativa da caixa
**Contexto:** no teste real (24/11) a saudação nativa (mensagem "template") era reenviada pelo
Evolution e regravada como mensagem nova: o cliente recebia uma, o painel mostrava duas.
**Decisão:** nas caixas de WhatsApp a saudação é a ação `send_message` de uma regra de
`message_created` (mensagem recebida + conversa sem equipe), que também atribui a equipe; a
saudação nativa fica desligada. O Instagram (canal nativo) segue com a nativa.
Primeiro a regra era de `conversation_created`, mas no teste real da Loja da Praça ela rodou
antes de a mensagem do cliente existir e o Evolution não enviou a saudação (corrida de tempo).
Com `message_created` ela sempre vem depois da mensagem do cliente.
**Consequências:** sai pelo mesmo caminho das respostas dos atendentes, que não duplicam.
Confirmado com WhatsApp real em 24/11 (chip de teste) nas duas lojas: saudação uma vez só, entregue e lida; a 2ª mensagem não gera outra.

## ADR-008 — Grupos ignorados e logs sem conteúdo de mensagem
**Contexto:** no teste real, mensagens de grupos do número entraram no painel, e o log do
Evolution em nível INFO registrava o texto das mensagens.
**Decisão:** `groupsIgnore: true` em cada instância (aplicado pelo `configurar.py`);
`LOG_LEVEL: ERROR,WARN`.
**Consequências:** para depurar, subir o nível temporariamente e recriar o container depois.

## ADR-009 — Central do Atendimento (página da equipe) e marca do painel
**Contexto:** a equipe precisava saber dois endereços (painel e manager), não tinha como ver se
o número da loja estava conectado, e o QR do manager vencia antes de escanear (travou a conexão
no teste real). O painel mostrava a marca "Chatwoot".
**Decisão:** página estática em `portal/` servida por nginx (127.0.0.1:8090): botão do painel,
situação de cada número, guia rápido e área técnica com QR que se renova a cada 5 s. O nginx
expõe só três rotas: situação (lê o Evolution com a chave injetada, sem a página conhecê-la),
QR (exige a chave digitada) e saúde do painel. Marca do painel (nome, logos) e avatar das caixas
aplicados pelo `configurar.py` via `scripts/marca.rb`. Nada de fork do Chatwoot. Detalhes em
`docs/DESIGN.md`.
**Consequências:** quem abre a Central vê se os números estão conectados (não vê conversas nem
dados). A logo do painel vem da Central: no servidor, definir `PORTAL_URL` no `.env`.

## ADR-010 — Cores da Central no painel por CSS injetado
**Contexto:** a Central e o design system usam o azul da marca; o painel, onde a equipe passa o
dia, continuava com o azul padrão do Chatwoot.
**Decisão:** gerar `portal/painel-tema.css` a partir do CSS do próprio Chatwoot (só as regras
com o azul padrão, cor trocada por variáveis da marca) e injetar pela configuração
`DASHBOARD_SCRIPTS`. Sem fork, sem imagem própria, reversível apagando a configuração.
**Consequências:** a cada atualização do Chatwoot o tema precisa ser gerado de novo (classes
mudam); o teste avisa se o painel não estiver servindo o arquivo atual. Só a tela de redefinir senha
fica sem o tema (o Chatwoot não carrega scripts nela).

## Riscos observados no teste real
- **Mensagens duplicadas no painel** em algumas conversas do histórico copiado (mesmo ID do
  WhatsApp gravado duas vezes). Provável efeito dos identificadores novos do WhatsApp (LID)
  no Evolution 2.3.8. Conferir com o chip da loja; se repetir, testar versão mais nova.
- O histórico recente do chip entra no painel sem equipe atribuída (a regra só age em
  conversa criada depois da conexão).

## Pareamento instável (WhatsApp × Evolution 2.3.8)
Desde 28/07/2026 o WhatsApp envia `companion_reg_refresh` depois da leitura do QR, e o Baileys
7.0.0-rc.9 do Evolution 2.3.8 nem sempre conclui o pareamento: o celular mostra "Não foi
possível conectar novos dispositivos no momento". Correção proposta no PR #2727 (aberto, não
incorporado); acompanhamento na issue #2437. Na prática, em 24/11 falhou em vários aparelhos e
conectou numa tentativa seguinte. Quando sair versão com a correção, testar e atualizar a tag.
