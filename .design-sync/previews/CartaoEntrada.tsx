import * as React from "react";
import { CartaoEntrada, Botao } from "@atendimento-lojas/ui";

export const Saudacao = () => (
  <CartaoEntrada
    titulo="Bom atendimento! 👋"
    texto="Todas as conversas do WhatsApp e do Instagram ficam no painel. Entre com o seu e-mail e senha."
    acao={<Botao tamanho="grande" href="#painel" externo>Abrir o painel de conversas</Botao>}
  />
);
export const SemAcao = () => (
  <CartaoEntrada titulo="Painel em manutenção" texto="Voltamos em alguns minutos. As mensagens dos clientes ficam guardadas." />
);
