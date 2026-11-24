import * as React from "react";
import { Botao } from "@atendimento-lojas/ui";

export const PrincipalGrande = () => (
  <Botao tamanho="grande" href="#painel" externo>Abrir o painel de conversas</Botao>
);
export const Primario = () => <Botao type="submit">Gerar QR Code</Botao>;
export const Secundario = () => <Botao variante="secundario">Parar</Botao>;
export const Desativado = () => <Botao disabled>Gerando…</Botao>;
