import requests
import json
import ipaddress
from flask import Blueprint, render_template, request, redirect, url_for, jsonify

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations_bp.route('/')
def list():
    try:
        reservations = []
        resp_subnets = requests.post(
            'http://150.164.255.46:8100',
            headers={'Content-Type': 'application/json'},
            json={ "command": "subnet4-list" }
        )
        resp_subnets.raise_for_status()
        data_subnets = resp_subnets.json()
        subnets = data_subnets[0].get("arguments", {}).get("subnets", [])
        #print(type(subnets))
        #print(subnets)
        for value in subnets:
            #print(value)
            #print(type(value))
            #print(value)
            subnet_id = value.get('id')
            subnet_ip = value.get('subnet')
            if subnet_id is not None:
                response = requests.post(
                    'http://150.164.255.46:8100',
                    headers={'Content-Type': 'application/json'},
                    json={
                        "command": "reservation-get-all",
                        "service": ["dhcp4"],
                        "arguments": { "subnet-id": subnet_id }
                    }
                )                
                response.raise_for_status()
                result = response.json()
                # Extrair as reservas, assumindo que elas estão em result['arguments']['reservations']
                reservas = result[0].get("arguments", {}).get("hosts", [])
                #print(type(reservas))
                for r in reservas:
                    #print(subnet_id)
                    #print(subnet_ip)
                    #print(type(r))
                    #print(r)
                    mac = r.get('hw-address')
                    ip = r.get('ip-address')
                    reservations.append({
                        "mac": mac,
                        "ip": ip,
                        "subnetid": subnet_id,
                        "subnetip": subnet_ip
                    })
            
        return render_template("reservations.html", reservations=reservations)
    except Exception as e:
        return f"Erro ao consultar reservas: {e}"

@reservations_bp.route('/add', methods=['GET', 'POST'])
def add():
    return "Formulário para adicionar subnet (em breve)"

@reservations_bp.route('/<string:reservation_mac>/edit', methods=['GET', 'POST'])
def edit(reservation_mac):
    return f"Editar reserva {reservation_mac} (em breve)"

@reservations_bp.route('/<string:reservation_mac>/delete')
def delete(reservation_mac):
    return f"Excluir reserva {reservation_mac} (em breve)"

@reservations_bp.route('/create', methods=['POST'])
def create():
    return f"Criar reserva {reservation_mac} (em breve)"