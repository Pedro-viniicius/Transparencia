#!/usr/bin/env python3
"""Gera os avatares PNG das caixas (cor da loja + iniciais) em portal/img/.
Uso: python3 scripts/gerar_avatares.py   (precisa do Pillow)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
FONTES = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"]
AVATARES = {
    "caixa-loja-baixa.png": ("#0f766e", "LB"),
    "caixa-loja-praca.png": ("#b45309", "LP"),
    "caixa-instagram.png": ("#9d174d", "IG"),
}


def fonte(tamanho):
    for f in FONTES:
        if Path(f).exists():
            return ImageFont.truetype(f, tamanho)
    return ImageFont.load_default()


def main():
    destino = RAIZ / "portal" / "img"
    destino.mkdir(parents=True, exist_ok=True)
    lado = 256
    for nome, (cor, sigla) in AVATARES.items():
        img = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, lado - 1, lado - 1), radius=64, fill=cor)
        f = fonte(104)
        caixa = d.textbbox((0, 0), sigla, font=f)
        x = (lado - (caixa[2] - caixa[0])) / 2 - caixa[0]
        y = (lado - (caixa[3] - caixa[1])) / 2 - caixa[1]
        d.text((x, y), sigla, font=f, fill="#ffffff")
        img.save(destino / nome, optimize=True)
        print(destino / nome)


if __name__ == "__main__":
    main()
