
#!/usr/bin/env python3
"""
Sistema de Agendamento DevOps 2.0 com Docker, Jenkins e E-mails
Aplicação principal que orquestra o processamento de agendamentos

Versão 2.0 - Melhorado com:
- Logs mais detalhados
- Tratamento de erros aprimorado  
- Estatísticas de execução
- Integração completa CI/CD
"""

import sys
import time
import os
from datetime import datetime
from agendamento import processar_agendamento

def exibir_banner():
    """Exibe banner de inicialização do sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🚀 SISTEMA DE AGENDAMENTO DEVOPS 2.0                     ║
    ║                                                              ║
    ║    📧 Automação de E-mails | 🐳 Docker | 🔧 Jenkins        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def exibir_informacoes_sistema():
    """Exibe informações do ambiente de execução"""
    print("📊 INFORMAÇÕES DO SISTEMA:")
    print("=" * 50)
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"🖥️  Sistema: {os.name}")
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📁 Diretório: {os.getcwd()}")
    print(f"👤 Usuário: {os.getenv('USER', 'N/A')}")
    
    # Verificar variáveis de ambiente do Jenkins
    jenkins_vars = ['BUILD_NUMBER', 'JOB_NAME', 'WORKSPACE']
    jenkins_info = {var: os.getenv(var, 'N/A') for var in jenkins_vars}
    
    if any(value != 'N/A' for value in jenkins_info.values()):
        print("\n🔧 INFORMAÇÕES DO JENKINS:")
        for var, value in jenkins_info.items():
            print(f"   {var}: {value}")
    
    print("=" * 50)

def main():
    """Função principal da aplicação"""
    inicio_execucao = time.time()
    
    try:
        # Exibir banner e informações
        exibir_banner()
        exibir_informacoes_sistema()
        
        print("\n🚀 Iniciando processamento de agendamentos...")
        print("⏳ Aguarde enquanto processamos todos os agendamentos...")
        print("=" * 50)
        
        # Processar agendamentos
        sucesso = processar_agendamento()
        
        # Calcular tempo de execução
        tempo_execucao = time.time() - inicio_execucao
        
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO DE EXECUÇÃO:")
        print(f"⏱️  Tempo total: {tempo_execucao:.2f} segundos")
        print(f"📅 Finalizado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
        
        if sucesso:
            print("🎉 ✅ Sistema executado com sucesso!")
            print("📧 Todos os e-mails foram processados")
            print("🚀 Agendamentos finalizados com êxito!")
        else:
            print("⚠️ ❌ Sistema executado com problemas!")
            print("📧 Alguns e-mails podem não ter sido enviados")
            print("🔍 Verifique os logs acima para detalhes")
            
        print("=" * 50)
        
        # Código de saída baseado no sucesso
        sys.exit(0 if sucesso else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ ❌ Execução interrompida pelo usuário!")
        print("🔄 Para continuar, execute o sistema novamente")
        sys.exit(1)
        
    except Exception as e:
        tempo_execucao = time.time() - inicio_execucao
        
        print(f"\n❌ 🚨 ERRO CRÍTICO durante execução:")
        print(f"   Erro: {str(e)}")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Tempo até falha: {tempo_execucao:.2f} segundos")
        print("\n🔍 DICAS PARA SOLUÇÃO:")
        print("   1. Verifique as credenciais de e-mail em agendamento.py")
        print("   2. Confirme se todas as dependências estão instaladas")
        print("   3. Teste a conexão de internet e acesso ao servidor SMTP")
        print("   4. Revise os logs detalhados acima")
        print("=" * 50)
        
        sys.exit(1)

if __name__ == "__main__":
    main()
