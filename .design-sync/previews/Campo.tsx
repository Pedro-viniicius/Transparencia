import * as React from "react";
import { Campo, Entrada, Selecao } from "@atendimento-lojas/ui";

export const ComAjuda = () => (
  <div style={{ maxWidth: 360 }}>
    <Campo id="chave" rotulo="Chave do sistema (apikey)" ajuda="Está em credenciais.txt. Fica guardada só nesta aba.">
      <Entrada id="chave" type="password" descritoPor="chave-ajuda" defaultValue="exemplo-de-chave" />
    </Campo>
  </div>
);
export const ComErro = () => (
  <div style={{ maxWidth: 360 }}>
    <Campo id="chave2" rotulo="Chave do sistema (apikey)" erro="Chave incorreta. Confira em credenciais.txt.">
      <Entrada id="chave2" type="password" invalido defaultValue="chave-errada" />
    </Campo>
  </div>
);
export const ComSelecao = () => (
  <div style={{ maxWidth: 360 }}>
    <Campo id="loja" rotulo="Loja">
      <Selecao id="loja" opcoes={[{ valor: "loja-baixa", texto: "Loja de Baixo" }, { valor: "loja-praca", texto: "Loja da Praça" }]} />
    </Campo>
  </div>
);
