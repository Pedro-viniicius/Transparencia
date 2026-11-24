import * as React from "react";
import { Aviso } from "@atendimento-lojas/ui";

export const AntesDeEscanear = () => (
  <Aviso titulo="Antes de escanear:">
    <ul>
      <li>Use <strong>só o chip da loja</strong>. Nunca um número pessoal: o histórico inteiro é copiado para o painel.</li>
      <li>Desligue as automações das caixas de WhatsApp antes de conectar.</li>
    </ul>
  </Aviso>
);
export const Curto = () => <Aviso titulo="Atenção:"> o QR Code vence em poucos segundos; escaneie logo.</Aviso>;
