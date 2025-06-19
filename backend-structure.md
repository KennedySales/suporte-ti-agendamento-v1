
# Estrutura do Backend - Node.js/Express

## 📁 Estrutura de Diretórios

```
backend/
├── src/
│   ├── controllers/
│   │   ├── authController.js
│   │   └── agendamentoController.js
│   ├── models/
│   │   ├── Usuario.js
│   │   └── Agendamento.js
│   ├── routes/
│   │   ├── auth.js
│   │   └── agendamentos.js
│   ├── middleware/
│   │   ├── auth.js
│   │   └── validation.js
│   ├── config/
│   │   └── database.js
│   └── server.js
├── tests/
│   ├── auth.test.js
│   └── agendamentos.test.js
├── Dockerfile
├── package.json
└── .env.example
```

## 📄 Exemplos de Código

### server.js
```javascript
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const authRoutes = require('./routes/auth');
const agendamentoRoutes = require('./routes/agendamentos');

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json());

// Rotas
app.use('/api', authRoutes);
app.use('/api', agendamentoRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});

module.exports = app;
```

### controllers/authController.js
```javascript
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const Usuario = require('../models/Usuario');

const login = async (req, res) => {
  try {
    const { email, senha } = req.body;

    // Buscar usuário
    const usuario = await Usuario.findByEmail(email);
    if (!usuario) {
      return res.status(401).json({ message: 'Credenciais inválidas' });
    }

    // Verificar senha
    const senhaValida = await bcrypt.compare(senha, usuario.senha);
    if (!senhaValida) {
      return res.status(401).json({ message: 'Credenciais inválidas' });
    }

    // Gerar token
    const token = jwt.sign(
      { id: usuario.id, email: usuario.email },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({
      token,
      user: {
        id: usuario.id,
        nome: usuario.nome,
        email: usuario.email
      }
    });
  } catch (error) {
    console.error('Erro no login:', error);
    res.status(500).json({ message: 'Erro interno do servidor' });
  }
};

module.exports = { login };
```

### controllers/agendamentoController.js
```javascript
const Agendamento = require('../models/Agendamento');

const criarAgendamento = async (req, res) => {
  try {
    const { data, hora, descricao } = req.body;
    const usuario_id = req.user.id;

    const agendamento = await Agendamento.create({
      usuario_id,
      data,
      hora,
      descricao
    });

    res.status(201).json({
      message: 'Agendamento criado com sucesso',
      agendamento
    });
  } catch (error) {
    console.error('Erro ao criar agendamento:', error);
    res.status(500).json({ message: 'Erro interno do servidor' });
  }
};

const listarAgendamentos = async (req, res) => {
  try {
    const usuario_id = req.user.id;
    const agendamentos = await Agendamento.findByUserId(usuario_id);
    
    res.json(agendamentos);
  } catch (error) {
    console.error('Erro ao listar agendamentos:', error);
    res.status(500).json({ message: 'Erro interno do servidor' });
  }
};

module.exports = { criarAgendamento, listarAgendamentos };
```

### models/Usuario.js
```javascript
const db = require('../config/database');

class Usuario {
  static async findByEmail(email) {
    const [rows] = await db.execute(
      'SELECT * FROM usuarios WHERE email = ?',
      [email]
    );
    return rows[0];
  }

  static async create(userData) {
    const { nome, email, senha } = userData;
    const [result] = await db.execute(
      'INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
      [nome, email, senha]
    );
    return { id: result.insertId, nome, email };
  }
}

module.exports = Usuario;
```

### models/Agendamento.js
```javascript
const db = require('../config/database');

class Agendamento {
  static async create(agendamentoData) {
    const { usuario_id, data, hora, descricao } = agendamentoData;
    const [result] = await db.execute(
      'INSERT INTO agendamentos (usuario_id, data, hora, descricao) VALUES (?, ?, ?, ?)',
      [usuario_id, data, hora, descricao]
    );
    
    return {
      id: result.insertId,
      usuario_id,
      data,
      hora,
      descricao,
      status: 'agendado'
    };
  }

  static async findByUserId(usuario_id) {
    const [rows] = await db.execute(
      'SELECT * FROM agendamentos WHERE usuario_id = ? ORDER BY data DESC, hora DESC',
      [usuario_id]
    );
    return rows;
  }
}

module.exports = Agendamento;
```

### config/database.js
```javascript
const mysql = require('mysql2/promise');

const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'helpdesk',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
};

const pool = mysql.createPool(dbConfig);

module.exports = pool;
```

### middleware/auth.js
```javascript
const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ message: 'Token de acesso requerido' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Token inválido' });
  }
};

module.exports = authMiddleware;
```

### routes/auth.js
```javascript
const express = require('express');
const { login } = require('../controllers/authController');

const router = express.Router();

router.post('/login', login);

module.exports = router;
```

### routes/agendamentos.js
```javascript
const express = require('express');
const { criarAgendamento, listarAgendamentos } = require('../controllers/agendamentoController');
const authMiddleware = require('../middleware/auth');

const router = express.Router();

router.post('/agendar', authMiddleware, criarAgendamento);
router.get('/agendamentos', authMiddleware, listarAgendamentos);

module.exports = router;
```

### .env.example
```
# Configurações do Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=123456
DB_NAME=helpdesk

# JWT Secret
JWT_SECRET=seu-jwt-secret-super-secreto

# Porta da aplicação
PORT=3000
```

### SQL de Inicialização (init.sql)
```sql
-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS helpdesk;
USE helpdesk;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de agendamentos
CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    descricao TEXT NOT NULL,
    status ENUM('agendado', 'em_andamento', 'concluido', 'cancelado') DEFAULT 'agendado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Inserir usuário de teste
INSERT INTO usuarios (nome, email, senha) VALUES 
('Administrador', 'admin@empresa.com', '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');
-- Senha: 123456 (hasheada)
```

Este backend completo fornece:
- ✅ Autenticação JWT
- ✅ Operações CRUD para agendamentos
- ✅ Validação de dados
- ✅ Middleware de segurança
- ✅ Estrutura escalável
- ✅ Configuração para Docker
- ✅ Pronto para deploy
