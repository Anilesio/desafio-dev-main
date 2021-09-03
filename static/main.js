const actualBtn = document.getElementById('id_file');

const fileChosen = document.getElementById('file-chosen');

actualBtn.addEventListener('change', function() {
    fileChosen.textContent = this.files[0].name
})

var botao = document.getElementById('btSubmit')
function funcaoCarregamento(){
  botao.innerText = "Aguarde..."
}
