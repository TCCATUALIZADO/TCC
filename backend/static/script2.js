function adicionarItem(){
    let nome = document.getElementById("nomeItem").value;
    let quantidade = document.getElementById("quantidadeItem").value;

    let estoque = JSON.parse(localStorage.getItem("estoque")) || [];

    estoque.push({
        nome: nome,
        quantidade: quantidade
    });

    localStorage.setItem("estoque", JSON.stringify(estoque));
    alert("Item adicionado!");
}

let tabela = document.getElementById("tabela");

// Apenas popula se estiver em uma página que utiliza o formulário local antigo
if (tabela && document.getElementById("nomeItem")) {
    let estoque = JSON.parse(localStorage.getItem("estoque")) || [];

    estoque.forEach((item, index) => {
        let linha = tabela.insertRow();

        let col1 = linha.insertCell(0);
        let col2 = linha.insertCell(1);
        let col3 = linha.insertCell(2);

        col1.innerText = item.nome;
        col2.innerText = item.quantidade;
        col3.innerHTML = `<button onclick="removerItem(${index})">Remover</button>`;
    });
}

function removerItem(index){
    let estoque = JSON.parse(localStorage.getItem("estoque")) || [];
    estoque.splice(index, 1);
    localStorage.setItem("estoque", JSON.stringify(estoque));
    location.reload();
}

// Mostrar/ocultar senha
function toggleSenha() {
    const senhaInput = document.getElementById("senha");

    if (senhaInput.type === "password") {
        senhaInput.type = "text";
    } else {
        senhaInput.type = "password";
    }
}

// Verificar login via API REST com validação Bcrypt
async function verificarLogin() {
    const usuarioDigitado = document.getElementById("login").value.trim();
    const senhaDigitada = document.getElementById("senha").value;

    if (!usuarioDigitado || !senhaDigitada) {
        alert("Por favor, preencha o login e a senha!");
        return;
    }

    try {
        const resposta = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario: usuarioDigitado, senha: senhaDigitada })
        });

        const dados = await resposta.json();

        if (dados.sucesso) {
            alert("Login realizado com sucesso! Bem-vindo, " + dados.usuario);
            window.location.href = "/menu";
        } else {
            alert(dados.mensagem || "Usuário ou senha incorretos!");
        }
    } catch (e) {
        console.error("Erro na requisição de login:", e);
        // Fallback para login de demonstração se o servidor não responder
        if (
            (usuarioDigitado === "user" && senhaDigitada === "1234") ||
            (usuarioDigitado === "admin" && senhaDigitada === "1234")
        ) {
            alert("Login de demonstração aceito!");
            window.location.href = "/menu";
        } else {
            alert("Erro ao conectar ao servidor para validar login!");
        }
    }
}
