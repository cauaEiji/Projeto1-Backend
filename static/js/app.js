const API = "/api/eventos";

const formEvento = document.getElementById("form-evento");
const formBusca = document.getElementById("form-busca");
const campoBusca = document.getElementById("busca");
const lista = document.getElementById("lista");
const mensagem = document.getElementById("mensagem");

function mostrarMensagem(texto, tipo) {
  mensagem.textContent = texto;
  mensagem.className = tipo;
}

function formatarData(iso) {
  const [ano, mes, dia] = iso.split("-");
  return `${dia}/${mes}/${ano}`;
}

function criarItem(ev) {
  const li = document.createElement("li");

  const info = document.createElement("div");
  info.className = "info";

  const titulo = document.createElement("strong");
  titulo.textContent = ev.titulo;

  const quando = document.createElement("p");
  quando.textContent = `Dia: ${formatarData(ev.data)}${ev.hora ? " às " + ev.hora : ""}`;

  const local = document.createElement("p");
  local.textContent = `Local: ${ev.local}`;

  info.append(titulo, quando, local);

  if (ev.descricao) {
    const desc = document.createElement("p");
    desc.textContent = ev.descricao;
    info.append(desc);
  }

  const btn = document.createElement("button");
  btn.className = "excluir";
  btn.textContent = "Excluir";
  btn.addEventListener("click", () => excluirEvento(ev.id));

  li.append(info, btn);
  return li;
}

async function carregarEventos(nome = "") {
  const url = nome ? `${API}?nome=${encodeURIComponent(nome)}` : API;
  const resp = await fetch(url);
  const eventos = await resp.json();

  lista.innerHTML = "";
  if (eventos.length === 0) {
    const li = document.createElement("li");
    li.className = "vazio";
    li.textContent = "Nenhum evento encontrado.";
    lista.append(li);
    return;
  }
  eventos.forEach((ev) => lista.append(criarItem(ev)));
}

async function excluirEvento(id) {
  const resp = await fetch(`${API}/${id}`, { method: "DELETE" });
  const dados = await resp.json();
  mostrarMensagem(resp.ok ? "Evento excluído." : dados.erro, resp.ok ? "ok" : "erro");
  carregarEventos(campoBusca.value.trim());
}

formEvento.addEventListener("submit", async (e) => {
  e.preventDefault();
  const evento = {
    titulo: document.getElementById("titulo").value,
    local: document.getElementById("local").value,
    data: document.getElementById("data").value,
    hora: document.getElementById("hora").value,
    descricao: document.getElementById("descricao").value,
  };

  const resp = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(evento),
  });
  const dados = await resp.json();

  if (resp.ok) {
    mostrarMensagem("Evento cadastrado!", "ok");
    formEvento.reset();
    carregarEventos(campoBusca.value.trim());
  } else {
    mostrarMensagem(dados.erro, "erro");
  }
});

formBusca.addEventListener("submit", (e) => {
  e.preventDefault();
  carregarEventos(campoBusca.value.trim());
});

document.getElementById("limpar").addEventListener("click", () => {
  campoBusca.value = "";
  carregarEventos();
});

carregarEventos();
