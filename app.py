#!/usr/bin/env python3
"""
NARAYAMA v8 - API REST FASTAPI (ATUALIZADA)
Com fórmulas simplificadas e novos índices calculados
Data: 28/04/2026
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json

# ========================================
# CONFIGURAÇÃO FASTAPI
# ========================================

app = FastAPI(
    title="Narayama v8 API (Atualizada)",
    description="API RESTful para Índice de Sustentabilidade Intergeracional com Fórmulas Simplificadas",
    version="8.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# MODELOS PYDANTIC
# ========================================

class Indices(BaseModel):
    NS: float
    NGII: float
    NCII: float
    NSII: float
    L: float
    EIS: float

class Pais(BaseModel):
    codigo: str
    nome: str
    regiao: str
    indices: Indices

class CenarioRequest(BaseModel):
    pais_codigo: str
    multiplicadores: Dict[str, float]

class CenarioResponse(BaseModel):
    pais_codigo: str
    pais_nome: str
    ns_atual: float
    ns_cenario: float
    delta: float
    delta_percentual: float
    interpretacao: str

# ========================================
# DADOS ATUALIZADO COM NOVOS CÁLCULOS
# ========================================

DADOS_INDICES = {
    'SA': {'nome': 'Arábia Saudita', 'regiao': 'Ásia', 'indices': {'NS': 516.76, 'NGII': 12.5, 'NCII': 100.0, 'NSII': 416.67, 'L': 0.528, 'EIS': 0.3640}},
    'US': {'nome': 'Estados Unidos', 'regiao': 'América do Norte', 'indices': {'NS': 487.88, 'NGII': 1.286, 'NCII': 175.0, 'NSII': 500.0, 'L': 0.782, 'EIS': 0.6084}},
    'CA': {'nome': 'Canadá', 'regiao': 'América do Norte', 'indices': {'NS': 461.05, 'NGII': 1.544, 'NCII': 115.789, 'NSII': 500.0, 'L': 0.769, 'EIS': 0.5887}},
    'SE': {'nome': 'Suécia', 'regiao': 'Europa', 'indices': {'NS': 436.34, 'NGII': 1.316, 'NCII': 115.385, 'NSII': 400.0, 'L': 0.815, 'EIS': 0.6545}},
    'AU': {'nome': 'Austrália', 'regiao': 'Oceania', 'indices': {'NS': 424.20, 'NGII': 1.447, 'NCII': 107.692, 'NSII': 428.571, 'L': 0.767, 'EIS': 0.5874}},
    'GB': {'nome': 'Reino Unido', 'regiao': 'Europa', 'indices': {'NS': 343.12, 'NGII': 1.125, 'NCII': 98.462, 'NSII': 400.0, 'L': 0.759, 'EIS': 0.5707}},
    'FR': {'nome': 'França', 'regiao': 'Europa', 'indices': {'NS': 322.90, 'NGII': 0.963, 'NCII': 107.143, 'NSII': 375.0, 'L': 0.744, 'EIS': 0.5598}},
    'DE': {'nome': 'Alemanha', 'regiao': 'Europa', 'indices': {'NS': 297.84, 'NGII': 0.763, 'NCII': 100.0, 'NSII': 344.828, 'L': 0.791, 'EIS': 0.5994}},
    'KR': {'nome': 'Coreia do Sul', 'regiao': 'Ásia', 'indices': {'NS': 271.79, 'NGII': 1.033, 'NCII': 77.778, 'NSII': 416.667, 'L': 0.743, 'EIS': 0.5586}},
    'CL': {'nome': 'Chile', 'regiao': 'América do Sul', 'indices': {'NS': 236.10, 'NGII': 2.5, 'NCII': 39.773, 'NSII': 333.333, 'L': 0.644, 'EIS': 0.4864}},
    'IT': {'nome': 'Itália', 'regiao': 'Europa', 'indices': {'NS': 228.55, 'NGII': 0.792, 'NCII': 93.333, 'NSII': 312.5, 'L': 0.694, 'EIS': 0.5232}},
    'JP': {'nome': 'Japão', 'regiao': 'Ásia', 'indices': {'NS': 208.65, 'NGII': 0.486, 'NCII': 76.923, 'NSII': 266.667, 'L': 0.770, 'EIS': 0.5819}},
    'PL': {'nome': 'Polônia', 'regiao': 'Europa', 'indices': {'NS': 176.08, 'NGII': 2.228, 'NCII': 50.0, 'NSII': 285.714, 'L': 0.644, 'EIS': 0.4864}},
    'AR': {'nome': 'Argentina', 'regiao': 'América do Sul', 'indices': {'NS': 145.77, 'NGII': 2.684, 'NCII': 29.697, 'NSII': 240.0, 'L': 0.608, 'EIS': 0.4602}},
    'ZA': {'nome': 'África do Sul', 'regiao': 'África', 'indices': {'NS': 141.26, 'NGII': 4.857, 'NCII': 30.0, 'NSII': 200.0, 'L': 0.681, 'EIS': 0.5146}},
    'MX': {'nome': 'México', 'regiao': 'América do Norte', 'indices': {'NS': 129.36, 'NGII': 4.667, 'NCII': 22.414, 'NSII': 250.0, 'L': 0.628, 'EIS': 0.4752}},
    'IR': {'nome': 'Irã', 'regiao': 'Ásia', 'indices': {'NS': 109.33, 'NGII': 7.778, 'NCII': 18.75, 'NSII': 200.0, 'L': 0.607, 'EIS': 0.4595}},
    'MA': {'nome': 'Marrocos', 'regiao': 'África', 'indices': {'NS': 107.35, 'NGII': 6.0, 'NCII': 27.273, 'NSII': 166.667, 'L': 0.631, 'EIS': 0.4769}},
    'EG': {'nome': 'Egito', 'regiao': 'África', 'indices': {'NS': 97.45, 'NGII': 9.091, 'NCII': 15.625, 'NSII': 166.667, 'L': 0.604, 'EIS': 0.4573}},
    'RU': {'nome': 'Rússia', 'regiao': 'Eurásia', 'indices': {'NS': 88.99, 'NGII': 1.429, 'NCII': 34.247, 'NSII': 187.5, 'L': 0.668, 'EIS': 0.5050}},
    'BR': {'nome': 'Brasil', 'regiao': 'América do Sul', 'indices': {'NS': 81.31, 'NGII': 4.483, 'NCII': 19.048, 'NSII': 200.0, 'L': 0.603, 'EIS': 0.4567}},
    'CN': {'nome': 'China', 'regiao': 'Ásia', 'indices': {'NS': 69.64, 'NGII': 1.264, 'NCII': 24.0, 'NSII': 166.667, 'L': 0.573, 'EIS': 0.4331}},
    'ID': {'nome': 'Indonésia', 'regiao': 'Ásia', 'indices': {'NS': 62.80, 'NGII': 4.5, 'NCII': 10.0, 'NSII': 166.667, 'L': 0.659, 'EIS': 0.4985}},
    'IN': {'nome': 'Índia', 'regiao': 'Ásia', 'indices': {'NS': 54.60, 'NGII': 5.625, 'NCII': 8.889, 'NSII': 125.0, 'L': 0.570, 'EIS': 0.4311}},
    'NG': {'nome': 'Nigéria', 'regiao': 'África', 'indices': {'NS': 47.59, 'NGII': 11.875, 'NCII': 5.882, 'NSII': 125.0, 'L': 0.627, 'EIS': 0.4737}},
    'ET': {'nome': 'Etiópia', 'regiao': 'África', 'indices': {'NS': 31.80, 'NGII': 12.222, 'NCII': 4.167, 'NSII': 85.714, 'L': 0.639, 'EIS': 0.4834}},
    'CD': {'nome': 'RDC', 'regiao': 'África', 'indices': {'NS': 28.92, 'NGII': 20.0, 'NCII': 4.0, 'NSII': 90.909, 'L': 0.637, 'EIS': 0.4819}},
}

# ========================================
# ENDPOINTS
# ========================================

@app.get("/", tags=["Info"])
async def root():
    """Endpoint raiz"""
    return {
        "mensagem": "API Narayama v8 (Atualizada com Fórmulas Simplificadas)",
        "documentacao": "/docs",
        "versao": "8.1.0",
    }

@app.get("/status", tags=["Info"])
async def status():
    """Status da API"""
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "versao": "8.1.0",
        "paises_total": len(DADOS_INDICES),
        "indices_total": 6,
    }

@app.get("/paises", tags=["Países"], response_model=List[Pais])
async def listar_paises(
    regiao: Optional[str] = Query(None),
    ordenar_por: str = Query("NS"),
    ordem: str = Query("desc"),
):
    """Lista todos os 27 países"""
    paises = []
    for cod, dados in DADOS_INDICES.items():
        if regiao and dados['regiao'].lower() != regiao.lower():
            continue
        paises.append({
            'codigo': cod,
            'nome': dados['nome'],
            'regiao': dados['regiao'],
            'indices': dados['indices'],
        })
    
    reverse = ordem.lower() == 'desc'
    paises.sort(key=lambda x: x['indices'].get(ordenar_por, 0), reverse=reverse)
    return paises

@app.get("/paises/{codigo}", tags=["Países"], response_model=Pais)
async def obter_pais(codigo: str):
    """Detalhe de um país"""
    codigo = codigo.upper()
    if codigo not in DADOS_INDICES:
        raise HTTPException(status_code=404, detail=f"País '{codigo}' não encontrado")
    
    dados = DADOS_INDICES[codigo]
    return {
        'codigo': codigo,
        'nome': dados['nome'],
        'regiao': dados['regiao'],
        'indices': dados['indices'],
    }

@app.get("/ranking/{indice}", tags=["Análises"])
async def ranking(indice: str = "NS", limite: int = Query(27, ge=1, le=27)):
    """Ranking por índice"""
    indices_validos = ['NS', 'NGII', 'NCII', 'NSII', 'L', 'EIS']
    if indice not in indices_validos:
        raise HTTPException(status_code=400, detail=f"Índice inválido. Use: {', '.join(indices_validos)}")
    
    ranking_list = []
    for cod, dados in DADOS_INDICES.items():
        ranking_list.append({
            'posicao': 0,
            'codigo': cod,
            'nome': dados['nome'],
            'regiao': dados['regiao'],
            'valor': dados['indices'].get(indice, 0),
        })
    
    ranking_list.sort(key=lambda x: x['valor'], reverse=True)
    for i, item in enumerate(ranking_list[:limite], 1):
        item['posicao'] = i
    
    return ranking_list[:limite]

@app.get("/destaques", tags=["Análises"])
async def destaques_paises():
    """5 países com maior NS"""
    top_5 = sorted(DADOS_INDICES.items(), key=lambda x: x[1]['indices']['NS'], reverse=True)[:5]
    return {
        'total': len(top_5),
        'paises': [
            {
                'posicao': i+1,
                'codigo': cod,
                'nome': dados['nome'],
                'regiao': dados['regiao'],
                'indices': dados['indices'],
            }
            for i, (cod, dados) in enumerate(top_5)
        ]
    }

@app.get("/estatisticas", tags=["Análises"])
async def estatisticas():
    """Estatísticas globais"""
    todos_ns = [d['indices']['NS'] for d in DADOS_INDICES.values()]
    
    return {
        'total_paises': len(DADOS_INDICES),
        'ns': {
            'media': round(sum(todos_ns) / len(todos_ns), 2),
            'minimo': round(min(todos_ns), 2),
            'maximo': round(max(todos_ns), 2),
            'mediana': round(sorted(todos_ns)[len(todos_ns)//2], 2),
        },
        'regioes': list(set(d['regiao'] for d in DADOS_INDICES.values())),
        'timestamp': datetime.now().isoformat(),
    }

@app.post("/simulador", tags=["Simulação"], response_model=CenarioResponse)
async def simulador(request: CenarioRequest):
    """Simular cenário"""
    codigo = request.pais_codigo.upper()
    if codigo not in DADOS_INDICES:
        raise HTTPException(status_code=404, detail=f"País '{codigo}' não encontrado")
    
    pais_dados = DADOS_INDICES[codigo]
    ns_atual = pais_dados['indices']['NS']
    
    # Aplicar multiplicadores
    ngii_novo = pais_dados['indices']['NGII'] * request.multiplicadores.get('NGII', 1.0)
    ncii_novo = pais_dados['indices']['NCII'] * request.multiplicadores.get('NCII', 1.0)
    nsii_novo = pais_dados['indices']['NSII'] * request.multiplicadores.get('NSII', 1.0)
    l_novo = pais_dados['indices']['L'] * request.multiplicadores.get('L', 1.0)
    
    # Recalcular NS: N* = L × (NGII × NCII × NSII)^{1/3}
    termo = (ngii_novo * ncii_novo * nsii_novo) ** (1/3)
    ns_cenario = l_novo * termo
    
    delta = ns_cenario - ns_atual
    delta_pct = (delta / ns_atual * 100) if ns_atual != 0 else 0
    
    interpretacao = "✓ Sustentável" if ns_cenario >= 1.5 else "⚠ Frágil" if ns_cenario >= 1.0 else "🔴 Crítico"
    
    return {
        'pais_codigo': codigo,
        'pais_nome': pais_dados['nome'],
        'ns_atual': round(ns_atual, 2),
        'ns_cenario': round(ns_cenario, 2),
        'delta': round(delta, 2),
        'delta_percentual': round(delta_pct, 2),
        'interpretacao': interpretacao,
    }

# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 NARAYAMA v8 API - ATUALIZADA")
    print("="*60)
    print(f"Versão: 8.1.0")
    print(f"Países: {len(DADOS_INDICES)}")
    print(f"Índices: 6 (NS, NGII, NCII, NSII, L, EIS)")
    print(f"Docs: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
