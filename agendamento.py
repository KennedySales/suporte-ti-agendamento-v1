
#!/usr/bin/env python3
"""
Módulo de Agendamento - Sistema de E-mails
Responsável pelo processamento de agendamentos e envio de e-mails
Versão 2.0 - Melhorado com EmailMessage e logs detalhados
"""

import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
import time

# ⚠️ CONFIGURAÇÕES DE E-MAIL - ALTERE AQUI SUAS CREDENCIAIS
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_USUARIO = "seuemail@gmail.com"  # ← Altere aqui
EMAIL_SENHA = "SENHA_DO_APP"          # ← Altere aqui (senha de aplicativo)

# Lista de usuários para agendamento - Versão 2.0 com mais dados
USUARIOS = [
    {
        "nome": "João Silva",
        "email": "joao.silva@exemplo.com",
        "servico": "Instalação de Software",
        "data": "2024-06-15",
        "horario": "14:00",
        "prioridade": "Alta"
    },
    {
        "nome": "Maria Santos",
        "email": "maria.santos@exemplo.com", 
        "servico": "Manutenção de Hardware",
        "data": "2024-06-16",
        "horario": "10:30",
        "prioridade": "Média"
    },
    {
        "nome": "Pedro Costa",
        "email": "pedro.costa@exemplo.com",
        "servico": "Configuração de Rede",
        "data": "2024-06-17",
        "horario": "16:00",
        "prioridade": "Baixa"
    },
    {
        "nome": "Ana Oliveira",
        "email": "ana.oliveira@exemplo.com",
        "servico": "Backup de Dados",
        "data": "2024-06-18",
        "horario": "09:00",
        "prioridade": "Alta"
    }
]

def validar_email(email):
    """Valida se o e-mail possui formato correto"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def enviar_email(destinatario, assunto, corpo):
    """
    Envia e-mail via SMTP usando EmailMessage
    
    Args:
        destinatario (str): E-mail do destinatário
        assunto (str): Assunto do e-mail
        corpo (str): Corpo da mensagem em HTML
    """
    try:
        print(f"📧 Preparando envio de e-mail para: {destinatario}")
        
        # Validar e-mail do destinatário
        if not validar_email(destinatario):
            print(f"❌ E-mail inválido: {destinatario}")
            return False
        
        # Criar mensagem usando EmailMessage
        mensagem = EmailMessage()
        mensagem["Subject"] = assunto
        mensagem["From"] = EMAIL_USUARIO
        mensagem["To"] = destinatario
        
        # Definir conteúdo HTML
        mensagem.set_content(corpo, subtype='html')
        
        print(f"🔐 Conectando ao servidor SMTP {SMTP_SERVER}:{SMTP_PORT}")
        
        # Configurar SSL e enviar
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            print("🔑 Fazendo login no servidor SMTP...")
            server.login(EMAIL_USUARIO, EMAIL_SENHA)
            
            print("📤 Enviando e-mail...")
            server.send_message(mensagem)
        
        print(f"✅ E-mail enviado com sucesso para: {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail para {destinatario}: {str(e)}")
        return False

def gerar_template_solicitacao(usuario):
    """Gera template HTML aprimorado para e-mail de solicitação"""
    timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🎯 HelpDesk Pro</h1>
                <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">Sistema de Agendamento Técnico</p>
            </div>
            
            <div style="padding: 30px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
                <h2 style="color: #2c5aa0; margin-top: 0;">Agendamento Solicitado com Sucesso!</h2>
                
                <p>Olá <strong>{usuario['nome']}</strong>,</p>
                
                <p>Recebemos sua solicitação de agendamento e ela está sendo processada por nossa equipe técnica.</p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2c5aa0;">
                    <h3 style="margin-top: 0; color: #495057;">📋 Detalhes do Agendamento:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">🛠️ Serviço:</td><td style="padding: 8px 0;">{usuario['servico']}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📅 Data:</td><td style="padding: 8px 0;">{usuario['data']}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">⏰ Horário:</td><td style="padding: 8px 0;">{usuario['horario']}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">⚡ Prioridade:</td><td style="padding: 8px 0;"><span style="background: #fff3cd; padding: 2px 8px; border-radius: 4px;">{usuario['prioridade']}</span></td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📊 Status:</td><td style="padding: 8px 0;"><span style="color: #856404;">Aguardando Atendimento</span></td></tr>
                    </table>
                </div>
                
                <div style="background: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #bee5eb;">
                    <p style="margin: 0;"><strong>💡 Próximos Passos:</strong></p>
                    <p style="margin: 5px 0 0 0;">Em breve você receberá uma confirmação quando o atendimento for realizado por nossa equipe.</p>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #dee2e6;">
                
                <div style="text-align: center; color: #6c757d; font-size: 12px;">
                    <p>Sistema de Suporte Técnico - HelpDesk Pro</p>
                    <p>Solicitação processada em {timestamp}</p>
                    <p>Este é um e-mail automático, não responda.</p>
                </div>
            </div>
        </body>
    </html>
    """

