import * as React from "react";

export interface AreaRecolhivelProps {
  /** Título da área. */
  titulo: string;
  /** Linha menor abaixo do título (para quem é, o que pede). */
  subtitulo?: string;
  /** Começa aberta. */
  aberta?: boolean;
  children?: React.ReactNode;
}

/**
 * Área que abre e fecha (<details>), para conteúdo técnico ou raro que não deve distrair a equipe.
 * Seta gira ao abrir; o cabeçalho inteiro é clicável (alvo de 44 px).
 */
export function AreaRecolhivel({ titulo, subtitulo, aberta, children }: AreaRecolhivelProps) {
  return (
    <details className="al-recolhivel" open={aberta}>
      <summary className="al-recolhivel__resumo">
        <span className="al-recolhivel__textos">
          <span className="al-recolhivel__titulo">{titulo}</span>
          {subtitulo && <span className="al-recolhivel__sub">{subtitulo}</span>}
        </span>
        <svg className="al-recolhivel__seta" aria-hidden="true" viewBox="0 0 24 24" width="20" height="20">
          <path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </summary>
      <div className="al-recolhivel__corpo">{children}</div>
    </details>
  );
}
