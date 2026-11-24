// Central do Atendimento. Sem dependências. As rotas /api/* são do nginx (docker/nginx).
"use strict";

const LOJAS = { "loja-baixa": "Loja de Baixo", "loja-praca": "Loja da Praça" };
const ESTADOS = {
  open: { texto: "Conectado", classe: "ok", dica: "Recebendo e enviando mensagens." },
  connecting: { texto: "Conectando", classe: "alerta", dica: "Esperando o celular ler o QR Code." },
  close: { texto: "Desconectado", classe: "erro", dica: "As mensagens deste número não chegam ao painel. Avise o responsável técnico." },
  ausente: { texto: "Não criado", classe: "neutro", dica: "Este número ainda não foi configurado." },
  falha: { texto: "Sem resposta", classe: "erro", dica: "O sistema do WhatsApp não respondeu. O computador e o Docker estão ligados?" },
};
const INTERVALO_SITUACAO = 15000;
const INTERVALO_QR = 5000;
const LIMITE_QR = 3 * 60 * 1000;

async function pedir(url, opcoes = {}, ms = 8000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    const r = await fetch(url, { ...opcoes, signal: ctrl.signal, cache: "no-store" });
    let corpo = null;
    try { corpo = await r.json(); } catch { /* sem corpo JSON */ }
    return { status: r.status, corpo };
  } finally {
    clearTimeout(t);
  }
}

async function estadoDaLoja(loja) {
  try {
    const { status, corpo } = await pedir(`api/status/${loja}`);
    if (status === 404) return "ausente";
    if (status !== 200) return "falha";
    const estado = corpo && corpo.instance && corpo.instance.state;
    return ESTADOS[estado] ? estado : "falha";
  } catch {
    return "falha";
  }
}

function hora() {
  return new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

async function atualizarLojas() {
  await Promise.all(Object.keys(LOJAS).map(async (loja) => {
    const estado = ESTADOS[await estadoDaLoja(loja)];
    const cartao = document.querySelector(`.loja[data-loja="${loja}"]`);
    const selo = cartao.querySelector(".situacao");
    selo.className = `situacao situacao--${estado.classe}`;
    selo.textContent = estado.texto;
    cartao.querySelector(".loja__dica").textContent = estado.dica;
  }));
  document.getElementById("atualizado").textContent = `Atualizado às ${hora()} · a cada 15 s`;
}

async function atualizarPainel() {
  const el = document.getElementById("painel-situacao");
  let ok = false;
  try {
    const { status } = await pedir("api/painel");
    ok = status === 200;
  } catch { /* fora do ar */ }
  el.dataset.estado = ok ? "ok" : "erro";
  el.lastElementChild.textContent = ok ? "Painel no ar" : "Painel fora do ar";
}

function situacaoPeriodica() {
  atualizarLojas();
  atualizarPainel();
  setInterval(() => {
    if (document.visibilityState === "visible") { atualizarLojas(); atualizarPainel(); }
  }, INTERVALO_SITUACAO);
}

// ---- Conectar número (área técnica) ----
const sessao = {
  ler() { try { return sessionStorage.getItem("apikey") || ""; } catch { return ""; } },
  gravar(v) { try { sessionStorage.setItem("apikey", v); } catch { /* sem armazenamento */ } },
  apagar() { try { sessionStorage.removeItem("apikey"); } catch { /* idem */ } },
};

let ciclo = null;

function mostrarEstadoQR(texto, estado) {
  const el = document.getElementById("qr-estado");
  el.textContent = texto;
  if (estado) el.dataset.estado = estado; else delete el.dataset.estado;
}

function pararQR(mensagem, estado) {
  if (ciclo) { clearTimeout(ciclo.timer); ciclo = null; }
  document.getElementById("gerar").disabled = false;
  document.getElementById("parar").hidden = true;
  document.getElementById("loja-qr").disabled = false;
  document.getElementById("qr-img").removeAttribute("src");
  document.getElementById("qr").hidden = true;
  if (mensagem) mostrarEstadoQR(mensagem, estado);
}

async function passoQR() {
  if (!ciclo) return;
  const { loja, chave, inicio } = ciclo;
  if (Date.now() - inicio > LIMITE_QR) {
    pararQR("Tempo esgotado. Clique em “Gerar QR Code” para tentar de novo.");
    return;
  }
  if ((await estadoDaLoja(loja)) === "open") {
    pararQR(`✅ ${LOJAS[loja]} conectada. Confira o número no painel e religue as automações.`, "ok");
    atualizarLojas();
    return;
  }
  try {
    const { status, corpo } = await pedir(`api/conectar/${loja}`, { headers: { apikey: chave } });
    if (status === 401 || status === 403) {
      sessao.apagar();
      pararQR("Chave incorreta. Confira em credenciais.txt.", "erro");
      document.getElementById("chave").focus();
      return;
    }
    if (status === 404) { pararQR("Este número ainda não foi criado. Rode scripts/subir.sh.", "erro"); return; }
    if (corpo && typeof corpo.base64 === "string" && corpo.base64.startsWith("data:image/")) {
      document.getElementById("qr-img").src = corpo.base64;
      document.getElementById("qr").hidden = false;
      mostrarEstadoQR(`QR Code da ${LOJAS[loja]} pronto. Renova a cada ${INTERVALO_QR / 1000} s.`);
    } else {
      mostrarEstadoQR("Esperando o próximo código…");
    }
  } catch {
    mostrarEstadoQR("Sem resposta do sistema do WhatsApp. Tentando de novo…", "erro");
  }
  if (ciclo) ciclo.timer = setTimeout(passoQR, INTERVALO_QR);
}

async function iniciarQR(evento) {
  evento.preventDefault();
  const loja = document.getElementById("loja-qr").value;
  const chave = document.getElementById("chave").value.trim();
  if (!chave) { document.getElementById("chave").focus(); return; }
  sessao.gravar(chave);
  pararQR("Verificando o número…");
  if ((await estadoDaLoja(loja)) === "open") {
    mostrarEstadoQR(`A ${LOJAS[loja]} já está conectada. Para trocar o chip, desconecte antes (docs/OPERACAO.md).`, "ok");
    return;
  }
  ciclo = { loja, chave, inicio: Date.now(), timer: null };
  document.getElementById("gerar").disabled = true;
  document.getElementById("parar").hidden = false;
  document.getElementById("loja-qr").disabled = true;
  mostrarEstadoQR("Gerando o QR Code…");
  passoQR();
}

document.addEventListener("DOMContentLoaded", () => {
  situacaoPeriodica();
  const chave = sessao.ler();
  if (chave) document.getElementById("chave").value = chave;
  document.getElementById("form-conectar").addEventListener("submit", iniciarQR);
  document.getElementById("parar").addEventListener("click", () => pararQR("Parado."));
  document.getElementById("tecnica").addEventListener("toggle", (e) => {
    if (!e.target.open) pararQR();
  });
});
