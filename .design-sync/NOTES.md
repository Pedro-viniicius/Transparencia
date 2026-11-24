# Notas do design-sync

- O design system é o pacote `design-system/` (`@atendimento-lojas/ui`, React 18): os componentes
  da Central do Atendimento (`portal/`) reescritos em React para o claude.ai. A Central em si
  continua HTML/CSS/JS puro e NÃO usa este pacote.
- Build: `cd design-system && npm ci && npm run build` (esbuild + tsc + cópia do CSS).
  Conversor: `--entry ./design-system/dist/index.js --node-modules ./design-system/node_modules`.
- Render check e capturas usam o Chrome do sistema: `export DS_CHROMIUM_PATH=/usr/bin/google-chrome`
  (sem baixar o chromium do playwright). O pacote `playwright` fica em `.ds-sync/`.
- `provider: Tela` envolve toda prévia (fundo, fonte e tokens). A prévia de `Tela` aninha uma
  `Tela` com tema fixo, de propósito.
- Componentes largos em `cardMode: column` (cartões, listas, seção, aviso, área recolhível).
- `tokens.json` sai só com o tema claro (o layout lê o `:root`); o tema escuro vive no CSS
  (`prefers-color-scheme` e `[data-tema="escuro"]`).

- `libOverrides`: `.design-sync/overrides/dts.mjs` é um fork de `.ds-sync/lib/dts.mjs` só para o
  `jsdocFor` manter acentos no índice de componentes (o original apaga tudo fora de `\w`). Precisa do
  symlink `.design-sync/node_modules -> ../.ds-sync/node_modules` (recrie com
  `ln -s ../.ds-sync/node_modules .design-sync/node_modules` depois de reinstalar o `.ds-sync/`).

## Re-sync risks

- Se a skill atualizar `lib/dts.mjs`, compare com o fork e reaplique a troca da regex
  (`[^\p{L}\p{N}_\s.,()'/:+-]` com a flag `u`).

- Tokens duplicados: `design-system/src/estilo.css` copia os tokens de `portal/estilo.css`.
  Mudou a cor na Central, mude no pacote também (não há ligação automática).
- As prévias (`.design-sync/previews/`) usam textos da Central; se o texto da Central mudar, elas
  ficam desatualizadas, mas continuam válidas.
- Primeira sincronização em 24/11/2026: 16 componentes, 16 prévias autorais avaliadas "good".
