import * as React from "react";
import { cx } from "./util";
import { Estado, PilulaSituacao } from "./PilulaSituacao";

/** As duas lojas. Cada uma tem a sua cor: verde-azulado (de Baixo) e âmbar (da Praça). */
export type Loja = "loja-baixa" | "loja-praca";

const PADRAO: Record<Loja, { nome: string; sigla: string }> = {
  "loja-baixa": { nome: "Loja de Baixo", sigla: "LB" },
  "loja-praca": { nome: "Loja da Praça", sigla: "LP" },
};

export interface CartaoLojaProps {
  /** Qual loja: define a cor da faixa e do selo. */
  loja: Loja;
  /** Nome exibido. Padrão: "Loja de Baixo" / "Loja da Praça". */
  nome?: string;
  /** Explicação em linguagem simples do que a situação significa para a atendente. */
  dica?: React.ReactNode;
  /** Situação do número da loja. */
  estado: Estado;
  /** Texto da pílula ("Conectado", "Desconectado"…). */
  textoEstado: string;
}

/**
 * Cartão de uma loja: faixa lateral e selo (LB/LP) na cor da loja, nome, dica e pílula de situação.
 * Coloque dois lado a lado dentro de <ListaLojas>.
 */
export function CartaoLoja({ loja, nome, dica, estado, textoEstado }: CartaoLojaProps) {
  const p = PADRAO[loja];
  return (
    <li className={cx("al-loja", `al-loja--${loja}`)}>
      <span className="al-loja__selo" aria-hidden="true">{p.sigla}</span>
      <div>
        <h3 className="al-loja__nome">{nome ?? p.nome}</h3>
        {dica && <p className="al-loja__dica">{dica}</p>}
      </div>
      <PilulaSituacao estado={estado}>{textoEstado}</PilulaSituacao>
    </li>
  );
}

export interface ListaLojasProps {
  /** Elementos <CartaoLoja>. */
  children: React.ReactNode;
}

/** Grade responsiva de cartões de loja (lado a lado no computador, empilhados no celular). */
export function ListaLojas({ children }: ListaLojasProps) {
  return <ul className="al-lojas" aria-live="polite">{children}</ul>;
}
