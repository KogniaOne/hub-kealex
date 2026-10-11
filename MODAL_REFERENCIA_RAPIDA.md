# Modal Padrão - Referência Rápida

## 📦 Arquivos Criados

1. **shared_modal.py** - Componentes reutilizáveis de modal
2. **EXEMPLO_USO_MODAL.md** - Guia completo de uso
3. **exemplo_servico_com_modal.py** - Serviço exemplo funcional
4. **MODAL_REFERENCIA_RAPIDA.md** - Este arquivo

## 🚀 Quick Start

### 1. Copiar arquivo compartilhado
```bash
# O arquivo shared_modal.py já está na raiz do projeto
# Certifique-se de que está em: /hubKealex/shared_modal.py
```

### 2. Importar no seu serviço
```python
from shared_modal import (
    criar_modal_sucesso,
    criar_modal_erro,
    criar_resposta_modal
)
```

### 3. Usar em um endpoint
```python
@app.post("/criar")
def criar_algo(body: dict):
    try:
        # ... sua lógica ...
        modal = criar_modal_sucesso("Criado com sucesso!")
        return criar_resposta_modal(True, "Sucesso", modal, dados)
    except Exception as e:
        modal = criar_modal_erro(f"Erro: {str(e)}")
        return criar_resposta_modal(False, "Erro", modal)
```

## 📋 Funções Disponíveis

### Criar Modais

```python
# Modal de Sucesso
criar_modal_sucesso(mensagem: str) -> ModalSucesso

# Modal de Erro
criar_modal_erro(mensagem: str) -> ModalErro

# Modal de Confirmação
criar_modal_confirmacao(titulo: str, descricao: str) -> ModalConfirmacao

# Modal de Formulário
criar_modal_formulario(titulo: str, campos: List[ModalField]) -> ModalFormulario

# Resposta Padrão
criar_resposta_modal(
    sucesso: bool,
    mensagem: str,
    modal: Optional[Modal] = None,
    dados: Optional[Dict] = None
) -> ModalResponse
```

### Criar Campos de Formulário

```python
ModalField(
    id="campo_id",
    label="Rótulo",
    tipo="text",  # text, email, password, number, select, textarea, checkbox, radio, date
    placeholder="Placeholder",
    obrigatorio=True,
    validacao="regex_pattern",  # opcional
    opcoes=[{"id": "1", "label": "Opção 1"}],  # para select/radio
    help_text="Texto de ajuda"
)
```

### Criar Botões

```python
ModalButton(
    id="btn_id",
    label="Rótulo",
    tipo="default",  # default, primary, danger, success
    acao="callback_action",
    disabled=False
)
```

## 🎯 Padrões de Uso

### Padrão 1: Sucesso Simples
```python
@app.post("/criar")
def criar(body: dict):
    try:
        item = criar_item(body)
        modal = criar_modal_sucesso("Item criado!")
        return criar_resposta_modal(True, "Sucesso", modal, {"id": item.id})
    except Exception as e:
        modal = criar_modal_erro(str(e))
        return criar_resposta_modal(False, "Erro", modal)
```

### Padrão 2: Confirmação
```python
@app.post("/deletar/{id}")
def deletar(id: str):
    modal = criar_modal_confirmacao(
        "Confirmar Exclusão",
        f"Deletar item {id}?"
    )
    return criar_resposta_modal(True, "Confirmação", modal)
```

### Padrão 3: Formulário
```python
@app.get("/novo")
def novo():
    campos = [
        ModalField(id="nome", label="Nome", tipo="text", obrigatorio=True),
        ModalField(id="email", label="Email", tipo="email", obrigatorio=True),
    ]
    modal = criar_modal_formulario("Novo Item", campos)
    return criar_resposta_modal(True, "Preencha", modal)
```

### Padrão 4: Validação com Modal
```python
@app.post("/validar")
def validar(body: dict):
    if not body.get("nome"):
        modal = criar_modal_erro("Nome é obrigatório")
        return criar_resposta_modal(False, "Validação", modal)
    
    # ... continuar ...
```

## 🔧 Tipos de Modal

