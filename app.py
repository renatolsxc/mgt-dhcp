from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
from crud_subnets import subnets_bp
from crud_reservations import reservations_bp

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Troque por algo mais seguro em produção
app.register_blueprint(subnets_bp)
app.register_blueprint(reservations_bp)

# Usuário fixo para teste
USER = {'username': 'admin', 'password': 'admin'}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USER['username'] and password == USER['password']:
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Por favor, faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

#from flask import render_template
#import requests


#@app.route('/subnets')
#def list_subnets():
#    curl_command = [
#        "curl", "--location", "http://150.164.255.46:8100",
#        "--header", "Content-Type: application/json",
#        "--data", '{ "command": "subnet4-list" }'
#    ]
#    result = subprocess.run(curl_command, capture_output=True, text=True)
#    body = result.stdout
#    return render_template_string("""
#        <h1>Resposta bruta do curl /subnets</h1>
#        <pre>{{ body }}</pre>
#    """, body=body)

#@app.route('/subnets')
#def list_subnets():
#    if 'username' not in session:
#        flash('Por favor, faça login para acessar o sistema.', 'warning')
#        return redirect(url_for('login'))
    # Exemplo estático
#    subnets = [
#        {'id': 1, 'subnet': '192.168.1.0/24', 'description': 'Rede local'},
#        {'id': 2, 'subnet': '10.0.0.0/24', 'description': 'Rede interna'},
#    ]
#    return render_template('subnets.html', subnets=subnets)

#@app.route('/reservations')
#def list_reservations():
#    if 'username' not in session:
#        flash('Por favor, faça login para acessar o sistema.', 'warning')
#        return redirect(url_for('login'))
#    # Exemplo estático
#    reservations = [
#        {'id': 1, 'mac': 'AA:BB:CC:DD:EE:FF', 'ip': '192.168.1.100', 'hostname': 'host1'},
#        {'id': 2, 'mac': '11:22:33:44:55:66', 'ip': '192.168.1.101', 'hostname': 'host2'},
#    ]
#    return render_template('reservations.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)




if __name__ == '__main__':
    print(app.url_map)  # Lista todas as rotas registradas
    app.run(debug=True)