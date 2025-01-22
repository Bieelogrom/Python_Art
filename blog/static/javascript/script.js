
document.addEventListener('DOMContentLoaded', function(){
    let input_senha = document.getElementById("id_password")
    let botao_teste = document.getElementById("botao_teste")

    input_senha.addEventListener("input", function(){
        const senha = this.value;
        const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch('/validar_senha/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrf,
            },
            body: new URLSearchParams({ password: senha })
        })
        .then(response => response.json())
        .then(data => {
            var texto = document.getElementById("Erros")
            if(data.valido){
                texto.innerHTML = "<p class='text-success'>Senha válida!</p>"
            }else{
                texto.innerHTML = '<ul class=>' + data.erros.map(e => `<li class='text-danger'>${e}</li>`).join('') + '</ul>';
            }
        })
    })
})