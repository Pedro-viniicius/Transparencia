# Operação

## Conectar (ou reconectar) um número de WhatsApp

Quem faz: o responsável técnico ou o dono. **Nunca** escanear com um celular pessoal: o WhatsApp que escanear
vira o número da loja no painel. No teste de 24/11 um número pessoal foi escaneado e, em
segundos, o WhatsApp copiou o histórico recente (milhares de mensagens e contatos) para o
sistema, e qualquer pessoa nova que escrevesse receberia a saudação da loja. Foi tudo apagado
(ver "Desfazer uma conexão errada" abaixo).

Ao conectar o chip da loja, o histórico recente dele também entra no painel. Grupos são
ignorados (configurado pelo `scripts/configurar.py`).

1. No celular com o chip da loja, abra o WhatsApp (de preferência WhatsApp Business) já ativado.
2. No computador, abra a **Central do Atendimento** (http://127.0.0.1:8090) → **Área técnica**,
   escolha a loja, cole a `apikey` de `credenciais.txt` e clique em **Gerar QR Code**.
   (Alternativa: http://127.0.0.1:8080/manager → instância → engrenagem → **Get QR Code**.)
3. No celular: **Configurações → Aparelhos conectados → Conectar aparelho** e escaneie.
4. A Central mostra **Conectado** (no manager, o status muda para **Open**). Mande uma
   mensagem de outro celular para o número da loja: ela aparece no painel na caixa da loja, com a boas-vindas e a equipe certa.

Na Central o QR se renova a cada 5 s, por até 3 minutos, e para sozinho quando conecta. Se o
número já estiver conectado, a Central avisa e não gera QR (desconecte antes para trocar de chip).
O celular da loja pode ficar parado no carregador, com internet.

Ordem segura (adotada depois do teste de 24/11):
1. Antes de escanear, desligar as automações das caixas de WhatsApp (painel → Configurações →
   Automação), para ninguém receber a saudação se o número errado for conectado.
2. Escanear e conferir no `/manager` o número conectado e o volume de conversas importadas.
3. Número certo → `python3 scripts/configurar.py` religa as automações.

Se o celular disser **"Não foi possível conectar novos dispositivos no momento, tente novamente
mais tarde"**, o bloqueio é do próprio WhatsApp (comum em chip recém-ativado ou depois de várias
tentativas) ou da falha conhecida de pareamento do Evolution 2.3.8 (ver DECISOES.md). Tentar
mais algumas vezes, com QR recém-gerado (a Central já renova sozinha; o do manager vence em
~20 s). Se persistir, esperar algumas horas.

Cuidados (conexão não oficial, pelo QR): nada de envio em massa nem mensagem para quem não
chamou a loja. Isso é o que leva o WhatsApp a bloquear números.

## Desfazer uma conexão errada (número errado escaneado)

1. Desligar as automações das caixas de WhatsApp (painel → Configurações → Automação), para
   ninguém receber a saudação.
2. Apagar a instância no `/manager` (Delete) ou `DELETE /instance/delete/<nome>`: some a sessão
   e tudo o que o Evolution guardou (mensagens, contatos, conversas).
3. No painel, apagar as conversas e contatos copiados para a caixa.
4. `docker compose exec -T postgres psql -U postgres -d evolution -c 'VACUUM FULL;'` (idem
   `chatwoot`) e `docker compose up -d --force-recreate evolution chatwoot sidekiq` (zera os logs).
5. `scripts/subir.sh` recria a instância vazia e religa as automações.

## Ligar o Instagram (só com servidor)

O Instagram exige endereço público com HTTPS para receber as mensagens. No servidor:

1. Criar um app na Meta (developers.facebook.com) com o produto Instagram e as permissões de
   mensagens; conta do Instagram como **Profissional**.
2. Pôr no `.env` as chaves do app (`INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET`,
   `INSTAGRAM_VERIFY_TOKEN`) e apontar o webhook do app para `https://<domínio>/webhooks/instagram`.
   Conferir os nomes exatos na documentação do Chatwoot da versão instalada.
3. No painel: Configurações → Caixas de entrada → Adicionar → Instagram, login com a conta da loja.
4. Rodar `scripts/subir.sh`: o menu "1 Loja de Baixo / 2 Loja da Praça" passa a valer para a
   caixa real. Apagar a caixa "Teste · Instagram (simulação)".

## Migrar para o servidor

Servidor sugerido: 2 vCPU, 4 GB de RAM, Linux com Docker.

1. Aqui: `scripts/backup.sh`.
2. No servidor: copiar a pasta do projeto e o backup; restaurar o `.env` do backup.
3. Trocar no `.env`: `FRONTEND_URL=https://<domínio>`; pôr um proxy com HTTPS (Caddy ou Nginx)
   na frente das portas 3000 (painel) e 8080 (manager, só com acesso restrito).
   A Central (porta 8090) também só com acesso restrito; definir `PORTAL_URL=https://<endereço
   da Central>` no `.env` (a logo do painel vem dela) e trocar o link do botão do painel em
   `portal/index.html` (`id="abrir-painel"`).
4. `docker compose up -d postgres redis`, depois restaurar:
   `docker compose exec -T postgres pg_restore -U postgres -d chatwoot --clean < chatwoot.dump`
   (idem `evolution`), e as sessões:
   `docker compose run --rm -T evolution tar -C /evolution -xzf - < evolution-instances.tgz`.
5. `scripts/subir.sh`. Se a sessão do WhatsApp não voltar, reconectar pelo QR (acima).
   A URL interna que o Evolution usa (`http://chatwoot.localhost:3000`) não muda.

## Rotina

- Backup: `scripts/backup.sh` (no servidor, agendar diário e copiar para fora da máquina).
- Saúde: abrir a Central (http://127.0.0.1:8090): mostra o painel e os dois números. Pelo
  terminal: `curl http://127.0.0.1:3000/api` e `curl http://127.0.0.1:8080/`.
- Logs: `docker compose logs -f evolution` / `chatwoot` / `sidekiq`.
- Atualizar versões: rodar `scripts/backup.sh`, trocar a tag no `docker-compose.yml` e
  rodar `scripts/subir.sh` (que termina com o teste).
