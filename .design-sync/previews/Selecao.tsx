import * as React from "react";
import { Campo, Selecao } from "@atendimento-lojas/ui";

export const Lojas = () => (
  <div style={{ maxWidth: 360 }}>
    <Campo id="loja-qr" rotulo="Loja">
      <Selecao id="loja-qr" defaultValue="loja-praca" opcoes={[{ valor: "loja-baixa", texto: "Loja de Baixo" }, { valor: "loja-praca", texto: "Loja da Praça" }]} />
    </Campo>
  </div>
);
