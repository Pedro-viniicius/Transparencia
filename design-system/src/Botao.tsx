import * as React from "react";
import { cx } from "./util";

export interface BotaoProps {
  /** "primario" (azul da marca, a ação principal da tela) ou "secundario" (contorno, ações de apoio). */
  variante?: "primario" | "secundario";
  /** "grande" para a ação principal de uma tela; "normal" no resto. */
  tamanho?: "normal" | "grande";
  /** Com `href`, vira link (<a>); sem, é <button>. */
  href?: string;
  /** Abre o link em outra aba e mostra o ícone de link externo. */
  externo?: boolean;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  onClick?: (evento: React.MouseEvent<HTMLElement>) => void;
  children?: React.ReactNode;
}

/**
 * Botão do Atendimento das Lojas: alvo de toque de 44 px (52 px no grande), cantos de 10 px, foco
 * visível. Uma ação primária por área; o resto em secundário.
 */
export function Botao({ variante = "primario", tamanho = "normal", href, externo = false, type = "button", disabled, onClick, children }: BotaoProps) {
  const classe = cx("al-botao", variante === "secundario" && "al-botao--secundario", tamanho === "grande" && "al-botao--grande");
  const icone = externo ? (
    <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20">
      <path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  ) : null;
  if (href) {
    return (
      <a className={classe} href={href} onClick={onClick} {...(externo ? { target: "_blank", rel: "noopener" } : {})}>
        {children}
        {icone}
      </a>
    );
  }
  return (
    <button className={classe} type={type} disabled={disabled} onClick={onClick}>
      {children}
      {icone}
    </button>
  );
}
