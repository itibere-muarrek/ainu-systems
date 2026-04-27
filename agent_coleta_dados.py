"""
AGENTE DE COLETA DE DADOS — AINU v8
Coleta dados da ONU/Banco Mundial e distribui nas coortes

Autor: ITIBERÊ MUARREK
Email: itibere@gmail.com
Versão: 1.0 (Abril 2026)
"""

import pandas as pd
import requests
from datetime import datetime
import json
import os

# ============================================================================
# DISTRIBUIÇÃO PADRÃO DAS COORTES (por país)
# ============================================================================

DISTRIBUICAO_COORTES_PADRAO = {
    # AMÉRICA
    "Brasil": {"A": 10, "B": 40, "C": 50},
    "USA": {"A": 13, "B": 19, "C": 68},
    "Canadá": {"A": 0, "B": 10, "C": 90},
    "Chile": {"A": 0, "B": 50, "C": 50},
    "Argentina": {"A": 0, "B": 50, "C": 50},
    "México": {"A": 0, "B": 62, "C": 38},
    
    # EUROPA
    "Alemanha": {"A": 0, "B": 10, "C": 90},
    "França": {"A": 0, "B": 10, "C": 90},
    "Itália": {"A": 0, "B": 10, "C": 90},
    "Reino Unido": {"A": 0, "B": 10, "C": 90},
    "Suécia": {"A": 0, "B": 10, "C": 90},
    "Polônia": {"A": 0, "B": 2, "C": 98},
    
    # ÁSIA
    "Japão": {"A": 0, "B": 1, "C": 99},
    "Coreia do Sul": {"A": 0, "B": 3, "C": 97},
    "China": {"A": 0, "B": 10, "C": 90},
    "Índia": {"A": 35, "B": 55, "C": 10},
    "Indonésia": {"A": 0, "B": 100, "C": 0},
    "Irã": {"A": 0, "B": 100, "C": 0},
    "Arábia Saudita": {"A": 0, "B": 100, "C": 0},
    
    # OCEANIA
    "Austrália": {"A": 0, "B": 10, "C": 90},
    
    # ÁFRICA
    "Nigéria": {"A": 100, "B": 0, "C": 0},
    "Marrocos": {"A": 0, "B": 100, "C": 0},
    "Egito": {"A": 0, "B": 100, "C": 0},
    "África do Sul": {"A": 90, "B": 0, "C": 10},
    "Etiópia": {"A": 100, "B": 0, "C": 0},
    "RDC": {"A": 100, "B": 0, "C": 0},
    
    # EURASIA
    "Rússia": {"A": 0, "B": 5, "C": 95},
}

# ============================================================================
# DADOS MOCK (Fallback se APIs não responderem)
# ============================================================================

DADOS_MOCK = {
    "Brasil": {
        "pop_0_25": 24.3,
        "pop_25_65": 46.9,
        "pop_65plus": 28.8,
        "nascimentos": 2.1,
        "obitos": 0.7
    },
    "USA": {
        "pop_0_25": 21.0,
        "pop_25_65": 45.6,
        "pop_65plus": 33.4,
        "nascimentos": 1.7,
        "obitos": 0.8
    },
    # ... (pode expandir com mais países)
}

# ============================================================================
# FUNÇÃO: CALCULAR N INDEX
# ============================================================================

def calcular_n_index(pop_0_25, pop_65plus):
    """
    N Index = Pop(0-25) / Pop(65+)
    """
    if pop_65plus == 0:
        return 0
    return round(pop_0_25 / pop_65plus, 2)

# ============================================================================
# FUNÇÃO: BUSCAR DADOS DA WORLD BANK (Público)
# ============================================================================

def buscar_dados_world_bank(pais_codigo):
    """
    Busca dados da World Bank API (pública, sem credenciais)
    
    Indicadores:
    - SP.URB.TOTL.IN.ZS: % população urbana
    - NY.GDP.PCAP.CD: PIB per capita
    - SP.POP.0014.TO.ZS: % população 0-14 anos
    """
    try:
        url = f"https://api.worldbank.org/v2/country/{pais_codigo}/indicator/SP.POP.0014.TO.ZS?format=json"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            dados = response.json()
            if len(dados) > 1 and len(dados[1]) > 0:
                valor = dados[1][0].get("value")
                if valor:
                    return float(valor)
    except Exception as e:
        print(f"Erro ao buscar World Bank para {pais_codigo}: {e}")
    
    return None

