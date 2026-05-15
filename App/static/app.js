const COLUNAS = {
  produtos: [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "codigo", titulo: "Código" },
    { chave: "categoria", titulo: "Categoria" },
    { chave: "preco", titulo: "Preço" },
    { chave: "quantidade", titulo: "Quantidade" },
    { chave: "valor_total", titulo: "Valor Total" },
    { chave: "data_entrada", titulo: "Data Entrada" },
    { chave: "hora_entrada", titulo: "Hora Entrada" },
    { chave: "data_saida", titulo: "Data Saída" },
    { chave: "hora_saida", titulo: "Hora Saída" },
    { chave: "updated_at", titulo: "Alteração" },
    { chave: "acoes", titulo: "Ações" },
  ],
  categorias: [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
  ],
  funcionarios: [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "email", titulo: "Email" },
    { chave: "cargo", titulo: "Cargo" },
  ],
};

const TITULOS = {
  produtos: { lista: "Produtos", form: "Novo produto" },
  categorias: { lista: "Categorias", form: "Nova categoria" },
  funcionarios: { lista: "Funcionários", form: "Novo funcionário" },
};

const CAMPOS = {
  produtos: [
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
    { nome: "codigo", rotulo: "Código", obrigatorio: true },
    { nome: "id_categoria", rotulo: "Categoria", tipo: "select", origem: "categorias" },
    { nome: "preco", rotulo: "Preço", tipo: "number" },
    { nome: "quantidade", rotulo: "Quantidade", tipo: "number" },
    { nome: "entrada", rotulo: "Entrada", tipo: "number", placeholder: "Quantidade que entra" },
    { nome: "saida", rotulo: "Saída", tipo: "number", placeholder: "Quantidade que sai" },
    { nome: "data_entrada", rotulo: "Data Entrada (Auto)", tipo: "datetime-local" },
    { nome: "hora_entrada", rotulo: "Hora Entrada (Auto)", tipo: "time" },
    { nome: "data_saida", rotulo: "Data Saída (Auto)", tipo: "datetime-local" },
    { nome: "hora_saida", rotulo: "Hora Saída (Auto)", tipo: "time" },
    { nome: "descricao", rotulo: "Descrição", tipo: "text" },
  ],
  categorias: [
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
  ],
  funcionarios: [
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
    { nome: "email", rotulo: "Email", tipo: "email", obrigatorio: true },
    { nome: "cargo", rotulo: "Cargo" },
    { nome: "senha", rotulo: "Senha", tipo: "password", obrigatorio: true },
  ],
};



const elementoStatus = document.getElementById("status");
const elementoTituloLista = document.getElementById("titulo-lista");
const elementoTituloFormulario = document.getElementById("titulo-formulario");
const elementoCabecalho = document.getElementById("cabecalho");
const elementoCorpo = document.getElementById("corpo");
const elementoCampos = document.getElementById("campos");
const formulario = document.getElementById("formulario");
const mensagemFormulario = document.getElementById("mensagem-formulario");
const botaoRecarregar = document.getElementById("botao-recarregar");
const abas = document.querySelectorAll(".aba");

let tipoAtual = "produtos";
let editandoId = null;

async function buscar(tipo) {
  const resposta = await fetch(`/api/${tipo}`);
  if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
  return resposta.json();
}

async function carregar(tipo) {
  tipoAtual = tipo;
  elementoTituloLista.textContent = TITULOS[tipo].lista;
  elementoTituloFormulario.textContent = TITULOS[tipo].form;
  limparMensagem();

  await renderizarFormulario(tipo);
  renderizarCabecalho(tipo);
  elementoCorpo.innerHTML = "";

  elementoStatus.classList.remove("erro");
  elementoStatus.textContent = "Carregando...";

  try {
    const dados = await buscar(tipo);
    renderizarLinhas(tipo, dados);
    elementoStatus.textContent = `${dados.length} registro(s) carregado(s).`;
  } catch (erro) {
    elementoStatus.textContent = `Falha ao carregar: ${erro.message}`;
    elementoStatus.classList.add("erro");
  }
}

