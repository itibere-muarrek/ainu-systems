"""
NARAYAMA.LIVE — Índice Demográfico Público
5 países público + 27 com email confirmado
Dados dinâmicos de AINU.Systems

Versão: 2.0 (Abril 2026)
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Narayama Sistêmico", layout="wide")

# ============================================================================
# ESTADO DA SESSÃO
# ============================================================================

if "email_confirmado" not in st.session_state:
    st.session_state.email_confirmado = False
    st.session_state.email = None

# ============================================================================
# CARREGAR DADOS DE AINU.SYSTEMS
# ============================================================================

def carregar_dados_ainu():
    """Carrega dados do exports.json gerado por AINU.Systems"""
    try:
        with open("exports.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
    except:
        return None

def criar_dataframe_de_json(dados_json):
    """Converte JSON de AINU.Systems em DataFrame"""
    paises_list = []
    for pais in dados_json["paises"]:
        paises_list.append({
            "País": pais["pais"],
            "Região": pais["regiao"],
            "N_Index": pais["n_index"],
            "Status": pais["status"],
            "Pop_0_25": pais["pop_0_25"],
            "Pop_65plus": pais["pop_65plus"],
            "Coorte_A": pais["coorte_a"],
            "Coorte_B": pais["coorte_b"],
            "Coorte_C": pais["coorte_c"]
        })
    return pd.DataFrame(paises_list)

# ============================================================================
# 5 PAÍSES PÚBLICOS (subset)
# ============================================================================

PAISES_PUBLICOS = ["Brasil", "USA", "China", "Japão", "Argentina"]

def filtrar_paises_publicos(df):
    """Filtra apenas os 5 países públicos"""
    return df[df["País"].isin(PAISES_PUBLICOS)]

# ============================================================================
# PÁGINA PÚBLICA (5 PAÍSES)
# ============================================================================

def pagina_publica():
    st.markdown("""
    <div style="text-align: center;">
    <h1 style="color: #1f77b4; font-size: 48px;">Narayama Sistêmico</h1>
    <h3 style="color: #666;">N Index - Índice Demográfico</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Nomenclatura
    st.subheader("Nomenclatura do N Index:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px;">
        <strong>✅ Superávit Geracional</strong><br/>
        <code>N > 1.8</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px;">
        <strong>⚠️ Equilibrada</strong><br/>
        <code>1.8 ≥ N ≥ 1.0</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px;">
        <strong>🔴 Déficit Geracional</strong><br/>
        <code>N < 1.0</code>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # O que é N?
    st.subheader("O que é N?")
    st.markdown("""
    A relação entre **jovens (0-25 anos)** e **idosos (65+ anos)**.

    Um país com **N = 1.8** tem 1.8 jovens para cada idoso — suficiente para reposição geracional e sustentabilidade econômica.

    - 🟢 **Quanto maior N**, mais jovem a população e maior capacidade de crescimento
    - 🔴 **Quanto menor N**, mais envelhecida a população e maior pressão sobre sistemas de previdência e saúde
    """)
    
    st.markdown("---")
    
    # Carregar dados
    dados_json = carregar_dados_ainu()
    
    if dados_json is None:
        st.warning("⚠️ Dados não disponíveis. Sistema ainda não foi atualizado.")
        return
    
    df_completo = criar_dataframe_de_json(dados_json)
    df_publico = filtrar_paises_publicos(df_completo)
    
    # Tabela dos 5 países
    st.subheader("Índice Demográfico (5 Países)")
    
    df_display = df_publico[["País", "N_Index", "Status"]].copy()
    df_display.columns = ["País", "N Index", "Status Geracional"]
    df_display["N Index"] = df_display["N Index"].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Confirmação de email
    st.subheader("🔓 Acessar dados completos (27 países)")
    
    with st.form("form_email"):
        email = st.text_input("Digite seu email para confirmar:", placeholder="seu@email.com")
        submitted = st.form_submit_button("✅ Confirmar Email", use_container_width=True)
        
        if submitted:
            if "@" in email and "." in email:
                st.session_state.email_confirmado = True
                st.session_state.email = email
                st.success(f"✅ Email confirmado!")
                st.rerun()
            else:
                st.error("❌ Email inválido!")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 12px; margin-top: 40px;">
    Powered by <strong>AINU.SYSTEMS</strong>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA COM EMAIL CONFIRMADO (27 PAÍSES)
# ============================================================================

def pagina_27_paises():
    st.markdown("""
    <div style="text-align: center;">
    <h1 style="color: #1f77b4; font-size: 48px;">Narayama Sistêmico</h1>
    <h3 style="color: #666;">N Index - Índice Demográfico Completo</h3>
    <p style="color: #999; font-size: 12px;">✅ Email confirmado: <strong>""" + st.session_state.email + """</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Remover Confirmação", use_container_width=True):
        st.session_state.email_confirmado = False
        st.session_state.email = None
        st.rerun()
    
    st.markdown("---")
    
    # Nomenclatura
    st.subheader("Nomenclatura do N Index:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px;">
        <strong>✅ Superávit Geracional</strong><br/>
        <code>N > 1.8</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px;">
        <strong>⚠️ Equilibrada</strong><br/>
        <code>1.8 ≥ N ≥ 1.0</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px;">
        <strong>🔴 Déficit Geracional</strong><br/>
        <code>N < 1.0</code>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # O que é N?
    st.subheader("O que é N?")
    st.markdown("""
    A relação entre **jovens (0-25 anos)** e **idosos (65+ anos)**.

    Um país com **N = 1.8** tem 1.8 jovens para cada idoso — suficiente para reposição geracional e sustentabilidade econômica.

    - 🟢 **Quanto maior N**, mais jovem a população e maior capacidade de crescimento
    - 🔴 **Quanto menor N**, mais envelhecida a população e maior pressão sobre sistemas de previdência e saúde
    """)
    
    st.markdown("---")
    
    # Carregar dados
    dados_json = carregar_dados_ainu()
    
    if dados_json is None:
        st.warning("⚠️ Dados não disponíveis.")
        return
    
    df_completo = criar_dataframe_de_json(dados_json)
    
    # Tabela dos 27 países
    st.subheader("Índice Demográfico (27 Países)")
    
    df_display = df_completo[["País", "Região", "N_Index", "Status"]].copy()
    df_display.columns = ["País", "Região", "N Index", "Status"]
    df_display["N Index"] = df_display["N Index"].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Gráfico
    st.subheader("Visualização do N Index")
    
    df_sorted = df_completo.sort_values("N_Index", ascending=False)
    st.bar_chart(df_sorted[["País", "N_Index"]].set_index("País"), width='stretch')
    
    st.markdown("---")
    
    # Estatísticas
    st.subheader("Estatísticas")
    
    superavit = len(df_completo[df_completo["N_Index"] > 1.8])
    equilibrada = len(df_completo[(df_completo["N_Index"] >= 1.0) & (df_completo["N_Index"] <= 1.8)])
    deficit = len(df_completo[df_completo["N_Index"] < 1.0])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🟢 Superávit", superavit)
    with col2:
        st.metric("🟡 Equilibrada", equilibrada)
    with col3:
        st.metric("🔴 Déficit", deficit)
    with col4:
        st.metric("Total", len(df_completo))
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 12px; margin-top: 40px;">
    Powered by <strong>AINU.SYSTEMS</strong>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ROUTER
# ============================================================================

if st.session_state.email_confirmado:
    pagina_27_paises()
else:
    pagina_publica()
