/*!
  * Sistema de Apoio às CADDs
  * Copyright 2018
  */

window.onload = function calcularTotalCadds(){
  var totalCadds = document.getElementById("bloco-central-lista").childElementCount;
  document.getElementById("total-cadds-value").innerHTML = totalCadds;
}

function visualizarCADD(e){
  var idComissao = e.target.parentNode.parentNode.id;
  var nomeComissao = e.target.parentNode.parentNode.getElementsByClassName("nome-comissao");
  nomeComissao = nomeComissao[0].innerHTML;
  var descricaoComissao = e.target.parentNode.parentNode.getElementsByClassName("descricao-comissao");
  descricaoComissao = descricaoComissao[0].innerHTML;

  document.getElementById("id").value = idComissao;
  document.getElementById("nome-cadd").value = nomeComissao;
  document.getElementById("nome-cadd").disabled = true;
  document.getElementById("descricao-cadd").value = descricaoComissao;
  document.getElementById("descricao-cadd").disabled = true;
}

function editarCADD(e){
  var idComissao = e.target.parentNode.previousElementSibling.getElementsByClassName("id-comissao")[0];
  var nomeComissao = e.target.parentNode.previousElementSibling.getElementsByClassName("nome-cadd")[0];
  var descricaoComissao = e.target.parentNode.previousElementSibling.getElementsByClassName("descricao-cadd")[0];

  var botaoEditar = e.target;
  var botaoSalvar = e.target.nextElementSibling;

  nomeComissao.disabled = false;
  descricaoComissao.disabled = false;
  botaoEditar.disabled = true;
  botaoEditar.className = "botao-padrao botao-cinza";
  botaoSalvar.disabled = false;
  botaoSalvar.className = "botao-padrao botao-verde";
}

function cancelarEdicao(e){
  var botaoEditar = e.target.parentNode.parentNode.parentNode.children[2].children[0];
  // if (botaoEditar.id = "xcancelar"){
  //   botaoEditar.children[2].children[0];
  // }
  // else{
  //   botaoEditar = e.target.parentNode.parentNode.children[2].children[0];
  // }
  var botaoSalvar = e.target.parentNode.parentNode.parentNode.children[2].children[1];
  botaoEditar.disabled = false;
  botaoEditar.className = "botao-padrao botao-azul";
  botaoSalvar.disabled = true;
  botaoSalvar.className = "botao-padrao botao-cinza";
}

function editarMembro(e){
  var membroID = e.target.parentNode.parentNode.id;
  var nomeMembro = e.target.parentNode.parentNode.getElementsByClassName("nome-membro")[0].innerHTML;
  var portaria = e.target.parentNode.parentNode.getElementsByClassName("portaria")[0].innerHTML;
  var presidente = e.target.parentNode.parentNode.getElementsByClassName("presidente")[0].innerHTML;
  var ativo = e.target.parentNode.parentNode.getElementsByClassName("ativo")[0].innerHTML;

  document.getElementById("id-membro-edit").value = membroID;
  document.getElementById("nome-membro-edit").value = nomeMembro;
  document.getElementById("portaria-edit").value = portaria;
  if (presidente === "Sim") {
    document.getElementById("presidente-edit").checked = true;
  }else{
    document.getElementById("presidente-edit").checked = false;
  }
  if (ativo === "Sim") {
    document.getElementById("ativo-edit").checked = true;
  }else{
    document.getElementById("ativo-edit").checked = false;
  }
}

function submitCriarCaddForm(){
  document.getElementById("criarCaddForm").submit();
}

function submitExcluirMembroForm(e){
  var membro = e.target.parentNode.parentNode;
  var membroID = membro.id;
  document.getElementById("membroParaExcluir").value = "membroID";
  document.getElementById("fomrTempExcluirMembro").submit();
}

function submitEditarMembrosForm(){
  document.getElementById("editarMembroForm").submit();
}

function submitEditarComissaoForm(){
  document.getElementById("editarComissaoForm").submit();
}

function submitExcluirComissaoForm(e){
  var comissao = e.target.parentNode.parentNode;
  var comissaoID = comissao.id;
  document.getElementById("comissaoParaExcluir").value = "comissaoID";
  document.getElementById("fomrTempExcluirComissao").submit();
}
