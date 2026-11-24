#!/usr/bin/env python3
"""Gera portal/painel-tema.css: o visual da Central aplicado ao painel de conversas (Chatwoot).

O Chatwoot pinta o azul dele (#2781f6) de dois jeitos: pelas variáveis --blue-1..12 e por
centenas de classes com a cor escrita direto no CSS. Este script lê o CSS do Chatwoot que está
rodando, copia só as regras que usam esse azul (com os mesmos seletores, @media e @supports)
e troca a cor por variáveis da marca. O configurar.py injeta o resultado no painel pela
configuração DASHBOARD_SCRIPTS. Nenhum arquivo do Chatwoot é alterado.

Rode de novo depois de atualizar a imagem do Chatwoot (os nomes das classes mudam):
    python3 scripts/gerar_tema_painel.py && python3 scripts/configurar.py
"""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "portal" / "painel-tema.css"

# Folhas que o painel carrega (widget, portal de ajuda, pesquisa e superadmin ficam de fora).
PREFIXOS = ("dashboard-", "v3app-", "ArticleEditor-", "Messages-", "DashboardIcon-",
            "CategoryHeaderControls-", "chatwoot-viz-", "commandbar-", "useBranding-")

AZUL = re.compile(r"#2781f6([0-9a-f]{2})?\b|rgba?\(\s*39[\s,]+129[\s,]+246\s*(?:[,/]\s*([^)]+))?\)", re.I)

# Escala no estilo Radix (canais RGB, como o Chatwoot usa) a partir dos tokens da Central.
MARCA_CLARO = (36, 83, 199)      # --marca #2453c7
MARCA_ESCURO = (70, 110, 222)    # fundo de botão no escuro: texto branco com contraste 4,6
TEXTO_ESCURO = (125, 156, 240)   # --marca do tema escuro (#7d9cf0), para texto sobre fundo escuro
MISTURA = (0.02, 0.05, 0.10, 0.16, 0.23, 0.32, 0.45, 0.65)


