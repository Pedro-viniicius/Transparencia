import * as React from "react";
import { AreaRecolhivel, Aviso, Botao } from "@atendimento-lojas/ui";

export const Fechada = () => (
  <AreaRecolhivel titulo="Área técnica: conectar um número" subtitulo="Só para o responsável técnico. Pede a chave do sistema.">
    <p>Conteúdo técnico.</p>
  </AreaRecolhivel>
);
export const Aberta = () => (
  <AreaRecolhivel aberta titulo="Área técnica: conectar um número" subtitulo="Só para o responsável técnico. Pede a chave do sistema.">
    <Aviso titulo="Antes de escanear:"> use só o chip da loja, nunca um número pessoal.</Aviso>
    <div><Botao>Gerar QR Code</Botao></div>
  </AreaRecolhivel>
);
