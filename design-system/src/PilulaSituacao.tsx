import * as React from "react";
import { cx } from "./util";

/** Estados de situação: ok = verde, alerta = âmbar, erro = vermelho, neutro = cinza. */
export type Estado = "ok" | "alerta" | "erro" | "neutro";

export interface PilulaSituacaoProps {
  /** Cor da pílula. */
  estado: Estado;
  /** Texto curto: "Conectado", "Conectando", "Desconectado", "Não criado"… */
  children: React.ReactNode;
}

/**
 * Pílula com ponto e texto que mostra a situação de algo (um número de WhatsApp, um serviço). O texto
 * sempre acompanha a cor: nunca use só a cor para dizer o estado.
 */
export function PilulaSituacao({ estado, children }: PilulaSituacaoProps) {
  return <span className={cx("al-pilula", `al-pilula--${estado}`)}>{children}</span>;
}
