const COLUNAS = {

  produtos: [
    { chave: "id", titulo: "ID" },
    {chave:"imagem", titulo:"Imagem"},
    { chave: "nome", titulo: "Nome" },
    { chave: "codigo", titulo: "Código" },
    { chave: "categoria", titulo: "Categoria" },
    { chave: "preco", titulo: "Preço" },
    { chave: "quantidade", titulo: "Quantidade" },
    { chave: "status", titulo: "Status" },
    { chave: "descricao", titulo: "Descrição" },
    { chave: "data", titulo: "Data" },
    { chave: "hora", titulo: "Hora" },
    { chave: "updated_at", titulo: "Alteração" },
    { chave: "valor_total", titulo: "Valor Total" },
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

  movimentos: [
    { chave: "id", titulo: "ID" },
    {chave: "imagem", titulo:"Imagem"},
    { chave: "nome_produto", titulo: "Nome do Produto" },
    { chave: "categoria", titulo: "Categoria" },
    { chave: "acao", titulo: "Ação" },
    { chave: "quantidade", titulo: "Quantidade" },
    { chave: "data", titulo: "Data" },
    { chave: "hora", titulo: "Hora" },
    { chave: "info", titulo: "Detalhes" },
  ],
};

const TITULOS = {
  produtos: { lista: "Produtos", form: "Novo produto" },
  categorias: { lista: "Categorias", form: "Nova categoria" },
  funcionarios: { lista: "Funcionários", form: "Novo funcionário" },
  movimentos: { lista: "Movimentações", form: "Movimentação" },
};

const STATUS_OPCOES = [
  { valor: "ativo", rotulo: "Ativo" },
  { valor: "inativo", rotulo: "Inativo" },
];

const CAMPOS = {
  produtos: [
    { nome: "imagem", rotulo: "Imagem", tipo: "file" },
    { nome: "nome", rotulo: "Nome", obrigatorio: true },
    { nome: "codigo", rotulo: "Código", obrigatorio: true },
    { nome: "id_categoria", rotulo: "Categoria", tipo: "select", origem: "categorias" },
    { nome: "preco", rotulo: "Preço", tipo: "number" },
    { nome: "quantidade", rotulo: "Quantidade", tipo: "number" },
    { nome: "status", rotulo: "Status", tipo: "select", origem: "status" },
    { nome: "data", rotulo: "Data (Auto)", tipo: "datetime-local" },
    { nome: "hora", rotulo: "Hora (Auto)", tipo: "time" },
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

const MOVIMENTOS_KEY = "movimentos_log";



const elementoStatus = document.getElementById("status");
const elementoTituloLista = document.getElementById("titulo-lista");
const elementoTituloFormulario = document.getElementById("titulo-formulario");
const elementoCabecalho = document.getElementById("cabecalho");
const elementoCorpo = document.getElementById("corpo");
const elementoCampos = document.getElementById("campos");
const formulario = document.getElementById("formulario");
const mensagemFormulario = document.getElementById("mensagem-formulario");
const botaoRecarregar = document.getElementById("botao-recarregar");
const filtroStatus = document.getElementById("filtro-status");
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

  if (filtroStatus) {
    filtroStatus.parentElement.style.display = tipo === "produtos" ? "flex" : "none";
  }

  document.getElementById("painel-formulario").style.display = tipo === "movimentos" ? "none" : "block";

  await renderizarFormulario(tipo);
  renderizarCabecalho(tipo);
  elementoCorpo.innerHTML = "";

  elementoStatus.classList.remove("erro");
  elementoStatus.textContent = "Carregando...";

  try {
    const dados = tipo === "movimentos" ? obterMovimentos() : await buscar(tipo);
    const dadosFiltrados = tipo === "produtos" && filtroStatus && filtroStatus.value
      ? dados.filter((item) => item.status === filtroStatus.value)
      : dados;
    renderizarLinhas(tipo, dadosFiltrados);
    elementoStatus.textContent = `${dadosFiltrados.length} registro(s) carregado(s).`;
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

      if (coluna.chave === "imagem" && item[coluna.chave]) {
        const img = document.createElement("img");
        img.src = item[coluna.chave];
        img.width = 50;
        img.height = 50;
        img.style.objectFit = "cover";
        img.style.borderRadius = "6px";
        td.appendChild(img);
        tr.appendChild(td);
        continue;
      }

      if (coluna.chave === "acoes") {
        if (tipo === "produtos") {
          const btnRetirar = document.createElement("button");
          btnRetirar.textContent = "➖ Retirar";
          btnRetirar.className = "btn-acao btn-retirar";
          btnRetirar.disabled = item.quantidade <= 0;
          btnRetirar.title = item.quantidade > 0 ? "Retirar produto" : "Sem estoque";
          btnRetirar.onclick = () => retirarProduto(item.id);
          td.appendChild(btnRetirar);

          const btnEditar = document.createElement("button");
          btnEditar.textContent = "✏️ Editar";
          btnEditar.className = "btn-acao btn-editar";
          btnEditar.onclick = () => editarItem(item.id);
          td.appendChild(btnEditar);
        }
      } else {
        let valor = item[coluna.chave];
        if (tipo === "movimentos") {
          if (coluna.chave === "produto") {
            valor = item.produto;
          } else if (coluna.chave === "data") {
            valor = item.data;
          } else if (coluna.chave === "hora") {
            valor = item.hora;
          } else if (coluna.chave === "info") {
            valor = item.info;
          }
        }

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
  if (tipo === "movimentos") {
    return;
  }
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

      if (campo.origem === "status") {
        for (const status of STATUS_OPCOES) {
          const option = document.createElement("option");
          option.value = status.valor;
          option.textContent = status.rotulo;
          select.appendChild(option);
        }
      } else {
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
      }

      wrapper.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.type = campo.tipo || "text";
      if (campo.tipo === "file") {
        input.accept = "image/*";
      }
      input.id = `campo-${campo.nome}`;
      input.name = campo.nome;
      if (campo.obrigatorio) input.required = true;
      if (campo.placeholder) input.placeholder = campo.placeholder;
      
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

function lerArquivoComoDataURL(arquivo) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(arquivo);
  });
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
    if (campo.tipo === "file") {
      const arquivo = elemento.files[0];
      if (campo.obrigatorio && !arquivo) {
        mensagemFormulario.textContent = `Preencha ${campo.rotulo}.`;
        mensagemFormulario.classList.add("erro");
        elemento.focus();
        return;
      }
      if (arquivo) {
        dados[campo.nome] = await lerArquivoComoDataURL(arquivo);
      }
      continue;
    }
    const valor = elemento.value.trim();
    if (campo.obrigatorio && !valor) {
      mensagemFormulario.textContent = `Preencha ${campo.rotulo}.`;
      mensagemFormulario.classList.add("erro");
      elemento.focus();
      return;
    }
    // Validação específica para preço
    if (campo.nome === "preco" && valor !== "") {
      // Não permite letras, nem número negativo
      if (!/^(\d+)([\.,]\d{1,2})?$/.test(valor) || parseFloat(valor.replace(',', '.')) < 0) {
        mensagemFormulario.textContent = "Digite um preço válido e positivo.";
        mensagemFormulario.classList.add("erro");
        elemento.focus();
        return;
      }
    }
    if (valor !== "") dados[campo.nome] = valor;
  }

  // Preencher automaticamente data e hora para entrada/saída
  if (tipoAtual === "produtos") {
  const agora = new Date();

  // Produto novo
  if (!editandoId) {
    dados.data_entrada = agora.toISOString();
    dados.hora_entrada = agora.toTimeString().slice(0, 5);
  }

  // Produto editado
  if (editandoId) {
    dados.updated_at = agora.toISOString();
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
    const item = corpo;

    const acao = editandoId ? "Atualizado" : "Cadastrado";
    mensagemFormulario.textContent = `${acao} com sucesso.`;
    mensagemFormulario.classList.add("sucesso");
    formulario.reset();
    let eraEdicao = false;
    if (editandoId) {
      eraEdicao = true;
      editandoId = null;
      elementoTituloFormulario.textContent = TITULOS[tipoAtual].form;
      botao.textContent = "Cadastrar";
    }
    if (tipoAtual === "produtos") {
      let movimentoTipo = "entrada";
      let infoExtra = "";
      if (eraEdicao) {
        movimentoTipo = "editar";
        infoExtra = "Produto alterado";
      }
      if (eraEdicao && dados.saida) {
        movimentoTipo = "saida";
        infoExtra = `${dados.saida} unidade(s) removida(s)`;
      } else if (eraEdicao && dados.entrada) {
        movimentoTipo = "entrada";
        infoExtra = `${dados.entrada} unidade(s) adicionada(s)`;
      }
      registrarMovimento(item, movimentoTipo, dados, infoExtra);
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

async function retirarProduto(id) {
  try {
    const respostaProduto = await fetch(`/api/produtos/${id}`);
    if (!respostaProduto.ok) throw new Error(`HTTP ${respostaProduto.status}`);

    const produto = await respostaProduto.json();
    const quantidadeAtual = Number(produto.quantidade || 0);

    if (quantidadeAtual <= 0) {
      alert("Não é possível retirar: estoque vazio.");
      return;
    }
    const quantidadeRetirada = Number(prompt("Quantas unidades você deseja retirar?", "1"));
    if (!Number.isInteger(quantidadeRetirada) || quantidadeRetirada <= 0) {
      alert("Informe um número válido de unidades para retirar.");
      return;
    }
    if (quantidadeRetirada > quantidadeAtual) {
      alert("A quantidade solicitada é maior que o estoque disponível.");
      return;
    }


    const agora = new Date();
    const dadosAtualizados = {
      quantidade: quantidadeAtual - quantidadeRetirada,
      saida: quantidadeRetirada,
      data_saida: agora.toISOString(),
      hora_saida: agora.toTimeString().slice(0, 5),
    };

    const resposta = await fetch(`/api/produtos/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dadosAtualizados),
    });
    const corpo = await resposta.json().catch(() => ({}));
    if (!resposta.ok) {
      throw new Error(corpo.erro || `HTTP ${resposta.status}`);
    }

    const itemAtualizado = corpo;
    registrarMovimento(itemAtualizado, "saida", { saida: quantidadeRetirada });
    await carregar(tipoAtual);
  } catch (erro) {
    alert(`Erro ao retirar produto: ${erro.message}`);
  }
}

function obterMovimentos() {
  return JSON.parse(localStorage.getItem(MOVIMENTOS_KEY) || "[]");
}

function salvarMovimento(movimento) {
  const movimentos = obterMovimentos();
  movimentos.unshift(movimento);
  localStorage.setItem(MOVIMENTOS_KEY, JSON.stringify(movimentos.slice(0, 50)));
}

function registrarMovimento(item, acao, dados = {}, infoExtra = "") {
  if (!item) return;

  // Prioridade de timestamp: data_saida, data_entrada, updated_at, agora
  let dataMov = null;
  if (item.data_saida) {
    dataMov = new Date(item.data_saida);
  } else if (item.data_entrada) {
    dataMov = new Date(item.data_entrada);
  } else if (item.updated_at) {
    dataMov = new Date(item.updated_at);
  } else {
    dataMov = new Date();
  }

  const quantidade = Number(dados.entrada || dados.saida || dados.quantidade || 0);

  let acaoExibir = "";
  let infoDefault = "";

  // CADASTRO
  if (acao === "entrada") {
    acaoExibir = "Entrada";
    infoDefault = "Produto cadastrado";
  }

  // EDIÇÃO
  else if (acao === "editar") {
    acaoExibir = "Editar";
    infoDefault = "Produto editado";
  }

  // RETIRADA
  else if (acao === "saida") {
    acaoExibir = "Saída";
    infoDefault = "Produto saída";
  }

  const movimento = {
    id: item.id,
    imagem: item.imagem || null,
    nome_produto: item.nome || `ID ${item.id}`,
    categoria: item.categoria || "-",
    acao: acaoExibir,
    quantidade: dados.quantidade || dados.saida || "-",
    data: dataMov.toLocaleDateString("pt-BR"),
    hora: dataMov.toTimeString().slice(0, 5),
    info: infoExtra || infoDefault,
  };

  salvarMovimento(movimento);
}

abas.forEach((aba) => {
  aba.addEventListener("click", () => {
    abas.forEach((a) => a.classList.remove("ativa"));
    aba.classList.add("ativa");
    carregar(aba.dataset.tipo);
  });
});

botaoRecarregar.addEventListener("click", () => carregar(tipoAtual));
if (filtroStatus) {
  filtroStatus.addEventListener("change", () => carregar(tipoAtual));
}
formulario.addEventListener("submit", enviarFormulario);

carregar("produtos");
