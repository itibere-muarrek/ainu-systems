"""
CONFIG.PY - Credenciais do Sistema
ARQUIVO LOCAL APENAS - NÃO COMMITAR NO GIT!

Autor: ITIBERÊ MUARREK
"""

# ============================================================================
# CREDENCIAIS (MUDAR ANTES DE DEPLOY)
# ============================================================================

CREDENCIAIS = {
    "admin": {
        "password": "admin123",
        "tipo": "ADMIN"
    },
    "visitor": {
        "password": "visitor123",
        "tipo": "VISITOR"
    }
}

# ============================================================================
# ANTES DE FAZER DEPLOY ONLINE:
# ============================================================================
# 1. MUDAR TODAS AS SENHAS
# 2. ADICIONAR ESTE ARQUIVO AO .gitignore
# 3. USAR VARIÁVEIS DE AMBIENTE PARA CREDENCIAIS REAIS
# 4. IMPLEMENTAR BANCO DE DADOS PARA USUÁRIOS

# Exemplo com variáveis de ambiente (PRODUÇÃO):
# import os
# CREDENCIAIS = {
#     "admin": {
#         "password": os.getenv("ADMIN_PASSWORD"),
#         "tipo": "ADMIN"
#     },
#     "visitor": {
#         "password": os.getenv("VISITOR_PASSWORD"),
#         "tipo": "VISITOR"
#     }
# }
