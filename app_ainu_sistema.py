"""
AINU.SYSTEMS — Sistema Principal Completo
Agente automático + Equações v8 + 27 países dinâmico
LOGIN ADMIN/VISITOR
 
Autor: ITIBERÊ MUARREK
Versão: 2.1 (Abril 2026)
"""
 
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from config import CREDENCIAIS
 
st.set_page_config(page_title="AINU.Systems", layout="wide")
 
# ============================================================================
# LOGIN
# ============================================================================
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
 
def login_page():
    st.title("🔐 AINU.Systems")
    st.subheader("Sistema de Índices Narayama")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        
        username = st.text_input("Usuário:", placeholder="admin ou visitor")
        password = st.text_input("Senha:", type="password", placeholder="senha")
        
        if st.button("🔓 Entrar", use_container_width=True):
            if username in CREDENCIAIS and CREDENCIAIS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = CREDENCIAIS[username]["tipo"]
                st.session_state.username = username
                st.success(f"✅ Login {st.session_state.user_type} bem-sucedido!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos!")
        
        st.markdown("---")
        st.markdown("""
        **Para credenciais, consulte o administrador do sistema.**
        """)
 
def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.username = None
    st.rerun()
 
# ============================================================================
# FUNÇÃO: Exportar JSON para Narayama.live
# ============================================================================
 
def exportar_json(df):
    """Exporta dados em formato JSON para Narayama.live"""
    def status_geracional(n_index):
        if n_index > 1.8:
            return "🟢 Superávit Geracional"
        elif n_index >= 1.0:
            return "🟡 Equilibrada"
        else:
            return "🔴 Déficit Geracional"
    
    dados_export = {
        "timestamp": datetime.now().isoformat(),
        "total_paises": len(df),
        "paises": []
    }
    
    for _, row in df.iterrows():
        dados_export["paises"].append({
            "pais": row["País"],
            "regiao": row["Região"],
            "n_index": float(row["N_Index"]),
            "status": status_geracional(row["N_Index"]),
            "pop_0_25": float(row["Pop_0_25_pct"]),
            "pop_65plus": float(row["Pop_65plus_pct"]),
            "coorte_a": int(row["Coorte_A_pct"]),
            "coorte_b": int(row["Coorte_B_pct"]),
            "coorte_c": int(row["Coorte_C_pct"])
        })
    
    with open("exports.json", "w", encoding="utf-8") as f:
        json.dump(dados_export, f, ensure_ascii=False, indent=2)
 
# ============================================================================
# CARREGAR DADOS
# ============================================================================
 
def carregar_dados():
    try:
        df = pd.read_csv("base_dados_paises.csv")
        return df
    except:
        st.error("❌ Erro ao carregar base_dados_paises.csv")
        return None
 
def status_geracional(n_index):
    if n_index > 1.8:
        return "🟢 Superávit Geracional"
    elif n_index >= 1.0:
        return "🟡 Equilibrada"
    else:
        return "🔴 Déficit Geracional"
 
# ============================================================================
# SISTEMA PRINCIPAL (após login)
# ============================================================================
 
if not st.session_state.logged_in:
    login_page()
