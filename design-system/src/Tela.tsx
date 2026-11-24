import * as React from "react";
import { cx } from "./util";

export interface TelaProps {
  /** Tema fixo. Sem valor, segue o sistema (claro ou escuro). */
  tema?: "claro" | "escuro";
  /** Envolve o conteúdo na coluna central (até 1040 px, com margens laterais). */
  centralizado?: boolean;
  className?: string;
  children?: React.ReactNode;
}

/**
 * Raiz obrigatória de qualquer tela do Atendimento das Lojas: aplica fundo, cor do texto, fonte do
 * sistema, foco visível e o tema. Sem ela os componentes ficam sem a fonte e sem o fundo certos.
 */
export function Tela({ tema, centralizado = false, className, children }: TelaProps) {
  return (
    <div className={cx("al-tela", className)} data-tema={tema}>
      {centralizado ? <div className="al-conteudo">{children}</div> : children}
    </div>
  );
}
