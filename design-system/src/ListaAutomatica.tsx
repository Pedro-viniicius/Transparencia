import * as React from "react";
import { cx } from "./util";

export interface ItemAutomatico {
  /** O que o sistema faz sozinho. */
  texto: React.ReactNode;
  /** Cor do marcador: a de uma loja ou a da marca (padrão). */
  cor?: "loja-baixa" | "loja-praca" | "marca";
}

export interface ListaAutomaticaProps {
  /** Título do bloco. */
  titulo?: string;
  itens: ItemAutomatico[];
}

/** Bloco de contorno tracejado que lista o que acontece automaticamente, com marcadores coloridos. */
export function ListaAutomatica({ titulo = "O que o sistema faz sozinho", itens }: ListaAutomaticaProps) {
  return (
    <div className="al-automatico">
      <h3 className="al-automatico__titulo">{titulo}</h3>
      <ul>
        {itens.map((item, i) => (
          <li key={i}>
            <span className={cx("al-marcador", item.cor && item.cor !== "marca" && `al-marcador--${item.cor}`)} aria-hidden="true" />
            {item.texto}
          </li>
        ))}
      </ul>
    </div>
  );
}
