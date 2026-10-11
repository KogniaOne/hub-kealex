"""
Exemplo de Serviço com Modal Padrão Integrado
Este arquivo mostra como usar o shared_modal.py em um serviço FastAPI
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

# Importar componentes do modal padrão
try:
    from shared_modal import (
        Modal, ModalResponse, ModalButton, ModalField,
        criar_modal_confirmacao, criar_modal_sucesso, criar_modal_erro,
        criar_modal_formulario, criar_resposta_modal
    )
    MODAL_DISPONIVEL = True
except ImportError:
    MODAL_DISPONIVEL = False
    print("[AVISO] shared_modal.py não encontrado. Modais desativados.")


app = FastAPI(title="Exemplo Serviço com Modal")


# ─── Modelos Pydantic ───────────────────────────────────────────────────────

class ItemIn(BaseModel):
    nome: str
    descricao: Optional[str] = None
    valor: float


class ItemOut(BaseModel):
    id: str
    nome: str
    descricao: Optional[str]
    valor: float


# ─── Endpoints com Modal ─────────────────────────────────────────────────────

@app.post("/items", response_model=ModalResponse)
def criar_item(body: ItemIn):
    """
    Cria um novo item com resposta em modal
    """
    try:
        # Validação
        if not body.nome or len(body.nome) < 3:
            if MODAL_DISPONIVEL:
                modal = criar_modal_erro("Nome deve ter no mínimo 3 caracteres")
                return criar_resposta_modal(False, "Validação falhou", modal)
            raise HTTPException(400, "Nome inválido")
        
        if body.valor <= 0:
            if MODAL_DISPONIVEL:
                modal = criar_modal_erro("Valor deve ser maior que zero")
                return criar_resposta_modal(False, "Validação falhou", modal)
            raise HTTPException(400, "Valor inválido")
        
        # Simular criação
        item = {
            "id": "123",
            "nome": body.nome,
            "descricao": body.descricao,
            "valor": body.valor
        }
        
        if MODAL_DISPONIVEL:
            modal = criar_modal_sucesso(f"Item '{body.nome}' criado com sucesso!")
            return criar_resposta_modal(
                True,
                "Item criado",
                modal,
                item
            )
        
        return item
        
    except Exception as e:
        if MODAL_DISPONIVEL:
            modal = criar_modal_erro(f"Erro ao criar item: {str(e)}")
            return criar_resposta_modal(False, "Erro", modal)
        raise HTTPException(500, str(e))


@app.post("/items/{item_id}/deletar", response_model=ModalResponse)
def deletar_item(item_id: str):
    """
    Retorna modal de confirmação antes de deletar
    """
    try:
        if MODAL_DISPONIVEL:
            modal = criar_modal_confirmacao(
                titulo="Confirmar Exclusão",
                descricao=f"Tem certeza que deseja deletar o item {item_id}? Esta ação não pode ser desfeita."
            )
            return criar_resposta_modal(
                True,
                "Confirmação necessária",
                modal,
                {"item_id": item_id, "acao": "aguardando_confirmacao"}
            )
        
        return {"ok": True}
        
    except Exception as e:
        if MODAL_DISPONIVEL:
            modal = criar_modal_erro(f"Erro: {str(e)}")
            return criar_resposta_modal(False, "Erro", modal)
        raise HTTPException(500, str(e))


@app.post("/items/{item_id}/confirmar-deletar", response_model=ModalResponse)
def confirmar_deletar_item(item_id: str):
    """
    Confirma a exclusão após modal de confirmação
    """
    try:
        # Simular exclusão
        if MODAL_DISPONIVEL:
            modal = criar_modal_sucesso(f"Item {item_id} deletado com sucesso!")
            return criar_resposta_modal(
                True,
                "Item deletado",
                modal,
                {"item_id": item_id, "deletado": True}
            )
        
        return {"ok": True}
        
    except Exception as e:
        if MODAL_DISPONIVEL:
            modal = criar_modal_erro(f"Erro ao deletar: {str(e)}")
            return criar_resposta_modal(False, "Erro", modal)
        raise HTTPException(500, str(e))


@app.get("/items/novo/formulario", response_model=ModalResponse)
def formulario_novo_item():
    """
    Retorna um modal com formulário para criar novo item
    """
    try:
        if MODAL_DISPONIVEL:
            campos = [
                ModalField(
                    id="nome",
                    label="Nome do Item",
                    tipo="text",
                    placeholder="Digite o nome",
                    obrigatorio=True,
                    help_text="Mínimo 3 caracteres"
                ),
                ModalField(
                    id="descricao",
                    label="Descrição",
                    tipo="textarea",
                    placeholder="Descreva o item",
                    obrigatorio=False,
                    help_text="Opcional"
                ),
                ModalField(
                    id="valor",
                    label="Valor (R$)",
                    tipo="number",
                    placeholder="0.00",
                    obrigatorio=True,
                    validacao="^[0-9]+(\\.[0-9]{2})?$"
                ),
                ModalField(
                    id="categoria",
                    label="Categoria",
                    tipo="select",
                    obrigatorio=True,
                    opcoes=[
                        {"id": "eletronico", "label": "Eletrônico"},
                        {"id": "livro", "label": "Livro"},
                        {"id": "roupa", "label": "Roupa"},
                        {"id": "outro", "label": "Outro"},
                    ]
                ),
            ]
            
            modal = criar_modal_formulario("Novo Item", campos)
            return criar_resposta_modal(
                True,
                "Preencha o formulário",
                modal
            )
        
        return {"ok": True}
        
    except Exception as e:
        if MODAL_DISPONIVEL:
            modal = criar_modal_erro(f"Erro: {str(e)}")
            return criar_resposta_modal(False, "Erro", modal)
        raise HTTPException(500, str(e))


@app.post("/items/{item_id}/atualizar", response_model=ModalResponse)
def atualizar_item(item_id: str, body: ItemIn):
    """
    Atualiza um item com resposta em modal
    """
    try:
        # Validação
        if not body.nome or len(body.nome) < 3:
            if MODAL_DISPONIVEL:
                modal = criar_modal_erro("Nome deve ter no mínimo 3 caracteres")
                return criar_resposta_modal(False, "Validação falhou", modal)
            raise HTTPException(400, "Nome inválido")
        
        # Simular atualização
        item = {
            "id": item_id,
            "nome": body.nome,
            "descricao": body.descricao,
            "valor": body.valor
        }
        
        if MODAL_DISPONIVEL:
            modal = criar_modal_sucesso(f"Item '{body.nome}' atualizado com sucesso!")
            return criar_resposta_modal(
                True,
                "Item atualizado",
                modal,
                item
            )
        
        return item
        
    except Exception as e:
        if MODAL_DISPONIVEL:
            modal = criar_modal_erro(f"Erro ao atualizar: {str(e)}")
            return criar_resposta_modal(False, "Erro", modal)
        raise HTTPException(500, str(e))


@app.get("/health")
def health():
    """Health check"""
    return {
        "status": "healthy",
        "modal_disponivel": MODAL_DISPONIVEL
    }


# ─── Exemplo de Uso ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║  Exemplo de Serviço com Modal Padrão                          ║
    ║  Modal Disponível: {}                                    ║
    ║                                                                ║
    ║  Endpoints:                                                    ║
    ║  - POST   /items                    (criar item)              ║
    ║  - GET    /items/novo/formulario    (formulário novo item)    ║
    ║  - POST   /items/{{id}}/atualizar   (atualizar item)          ║
    ║  - POST   /items/{{id}}/deletar     (confirmar exclusão)      ║
    ║  - POST   /items/{{id}}/confirmar-deletar (deletar)           ║
    ║  - GET    /health                   (health check)            ║
    ║                                                                ║
    ║  Acesse: http://localhost:8000/docs                           ║
    ╚════════════════════════════════════════════════════════════════╝
    """.format("✓ SIM" if MODAL_DISPONIVEL else "✗ NÃO"))
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