function renderizarCabecalho(tipo) {
  elementoCabecalho.innerHTML = "";
  for (const coluna of COLUNAS[tipo]) {
    const th = document.createElement("th");
    th.textContent = coluna.titulo;
    elementoCabecalho.appendChild(th);
  }
}

function renderizarLinhas(tipo, dados) {
  if (!dados.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = COLUNAS[tipo].length;
    td.className = "vazio";
    td.textContent = "Nenhum registro encontrado.";
    tr.appendChild(td);
    elementoCorpo.appendChild(tr);
    return;
  }

  for (const item of dados) {
    const tr = document.createElement("tr");
    for (const coluna of COLUNAS[tipo]) {
      const td = document.createElement("td");
      if (coluna.chave === "acoes") {
        if (tipo === "produtos") {
          const btnEditar = document.createElement("button");
          btnEditar.textContent = "✏️ Editar";
          btnEditar.className = "btn-acao btn-editar";
          btnEditar.onclick = () => editarItem(item.id);
          td.appendChild(btnEditar);

          const btnApagar = document.createElement("button");
          btnApagar.textContent = "🗑️ Apagar";
          btnApagar.className = "btn-acao btn-apagar";
          btnApagar.onclick = () => deletarItem(item.id);
          td.appendChild(btnApagar);
        }
      } else {
        const valor = item[coluna.chave];
        let textoExibir = "—";
        if (valor !== null && valor !== undefined) {
          if (coluna.chave === "data_entrada" || coluna.chave === "data_saida" || coluna.chave === "updated_at") {
            textoExibir = new Date(valor).toLocaleDateString("pt-BR");
          } else if (coluna.chave === "preco" || coluna.chave === "valor_total") {
            textoExibir = parseFloat(valor).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
          } else {
            textoExibir = valor;
          }
        }
        td.textContent = textoExibir;
      }
      tr.appendChild(td);
    }
    elementoCorpo.appendChild(tr);
  }
}

async function renderizarFormulario(tipo) {
  elementoCampos.innerHTML = "";
  for (const campo of CAMPOS[tipo]) {
    const wrapper = document.createElement("div");
    wrapper.className = "campo";

    const label = document.createElement("label");
    label.htmlFor = `campo-${campo.nome}`;
    label.textContent = campo.rotulo + (campo.obrigatorio ? " *" : "");
    wrapper.appendChild(label);

    if (campo.tipo === "select") {
      const select = document.createElement("select");
      select.id = `campo-${campo.nome}`;
      select.name = campo.nome;
      if (campo.obrigatorio) select.required = true;

      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = "Selecione...";
      select.appendChild(placeholder);

      try {
        const itens = await buscar(campo.origem);
        for (const item of itens) {
          const option = document.createElement("option");
          option.value = item.id;
          option.textContent = rotuloItem(campo.origem, item);
          select.appendChild(option);
        }
      } catch (erro) {
        const option = document.createElement("option");
        option.disabled = true;
        option.textContent = `Erro ao carregar: ${erro.message}`;
        select.appendChild(option);
      }

      wrapper.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.type = campo.tipo || "text";
      input.id = `campo-${campo.nome}`;
      input.name = campo.nome;
      if (campo.obrigatorio) input.required = true;
      if (campo.placeholder) input.placeholder = campo.placeholder;
      
      // Desabilitar campos de data/hora que são preenchidos automaticamente
      if (campo.nome.includes("data_") || campo.nome.includes("hora_")) {
        input.disabled = true;
        input.title = "Preenchido automaticamente ao registrar entrada/saída";
      }
      
      wrapper.appendChild(input);
    }

    elementoCampos.appendChild(wrapper);
  }
}

