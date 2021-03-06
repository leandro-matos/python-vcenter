import requests, urllib3, os, json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server   = os.getenv('VCENTER_HOST')
username = os.getenv('VCENTER_USERNAME')
password = os.getenv('VCENTER_PASSWORD')
datastore_name = os.getenv('DATASTORE_NAME')
folder_name = os.getenv('FOLDER_NAME')

ENDPOINT_SESSION = f'https://{server}/rest/com/vmare/cis/session'

def login_vmare(): # Login no Vmware
    try:
        url = ENDPOINT_SESSION
        response = requests.post(url, auth=(username, password), verify=False)
        if response.status_code == 200:
            content = response.json()
            token = content['value']
            return token
    except:
        print('Token Inválido, verifique novamente.')

def list_vms(token): # Listar as VM's
    try:
        url = f'https://{server}/rest/vcenter/vm'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token
        }

        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            vms = []
            content = response.json()
            for vm in content['value']:
                temp_dict = {}
                vm_id = vm['vm']
                vm_name = vm['name']
                vm_power_state = vm['power_state']
                vm_cpu_count = vm['cpu_count']
                temp_dict['vm_id'] = vm_id
                temp_dict['vm_name'] = vm_name
                temp_dict['vm_power_state'] = vm_power_state
                temp_dict['vm_cpu_count'] = vm_cpu_count
                vms.append(temp_dict)
            return vms
    except:
        print('Não foi possível listar as VMs. Verifique novamente')
    
def poweroff_vm(token, vmid): # Desligar uma VM
    try:
        url = f'https://{server}/rest/vcenter/vm/{vmid}/power/stop'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token
        }
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code == 200:
            message = f'VM {vmid} was stopped'
            return message
        elif response.status_code == 400:
            content = response.json()
            result = content['value']['messages'][0]['default_message']
            message = f'[{vmid}]: {result}'
            return message
    except:
        print('Não foi possível desligar a VM. Tente novamente')

def poweron_vm(token, vmid):  # Ligar uma VM
    try:
        url = f'https://{server}/rest/vcenter/vm/{vmid}/power/start'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token
        }
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code == 200:
            message = f'VM {vmid} was started'
            return message
        elif response.status_code == 400:
            content = response.json()
            result = content['value']['messages'][0]['default_message']
            message = f'[{vmid}]: {result}'
            return message
    except:
        print('Não foi possível ligar a VM. Tente novamente')
    
def update_cpu(token, vmid, cpu): # Alterar CPU de uma VM
    try:
        url = f'https://{server}/rest/vcenter/vm/{vmid}/hardware/cpu'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token
        }

        data = {
            "spec": {
                "cores_per_socket": cpu,
                "count": cpu
            }
        }

        response = requests.patch(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            message = f'VM {vmid} was updated'
            print(message)
        elif response.status_code == 400:
            content = response.json()
            result = content['value']['messages'][0]['default_message']
            message = f'[{vmid}]: {result}'
    except:
        print('Não foi possível atualizar a VM. Tente novamente')

def get_datastores(token): # Listar DataStore
    try:
        url = f'https://{server}/rest/vcenter/datastore'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token
        }
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            datastores = []
            content = response.json()
            for datastore in content['value']:
                datastore_id = datastore['datastore']
                datastore_name = datastore['name']
                datastore_type = datastore['type']
                datastore_free_space = datastore['free_space']
                datastore_capacity = datastore['capacity']
                datastore_utilization_perc = (datastore_free_space * 100) / datastore_capacity
                print(f'{datastore_name}, {datastore_utilization_perc:.2f}%')
                temp_dict = {}
                temp_dict['datastore_id'] = datastore_id
                temp_dict['datastore_name'] = datastore_name
                temp_dict['datastore_type'] = datastore_type
                temp_dict['datstore_free_space'] = datastore_free_space
                temp_dict['datastore_capacity'] = datastore_capacity
                temp_dict['datastore_utilization_perc']  = datastore_utilization_perc
                datastore.append(temp_dict)
            return datastore
    except:
        print('Não foi possível listar os datastores. Tente novamente')
    
