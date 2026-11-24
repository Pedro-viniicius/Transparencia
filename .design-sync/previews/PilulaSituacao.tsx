import * as React from "react";
import { PilulaSituacao } from "@atendimento-lojas/ui";

export const Estados = () => (
  <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
    <PilulaSituacao estado="ok">Conectado</PilulaSituacao>
    <PilulaSituacao estado="alerta">Conectando</PilulaSituacao>
    <PilulaSituacao estado="erro">Desconectado</PilulaSituacao>
    <PilulaSituacao estado="neutro">Não criado</PilulaSituacao>
  </div>
);
export const Conectado = () => <PilulaSituacao estado="ok">Conectado</PilulaSituacao>;
export const SemResposta = () => <PilulaSituacao estado="erro">Sem resposta</PilulaSituacao>;
