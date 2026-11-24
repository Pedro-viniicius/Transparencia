import * as React from "react";
import { CartaoLoja, ListaLojas } from "@atendimento-lojas/ui";

export const DuasLojas = () => (
  <ListaLojas>
    <CartaoLoja loja="loja-baixa" estado="erro" textoEstado="Desconectado"
      dica="As mensagens deste número não chegam ao painel. Avise o responsável técnico." />
    <CartaoLoja loja="loja-praca" estado="ok" textoEstado="Conectado" dica="Recebendo e enviando mensagens." />
  </ListaLojas>
);
export const Conectando = () => (
  <ListaLojas>
    <CartaoLoja loja="loja-praca" estado="alerta" textoEstado="Conectando" dica="Esperando o celular ler o QR Code." />
  </ListaLojas>
);
export const NaoCriado = () => (
  <ListaLojas>
    <CartaoLoja loja="loja-baixa" estado="neutro" textoEstado="Não criado" dica="Este número ainda não foi configurado." />
  </ListaLojas>
);