def get_cluster_id(token): # Listar os clusters
    try:
        url = f'https://{server}/rest/vcenter/cluster'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token,
        }

        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            content = response.json()
            cluster_id = content['value'][0]['cluster']
            return cluster_id
    except:
        print('Não foi possível obter o Cluster ID. Tente novamente')

def get_datastore_id(token, datastore_name): # Listar Datastore
    try:
        url = f'https://{server}/rest/vcenter/datastore'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token,
        }

        query_string = {'filter.names.1': datastore_name}

        response = requests.get(url, headers=headers, params=query_string, verify=False)
        if response.status_code == 200:
            content = response.json()
            datastore_id = content['value'][0]['datastore']
            return datastore_id
    except:
        print('Não foi possível obter o datastore_id. Tente novamente')

def get_folder_id(token, folder_name): # Listar Folder
    try:
        url = f'https://{server}/rest/vcenter/folder'
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token,
        }

        query_string = {'filter.names.1': folder_name}

        response = requests.get(url, headers=headers, params=query_string, verify=False)
        if response.status_code == 200:
            content = response.json()
            folder_id = content['value'][0]['folder']
            return folder_id
    except:
        print('Não foi possível obter o folder_id. Tente novamente')
   
def create_vm_default(token, vm_name, cluster_id, datastore_id, folder_id): # Criar uma Vm
    try:
        headers = {
            'Content-Type': 'application/json',
            'vmware-api-session-id': token,
        }

        data = {
            "spec": {
                "name": vm_name,
                "guest_OS": 'RHEL_8_64',
                "placement": {
                    "cluster": cluster_id,
                    "datastore": datastore_id,
                    "folder": folder_id,
                },
            }
        }

        url = f'https://{server}/rest/vcenter/vm'
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        if response.status_code == 200:
            content = response.json()
            result = content['value']
            message = f'VM {vm_name} was created with id {result}'
            return message
        elif response.status_code == 400:
            content = response.json()
            result = content['value']['messages'][0]['default_message']
            message = result
            return message
    except:
        print('Não foi possível criar uma VM. Tente novamente')

def delete_vm(token, vmid): # Deletar uma VM
    try:
        url = f'https://{server}/rest/vcenter/vm/{vmid}'
        headers = {
            'Content-type': 'application/json',
            'vmware-api-session-id': token,
        }
        response = requests.delete(url, headers=headers, verify=False)
        if response.status_code == 200:
            message = f'VM {vmid} was deleted'
            return message
        elif response.status_code == 404:
            content = response.json()
            message = content['value']['messages'][0]['default_mesage']
            return message
    except:
        print('Não foi possível deletar a VM. Tente novamente')

print()
token = login_vmare()
vmid = 'vm-01'
vm_name = 'maquina_01'
cpu = 2
print()

print('Listando as VMs:')
try:
    for vm in list_vms(token):
        print(vm)
except:
    print('Não foi possível listar as VMs')
print()

print('='*30)
print('Delisgar uma VM:')
poweroff_vm(token, vmid)
print()

print('='*30)
print('Ligando uma VM:')
poweron_vm(token, vmid)
print()

print('='*30)
print('Atualizando VM:')
update_cpu(token, vmid, cpu)
print()

print('='*30)
print('Listando Datastore:')
try:
    for datastore in get_datastores(token):
        print(datastore)
except:
    print('Não foi possível listar os DataStores')
print()

cluster_id = (get_cluster_id(token))
datastore_id = (get_datastore_id(token, datastore_name))
folder_id = (get_folder_id(token, folder_name))

print('Criando uma VM:')
create_vm_default(token, vm_name, cluster_id, datastore_id, folder_id)
print()
print('Deletando uma VM')
delete_vm(token, vmid)



