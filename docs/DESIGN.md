# Design — melhoria geral sem mudar o funcionamento

Data: 24/11/2026. Regra do PO: **não mudar o que já funciona** (caixas, equipes, regras,
mensagens automáticas, permissões). Só aparência, organização e facilidade de uso.

## Equipe

**🎨 UX:** o painel (Chatwoot) é de terceiros; não vamos fazer fork. Onde dá para mexer sem
risco: marca da instalação (nome, logo), avatar de cada caixa com a cor da loja e uma
**Central do Atendimento**: uma página de entrada simples para a equipe, com o botão do painel,
a situação de cada número e um guia rápido. Hoje a pessoa precisa saber dois endereços
(painel e manager) e o QR do manager vence antes de escanear: no teste real isso travou a
conexão. A Central resolve com um QR que se renova sozinho.

**🏛️ Arq:** a Central é estática (HTML/CSS/JS, sem framework) servida por um nginx na mesma
pilha Docker. O nginx faz proxy para o Evolution, então a página não precisa de CORS. A
situação dos números (só leitura) vem por uma rota em que o nginx injeta a chave; conectar
(QR) exige digitar a chave na página. Nada muda no Chatwoot além de configurações de marca.

**💻 Dev:** tokens de design em CSS (cores por loja, espaçamento, tipografia do sistema, modo
escuro). Avatares PNG gerados por script. Marca e avatares aplicados pelo `configurar.py`
(idempotente).

**🧪 QA:** checar contraste AA, foco visível, tela de celular (360 px), modo escuro, página
sem a chave (não pode expor QR), e o teste ponta a ponta continua passando sem mudança.

**⚙️ DevOps:** nginx com versão fixa, só em 127.0.0.1:8090. A chave do Evolution entra no
nginx por variável, nunca no HTML nem no Git.

## Identidade

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `--marca` | `#2453c7` | `#7d9cf0` | botões, links (combina com o azul do painel) |
| `--loja-baixa` | `#0f766e` | `#2dd4bf` | Loja de Baixo |
| `--loja-praca` | `#b45309` | `#fbbf24` | Loja da Praça |
| `--ok` / `--alerta` / `--erro` | verde / âmbar / vermelho | versões claras | situação do número |

Tipografia do sistema (sem fonte externa, funciona offline). Raio 14 px nos cartões, alvos de
toque ≥ 44 px.

Contraste conferido (WCAG AA, texto normal ≥ 4,5:1) em todos os pares de cor, nos dois temas:
o menor é o selo da Loja da Praça no tema claro (4,51:1).

## O que foi entregue

| Onde | O quê |
|---|---|
| `portal/` | Central do Atendimento: `index.html`, `estilo.css` (tokens), `app.js` (sem dependências), logos SVG |
| `portal/img/` | Avatares das caixas (256 px), gerados por `scripts/gerar_avatares.py` |
| `docker/nginx/templates/` | nginx da Central: arquivos estáticos + 3 rotas de API, CSP restrita |
| `scripts/marca.rb` | Nome e logos do painel e avatar de cada caixa (chamado pelo `configurar.py`) |
| `scripts/testar.py` | +5 verificações da Central (página, situação das 2 lojas, QR sem chave recusado, rotas fechadas) |

### Componentes da Central

- **Topo:** marca + selo "Painel no ar / fora do ar".
- **Entrada:** saudação e botão primário grande "Abrir o painel de conversas" (abre em outra aba).
- **Cartão de loja:** faixa lateral e selo (LB/LP) na cor da loja, nome, dica em linguagem
  simples e pílula de situação: Conectado (verde), Conectando (âmbar), Desconectado / Sem
  resposta (vermelho), Não criado (cinza). Região `aria-live` para leitores de tela.
- **Guia rápido:** 4 passos numerados + "O que o sistema faz sozinho".
- **Área técnica** (`<details>` fechado): aviso âmbar com os cuidados (só chip da loja; desligar
  automações), formulário loja + chave, QR que se renova a cada 5 s por até 3 min. Não gera QR
  se o número já está conectado; chave errada é apagada da aba e o foco volta ao campo.

### Estados e erros tratados

Painel fora do ar; Evolution sem resposta (timeout de 8 s); instância inexistente (404); chave
errada (401); número já conectado; tempo esgotado; aba escondida (não consulta em segundo
plano); `sessionStorage` indisponível; `prefers-reduced-motion`.

### QA visual (24/11)

Desktop 1920 px no tema escuro (Chrome), celular 360 px nos temas claro e escuro (Chrome
headless), login do painel com a marca nos dois temas. Sem rolagem horizontal. Defeito achado e
corrigido: o botão "Parar" aparecia apesar do atributo `hidden`, e o quadro do QR aparecia vazio
junto da mensagem de erro.

## Painel de conversas com as cores da Central

O Chatwoot pinta o azul dele (#2781f6) pelas variáveis `--blue-1..12` e por centenas de classes
com a cor escrita direto. `scripts/gerar_tema_painel.py` lê o CSS do Chatwoot que está rodando,
copia só as regras com esse azul (mesmos seletores, `@media` e `@supports`) e troca a cor por
variáveis da marca. O resultado fica em `portal/painel-tema.css` (gerado, não editar à mão) e o
`configurar.py` o injeta pela configuração `DASHBOARD_SCRIPTS` do Chatwoot.

| | Claro | Escuro |
|---|---|---|
| Fundo de botão e destaque (`--al-marca-rgb`) | #2453c7 (branco 6,7:1) | #466ede (branco 4,6:1) |
| Texto e links (`--al-marca-texto-rgb`) | #2453c7 | #7d9cf0 (7:1 no fundo escuro) |
| Fundo da página | #f4f6fb (`--fundo`) | o do Chatwoot |

Também: foco de teclado visível na cor da marca onde o Chatwoot não define outro. A fonte (Inter)
e os cantos ficam os do Chatwoot, para não desalinhar o layout dele.

**Depois de atualizar o Chatwoot**, rode `python3 scripts/gerar_tema_painel.py` e
`python3 scripts/configurar.py` (os nomes das classes mudam a cada versão). O teste confere se o
painel serve o `painel-tema.css` atual. Para desligar: apagar `DASHBOARD_SCRIPTS` em
Super Admin → Installation Config (e tirar a linha do `configurar.py`).

## Design system no claude.ai

Os componentes da Central viraram o pacote React `design-system/` (`@atendimento-lojas/ui`),
sincronizado com o claude.ai pela skill `/design-sync` (iniciada pelo usuário). Notas da
sincronização em `.design-sync/NOTES.md`. Fonte da verdade das cores: `portal/estilo.css`
(bloco `:root`); o pacote e o tema do painel copiam esses valores.
