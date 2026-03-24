next-holding-app/
├── app.py              # Lógica principal (Back-end)
├── database.db         # Banco de dados (SQLite para começar)
├── requirements.txt    # Dependências do projeto
├── templates/
│   ├── login.html      # Tela de entrada Next
│   ├── admin.html      # Seu Painel (Dono/CEO)
│   └── dashboard.html  # Painel do Funcionário (Vendas/2k)
└── static/
    └── css/style.css   # Estilização visual (Dourado/Azul Marinho)
    from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "next_ceo_key_2026"

# Simulação de Banco de Dados (Configuração de Rotas)
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('login.html')

# LÓGICA DE DIVISÃO DE LUCRO (O SPLIT)
@app.route('/venda_concluida/<int:user_id>')
def processar_venda(user_id):
    db = get_db()
    # Adiciona R$ 225 para o vendedor (Saldo Interno)
    db.execute('UPDATE usuarios SET saldo_interno = saldo_interno + 225 WHERE id = ?', (user_id,))
    # Adiciona R$ 375 para o Dono (Lucro Real Wellington)
    db.execute('UPDATE lucro_ceo SET total = total + 375 WHERE id = 1')
    db.commit()
    return redirect(url_for('dashboard'))

# LÓGICA DE BANIMENTO (O BOTÃO X)
@app.route('/banir/<int:user_id>', methods=['POST'])
def banir_usuario(user_id):
    if session.get('cargo') != 'Dono':
        return "Acesso Negado", 403
    
    db = get_db()
    db.execute('UPDATE usuarios SET status = "Banido" WHERE id = ?', (user_id,))
    db.commit()
    flash(f"Usuário {user_id} banido com sucesso. Saldo retido.")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
    <!DOCTYPE html>
<html lang="pt-br">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Next Holding - Painel CEO</title>
</head>
<body class="bg-slate-900 text-white font-sans">
    <nav class="p-6 border-b border-yellow-600 flex justify-between">
        <h1 class="text-2xl font-bold text-yellow-500">NEXT HOLDING 👑</h1>
        <span>Bem-vindo, CEO Wellington</span>
    </nav>

    <main class="p-10">
        <div class="bg-gradient-to-r from-yellow-600 to-yellow-800 p-8 rounded-xl shadow-2xl mb-10">
            <h2 class="text-xl opacity-80">Seu Lucro Líquido Real (R$ 375/venda)</h2>
            <p class="text-5xl font-black mt-2">R$ {{ lucro_total }}</p>
        </div>

        <div class="bg-slate-800 rounded-lg p-6">
            <h3 class="text-xl mb-4 font-semibold text-blue-400 font-bold">Gerenciar Equipe (Elite Next)</h3>
            <table class="w-full text-left">
                <thead>
                    <tr class="border-b border-slate-700">
                        <th class="py-2">Vendedor</th>
                        <th>Vendas</th>
                        <th>Saldo 2k</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="border-b border-slate-700 hover:bg-slate-700 transition">
                        <td class="py-4">Carlos Vendas</td>
                        <td>12</td>
                        <td class="text-green-400">R$ 2.700,00</td>
                        <td>
                            <form action="/banir/2" method="POST">
                                <button class="bg-red-600 hover:bg-red-800 px-3 py-1 rounded text-sm">BANIR (X)</button>
                            </form>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>
</body>
</html>
