import * as React from "react";

export interface CartaoEntradaProps {
  /** Saudação ou título principal da tela (h1). */
  titulo: string;
  /** Uma ou duas frases que explicam o que fazer. */
  texto?: React.ReactNode;
  /** A ação principal, normalmente um <Botao tamanho="grande">. */
  acao?: React.ReactNode;
}

/**
 * Destaque do topo da tela: título grande, texto de apoio e a ação principal à direita (embaixo no
 * celular). Fundo com leve degradê do azul suave da marca. Use um por tela.
 */
export function CartaoEntrada({ titulo, texto, acao }: CartaoEntradaProps) {
  return (
    <section className="al-entrada">
      <div className="al-entrada__texto">
        <h1 className="al-entrada__titulo">{titulo}</h1>
        {texto && <p>{texto}</p>}
      </div>
      {acao}
    </section>
  );
}
