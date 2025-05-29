const express = require('express');
const mysql = require('mysql2');
const app = express();
const PORT = 3000;

app.use(express.json());

const conn = mysql.createConnection({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASS || '',
    database: process.env.DB_NAME || 'suporte_ti'
});

conn.connect(err => {
    if (err) throw err;
    console.log("Conectado ao MySQL!");
});

// Rota de login
app.post('/login', (req, res) => {
    const { email, senha } = req.body;

    conn.query(
        'SELECT * FROM usuarios WHERE email = ? AND senha = ?',
        [email, senha],
        (err, results) => {
            if (err) return res.status(500).send(err);
            if (results.length > 0) res.send("Login bem-sucedido!");
            else res.status(401).send("Usuário ou senha inválidos.");
        }
    );
});

// Rota de agendamento
app.post('/agendar', (req, res) => {
    const { usuario_id, data, descricao } = req.body;
    conn.query(
        'INSERT INTO agendamentos (usuario_id, data, descricao) VALUES (?, ?, ?)',
        [usuario_id, data, descricao],
        (err) => {
            if (err) return res.status(500).send(err);
            res.send("Agendamento registrado com sucesso!");
        }
    );
});

app.listen(PORT, () => console.log(`Servidor rodando em http://localhost:${PORT}`));