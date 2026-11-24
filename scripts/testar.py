#!/usr/bin/env python3
"""Teste ponta a ponta sem celular: simula clientes escrevendo em cada caixa e confere
boas-vindas, equipe atribuída, menu do Instagram e quem enxerga cada conversa.
Apaga os contatos e conversas de teste no fim. Uso: python3 scripts/testar.py
"""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import configurar as cfg  # noqa: E402

RUBY_TOKENS = """
require 'json'
emails = JSON.parse(ENV.fetch('EMAILS'))
puts JSON.generate(emails.to_h { |e| [e, User.find_by!(email: e).access_token.token] })
"""

falhas = []


def checar(ok, descricao):
    print(("  ✅ " if ok else "  ❌ ") + descricao)
    if not ok:
        falhas.append(descricao)


def tokens(emails):
    r = subprocess.run(
        ["docker", "compose", "exec", "-T", "-e", f"EMAILS={json.dumps(emails)}",
         "chatwoot", "bundle", "exec", "rails", "runner", "-"],
        input=RUBY_TOKENS, capture_output=True, text=True, cwd=cfg.RAIZ)
    linha = [l for l in r.stdout.splitlines() if l.startswith("{")]
    if not linha:
        raise SystemExit(r.stderr)
    return json.loads(linha[-1])


def esperar(funcao, tentativas=15):
    for _ in range(tentativas):
        r = funcao()
        if r:
            return r
        time.sleep(1)
    return funcao()


def portal(caminho):
    """(status, corpo) de uma rota da Central do Atendimento, sem enviar chave."""
    try:
        with urllib.request.urlopen(cfg.PORTAL_PADRAO + caminho, timeout=10) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except OSError:
        return 0, ""


def testar_portal():
    print("\nCentral do Atendimento")
    st, corpo = portal("/")
    checar(st == 200 and "Abrir o painel" in corpo, "a página abre com o botão do painel")
    for loja in cfg.LOJAS:
        st, corpo = portal(f"/api/status/{loja['chave']}")
        estado = json.loads(corpo).get("instance", {}).get("state") if st == 200 else None
        checar(estado in ("open", "close", "connecting"), f"mostra a situação da {loja['nome']} ({estado})")
    st, _ = portal(f"/api/conectar/{cfg.LOJAS[0]['chave']}")
    checar(st == 401, "QR Code sem a chave é recusado")
    st, _ = portal("/api/status/../instance/fetchInstances")
    checar(st in (400, 404), "outras rotas do Evolution não ficam expostas")
    try:
        with urllib.request.urlopen(cfg.CHATWOOT + "/app/login", timeout=10) as r:
            pagina = r.read().decode()
    except OSError:
        pagina = ""
    tema = (cfg.RAIZ / "portal" / "painel-tema.css").read_text(encoding="utf-8")
    checar('id="atendimento-lojas-tema"' in pagina and tema.strip() in pagina,
           "o painel carrega as cores da Central (painel-tema.css atual)")


