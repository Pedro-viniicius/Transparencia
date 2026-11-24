import * as React from "react";

export interface SecaoProps {
  /** Título da seção (h2). */
  titulo: string;
  /** Nota pequena à direita do título (ex.: "Atualiza a cada 15 s"). */
  nota?: React.ReactNode;
  children?: React.ReactNode;
}

/** Bloco de conteúdo com título h2 e nota opcional alinhada à direita. Separa as áreas da tela. */
export function Secao({ titulo, nota, children }: SecaoProps) {
  const id = "secao-" + titulo.toLowerCase().normalize("NFD").replace(/[^a-z0-9]+/g, "-");
  return (
    <section aria-labelledby={id}>
      <div className="al-secao__cabeca">
        <h2 className="al-secao__titulo" id={id}>{titulo}</h2>
        {nota && <p className="al-secao__nota">{nota}</p>}
      </div>
      {children}
    </section>
  );
}