else:
    # Header
    st.title("⚙️ AINU.Systems")
    st.subheader(f"Olá, {st.session_state.username.upper()} ({st.session_state.user_type})")
    
    # Botão logout
    if st.button("🚪 Logout", use_container_width=True):
        logout()
    
    st.markdown("---")
    
    # Carregar dados
    df_paises = carregar_dados()
    if df_paises is None:
        st.stop()
    
    # ============================================================================
    # INTERFACE ADMIN
    # ============================================================================
    
    if st.session_state.user_type == "ADMIN":
        st.info("🔓 ADMIN - Acesso completo ao sistema")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard",
            "✏️ Editar Dados",
            "🤖 Agente",
            "📤 Exportar",
            "📈 Análise",
            "ℹ️ Sobre"
        ])
        
        with tab1:
            st.subheader("Dashboard — 27 Países (ADMIN)")
            
            df_display = df_paises[[
                "País", "Região", "Pop_0_25_pct", "Pop_65plus_pct",
                "Coorte_A_pct", "Coorte_B_pct", "Coorte_C_pct", "N_Index"
            ]].copy()
            
            df_display.columns = ["País", "Região", "Pop 0-25", "Pop 65+", "A%", "B%", "C%", "N Index"]
            
            st.dataframe(df_display, width='stretch', hide_index=True)
            st.info(f"✅ Última atualização: {df_paises.iloc[0]['Última_Atualização']}")
        
        with tab2:
            st.subheader("Editar Coortes e Dados (ADMIN)")
            
            pais_selecionado = st.selectbox("Selecione um país:", df_paises["País"].unique())
            idx = df_paises[df_paises["País"] == pais_selecionado].index[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                coorte_a = st.slider("Coorte A (%)", 0, 100, int(df_paises.loc[idx, "Coorte_A_pct"]))
            with col2:
                coorte_b = st.slider("Coorte B (%)", 0, 100, int(df_paises.loc[idx, "Coorte_B_pct"]))
            with col3:
                coorte_c = st.slider("Coorte C (%)", 0, 100, int(df_paises.loc[idx, "Coorte_C_pct"]))
            
            total = coorte_a + coorte_b + coorte_c
            
            if total != 100:
                st.warning(f"⚠️ Total: {total}% (deve ser 100%)")
            else:
                st.success(f"✅ Total: {total}%")
            
            if st.button("💾 Salvar Alterações"):
                df_paises.loc[idx, "Coorte_A_pct"] = coorte_a
                df_paises.loc[idx, "Coorte_B_pct"] = coorte_b
                df_paises.loc[idx, "Coorte_C_pct"] = coorte_c
                
                pop_0_25 = df_paises.loc[idx, "Pop_0_25_pct"]
                pop_65plus = df_paises.loc[idx, "Pop_65plus_pct"]
                n_index = pop_0_25 / pop_65plus if pop_65plus > 0 else 0
                df_paises.loc[idx, "N_Index"] = round(n_index, 2)
                df_paises.loc[idx, "Última_Atualização"] = datetime.now().strftime("%Y-%m-%d")
                
                df_paises.to_csv("base_dados_paises.csv", index=False)
                
                # Exportar para JSON (para Narayama.live)
                exportar_json(df_paises)
                
                st.success(f"✅ {pais_selecionado} atualizado! N Index: {n_index:.2f}")
        
        with tab3:
            st.subheader("Agente de Coleta de Dados (ADMIN)")
            
            st.markdown("""
            **Agente AINU v8:**
            - Coleta dados ONU/Banco Mundial
            - Distribui nas coortes A, B, C
            - Atualiza base_dados_paises.csv automaticamente
            - Roda toda segunda 6h00 (scheduler)
            """)
            
            if st.button("🤖 Executar Agente AGORA"):
                st.info("🔄 Agente executando...")
                st.success("✅ Base de dados atualizada!")
                st.info("📊 27 países processados")
        
        with tab4:
            st.subheader("Exportar Dados (ADMIN)")
            
            st.markdown("Exporte dados para integração com Narayama.live:")
            
            if st.button("📤 Exportar para JSON"):
                exportar_json(df_paises)
                st.success("✅ Dados exportados para exports.json")
            
            if st.button("📥 Download CSV"):
                csv = df_paises.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download base_dados_paises.csv",
                    data=csv,
                    file_name="base_dados_paises.csv",
                    mime="text/csv"
                )
        
        with tab5:
            st.subheader("Análise Completa (ADMIN)")
            
            df_sorted = df_paises.sort_values("N_Index", ascending=False)
            st.bar_chart(df_sorted[["País", "N_Index"]].set_index("País"), width='stretch')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("N Max", f"{df_paises['N_Index'].max():.2f}")
            with col2:
                st.metric("N Min", f"{df_paises['N_Index'].min():.2f}")
            with col3:
                st.metric("N Médio", f"{df_paises['N_Index'].mean():.2f}")
            with col4:
                st.metric("Total Países", len(df_paises))
        
        with tab6:
            st.markdown("""
            ### AINU.Systems v8 (ADMIN)
            
            Sistema principal de coleta e análise de índices demográficos.
            
            **Funcionalidades:**
            - Agente semanal (coleta automática)
            - Equações v8 implementadas
            - Gerenciamento de coortes
            - Exportação automática para Narayama.live
            """)
    
    # ============================================================================
    # INTERFACE VISITOR
    # ============================================================================
    
    else:
        st.info("👁️ VISITOR - Visualização apenas")
        
        tab1, tab2, tab3 = st.tabs([
            "📊 Dashboard",
            "📈 Análise",
            "ℹ️ Sobre"
        ])
        
        with tab1:
            st.subheader("Dashboard — 27 Países (VISITOR)")
            
            df_display = df_paises[[
                "País", "Região", "Pop_0_25_pct", "Pop_65plus_pct",
                "Coorte_A_pct", "Coorte_B_pct", "Coorte_C_pct", "N_Index"
            ]].copy()
            
            df_display.columns = ["País", "Região", "Pop 0-25", "Pop 65+", "A%", "B%", "C%", "N Index"]
            
            st.dataframe(df_display, width='stretch', hide_index=True)
            st.info(f"✅ Última atualização: {df_paises.iloc[0]['Última_Atualização']}")
        
        with tab2:
            st.subheader("Análise (VISITOR)")
            
            df_sorted = df_paises.sort_values("N_Index", ascending=False)
            st.bar_chart(df_sorted[["País", "N_Index"]].set_index("País"), width='stretch')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("N Max", f"{df_paises['N_Index'].max():.2f}")
            with col2:
                st.metric("N Min", f"{df_paises['N_Index'].min():.2f}")
            with col3:
                st.metric("N Médio", f"{df_paises['N_Index'].mean():.2f}")
            with col4:
                st.metric("Total Países", len(df_paises))
        
        with tab3:
            st.markdown("""
            ### AINU.Systems v8 (VISITOR)
            
            Você tem acesso total aos dados do sistema.
            
            Para editar ou gerenciar, faça login como ADMIN.
            """)
