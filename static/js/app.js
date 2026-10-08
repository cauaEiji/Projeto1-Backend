const API_EVENTOS = "/api/eventos";
const API_USUARIOS = "/api/usuarios";
const ITENS_POR_PAGINA = 5;

let usuarioAtual = null;
let perfilAbertoId = null;

const formUsuario = document.getElementById("form-usuario");
const areaUsuario = document.getElementById("area-usuario");
const usuarioAtualTexto = document.getElementById("usuario-atual");
const meusEventos = document.getElementById("meus-eventos");
const paginacaoMeus = document.getElementById("paginacao-meus");
const mensagemUsuario = document.getElementById("mensagem-usuario");
const secaoEvento = document.getElementById("secao-evento");

const formEvento = document.getElementById("form-evento");
const formBusca = document.getElementById("form-busca");
const campoBusca = document.getElementById("busca");
const lista = document.getElementById("lista");
const mensagem = document.getElementById("mensagem");
const paginacaoEventos = document.getElementById("paginacao-eventos");

const formUsuarios = document.getElementById("form-usuarios");
const listaUsuarios = document.getElementById("lista-usuarios");
const perfil = document.getElementById("perfil");

function mostrarMensagem(texto, tipo, elemento = mensagem) {
  elemento.textContent = texto;
  elemento.className = tipo;
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

  const autor = document.createElement("p");
  const linkAutor = document.createElement("a");
  linkAutor.href = "#perfil";
  linkAutor.className = "autor";
  linkAutor.textContent = ev.autor;
  linkAutor.addEventListener("click", (e) => {
    e.preventDefault();
    abrirPerfil(ev.usuario_id);
  });
  autor.append("Autor: ", linkAutor);

  info.append(titulo, quando, local, autor);

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

function renderEventos(ul, eventos) {
  ul.innerHTML = "";
  if (eventos.length === 0) {
    const li = document.createElement("li");
    li.className = "vazio";
    li.textContent = "Nenhum evento encontrado.";
    ul.append(li);
  } else {
    eventos.forEach((ev) => ul.append(criarItemEvento(ev)));
  }
}

async function carregarEventos(nome = "", pagina = 1) {
  const params = new URLSearchParams({ page: pagina, per_page: ITENS_POR_PAGINA });
  if (nome) params.set("nome", nome);

  const resp = await fetch(`${API_EVENTOS}?${params}`);
  const dados = await resp.json();

  if (!resp.ok) {
    mostrarMensagem(dados.erro, "erro");
    return;
  }

  renderEventos(lista, dados.items);
  renderPaginacao(paginacaoEventos, dados, (p) => carregarEventos(campoBusca.value.trim(), p));
}

async function carregarMeusEventos(pagina = 1) {
  if (!usuarioAtual) return;

  const params = new URLSearchParams({ page: pagina, per_page: ITENS_POR_PAGINA });
  const resp = await fetch(`${API_USUARIOS}/${usuarioAtual.id}/eventos?${params}`);
  const dados = await resp.json();

  renderEventos(meusEventos, dados.items);
  renderPaginacao(paginacaoMeus, dados, (p) => carregarMeusEventos(p));
}

async function buscarUsuarios(nome) {
  const resp = await fetch(`${API_USUARIOS}/busca/${encodeURIComponent(nome)}`);
  const usuarios = await resp.json();

  listaUsuarios.innerHTML = "";
  if (usuarios.length === 0) {
    const li = document.createElement("li");
    li.className = "vazio";
    li.textContent = "Nenhum usuário encontrado.";
    listaUsuarios.append(li);
    return;
  }

  usuarios.forEach((u) => {
    const li = document.createElement("li");

    const info = document.createElement("div");
    info.className = "info";
    const nomeUsuario = document.createElement("strong");
    nomeUsuario.textContent = u.nome;
    const email = document.createElement("p");
    email.textContent = u.email;
    info.append(nomeUsuario, email);

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Ver perfil";
    btn.addEventListener("click", () => abrirPerfil(u.id));

    li.append(info, btn);
    listaUsuarios.append(li);
  });
}

async function abrirPerfil(id) {
  const resp = await fetch(`${API_USUARIOS}/${id}`);
  const dados = await resp.json();
  if (!resp.ok) return;

  perfilAbertoId = id;
  document.getElementById("perfil-nome").textContent = dados.nome;
  document.getElementById("perfil-email").textContent = dados.email;
  document.getElementById("perfil-total").textContent = `Eventos publicados: ${dados.total_eventos}`;
  renderEventos(document.getElementById("perfil-eventos"), dados.eventos);

  perfil.hidden = false;
  document.getElementById("secao-usuarios").scrollIntoView({ behavior: "smooth" });
}

function atualizarListas() {
  carregarMeusEventos(1);
  carregarEventos(campoBusca.value.trim(), 1);
  if (!perfil.hidden) abrirPerfil(perfilAbertoId);
}

async function excluirEvento(id) {
  const resp = await fetch(`${API_EVENTOS}/${id}`, { method: "DELETE" });
  const dados = await resp.json();
  mostrarMensagem(resp.ok ? "Evento excluído." : dados.erro, resp.ok ? "ok" : "erro");
  atualizarListas();
}

formUsuario.addEventListener("submit", async (e) => {
  e.preventDefault();
  const usuario = {
    nome: document.getElementById("usuario-nome").value,
    email: document.getElementById("usuario-email").value,
  };

  const resp = await fetch(API_USUARIOS, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(usuario),
  });
  const dados = await resp.json();

  if (!resp.ok) {
    mostrarMensagem(dados.erro, "erro", mensagemUsuario);
    return;
  }

  usuarioAtual = dados;
  usuarioAtualTexto.textContent = `Olá, ${dados.nome} (${dados.email}). Seus eventos:`;
  mostrarMensagem(resp.status === 201 ? "Usuário cadastrado!" : "", "ok", mensagemUsuario);
  formUsuario.reset();
  formUsuario.hidden = true;
  areaUsuario.hidden = false;
  secaoEvento.hidden = false;
  carregarMeusEventos(1);
});

document.getElementById("sair").addEventListener("click", () => {
  usuarioAtual = null;
  formUsuario.hidden = false;
  areaUsuario.hidden = true;
  secaoEvento.hidden = true;
  mostrarMensagem("", "", mensagemUsuario);
});

formEvento.addEventListener("submit", async (e) => {
  e.preventDefault();
  const evento = {
    usuario_id: usuarioAtual.id,
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
    atualizarListas();
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

formUsuarios.addEventListener("submit", (e) => {
  e.preventDefault();
  buscarUsuarios(document.getElementById("busca-usuario").value.trim());
});

document.getElementById("fechar-perfil").addEventListener("click", () => {
  perfil.hidden = true;
  perfilAbertoId = null;
});

carregarEventos();
