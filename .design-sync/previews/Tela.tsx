import * as React from "react";
import { Tela, Marca, PilulaSituacao } from "@atendimento-lojas/ui";

export const Claro = () => (
  <Tela tema="claro">
    <div style={{ padding: 16, display: "flex", gap: 12, alignItems: "center" }}>
      <Marca subtitulo="Central da equipe" />
      <PilulaSituacao estado="ok">Conectado</PilulaSituacao>
    </div>
  </Tela>
);

export const Escuro = () => (
  <Tela tema="escuro">
    <div style={{ padding: 16, display: "flex", gap: 12, alignItems: "center" }}>
      <Marca subtitulo="Central da equipe" />
      <PilulaSituacao estado="ok">Conectado</PilulaSituacao>
    </div>
  </Tela>
);
