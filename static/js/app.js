const API_EVENTOS = "/api/eventos";
const ITENS_POR_PAGINA = 5;

const formEvento = document.getElementById("form-evento");
const formBusca = document.getElementById("form-busca");
const campoBusca = document.getElementById("busca");
const lista = document.getElementById("lista");
const mensagem = document.getElementById("mensagem");
const paginacaoEventos = document.getElementById("paginacao-eventos");

function mostrarMensagem(texto, tipo) {
  mensagem.textContent = texto;
  mensagem.className = tipo;
}

function formatarData(iso) {
  const [ano, mes, dia] = iso.split("-");
  return `${dia}/${mes}/${ano}`;
}

function renderPaginacao(container, pagina, onMudarPagina) {
  container.innerHTML = "";
  if (pagina.total_pages <= 1) return;

  const anterior = document.createElement("button");
  anterior.type = "button";
  anterior.textContent = "Anterior";
  anterior.className = "secundario";
  anterior.disabled = pagina.page <= 1;
  anterior.addEventListener("click", () => onMudarPagina(pagina.page - 1));

  const texto = document.createElement("span");
  texto.textContent = `Página ${pagina.page} de ${pagina.total_pages} (${pagina.total} itens)`;

  const proxima = document.createElement("button");
  proxima.type = "button";
  proxima.textContent = "Próxima";
  proxima.className = "secundario";
  proxima.disabled = pagina.page >= pagina.total_pages;
  proxima.addEventListener("click", () => onMudarPagina(pagina.page + 1));

  container.append(anterior, texto, proxima);
}

function criarItemEvento(ev) {
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

async function carregarEventos(nome = "", pagina = 1) {
  const params = new URLSearchParams({ page: pagina, per_page: ITENS_POR_PAGINA });
  if (nome) params.set("nome", nome);

  const resp = await fetch(`${API_EVENTOS}?${params}`);
  const dados = await resp.json();

  lista.innerHTML = "";
  if (!resp.ok) {
    mostrarMensagem(dados.erro, "erro");
    return;
  }

  if (dados.items.length === 0) {
    const li = document.createElement("li");
    li.className = "vazio";
    li.textContent = "Nenhum evento encontrado.";
    lista.append(li);
  } else {
    dados.items.forEach((ev) => lista.append(criarItemEvento(ev)));
  }

  renderPaginacao(paginacaoEventos, dados, (p) => carregarEventos(campoBusca.value.trim(), p));
}

async function excluirEvento(id) {
  const resp = await fetch(`${API_EVENTOS}/${id}`, { method: "DELETE" });
  const dados = await resp.json();
  mostrarMensagem(resp.ok ? "Evento excluído." : dados.erro, resp.ok ? "ok" : "erro");
  carregarEventos(campoBusca.value.trim(), 1);
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

  const resp = await fetch(API_EVENTOS, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(evento),
  });
  const dados = await resp.json();

  if (resp.ok) {
    mostrarMensagem("Evento cadastrado!", "ok");
    formEvento.reset();
    carregarEventos(campoBusca.value.trim(), 1);
  } else {
    mostrarMensagem(dados.erro, "erro");
  }
});

formBusca.addEventListener("submit", (e) => {
  e.preventDefault();
  carregarEventos(campoBusca.value.trim(), 1);
});

document.getElementById("limpar").addEventListener("click", () => {
  campoBusca.value = "";
  carregarEventos("", 1);
});

carregarEventos();
