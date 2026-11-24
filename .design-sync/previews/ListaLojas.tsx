import * as React from "react";
import { CartaoLoja, ListaLojas } from "@atendimento-lojas/ui";

export const AmbasConectadas = () => (
  <ListaLojas>
    <CartaoLoja loja="loja-baixa" estado="ok" textoEstado="Conectado" dica="Recebendo e enviando mensagens." />
    <CartaoLoja loja="loja-praca" estado="ok" textoEstado="Conectado" dica="Recebendo e enviando mensagens." />
  </ListaLojas>
);