| Tipo | Ícone | Uso |
|------|-------|-----|
| `SUCESSO` | ✓ check-circle | Operação bem-sucedida |
| `ERRO` | ✗ x-circle | Erro na operação |
| `CONFIRMACAO` | ? info | Pedir confirmação |
| `ALERTA` | ⚠ warning | Avisar sobre algo |
| `INFORMACAO` | ℹ info | Informação geral |
| `FORMULARIO` | 📝 form | Coletar dados |
| `CARREGAMENTO` | ⏳ loading | Operação em progresso |

## 📐 Tamanhos de Modal

```python
config=ModalConfig(
    tamanho="sm"   # small
    tamanho="md"   # medium (padrão)
    tamanho="lg"   # large
    tamanho="xl"   # extra large
)
```

## 🎨 Tipos de Botão

```python
tipo="default"   # Cinza neutro
tipo="primary"   # Azul principal
tipo="danger"    # Vermelho perigoso
tipo="success"   # Verde sucesso
```

## 📝 Tipos de Campo

```python
tipo="text"       # Texto simples
tipo="email"      # Email
tipo="password"   # Senha
tipo="number"     # Número
tipo="select"     # Dropdown
tipo="textarea"   # Texto longo
tipo="checkbox"   # Checkbox
tipo="radio"      # Radio button
tipo="date"       # Data
```

## 🔄 Fluxo Completo de Exemplo

```python
# 1. Usuário clica em "Novo Item"
@app.get("/items/novo")
def novo_item():
    campos = [
        ModalField(id="nome", label="Nome", tipo="text", obrigatorio=True),
        ModalField(id="valor", label="Valor", tipo="number", obrigatorio=True),
    ]
    modal = criar_modal_formulario("Novo Item", campos)
    return criar_resposta_modal(True, "Preencha o formulário", modal)

# 2. Usuário preenche e envia
@app.post("/items")
def criar_item(body: ItemIn):
    try:
        item = salvar_item(body)
        modal = criar_modal_sucesso(f"Item '{item.nome}' criado!")
        return criar_resposta_modal(True, "Sucesso", modal, item.dict())
    except Exception as e:
        modal = criar_modal_erro(str(e))
        return criar_resposta_modal(False, "Erro", modal)

# 3. Usuário clica em "Deletar"
@app.post("/items/{id}/deletar")
def deletar_item(id: str):
    modal = criar_modal_confirmacao(
        "Confirmar Exclusão",
        f"Tem certeza que deseja deletar?"
    )
    return criar_resposta_modal(True, "Confirmação", modal)

# 4. Usuário confirma
@app.post("/items/{id}/confirmar-deletar")
def confirmar_deletar(id: str):
    try:
        deletar_do_banco(id)
        modal = criar_modal_sucesso("Item deletado!")
        return criar_resposta_modal(True, "Sucesso", modal)
    except Exception as e:
        modal = criar_modal_erro(str(e))
        return criar_resposta_modal(False, "Erro", modal)
```

## ✅ Checklist de Implementação

Para cada serviço que usar modal:

- [ ] Copiar `shared_modal.py` para raiz do projeto
- [ ] Adicionar import no `main.py` do serviço
- [ ] Envolver endpoints em try/except
- [ ] Retornar `ModalResponse` em endpoints críticos
- [ ] Testar modais no Swagger/Postman
- [ ] Validar estrutura de resposta
- [ ] Documentar endpoints customizados
- [ ] Testar no frontend

## 🐛 Troubleshooting

### ImportError: No module named 'shared_modal'
```python
# Solução: Adicionar ao sys.path
import sys
sys.path.insert(0, "/app")  # ou caminho correto
from shared_modal import ...
```

### Modal não aparece no frontend
```python
# Verificar se está retornando ModalResponse
# Não esquecer de importar e usar criar_resposta_modal()
return criar_resposta_modal(True, "msg", modal, dados)
```

### Erro ao serializar dados
```python
# Garantir que dados são JSON-serializable
# Converter datetime para isoformat()
dados = {
    "id": item.id,
    "criado_em": item.created_at.isoformat()  # ✓ Correto
}
```

## 📚 Referências

- **shared_modal.py** - Definições de classes
- **EXEMPLO_USO_MODAL.md** - Guia completo
- **exemplo_servico_com_modal.py** - Código funcional
- **Swagger** - http://localhost:8000/docs

## 🎓 Próximos Passos

1. Integrar em `svc-cobrancas`
2. Integrar em `svc-processos`
3. Integrar em `svc-clientes`
4. Integrar em outros serviços
5. Testar no frontend
6. Documentar endpoints customizados
