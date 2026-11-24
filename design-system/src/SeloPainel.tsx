import * as React from "react";
import { cx } from "./util";

export interface SeloPainelProps {
  /** true = no ar (ponto verde); false = fora do ar (ponto vermelho); omitido = verificando (cinza). */
  noAr?: boolean;
  /** Texto do selo. Padrão conforme `noAr`. */
  children?: React.ReactNode;
}

/**
 * Selo arredondado com ponto colorido que diz se o painel de conversas está no ar. Fica no canto
 * do topo; anuncia mudanças para leitores de tela (aria-live).
 */
export function SeloPainel({ noAr, children }: SeloPainelProps) {
  const texto = children ?? (noAr === undefined ? "Verificando o painel…" : noAr ? "Painel no ar" : "Painel fora do ar");
  return (
    <p className={cx("al-selo-painel", noAr === true && "al-selo-painel--ok", noAr === false && "al-selo-painel--erro")} aria-live="polite" style={{ margin: 0 }}>
      <span className="al-selo-painel__ponto" aria-hidden="true" />
      <span>{texto}</span>
    </p>
  );
}
