import * as React from "react";
import { Secao, CartaoLoja, ListaLojas } from "@atendimento-lojas/ui";

export const ComNota = () => (
  <Secao titulo="Números de WhatsApp" nota="Atualizado às 18:42:39 · a cada 15 s">
    <ListaLojas>
      <CartaoLoja loja="loja-baixa" estado="ok" textoEstado="Conectado" dica="Recebendo e enviando mensagens." />
      <CartaoLoja loja="loja-praca" estado="ok" textoEstado="Conectado" dica="Recebendo e enviando mensagens." />
    </ListaLojas>
  </Secao>
);
export const SoTitulo = () => (
  <Secao titulo="Guia rápido">
    <p style={{ color: "var(--texto-2)" }}>Quatro passos para começar o dia no painel.</p>
  </Secao>
);
