#!/usr/bin/env python3
"""Configura o atendimento das duas lojas. Idempotente: pode rodar quantas vezes quiser.

Cria/atualiza: pessoas (6), equipes por loja, instâncias do WhatsApp no Evolution (com a
integração do Chatwoot), membros e boas-vindas de cada caixa, regras de automação e o menu
do Instagram, nome/logos do painel e avatares das caixas. Grava credenciais.txt (fora do Git).

Uso: python3 scripts/configurar.py
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CHATWOOT = "http://127.0.0.1:3000"
EVOLUTION = "http://127.0.0.1:8080"
# Endereço que o Evolution usa para falar com o Chatwoot (rede interna do Docker).
CHATWOOT_INTERNO = "http://chatwoot.localhost:3000"
ADMIN_EMAIL = "admin@lojas.local"
# Central do Atendimento (serviço "portal"). O painel carrega a logo daqui; no servidor, trocar
# pelo endereço público (variável PORTAL_URL no .env).
PORTAL_PADRAO = "http://127.0.0.1:8090"
NOME_MARCA = "Atendimento das Lojas"

LOJAS = [
    {"chave": "loja-baixa", "nome": "Loja de Baixo", "caixa": "WhatsApp · Loja de Baixo"},
    {"chave": "loja-praca", "nome": "Loja da Praça", "caixa": "WhatsApp · Loja da Praça"},
]
# Nomes e e-mails provisórios: trocar pelos reais quando o cliente mandar.
PESSOAS = [
    {"nome": "Dono", "email": "dono@lojas.local", "papel": "administrator", "loja": None},
    {"nome": "Esposa", "email": "esposa@lojas.local", "papel": "administrator", "loja": None},
    {"nome": "Atendente 1 · Loja de Baixo", "email": "baixa1@lojas.local", "papel": "agent", "loja": "loja-baixa"},
    {"nome": "Atendente 2 · Loja de Baixo", "email": "baixa2@lojas.local", "papel": "agent", "loja": "loja-baixa"},
    {"nome": "Atendente 1 · Loja da Praça", "email": "praca1@lojas.local", "papel": "agent", "loja": "loja-praca"},
    {"nome": "Atendente 2 · Loja da Praça", "email": "praca2@lojas.local", "papel": "agent", "loja": "loja-praca"},
]

BOAS_VINDAS = "Olá! 😊 Obrigado por falar com a {loja}. Já vamos te atender."
MENU_INSTAGRAM = (
    "Olá! 😊 Obrigado pela mensagem.\n"
    "Com qual loja você quer falar?\n"
    "Digite *1* para a Loja de Baixo\n"
    "Digite *2* para a Loja da Praça"
)
CONFIRMA_LOJA = "Certo! Já passei sua conversa para a {loja}. Em instantes alguém te responde. 😊"
# Caixa de API usada só para testar o menu do Instagram enquanto o Instagram real não está ligado.
CAIXA_SIMULACAO = "Teste · Instagram (simulação)"


def ler_env():
    env = {}
    for linha in (RAIZ / ".env").read_text().splitlines():
        if "=" in linha and not linha.lstrip().startswith("#"):
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def http(metodo, url, corpo=None, cabecalhos=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo)
    req.add_header("Content-Type", "application/json")
    for k, v in (cabecalhos or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{metodo} {url} -> {e.code}: {e.read().decode()[:500]}")


class Chatwoot:
    def __init__(self, conta, token):
        self.base = f"{CHATWOOT}/api/v1/accounts/{conta}"
        self.cab = {"api_access_token": token}

    def __call__(self, metodo, caminho, corpo=None):
        return http(metodo, self.base + caminho, corpo, self.cab)


def rodar_pessoas(env):
    pessoas = [
        {**p, "senha": env["SENHA_ADMIN"] if p["papel"] == "administrator" else env["SENHA_EQUIPE"]}
        for p in PESSOAS
    ]
    script = (RAIZ / "scripts" / "pessoas.rb").read_text()
    r = subprocess.run(
        ["docker", "compose", "exec", "-T",
         "-e", f"ADMIN_EMAIL={ADMIN_EMAIL}", "-e", f"PESSOAS_JSON={json.dumps(pessoas)}",
         "chatwoot", "bundle", "exec", "rails", "runner", "-"],
        input=script, capture_output=True, text=True, cwd=RAIZ,
    )
    ultima = [l for l in r.stdout.splitlines() if l.startswith("{")]
    if r.returncode != 0 or not ultima:
        raise SystemExit(f"pessoas.rb falhou:\n{r.stdout}\n{r.stderr}")
    return json.loads(ultima[-1])


def aplicar_marca(env, avatares):
    """Nome, logos e cores do painel + avatar de cada caixa. avatares: [(inbox_id, arquivo em portal/img)]."""
    portal = env.get("PORTAL_URL", PORTAL_PADRAO).rstrip("/")
    dados = {
        "configs": {
            "INSTALLATION_NAME": NOME_MARCA,
            "BRAND_NAME": NOME_MARCA,
            "LOGO": f"{portal}/logo-painel.svg",
            "LOGO_DARK": f"{portal}/logo-painel-escuro.svg",
            "LOGO_THUMBNAIL": f"{portal}/logo.svg",
            # Cores da Central no painel (gerado por scripts/gerar_tema_painel.py).
            "DASHBOARD_SCRIPTS": '<style id="atendimento-lojas-tema">\n'
                                 + (RAIZ / "portal" / "painel-tema.css").read_text(encoding="utf-8")
                                 + "</style>",
        },
        "avatares": [
            {"inbox_id": i, "arquivo": arq,
             "base64": base64.b64encode((RAIZ / "portal" / "img" / arq).read_bytes()).decode()}
            for i, arq in avatares
        ],
    }
    r = subprocess.run(
        ["docker", "compose", "exec", "-T", "-e", f"MARCA_JSON={json.dumps(dados)}",
         "chatwoot", "bundle", "exec", "rails", "runner", "-"],
        input=(RAIZ / "scripts" / "marca.rb").read_text(), capture_output=True, text=True, cwd=RAIZ,
    )
    ultima = [l for l in r.stdout.splitlines() if l.startswith("{")]
    if r.returncode != 0 or not ultima:
        raise SystemExit(f"marca.rb falhou:\n{r.stdout}\n{r.stderr}")
    trocados = json.loads(ultima[-1])["avatares_trocados"]
    print(f"  nome, logos e cores: {NOME_MARCA}; avatares atualizados: {', '.join(trocados) or 'nenhum (já estavam)'}")


def garantir_equipes(cw, ids_por_email):
    # O Chatwoot guarda o nome da equipe em minúsculas.
    existentes = {t["name"].lower(): t for t in cw("GET", "/teams")}
    equipes = {}
    for loja in LOJAS:
        t = existentes.get(loja["nome"].lower()) or cw("POST", "/teams", {
            "name": loja["nome"], "description": f"Atendentes da {loja['nome']}",
            "allow_auto_assign": True,
        })
        membros = [ids_por_email[p["email"]] for p in PESSOAS if p["loja"] == loja["chave"]]
        cw("PATCH", f"/teams/{t['id']}/team_members", {"user_ids": membros})
        equipes[loja["chave"]] = t["id"]
        print(f"  equipe {loja['nome']}: id {t['id']}, membros {membros}")
    return equipes


def garantir_instancias(env, conta, token):
    cab = {"apikey": env["AUTHENTICATION_API_KEY"]}
    existentes = {i["name"] for i in http("GET", f"{EVOLUTION}/instance/fetchInstances", None, cab)}
    for loja in LOJAS:
        chatwoot = {
            "chatwootAccountId": str(conta), "chatwootToken": token, "chatwootUrl": CHATWOOT_INTERNO,
            "chatwootSignMsg": True, "chatwootReopenConversation": True,
            "chatwootConversationPending": False, "chatwootImportContacts": False,
            "chatwootImportMessages": False, "chatwootMergeBrazilContacts": True,
            "chatwootNameInbox": loja["caixa"], "chatwootOrganization": loja["nome"],
            "chatwootAutoCreate": True,
        }
        if loja["chave"] not in existentes:
            http("POST", f"{EVOLUTION}/instance/create", {
                "instanceName": loja["chave"], "integration": "WHATSAPP-BAILEYS", "qrcode": True,
                **chatwoot,
            }, cab)
            print(f"  instância {loja['chave']}: criada")
        else:
            # Mesmos campos sem o prefixo "chatwoot", como o endpoint /chatwoot/set espera.
            corpo = {"enabled": True, "autoCreate": True}
            for k, v in chatwoot.items():
                chave = k[len("chatwoot"):]
                corpo[chave[0].lower() + chave[1:]] = v
            corpo["nameInbox"] = loja["caixa"]
            http("POST", f"{EVOLUTION}/chatwoot/set/{loja['chave']}", corpo, cab)
            print(f"  instância {loja['chave']}: já existia, integração atualizada")
        # Grupos do WhatsApp não entram no painel (no teste real, grupos do número inundaram a caixa).
        http("POST", f"{EVOLUTION}/settings/set/{loja['chave']}", {
            "rejectCall": False, "msgCall": "", "groupsIgnore": True, "alwaysOnline": False,
            "readMessages": False, "readStatus": False, "syncFullHistory": False,
        }, cab)


def caixas_por_nome(cw):
    return {i["name"]: i for i in cw("GET", "/inboxes")["payload"]}


def configurar_caixa(cw, caixa, membros, saudacao=None):
    """saudacao=None desliga a saudação nativa (as caixas do WhatsApp usam a da automação)."""
    cw("PATCH", f"/inboxes/{caixa['id']}", {
        "enable_auto_assignment": True, "greeting_enabled": bool(saudacao),
        "greeting_message": saudacao or "",
    })
    cw("PATCH", "/inbox_members", {"inbox_id": caixa["id"], "user_ids": membros})


def garantir_regra(cw, regra):
    existentes = {r["name"]: r for r in cw("GET", "/automation_rules")["payload"]}
    if regra["name"] in existentes:
        cw("PATCH", f"/automation_rules/{existentes[regra['name']]['id']}", regra)
    else:
        cw("POST", "/automation_rules", regra)
    print(f"  regra: {regra['name']}")


def cond(atributo, operador, valores, juncao=None):
    c = {"attribute_key": atributo, "filter_operator": operador, "values": valores}
    if juncao:
        c["query_operator"] = juncao
    return c


def regras_instagram(cw, caixa, equipes):
    """Menu: a saudação da caixa pergunta a loja; '1' ou '2' manda para a equipe (só sem equipe)."""
    for opcao, loja in (("1", LOJAS[0]), ("2", LOJAS[1])):
        garantir_regra(cw, {
            "name": f"{caixa['name']} · opção {opcao} → {loja['nome']}",
            "description": "Menu do Instagram: escolha da loja",
            "event_name": "message_created",
            "active": True,
            "conditions": [
                cond("inbox_id", "equal_to", [caixa["id"]], "and"),
                cond("message_type", "equal_to", ["incoming"], "and"),
                cond("team_id", "is_not_present", [], "and"),
                cond("content", "equal_to", [opcao]),
            ],
            "actions": [
                {"action_name": "assign_team", "action_params": [equipes[loja["chave"]]]},
                {"action_name": "send_message", "action_params": [CONFIRMA_LOJA.format(loja=loja["nome"])]},
            ],
        })


def main():
    env = ler_env()
    print("Pessoas…")
    r = rodar_pessoas(env)
    conta, token = r["account_id"], r["admin_token"]
    ids = {p["email"]: p["id"] for p in r["pessoas"]}
    admins = [ids[p["email"]] for p in PESSOAS if p["papel"] == "administrator"]
    cw = Chatwoot(conta, token)

    print("Equipes…")
    equipes = garantir_equipes(cw, ids)

    print("WhatsApp (Evolution)…")
    garantir_instancias(env, conta, token)

    print("Caixas de entrada…")
    caixas = caixas_por_nome(cw)
    for loja in LOJAS:
        caixa = caixas.get(loja["caixa"])
        if not caixa:
            raise SystemExit(f"caixa '{loja['caixa']}' não apareceu no Chatwoot; veja os logs do Evolution")
        membros = admins + [ids[p["email"]] for p in PESSOAS if p["loja"] == loja["chave"]]
        # Saudação pela automação, não pela saudação nativa: a nativa é "template", e o Evolution
        # a regravava como mensagem nova (aparecia duas vezes no painel no teste real de 24/11).
        configurar_caixa(cw, caixa, membros)
        # Dispara na 1ª mensagem recebida de conversa ainda sem equipe (não em conversation_created):
        # no teste real de 24/11 a regra às vezes rodava antes de a mensagem do cliente existir e
        # o Evolution não enviava a saudação (Loja da Praça). Assim ela sempre vem depois.
        garantir_regra(cw, {
            "name": f"{caixa['name']} → equipe {loja['nome']}",
            "description": "1ª mensagem do cliente: boas-vindas e equipe da loja",
            "event_name": "message_created",
            "active": True,
            "conditions": [
                cond("inbox_id", "equal_to", [caixa["id"]], "and"),
                cond("message_type", "equal_to", ["incoming"], "and"),
                cond("team_id", "is_not_present", []),
            ],
            "actions": [
                {"action_name": "send_message", "action_params": [BOAS_VINDAS.format(loja=loja["nome"])]},
                {"action_name": "assign_team", "action_params": [equipes[loja["chave"]]]},
            ],
        })
        print(f"  caixa {caixa['name']}: id {caixa['id']}, membros {membros}")

    print("Instagram…")
    reais = [c for c in caixas.values()
             if c.get("channel_type") in ("Channel::Instagram", "Channel::FacebookPage")]
    # A simulação só existe enquanto o Instagram de verdade não estiver ligado.
    if not reais and CAIXA_SIMULACAO not in caixas:
        caixas[CAIXA_SIMULACAO] = cw("POST", "/inboxes", {
            "name": CAIXA_SIMULACAO, "channel": {"type": "api", "webhook_url": ""},
        })
    if reais and CAIXA_SIMULACAO in caixas:
        print(f"  Instagram real encontrado: apague a caixa '{CAIXA_SIMULACAO}' no painel.")
    instagram = reais or [caixas[CAIXA_SIMULACAO]]
    todos = list(ids.values())
    for caixa in instagram:
        configurar_caixa(cw, caixa, todos, MENU_INSTAGRAM)
        regras_instagram(cw, caixa, equipes)
        print(f"  caixa {caixa['name']}: id {caixa['id']}")

    print("Marca e avatares…")
    avatares = [(caixas[l["caixa"]]["id"], f"caixa-{l['chave']}.png") for l in LOJAS]
    avatares += [(c["id"], "caixa-instagram.png") for c in instagram]
    aplicar_marca(env, avatares)

    linhas = [
        f"Central da equipe: {env.get('PORTAL_URL', PORTAL_PADRAO)}",
        f"Painel: http://chatwoot.localhost:3000  (conta {conta})",
        f"Administrador técnico: {ADMIN_EMAIL} / {env['SENHA_ADMIN']}",
        "",
        "Pessoas (senha inicial; pedir para trocar no 1º acesso):",
    ]
    for p in PESSOAS:
        senha = env["SENHA_ADMIN"] if p["papel"] == "administrator" else env["SENHA_EQUIPE"]
        linhas.append(f"  {p['nome']:<30} {p['email']:<22} {p['papel']:<14} {senha}")
    linhas += ["", f"Evolution (manager): http://127.0.0.1:8080/manager  apikey: {env['AUTHENTICATION_API_KEY']}"]
    arq = RAIZ / "credenciais.txt"
    arq.write_text("\n".join(linhas) + "\n")
    arq.chmod(0o600)
    print("Pronto. Credenciais em credenciais.txt")


if __name__ == "__main__":
    sys.exit(main())