def main():
    emails = [cfg.ADMIN_EMAIL] + [p["email"] for p in cfg.PESSOAS]
    tk = tokens(emails)
    conta = 1
    adm = cfg.Chatwoot(conta, tk[cfg.ADMIN_EMAIL])
    caixas = cfg.caixas_por_nome(adm)
    equipes = {t["name"].lower(): t["id"] for t in adm("GET", "/teams")}
    criados = []  # (contato, conversa)

    def cliente(caixa, nome, telefone):
        c = adm("POST", "/contacts", {"inbox_id": caixa["id"], "name": nome, "phone_number": telefone})
        contato = c["payload"]["contact"]
        source = c["payload"]["contact_inbox"]["source_id"]
        conv = adm("POST", "/conversations", {"source_id": source, "inbox_id": caixa["id"],
                                               "contact_id": contato["id"]})
        criados.append((contato["id"], conv["id"]))
        return conv["id"]

    def escrever(conv, texto):
        adm("POST", f"/conversations/{conv}/messages", {"content": texto, "message_type": "incoming"})

    def conversa(conv):
        return adm("GET", f"/conversations/{conv}")

    def respostas(conv):
        msgs = adm("GET", f"/conversations/{conv}/messages")["payload"]
        # 1 = enviada por pessoa/automação; 3 = template (saudação). O Evolution repassa as duas.
        return [m["content"] for m in msgs if m["message_type"] in (1, 3)]

    testar_portal()
    try:
        conv_loja = {}
        for i, loja in enumerate(cfg.LOJAS):
            print(f"\n{loja['caixa']}")
            caixa = caixas[loja["caixa"]]
            conv = cliente(caixa, f"Cliente Teste {i + 1}", f"+55000000000{i + 1}")
            conv_loja[loja["chave"]] = conv
            escrever(conv, "Oi, vocês têm o boneco?")
            esperado = cfg.BOAS_VINDAS.format(loja=loja["nome"])
            checar(esperar(lambda: esperado in respostas(conv)), "recebeu as boas-vindas com o nome da loja")
            time_id = equipes[loja["nome"].lower()]
            checar(esperar(lambda: (conversa(conv).get("meta", {}).get("team") or {}).get("id") == time_id),
                   f"foi para a equipe {loja['nome']}")
            escrever(conv, "Ainda tem?")
            time.sleep(4)
            checar(respostas(conv).count(esperado) == 1, "a 2ª mensagem não gera outra saudação")

        print("\nResposta do atendente → Evolution")
        conv = conv_loja["loja-baixa"]
        msg = adm("POST", f"/conversations/{conv}/messages", {"content": "Temos sim!", "message_type": "outgoing"})

        def erro_envio():
            m = next(x for x in adm("GET", f"/conversations/{conv}/messages")["payload"] if x["id"] == msg["id"])
            return (m.get("content_attributes") or {}).get("external_error") or ""
        time.sleep(4)
        erro = erro_envio()
        checar("public ip" not in erro and "resolve" not in erro,
               f"o Chatwoot conseguiu entregar ao Evolution{(' (erro: ' + erro + ')') if erro else ''}")

        print("\nQuem enxerga o quê")
        for p in cfg.PESSOAS:
            cw = cfg.Chatwoot(conta, tk[p["email"]])
            vistas = {c["id"] for c in cw("GET", "/conversations?status=all&assignee_type=all")["data"]["payload"]}
            for chave, conv in conv_loja.items():
                deve = p["loja"] in (None, chave)
                checar((conv in vistas) == deve,
                       f"{p['nome']} {'vê' if deve else 'NÃO vê'} a conversa da {chave}")

        print(f"\n{cfg.CAIXA_SIMULACAO}")
        conv = cliente(caixas[cfg.CAIXA_SIMULACAO], "Cliente Instagram", "+5500000000009")
        escrever(conv, "oi, qual o preço?")
        checar(esperar(lambda: cfg.MENU_INSTAGRAM in respostas(conv)), "recebeu o menu das lojas")
        checar(conversa(conv).get("meta", {}).get("team") is None, "antes de escolher, fica sem equipe")
        escrever(conv, "2")
        praca = equipes["loja da praça"]
        checar(esperar(lambda: (conversa(conv)["meta"].get("team") or {}).get("id") == praca),
               "digitou 2 → foi para a Loja da Praça")
        checar(esperar(lambda: cfg.CONFIRMA_LOJA.format(loja="Loja da Praça") in respostas(conv)),
               "recebeu a confirmação da loja")
        escrever(conv, "1")
        time.sleep(4)
        checar(conversa(conv)["meta"]["team"]["id"] == praca, "digitar 1 depois não muda a loja")
    finally:
        for contato, conv in criados:
            adm("DELETE", f"/conversations/{conv}")
            adm("DELETE", f"/contacts/{contato}")
        print(f"\nLimpeza: {len(criados)} conversas e contatos de teste apagados.")

    print("\nRESULTADO:", "tudo certo" if not falhas else f"{len(falhas)} falha(s)")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
