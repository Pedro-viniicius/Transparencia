import * as React from "react";

export interface AvisoProps {
  /** Começo em negrito (ex.: "Antes de escanear:"). */
  titulo?: React.ReactNode;
  /** Texto ou lista (<ul>) com os cuidados. */
  children?: React.ReactNode;
}

/** Caixa âmbar de cuidado: algo que pode dar errado se for ignorado. Não use para erros (use texto de erro). */
export function Aviso({ titulo, children }: AvisoProps) {
  return (
    <div className="al-aviso" role="note">
      {titulo && <strong>{titulo}</strong>}
      {children}
    </div>
  );
}