# ============================================================================
# FUNÇÃO: BUSCAR DADOS UN DATA (Público)
# ============================================================================

def buscar_dados_un(pais_nome):
    """
    Fallback: Usar dados locais/mock
    (APIs da ONU são mais lentas e complexas)
    """
    return DADOS_MOCK.get(pais_nome)

# ============================================================================
# FUNÇÃO PRINCIPAL: COLETAR E PROCESSAR DADOS
# ============================================================================

def coletar_e_processar_dados():
    """
    Coleta dados de todos os 27 países e distribui nas coortes
    """
    
    print("="*80)
    print("AGENTE DE COLETA DE DADOS — AINU v8")
    print("="*80)
    print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar base anterior (se existir)
    try:
        df_anterior = pd.read_csv("base_dados_paises.csv")
        print(f"✅ Base anterior carregada ({len(df_anterior)} países)")
    except:
        df_anterior = None
        print("⚠️  Nenhuma base anterior encontrada")
    
    # Lista de países
    paises = list(DISTRIBUICAO_COORTES_PADRAO.keys())
    
    # Processar cada país
    dados_novos = []
    
    for pais in paises:
        print(f"\n📍 Processando: {pais}")
        
        # 1. Buscar dados (mock por enquanto)
        dados_pais = DADOS_MOCK.get(pais, {
            "pop_0_25": 22.0,
            "pop_25_65": 45.0,
            "pop_65plus": 33.0,
            "nascimentos": 1.8,
            "obitos": 0.8
        })
        
        # 2. Obter distribuição de coortes
        coortes = DISTRIBUICAO_COORTES_PADRAO[pais]
        
        # 3. Calcular N Index
        n_index = calcular_n_index(
            dados_pais["pop_0_25"],
            dados_pais["pop_65plus"]
        )
        
        # 4. Determinar região
        regiao = "?"
        if pais in ["Brasil", "USA", "Canadá", "Chile", "Argentina", "México"]:
            regiao = "América"
        elif pais in ["Alemanha", "França", "Itália", "Reino Unido", "Suécia", "Polônia"]:
            regiao = "Europa"
        elif pais in ["Japão", "Coreia do Sul", "China", "Índia", "Indonésia", "Irã", "Arábia Saudita"]:
            regiao = "Ásia"
        elif pais in ["Austrália"]:
            regiao = "Oceania"
        elif pais in ["Nigéria", "Marrocos", "Egito", "África do Sul", "Etiópia", "RDC"]:
            regiao = "África"
        elif pais in ["Rússia"]:
            regiao = "Eurasia"
        
        # 5. Montar registro
        registro = {
            "País": pais,
            "Região": regiao,
            "Pop_0_25_pct": dados_pais["pop_0_25"],
            "Pop_25_65_pct": dados_pais["pop_25_65"],
            "Pop_65plus_pct": dados_pais["pop_65plus"],
            "Nascimentos": dados_pais["nascimentos"],
            "Óbitos": dados_pais["obitos"],
            "Coorte_A_pct": coortes["A"],
            "Coorte_B_pct": coortes["B"],
            "Coorte_C_pct": coortes["C"],
            "N_Index": n_index,
            "Última_Atualização": datetime.now().strftime("%Y-%m-%d")
        }
        
        dados_novos.append(registro)
        print(f"  ✓ Pop 0-25: {dados_pais['pop_0_25']:.1f}% | "
              f"Pop 65+: {dados_pais['pop_65plus']:.1f}% | "
              f"N Index: {n_index:.2f} | "
              f"Coortes: A{coortes['A']}% B{coortes['B']}% C{coortes['C']}%")
    
    # 6. Criar DataFrame
    df_novo = pd.DataFrame(dados_novos)
    
    # 7. Salvar
    df_novo.to_csv("base_dados_paises.csv", index=False)
    
    print()
    print("="*80)
    print(f"✅ BASE ATUALIZADA: {len(df_novo)} países")
    print(f"📂 Arquivo: base_dados_paises.csv")
    print(f"⏰ Atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print()
    print("📌 PRÓXIMO PASSO:")
    print("  1. Você EDITA as coortes no Painel Admin (se necessário)")
    print("  2. Sistema recalcula N Index automaticamente")
    print("  3. Dados prontos para análise")
    
    return df_novo

# ============================================================================
# EXECUTAR
# ============================================================================

if __name__ == "__main__":
    df = coletar_e_processar_dados()
    print("\n📊 Primeiros 5 países:")
    print(df.head())