function rotuloItem(origem, item) {
  if (item.nome) return `${item.nome}`;
  return `${item.id}`;
}

function limparMensagem() {
  mensagemFormulario.textContent = "";
  mensagemFormulario.classList.remove("sucesso", "erro");
}

async function enviarFormulario(evento) {
  evento.preventDefault();
  limparMensagem();

  const dados = {};
  for (const campo of CAMPOS[tipoAtual]) {
    const elemento = formulario.elements[campo.nome];
    const valor = elemento.value.trim();
    if (campo.obrigatorio && !valor) {
      mensagemFormulario.textContent = `Preencha ${campo.rotulo}.`;
      mensagemFormulario.classList.add("erro");
      elemento.focus();
      return;
    }
    if (valor !== "") dados[campo.nome] = valor;
  }

  // Preencher automaticamente data e hora para entrada/saída
  if (tipoAtual === "produtos") {
    const agora = new Date();
    
    // Se tem entrada, preencher data_entrada e hora_entrada
    if (dados.entrada && !dados.data_entrada) {
      dados.data_entrada = agora.toISOString();
      dados.hora_entrada = agora.toTimeString().slice(0, 5);
    }
    
    // Se tem saída, preencher data_saida e hora_saida
    if (dados.saida && !dados.data_saida) {
      dados.data_saida = agora.toISOString();
      dados.hora_saida = agora.toTimeString().slice(0, 5);
    }
  }

  const botao = formulario.querySelector("button[type=submit]");
  botao.disabled = true;
  try {
    const method = editandoId ? "PUT" : "POST";
    const url = editandoId ? `/api/${tipoAtual}/${editandoId}` : `/api/${tipoAtual}`;
    const resposta = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const corpo = await resposta.json().catch(() => ({}));
    if (!resposta.ok) {
      throw new Error(corpo.erro || `HTTP ${resposta.status}`);
    }

    const acao = editandoId ? "Atualizado" : "Cadastrado";
    mensagemFormulario.textContent = `${acao} com sucesso.`;
    mensagemFormulario.classList.add("sucesso");
    formulario.reset();
    if (editandoId) {
      editandoId = null;
      elementoTituloFormulario.textContent = TITULOS[tipoAtual].form;
      botao.textContent = "Cadastrar";
    }
    await carregar(tipoAtual);
  } catch (erro) {
    mensagemFormulario.textContent = erro.message;
    mensagemFormulario.classList.add("erro");
  } finally {
    botao.disabled = false;
  }
}

async function editarItem(id) {
  try {
    const resposta = await fetch(`/api/${tipoAtual}/${id}`);
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    const item = await resposta.json();

    // Populate form
    for (const campo of CAMPOS[tipoAtual]) {
      const elemento = formulario.elements[campo.nome];
      if (elemento) {
        elemento.value = item[campo.nome] || "";
      }
    }

    editandoId = id;
    elementoTituloFormulario.textContent = `Editar ${TITULOS[tipoAtual].form.split(" ")[1]}`;
    formulario.querySelector("button[type=submit]").textContent = "Atualizar";
    limparMensagem();
  } catch (erro) {
    alert(`Erro ao carregar item: ${erro.message}`);
  }
}

async function deletarItem(id) {
  if (!confirm("Tem certeza que deseja apagar este item?")) return;

  try {
    const resposta = await fetch(`/api/${tipoAtual}/${id}`, {
      method: "DELETE",
    });
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    await carregar(tipoAtual);
  } catch (erro) {
    alert(`Erro ao apagar: ${erro.message}`);
  }
}

abas.forEach((aba) => {
  aba.addEventListener("click", () => {
    abas.forEach((a) => a.classList.remove("ativa"));
    aba.classList.add("ativa");
    carregar(aba.dataset.tipo);
  });
});

botaoRecarregar.addEventListener("click", () => carregar(tipoAtual));
formulario.addEventListener("submit", enviarFormulario);

carregar("produtos");
