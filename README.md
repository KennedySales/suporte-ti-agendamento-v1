# Sistema de Suporte Técnico em TI

Sistema completo de suporte técnico desenvolvido com **React/TypeScript** (frontend) e **Node.js/Express** (backend), incluindo autenticação de usuários e agendamento de atendimentos técnicos.

## 📋 Funcionalidades

- **Autenticação de Usuários**: Login seguro com email e senha
- **Agendamento de Atendimentos**: Interface intuitiva para agendar serviços técnicos
- **Interface Responsiva**: Design moderno e adaptável para diferentes dispositivos
- **Validação de Formulários**: Validação client-side e server-side
- **Notificações**: Sistema de toast para feedback ao usuário

## Backend (Estrutura Proposta)

- **Node.js** com **Express**
- **MySQL** para banco de dados
- **JWT** para autenticação
- **bcrypt** para hash de senhas

## DevOps (Estrutura Proposta)

- **Docker** e **Docker Compose**
- **Kubernetes**
- **Jenkins CI/CD**

## Dados para Teste

- **Email**: admin@empresa.com
- **Senha**: 123456

## 🐳 Backend - Estrutura Node.js/Express

### Arquivo `package.json` (backend)

```json
{
  "name": "helpdesk-backend",
  "version": "1.0.0",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mysql2": "^3.6.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.6.1"
  }
}
Estrutura do Banco de Dados
Tabela usuarios

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Tabela agendamentos

CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    descricao TEXT NOT NULL,
    status ENUM('agendado', 'em_andamento', 'concluido', 'cancelado') DEFAULT 'agendado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);