def gerar_template_atendimento(usuario):
    """Gera template HTML aprimorado para e-mail de atendimento"""
    timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 24px;">✅ HelpDesk Pro</h1>
                <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">Atendimento Concluído</p>
            </div>
            
            <div style="padding: 30px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
                <h2 style="color: #28a745; margin-top: 0;">Agendamento Atendido com Sucesso!</h2>
                
                <p>Olá <strong>{usuario['nome']}</strong>,</p>
                
                <p>Temos o prazer de informar que seu agendamento foi <strong>atendido com sucesso</strong> por nossa equipe técnica!</p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <h3 style="margin-top: 0; color: #155724;">📋 Serviço Concluído:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 8px 0; font-weight: bold;">🛠️ Serviço:</td><td style="padding: 8px 0;">{usuario['servico']}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">📅 Data:</td><td style="padding: 8px 0;">{usuario['data']}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">⏰ Horário:</td><td style="padding: 8px 0;">{usuario['horario']}</td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">⚡ Prioridade:</td><td style="padding: 8px 0;"><span style="background: #d4edda; padding: 2px 8px; border-radius: 4px;">{usuario['prioridade']}</span></td></tr>
                        <tr><td style="padding: 8px 0; font-weight: bold;">✅ Status:</td><td style="padding: 8px 0;"><span style="color: #28a745; font-weight: bold;">CONCLUÍDO</span></td></tr>
                    </table>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; text-align: center;">
                    <h4 style="margin-top: 0; color: #856404;">⭐ Avalie Nosso Atendimento</h4>
                    <p style="margin: 10px 0;">Sua opinião é muito importante para nós!</p>
                    <div style="margin: 15px 0;">
                        <span style="font-size: 24px; margin: 0 5px; cursor: pointer;">⭐⭐⭐⭐⭐</span>
                    </div>
                </div>
                
                <div style="background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>📞 Precisando de mais alguma coisa?</strong></p>
                    <p style="margin: 5px 0 0 0;">Nossa equipe está sempre disponível para ajudar. Entre em contato quando precisar!</p>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #dee2e6;">
                
                <div style="text-align: center; color: #6c757d; font-size: 12px;">
                    <p>Sistema de Suporte Técnico - HelpDesk Pro</p>
                    <p>Atendimento concluído em {timestamp}</p>
                    <p>Este é um e-mail automático, não responda.</p>
                </div>
            </div>
        </body>
    </html>
    """

def testar_conexao_smtp():
    """Testa conectividade SMTP antes do envio"""
    try:
        print("🔍 Iniciando teste de conexão SMTP...")
        print(f"📡 Servidor: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"👤 Usuário: {EMAIL_USUARIO}")
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            print("🔐 Estabelecendo conexão SSL...")
            server.login(EMAIL_USUARIO, EMAIL_SENHA)
            print("🔑 Login realizado com sucesso!")
            
        print("✅ Conexão SMTP estabelecida com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão SMTP: {str(e)}")
        print("⚠️  Verifique suas credenciais de e-mail!")
        return False

def processar_agendamento():
    """
    Processa todos os agendamentos e envia e-mails de confirmação
    Versão 2.0 - Com logs detalhados e estatísticas
    """
    print("🚀 Iniciando Sistema de Agendamento - Versão 2.0")
    print("=" * 60)
    
    # Estatísticas iniciais
    total_usuarios = len(USUARIOS)
    emails_enviados = 0
    emails_falharam = 0
    
    print(f"📊 Estatísticas:")
    print(f"   Total de usuários: {total_usuarios}")
    print(f"   E-mails a enviar: {total_usuarios * 2}")
    print("-" * 60)
    
    # Testar conexão SMTP primeiro
    if not testar_conexao_smtp():
        print("❌ Abortando execução devido a falha na conexão SMTP")
        return False
    
    print(f"\n📋 Processando agendamentos...")
    print("-" * 60)
    
    for i, usuario in enumerate(USUARIOS, 1):
        print(f"\n🔄 [{i}/{total_usuarios}] Processando: {usuario['nome']}")
        print(f"   📧 E-mail: {usuario['email']}")
        print(f"   🛠️  Serviço: {usuario['servico']}")
        print(f"   📅 Data/Hora: {usuario['data']} às {usuario['horario']}")
        print(f"   ⚡ Prioridade: {usuario['prioridade']}")
        
        # 1. Enviar e-mail de solicitação
        print(f"\n   📤 [1/2] Enviando confirmação de solicitação...")
        assunto_solicitacao = f"🎯 Agendamento Solicitado - {usuario['servico']}"
        corpo_solicitacao = gerar_template_solicitacao(usuario)
        
        if enviar_email(usuario['email'], assunto_solicitacao, corpo_solicitacao):
            emails_enviados += 1
            print(f"   ✅ Confirmação de solicitação enviada!")
        else:
            emails_falharam += 1
            print(f"   ❌ Falha no envio da confirmação de solicitação!")
        
        # Simular tempo de processamento
        print(f"   ⏳ Processando agendamento...")
        time.sleep(3)  # Simula tempo de atendimento
        
        # 2. Enviar e-mail de atendimento
        print(f"   📤 [2/2] Enviando confirmação de atendimento...")
        assunto_atendimento = f"✅ Agendamento Atendido - {usuario['servico']}"
        corpo_atendimento = gerar_template_atendimento(usuario)
        
        if enviar_email(usuario['email'], assunto_atendimento, corpo_atendimento):
            emails_enviados += 1
            print(f"   ✅ Confirmação de atendimento enviada!")
        else:
            emails_falharam += 1
            print(f"   ❌ Falha no envio da confirmação de atendimento!")
        
        print(f"   🎉 Usuário {usuario['nome']} processado com sucesso!")
        
        if i < total_usuarios:
            print(f"   ⏸️  Aguardando próximo usuário...")
            time.sleep(2)
    
    # Estatísticas finais
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL:")
    print(f"   👥 Usuários processados: {total_usuarios}")
    print(f"   ✅ E-mails enviados: {emails_enviados}")
    print(f"   ❌ E-mails falharam: {emails_falharam}")
    print(f"   📈 Taxa de sucesso: {(emails_enviados/(total_usuarios*2)*100):.1f}%")
    
    if emails_falharam == 0:
        print("\n🎉 TODOS OS AGENDAMENTOS FORAM PROCESSADOS COM SUCESSO!")
    else:
        print(f"\n⚠️  {emails_falharam} e-mails falharam. Verifique os logs acima.")
    
    print("=" * 60)
    return emails_falharam == 0

if __name__ == "__main__":
    processar_agendamento()
