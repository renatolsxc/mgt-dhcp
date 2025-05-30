import requests
import ipaddress
from flask import Blueprint, render_template, request, redirect, url_for, jsonify

subnets_bp = Blueprint('subnets', __name__, url_prefix='/subnets')


@subnets_bp.route('/')
def list_subnets():
    try:
        response = requests.post(
            'http://150.164.255.46:8100',
            headers={'Content-Type': 'application/json'},
            json={ "command": "subnet4-list" }
        )
        response.raise_for_status()
        data = response.json()
        subnets = data[0].get("arguments", {}).get("subnets", [])
        return render_template('subnets.html', subnets=subnets)
    except Exception as e:
        return f"Erro ao consultar subnets: {e}"

@subnets_bp.route('/add', methods=['GET', 'POST'])
def add_subnet():
    if request.method == 'POST':
        # Aqui você adicionaria a lógica para salvar a nova subnet
        return redirect(url_for('subnets.list_subnets'))
    return "Formulário para adicionar subnet (em breve)"

@subnets_bp.route('/<int:subnet_id>/edit', methods=['GET', 'POST'])
def edit_subnet(subnet_id):
    return f"Editar subnet {subnet_id} (em breve)"

@subnets_bp.route('/<int:subnet_id>/delete')
def delete_subnet(subnet_id):
    return f"Excluir subnet {subnet_id} (em breve)"

@subnets_bp.route('/create', methods=['POST'])
def create():
    try:
        response = requests.post(
            'http://150.164.255.46:8100',
            headers={'Content-Type': 'application/json'},
            json={ "command": "subnet4-list" }
        )
        response.raise_for_status()
        atuais = response.json()
        atuais_subs = atuais[0].get("arguments", {}).get("subnets", [])
        
        data = request.get_json()
        subnet_input = data['subnet']
        id_input = data['id']
        
        #if not data or 'subnet' not in data:
        #    return jsonify({"status": "error", "message": "Dados inválidos"}), 400
        
        # Validar formato da subnet
        try:
            ipaddress.ip_network(data['subnet'], strict=False)
        except:
            return jsonify({"status": "error", "message": "Formato de subnet inválido"}), 400

        # Verificar duplicidade de ID
        if any(s['id'] == id_input for s in atuais_subs):
            return jsonify({"status": "error", "message": f"ID {id_input} já existe"}), 400

        # Verificar duplicidade de subnet
        if any(s['subnet'] == subnet_input for s in atuais_subs):
            return jsonify({"status": "error", "message": "Subnet já cadastrada"}), 400

        # Lista local, inicializada a cada requisição
        subnets = []
        
        #new_id = 1  # Já que a lista está sempre vazia
        subnets.append({"id": data['id'], "subnet": data['subnet']})

        # Apenas para debug, já que a lista não será usada depois
        print("Subnet adicionada:", subnets)
        subnet_str = data["subnet"]
        subnet_id = int(data["id"])
        
        # Cria o IP do roteador: 172.17.{id}.254
        router_ip = f"172.17.{subnet_id}.254"
        payload = {
            "command": "config-test",
            "service": ["dhcp4"],
            "arguments": {
                "Dhcp4": {
                    "subnet4": [
                        {
                            "id": subnet_id,
                            "subnet": subnet_str,
                            "option-data": [
                                {
                                    "name": "routers",
                                    "data": router_ip
        
                                }
                            ]
                        }
                    ]
                }
            }
        }
        
        try:
            response = requests.post(
                "http://150.164.255.46:8100",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            resultado_cru = response.json()
            resultado = resultado_cru[0]
            # opcional: verificar se passou no teste
            if resultado.get("result") == 0:
                print("Tentou validar a config no kea:", resultado)
                return jsonify({"status": "success", "message": "Configuração válida, Kea aceitou!"}), 200
            else:
                print("Tentou validar a config no kea:", resultado)
                return jsonify({"status": "error", "message": "Configuração inválida, Kea rejeitou!"}), 400
        except requests.RequestException as e:
            return jsonify({"status": "error", "message": f"Erro ao testar config: {e}"}), 500
        
        return jsonify({"status": "success"})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
#    data = request.get_json()
#    if not data or 'subnet' not in data:
#        return jsonify({"status": "error", "message": "Dados inválidos"}), 400
#    new_id = max([s["id"] for s in subnets] + [0]) + 1
#    subnets.append({"id": new_id, "subnet": data['subnet']})
#    return jsonify({"status": "success"})