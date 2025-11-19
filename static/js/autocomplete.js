let livrosSelecionados = [];
let timeoutBusca = null;

const inputBusca = document.getElementById('buscarLivro');
const divResultados = document.getElementById('resultadosLivros');
const divLivrosSelecionados = document.getElementById('livrosSelecionados');
const btnNovoLivro = document.getElementById('btnNovoLivro');
const formNovoLivro = document.getElementById('formNovoLivro');

inputBusca.addEventListener('input', function() {
    const termo = this.value.trim();
    
    clearTimeout(timeoutBusca);
    
    if (termo.length < 2) {
        divResultados.style.display = 'none';
        return;
    }
    
    timeoutBusca = setTimeout(() => {
        buscarLivros(termo);
    }, 300);
});

async function buscarLivros(termo) {
    try {
        const response = await fetch(`/api/buscar-livros?q=${encodeURIComponent(termo)}`);
        const livros = await response.json();
        
        if (livros.length === 0) {
            divResultados.innerHTML = '<div class="list-group-item text-muted">Nenhum livro encontrado</div>';
        } else {
            divResultados.innerHTML = livros.map(livro => `
                <a href="#" class="list-group-item list-group-item-action livro-item" data-livro='${JSON.stringify(livro)}'>
                    <div class="fw-medium">${livro.titulo}</div>
                    <small class="text-muted">${livro.autor || 'Autor não informado'} • ${livro.editora || 'Editora não informada'}</small>
                </a>
            `).join('');
            
            document.querySelectorAll('.livro-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const livro = JSON.parse(this.dataset.livro);
                    adicionarLivro(livro);
                });
            });
        }
        
        divResultados.style.display = 'block';
    } catch (error) {
        console.error('Erro ao buscar livros:', error);
    }
}

function adicionarLivro(livro) {
    if (livrosSelecionados.find(l => l.id === livro.id)) {
        return;
    }
    
    livrosSelecionados.push(livro);
    atualizarListaLivros();
    
    inputBusca.value = '';
    divResultados.style.display = 'none';
}

function removerLivro(livroId) {
    livrosSelecionados = livrosSelecionados.filter(l => l.id !== livroId);
    atualizarListaLivros();
}

function atualizarListaLivros() {
    if (livrosSelecionados.length === 0) {
        divLivrosSelecionados.innerHTML = '';
        return;
    }
    
    divLivrosSelecionados.innerHTML = `
        <label class="form-label fw-medium">Livros selecionados:</label>
        <div class="list-group">
            ${livrosSelecionados.map(livro => `
                <div class="list-group-item livro-selecionado">
                    <div class="fw-medium">${livro.titulo}</div>
                    <small class="text-muted">${livro.autor || 'Autor não informado'} • ${livro.editora || 'Editora não informada'}</small>
                    <input type="hidden" name="livros_selecionados" value="${livro.id}">
                    <button type="button" class="btn btn-sm btn-danger btn-remover-livro" onclick="removerLivro(${livro.id})">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            `).join('')}
        </div>
    `;
}

btnNovoLivro.addEventListener('click', function() {
    formNovoLivro.style.display = formNovoLivro.style.display === 'none' ? 'block' : 'none';
});

document.addEventListener('click', function(e) {
    if (!inputBusca.contains(e.target) && !divResultados.contains(e.target)) {
        divResultados.style.display = 'none';
    }
});

document.getElementById('formAtuacao').addEventListener('submit', function(e) {
    const novoTitulo = document.getElementById('novo_livro_titulo').value.trim();
    
    if (novoTitulo && livrosSelecionados.length > 0) {
        alert('Por favor, adicione apenas livros da busca OU cadastre um novo livro, não ambos.');
        e.preventDefault();
        return false;
    }
});
