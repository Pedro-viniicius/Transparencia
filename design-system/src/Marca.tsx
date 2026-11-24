import * as React from "react";
import { cx } from "./util";

export interface MarcaProps {
  /** Nome exibido ao lado do símbolo. */
  nome?: string;
  /** Linha menor abaixo do nome (ex.: "Central da equipe"). */
  subtitulo?: string;
  /** Tamanho do símbolo: "m" (40 px, padrão) ou "p" (32 px). */
  tamanho?: "p" | "m";
  /** Mostra só o símbolo, sem o texto. */
  soSimbolo?: boolean;
}

/**
 * Símbolo e nome do Atendimento das Lojas: balão de conversa branco sobre azul, com um ponto de cada
 * loja (verde-azulado = Loja de Baixo, âmbar = Loja da Praça). Use no topo das telas.
 */
export function Marca({ nome = "Atendimento das Lojas", subtitulo, tamanho = "m", soSimbolo = false }: MarcaProps) {
  const lado = tamanho === "p" ? 32 : 40;
  return (
    <span className={cx("al-marca", tamanho === "p" && "al-marca--p")}>
      <svg className="al-marca__logo" width={lado} height={lado} viewBox="0 0 64 64" role="img" aria-label={nome}>
        <rect width="64" height="64" rx="16" fill="#2453c7" />
        <path d="M15 20a7 7 0 0 1 7-7h20a7 7 0 0 1 7 7v14a7 7 0 0 1-7 7H29l-9 8v-8h1a7 7 0 0 1-6-7z" fill="#fff" />
        <circle cx="26" cy="27" r="4" fill="#0f766e" />
        <circle cx="38" cy="27" r="4" fill="#b45309" />
      </svg>
      {!soSimbolo && (
        <span>
          <span className="al-marca__nome" style={{ display: "block" }}>{nome}</span>
          {subtitulo && <span className="al-marca__sub" style={{ display: "block" }}>{subtitulo}</span>}
        </span>
      )}
    </span>
  );
}
