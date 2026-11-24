import * as React from "react";

export interface CampoProps {
  /** id do controle; liga o rótulo, a ajuda e o erro. */
  id: string;
  /** Rótulo visível acima do controle. */
  rotulo: string;
  /** Texto de ajuda abaixo do controle. */
  ajuda?: React.ReactNode;
  /** Mensagem de erro (vermelha). Marca o controle como inválido. */
  erro?: React.ReactNode;
  /** O controle: <Entrada> ou <Selecao> com o mesmo `id`. */
  children: React.ReactNode;
}

/** Campo de formulário: rótulo, controle, ajuda e erro, já ligados para leitores de tela. */
export function Campo({ id, rotulo, ajuda, erro, children }: CampoProps) {
  return (
    <div className="al-campo">
      <label className="al-campo__rotulo" htmlFor={id}>{rotulo}</label>
      {children}
      {ajuda && <p className="al-campo__ajuda" id={`${id}-ajuda`}>{ajuda}</p>}
      {erro && <p className="al-campo__erro" id={`${id}-erro`} role="alert">{erro}</p>}
    </div>
  );
}

export interface EntradaProps {
  id: string;
  type?: "text" | "password" | "email" | "tel" | "search";
  value?: string;
  defaultValue?: string;
  placeholder?: string;
  /** Marca como inválido (borda vermelha). Use junto com `erro` no <Campo>. */
  invalido?: boolean;
  /** Ligue à ajuda do <Campo>: `${id}-ajuda`. */
  descritoPor?: string;
  required?: boolean;
  onChange?: (evento: React.ChangeEvent<HTMLInputElement>) => void;
}

/** Caixa de texto com altura de toque de 44 px. Use dentro de <Campo>. */
export function Entrada({ id, type = "text", invalido, descritoPor, ...resto }: EntradaProps) {
  return <input className="al-controle" id={id} type={type} aria-invalid={invalido || undefined} aria-describedby={descritoPor} {...resto} />;
}

export interface SelecaoProps {
  id: string;
  /** Opções: valor e texto. */
  opcoes: Array<{ valor: string; texto: string }>;
  value?: string;
  defaultValue?: string;
  onChange?: (evento: React.ChangeEvent<HTMLSelectElement>) => void;
}

/** Lista de seleção com altura de toque de 44 px. Use dentro de <Campo>. */
export function Selecao({ id, opcoes, ...resto }: SelecaoProps) {
  return (
    <select className="al-controle" id={id} {...resto}>
      {opcoes.map((o) => <option key={o.valor} value={o.valor}>{o.texto}</option>)}
    </select>
  );
}
