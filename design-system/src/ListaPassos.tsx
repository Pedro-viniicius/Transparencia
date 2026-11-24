import * as React from "react";

export interface Passo {
  /** Título curto do passo. */
  titulo: React.ReactNode;
  /** Explicação em uma ou duas frases. */
  texto: React.ReactNode;
}

export interface ListaPassosProps {
  /** Os passos, em ordem. Numerados automaticamente. */
  passos: Passo[];
}

/** Guia em passos numerados (cartões em grade). Ideal para orientar atendentes em 3 a 5 passos. */
export function ListaPassos({ passos }: ListaPassosProps) {
  return (
    <ol className="al-passos">
      {passos.map((p, i) => (
        <li className="al-passos__item" key={i}>
          <h3 className="al-passos__titulo">{p.titulo}</h3>
          <p className="al-passos__texto">{p.texto}</p>
        </li>
      ))}
    </ol>
  );
}
