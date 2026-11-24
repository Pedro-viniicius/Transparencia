import * as React from "react";
import { Campo, Entrada } from "@atendimento-lojas/ui";

export const Texto = () => (
  <div style={{ maxWidth: 360 }}>
    <Campo id="nome" rotulo="Nome do contato"><Entrada id="nome" placeholder="Ex.: Maria da Silva" /></Campo>
  </div>
);
export const Invalida = () => (
  <div style={{ maxWidth: 360 }}>
    <Campo id="email" rotulo="E-mail" erro="Digite um e-mail válido."><Entrada id="email" type="email" invalido defaultValue="maria@" /></Campo>
  </div>
);
