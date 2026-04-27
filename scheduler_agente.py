"""
SCHEDULER AGENTE SEMANAL — AINU v8
Executa coleta de dados automaticamente

Autor: ITIBERÊ MUARREK
Email: itibere@gmail.com
Versão: 1.0 (Abril 2026)
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import agent_coleta_dados
import logging

# ============================================================================
# CONFIGURAR LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# FUNÇÃO: EXECUTAR AGENTE
# ============================================================================

def executar_agente_semanal():
    """
    Função chamada automaticamente toda segunda 6h00
    """
    logger.info("="*80)
    logger.info("🤖 AGENTE SEMANAL INICIADO")
    logger.info("="*80)
    
    try:
        df = agent_coleta_dados.coletar_e_processar_dados()
        logger.info(f"✅ Agente executado com sucesso! {len(df)} países atualizados")
    except Exception as e:
        logger.error(f"❌ Erro ao executar agente: {e}")
    
    logger.info("="*80)

# ============================================================================
# INICIAR SCHEDULER
# ============================================================================

def iniciar_scheduler():
    """
    Inicia o scheduler que executa o agente toda segunda 6h00
    """
    scheduler = BackgroundScheduler()
    
    # Configurar: SEGUNDA-FEIRA (0) às 6h00 (06:00)
    trigger = CronTrigger(day_of_week=0, hour=6, minute=0)
    
    scheduler.add_job(
        func=executar_agente_semanal,
        trigger=trigger,
        id="agente_coleta_dados",
        name="Coleta de dados semanal",
        replace_existing=True
    )
    
    scheduler.start()
    
    logger.info("="*80)
    logger.info("✅ SCHEDULER INICIADO")
    logger.info("="*80)
    logger.info("⏰ Próxima execução: SEGUNDA-FEIRA às 6h00")
    logger.info("📊 Agente: Coleta dados ONU/BM e atualiza base_dados_paises.csv")
    logger.info("="*80)
    
    return scheduler

# ============================================================================
# EXECUTAR MANUALMENTE (para testes)
# ============================================================================

def executar_manualmente():
    """
    Executa o agente uma vez (para testes)
    """
    logger.info("🚀 Executando agente manualmente...")
    executar_agente_semanal()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("SCHEDULER AGENTE SEMANAL")
    print("="*80)
    print()
    print("Opções:")
    print("  1. Iniciar scheduler (agente roda toda segunda 6h00)")
    print("  2. Executar manualmente agora")
    print()
    
    escolha = input("Escolha (1 ou 2): ").strip()
    
    if escolha == "1":
        scheduler = iniciar_scheduler()
        try:
            print("\n✅ Scheduler rodando. Pressione CTRL+C para parar.")
            scheduler.start()
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Scheduler parado pelo usuário")
            scheduler.shutdown()
    
    elif escolha == "2":
        executar_manualmente()
    
    else:
        print("❌ Opção inválida")
