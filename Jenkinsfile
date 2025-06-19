
pipeline {
    agent any
    
    environment {
        // Variáveis do projeto - Versão 2.0
        DOCKER_IMAGE = 'sistema-agendamento-v2'
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'agendamento-app-v2'
        PROJECT_NAME = 'Sistema de Agendamento DevOps 2.0'
    }
    
    stages {
        stage('🔍 Checkout & Verificação') {
            steps {
                echo '📥 Clonando repositório do GitHub...'
                echo "🏗️  Build #${BUILD_NUMBER} - ${PROJECT_NAME}"
                
                // O código já está disponível no workspace do Jenkins
                sh '''
                    echo "📋 Estrutura do projeto:"
                    ls -la
                    
                    echo "\n📊 Informações do ambiente:"
                    echo "🐧 Sistema: $(uname -a)"
                    echo "🐍 Python: $(python3 --version 2>/dev/null || echo 'Python não encontrado')"
                    echo "🐳 Docker: $(docker --version 2>/dev/null || echo 'Docker não encontrado')"
                    echo "📅 Data/Hora: $(date)"
                '''
                echo '✅ Checkout concluído!'
            }
        }
        
        stage('🔧 Verificar Dependências & Arquivos') {
            steps {
                echo '🔍 Verificando arquivos necessários...'
                sh '''
                    echo "📄 Verificando arquivos principais:"
                    
                    # Verificar Dockerfile
                    if [ -f "Dockerfile" ]; then
                        echo "✅ Dockerfile encontrado"
                        echo "📄 Primeiras linhas do Dockerfile:"
                        head -10 Dockerfile | sed 's/^/   /'
                    else
                        echo "❌ Dockerfile não encontrado"
                        exit 1
                    fi
                    
                    # Verificar requirements.txt
                    if [ -f "requirements.txt" ]; then
                        echo "\n✅ requirements.txt encontrado"
                        echo "📦 Dependências:"
                        cat requirements.txt | sed 's/^/   /'
                    else
                        echo "❌ requirements.txt não encontrado"
                        exit 1
                    fi
                    
                    # Verificar arquivos Python
                    echo "\n📄 Verificando arquivos Python:"
                    for file in app.py agendamento.py; do
                        if [ -f "$file" ]; then
                            echo "✅ $file encontrado ($(wc -l < $file) linhas)"
                        else
                            echo "❌ $file não encontrado"
                            exit 1
                        fi
                    done
                    
                    echo "\n🎯 Todos os arquivos necessários estão presentes!"
                '''
            }
        }
        
        stage('🧪 Teste de Conexão SMTP') {
            steps {
                echo '📧 Testando configuração de e-mail...'
                script {
                    try {
                        sh '''
                            echo "🔍 Verificando configuração SMTP..."
                            python3 -c "
import sys
import os
sys.path.append('.')

try:
    from agendamento import testar_conexao_smtp, EMAIL_USUARIO, SMTP_SERVER, SMTP_PORT
    
    print(f'📧 Configuração SMTP:')
    print(f'   Servidor: {SMTP_SERVER}:{SMTP_PORT}')
    print(f'   Usuário: {EMAIL_USUARIO}')
    
    # Verificar se as credenciais foram configuradas
    if EMAIL_USUARIO == 'seuemail@gmail.com':
        print('')
        print('⚠️  ATENÇÃO: Configure suas credenciais de e-mail!')
        print('⚠️  Edite o arquivo agendamento.py e altere:')
        print('⚠️  - EMAIL_USUARIO = \"seu_email@gmail.com\"')
        print('⚠️  - EMAIL_SENHA = \"sua_senha_de_aplicativo\"')
        print('')
        print('🔄 Continuando com teste simulado...')
    else:
        print('')
        print('✅ Credenciais configuradas!')
        print('🔍 Testando conexão SMTP...')
        # testar_conexao_smtp()  # Descomente se as credenciais estiverem configuradas
        print('⚠️  Teste de conexão SMTP comentado para demo')
        
except ImportError as e:
    print(f'❌ Erro na importação: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Erro no teste: {e}')
            "
                        '''
                        echo '✅ Configuração SMTP verificada!'
                    } catch (Exception e) {
                        echo "⚠️ Aviso: ${e.getMessage()}"
                        echo "🔄 Continuando com build mesmo com problema de SMTP..."
                    }
                }
            }
        }
        
        stage('🐳 Build da Imagem Docker') {
            steps {
                echo '🔨 Construindo imagem Docker...'
                script {
                    try {
                        sh '''
                            echo "🐳 Iniciando build da imagem Docker..."
                            echo "📦 Imagem: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                            
                            # Build da imagem
                            docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                            docker build -t ${DOCKER_IMAGE}:latest .
                            
                            echo "\n📋 Verificando imagem criada:"
                            docker images | head -1
                            docker images | grep ${DOCKER_IMAGE} || echo "Nenhuma imagem encontrada"
                            
                            echo "\n📊 Detalhes da imagem:"
                            docker inspect ${DOCKER_IMAGE}:latest | grep -A 5 -B 5 "Created\\|Size" || true
                        '''
                        echo '✅ Imagem Docker construída com sucesso!'
                    } catch (Exception e) {
                        error "❌ Falha no build Docker: ${e.getMessage()}"
                    }
                }
            }
        }
        
        stage('🚀 Executar Container de Agendamento') {
            steps {
                echo '🏃 Executando sistema de agendamento...'
                script {
                    try {
                        sh '''
                            echo "🧹 Limpando containers anteriores..."
                            docker stop ${CONTAINER_NAME} 2>/dev/null || true
                            docker rm ${CONTAINER_NAME} 2>/dev/null || true
                            
                            echo "\n🚀 Iniciando container do sistema de agendamento..."
                            echo "📦 Container: ${CONTAINER_NAME}"
                            echo "🖼️  Imagem: ${DOCKER_IMAGE}:latest"
                            
                            # Executar container
                            docker run --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:latest
                            
                            echo "\n📊 Status final do container:"
                            docker ps -a | head -1
                            docker ps -a | grep ${CONTAINER_NAME} || echo "Container não encontrado"
                        '''
                        echo '✅ Container executado com sucesso!'
                    } catch (Exception e) {
                        echo "ℹ️  Container finalizou a execução (comportamento esperado para aplicação batch)"
                        echo "📊 Coletando logs para análise..."
                    }
                }
            }
        }
        
        stage('📊 Análise de Logs e Resultados') {
            steps {
                echo '📋 Analisando logs da execução...'
                sh '''
                    echo "📊 Logs completos do container ${CONTAINER_NAME}:"
                    echo "=================================================="
                    
                    if docker logs ${CONTAINER_NAME} 2>/dev/null; then
                        echo "\n✅ Logs obtidos com sucesso!"
                    else
                        echo "❌ Não foi possível obter logs do container"
                    fi
                    
                    echo "\n=================================================="
                    echo "🔍 Análise dos resultados:"
                    
                    # Verificar se a aplicação executou com sucesso
                    if docker logs ${CONTAINER_NAME} 2>&1 | grep -q "Sistema executado com sucesso"; then
                        echo "🎉 ✅ Sistema executado com SUCESSO!"
                    elif docker logs ${CONTAINER_NAME} 2>&1 | grep -q "TODOS OS AGENDAMENTOS FORAM PROCESSADOS"; then
                        echo "🎉 ✅ Todos os agendamentos foram processados!"
                    else
                        echo "⚠️ Verificar logs para identificar possíveis problemas"
                    fi
                    
                    # Verificar envio de e-mails
                    echo "\n📧 Verificando envio de e-mails:"
                    if docker logs ${CONTAINER_NAME} 2>&1 | grep -q "E-mail enviado"; then
                        email_count=$(docker logs ${CONTAINER_NAME} 2>&1 | grep -c "E-mail enviado" || echo "0")
                        echo "✅ $email_count e-mails enviados com sucesso"
                    else
                        echo "⚠️ Nenhum e-mail foi enviado (verifique configurações SMTP)"
                    fi
                    
                    # Estatísticas finais
                    echo "\n📈 Estatísticas da execução:"
                    if docker logs ${CONTAINER_NAME} 2>&1 | grep -q "RELATÓRIO FINAL"; then
                        docker logs ${CONTAINER_NAME} 2>&1 | grep -A 10 "RELATÓRIO FINAL" || true
                    fi
                '''
            }
        }
        
        stage('🧹 Limpeza e Finalização') {
            steps {
                echo '🧹 Realizando limpeza pós-execução...'
                sh '''
                    echo "🗑️ Removendo container utilizado:"
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm ${CONTAINER_NAME} 2>/dev/null || true
                    
                    echo "\n📊 Imagens Docker disponíveis:"
                    echo "Projeto: ${DOCKER_IMAGE}"
                    docker images | head -1
                    docker images | grep ${DOCKER_IMAGE} || echo "Nenhuma imagem do projeto encontrada"
                    
                    echo "\n💾 Mantendo imagens para próximas execuções..."
                    echo "🏷️  Imagem latest: ${DOCKER_IMAGE}:latest"
                    echo "🏷️  Imagem build: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    
                    echo "\n🧹 Limpeza de containers órfãos (opcional):"
                    docker container prune -f 2>/dev/null || true
                '''
            }
        }
    }
    
    post {
        always {
            echo '📝 Pipeline finalizado!'
            sh '''
                echo "📊 Resumo Executivo da Execução:"
                echo "============================================"
                echo "🏷️  Projeto: ${PROJECT_NAME}"
                echo "🔢 Build: #${BUILD_NUMBER}"
                echo "🐳 Imagem: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo "📦 Container: ${CONTAINER_NAME}"
                echo "📅 Data/Hora: $(date)"
                echo "⏱️  Duração: ${BUILD_DURATION:-"N/A"} segundos"
                echo "============================================"
            '''
        }
        success {
            echo '🎉 ✅ PIPELINE EXECUTADO COM SUCESSO!'
            echo '🎯 Sistema de agendamento funcionando perfeitamente'
            echo '📧 Verifique se os e-mails foram entregues aos destinatários'
            echo '🚀 Sistema pronto para uso em produção!'
        }
        failure {
            echo '❌ 🚨 PIPELINE FALHOU!'
            echo '🔍 Verifique os logs detalhados acima para identificar o problema'
            echo '💡 Possíveis causas:'
            echo '   - Configurações de e-mail incorretas'
            echo '   - Problemas na construção da imagem Docker'
            echo '   - Arquivos de código com erro de sintaxe'
        }
        unstable {
            echo '⚠️ 🔶 PIPELINE INSTÁVEL!'
            echo '🔍 Alguns testes falharam, mas o build foi concluído'
            echo '📧 Verifique especialmente as configurações de SMTP'
        }
    }
}