def misturar(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def rgb(c):
    return " ".join(str(v) for v in c)


def escala(fundo, marca, extra):
    linhas = [f"--blue-{i}: {rgb(misturar(fundo, marca, t))};" for i, t in enumerate(MISTURA, 1)]
    linhas.append(f"--blue-9: {rgb(marca)};")
    linhas += [f"--blue-{i}: {rgb(c)};" for i, c in zip((10, 11, 12), extra)]
    return linhas


def tokens():
    claro = escala((255, 255, 255), MARCA_CLARO, ((31, 72, 176), (27, 63, 153), (14, 31, 77))) + [
        f"--al-marca-rgb: {rgb(MARCA_CLARO)};",
        f"--al-marca-texto-rgb: {rgb(MARCA_CLARO)};",
        "--solid-blue: 219 228 250;",
        "--text-blue: 12 28 74;",
        "--border-blue-strong: 23 47 112;",
        "--border-blue: 36, 83, 199, .5;",
        "--background-color: 244 246 251;",  # --fundo da Central
    ]
    escuro = escala((23, 23, 26), MARCA_ESCURO, ((84, 124, 230), TEXTO_ESCURO, (214, 225, 252))) + [
        f"--al-marca-rgb: {rgb(MARCA_ESCURO)};",
        f"--al-marca-texto-rgb: {rgb(TEXTO_ESCURO)};",
        "--solid-blue: 28 41 82;",
        "--text-blue: 216 226 252;",
        "--border-blue-strong: 199 212 248;",
        "--border-blue: 70, 110, 222, .5;",
    ]
    junta = lambda ls: "\n  ".join(ls)
    return f":root {{\n  {junta(claro)}\n}}\n.dark {{\n  {junta(escuro)}\n}}\n"


def trocar(valor, texto):
    var = "--al-marca-texto-rgb" if texto else "--al-marca-rgb"

    def sub(m):
        hex_alfa, alfa = m.group(1), m.group(2)
        if hex_alfa:
            return f"rgb(var({var}) / {int(hex_alfa, 16) / 255:.2f})"
        if alfa:
            return f"rgb(var({var}) / {alfa.strip()})"
        return f"rgb(var({var}))"

    return AZUL.sub(sub, valor)


def declaracoes(corpo):
    """Divide por ';' fora de parênteses (data: URIs têm ';')."""
    partes, nivel, atual = [], 0, []
    for ch in corpo:
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel -= 1
        if ch == ";" and nivel == 0:
            partes.append("".join(atual))
            atual = []
        else:
            atual.append(ch)
    partes.append("".join(atual))
    return [p.strip() for p in partes if p.strip()]


def regras(css):
    """Percorre o CSS e devolve (contexto @, seletor, corpo) de cada regra de estilo."""
    pilha, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        k = css.find("}", i)
        if k != -1 and (j == -1 or k < j):  # fecha um bloco @
            if pilha:
                pilha.pop()
            i = k + 1
            continue
        if j == -1:
            break
        cabeca = css[i:j].strip()
        if cabeca.startswith("@"):
            if re.match(r"@(media|supports|layer|container)\b", cabeca):
                pilha.append(cabeca)
                i = j + 1
                continue
            # @keyframes, @font-face, @page...: pula o bloco inteiro
            nivel, p = 1, j + 1
            while p < n and nivel:
                nivel += {"{": 1, "}": -1}.get(css[p], 0)
                p += 1
            i = p
            continue
        fim = css.find("}", j)
        yield tuple(pilha), cabeca, css[j + 1:fim]
        i = fim + 1


def ler_css_do_chatwoot():
    lista = subprocess.run(["docker", "compose", "exec", "-T", "chatwoot", "sh", "-c",
                            "ls /app/public/vite/assets/*.css"],
                           cwd=RAIZ, capture_output=True, text=True, check=True).stdout.split()
    escolhidos = [c for c in lista if Path(c).name.startswith(PREFIXOS)]
    if not any(Path(c).name.startswith("dashboard-") for c in escolhidos):
        sys.exit("Não achei o CSS do painel no container do Chatwoot. Ele está rodando?")
    for caminho in escolhidos:
        yield Path(caminho).name, subprocess.run(
            ["docker", "compose", "exec", "-T", "chatwoot", "cat", caminho],
            cwd=RAIZ, capture_output=True, text=True, check=True).stdout


def gerar():
    saida, vistos, arquivos = [], set(), []
    for nome, css in ler_css_do_chatwoot():
        arquivos.append(re.sub(r"-[\w]{8}\.css$", ".css", nome))
        for contexto, seletor, corpo in regras(css):
            if seletor in (":root", ".dark") or not AZUL.search(corpo):
                continue
            decl = []
            for d in declaracoes(corpo):
                if ":" not in d or not AZUL.search(d):
                    continue
                prop, valor = d.split(":", 1)
                decl.append(f"{prop.strip()}:{trocar(valor, prop.strip() == 'color')}")
            if not decl:
                continue
            regra = f"{seletor}{{{';'.join(decl)}}}"
            for c in reversed(contexto):
                regra = f"{c}{{{regra}}}"
            if regra not in vistos:
                vistos.add(regra)
                saida.append(regra)

    cabecalho = (
        "/* Atendimento das Lojas: tema do painel de conversas (Chatwoot).\n"
        "   GERADO por scripts/gerar_tema_painel.py; não edite à mão.\n"
        "   Cores da Central (docs/DESIGN.md); folhas lidas: " + ", ".join(sorted(set(arquivos))) + ". */\n"
    )
    foco = (
        "/* Foco visível de teclado na cor da marca (onde o Chatwoot não define outro). */\n"
        ":where(a,button,summary,[role=button],[role=tab],[role=menuitem]):focus-visible"
        "{outline:2px solid rgb(var(--al-marca-texto-rgb));outline-offset:2px}\n"
    )
    SAIDA.write_text(cabecalho + tokens() + foco + "\n".join(saida) + "\n", encoding="utf-8")
    print(f"{SAIDA.relative_to(RAIZ)}: {len(saida)} regras, {SAIDA.stat().st_size // 1024} KB")


if __name__ == "__main__":
    gerar()
