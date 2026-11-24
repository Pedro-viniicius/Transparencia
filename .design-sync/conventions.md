# Atendimento das Lojas: como construir com este sistema

Telas internas de atendimento de duas lojas (WhatsApp + Instagram): a equipe confere a situação
dos números, lê orientações e abre o painel de conversas. Português do Brasil, linguagem simples,
uso no computador e no celular.

## Envolva tudo em `<Tela>`

`Tela` é a raiz: aplica `--fundo`, `--texto`, a fonte do sistema, o foco visível e o tema. Sem ela
o texto sai na fonte do navegador e sem fundo. `tema="claro"` ou `tema="escuro"` fixa o tema; sem
`tema`, segue o sistema. `centralizado` põe o conteúdo na coluna de até 1040 px.

```jsx
const { Tela, Marca, SeloPainel, CartaoEntrada, Botao, Secao, ListaLojas, CartaoLoja } = window.AtendimentoUI;

<Tela centralizado>
  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
    <Marca subtitulo="Central da equipe" />
    <SeloPainel noAr />
  </div>
  <CartaoEntrada titulo="Bom atendimento!" texto="As conversas ficam no painel."
    acao={<Botao tamanho="grande" href="#painel" externo>Abrir o painel de conversas</Botao>} />
  <Secao titulo="Números de WhatsApp" nota="Atualiza a cada 15 s">
    <ListaLojas>
      <CartaoLoja loja="loja-baixa" estado="ok" textoEstado="Conectado" dica="Recebendo e enviando mensagens." />
      <CartaoLoja loja="loja-praca" estado="erro" textoEstado="Desconectado" dica="Avise o responsável técnico." />
    </ListaLojas>
  </Secao>
</Tela>
```

## Estilo: componentes + variáveis CSS

Não há classes utilitárias. Use os componentes para os controles e, no seu próprio layout
(espaços, grades), `style` com as variáveis abaixo, nunca cores soltas:

- Marca: `--marca`, `--marca-forte` (hover), `--marca-suave` (fundos de destaque), `--texto-no-botao`.
- Lojas: `--loja-baixa` / `--loja-baixa-suave` (verde-azulado, Loja de Baixo), `--loja-praca` /
  `--loja-praca-suave` (âmbar, Loja da Praça). Cada loja SEMPRE com a sua cor.
- Superfícies e texto: `--fundo`, `--superficie`, `--texto`, `--texto-2` (secundário), `--borda`, `--sombra`.
- Situação: `--ok-fundo`/`--ok-texto`, `--alerta-fundo`/`--alerta-texto`,
  `--erro-fundo`/`--erro-texto`, `--neutro-fundo`/`--neutro-texto`. Prefira `<PilulaSituacao estado>`.
- Medidas: `--esp-1`…`--esp-6` (4, 8, 12, 16, 20, 28 px), `--raio` (14 px, cartões),
  `--raio-p` (10 px, botões e campos), `--raio-pilula`, `--alvo-toque` (44 px), `--fonte`, `--fonte-mono`.

Regras: uma ação primária por área (`Botao`), o resto `variante="secundario"`; estado sempre com
texto, nunca só cor; alvos de toque de 44 px; conteúdo técnico ou raro dentro de `AreaRecolhivel`;
cuidados em `Aviso` (âmbar), erros de formulário no `erro` do `Campo`.

## Onde está a verdade

- `components/index.d.ts`: as props de cada componente.
- `components/<Nome>/README.md`: uso e exemplos de cada um.
- `tokens.css` e `tokens.json`: todos os tokens, claro e escuro; `components/bundle.css`: os estilos.
