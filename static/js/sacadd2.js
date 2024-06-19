/*!
  * Sistema de Apoio às CADDs
  * Copyright 2018
  */

// para o form plano de estudos e plano de estudos cadastrados
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text/html");
  if(ev.target.parentNode.id == ""){
    exit();
  }
  ev.target.parentNode.appendChild(document.getElementById(data));
}

function dropparent(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text/html");
  ev.target.parentNode.parentNode.appendChild(document.getElementById(data));
}

function preencherDisciplinas(){
  var listaDeDisciplinas = document.getElementsByClassName("lista-de-disciplinas");
  var i;
  var y;
  for (i = 0; i < listaDeDisciplinas.length; i++) {
    var periodo = listaDeDisciplinas[i].parentNode.parentNode.parentNode.children[0].children[0].children[0].innerHTML;
    listaDeItens = listaDeDisciplinas[i].getElementsByClassName("item_disc_disciplinas");
    for (y = 0; y < listaDeItens.length; y++) {
      var hiddenText = document.getElementById("discip").value;
      document.getElementById("discip").value = ((hiddenText!="") ? "_" : "") + periodo.trim() + "#" + listaDeItens[y].id;
    }
  }
}
