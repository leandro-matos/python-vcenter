# Consumindo a API do Vcenter

Este script tem como objetivo consumir a API do Vcenter para listar, deletar, modificar vm's e datastores.

## Deploy

Para fazer o deploy na sua máquina e utilizar como exemplo, siga o passo a passo a seguir.

- Clone o repositório.

```bash
git clone https://github.com/leandro-matos/python-vcenter
```

- Acesse o diretório

```bash
cd python-vcenter
```

- Crie uma virtual env

```bash
python3 -m venv .venv
```

- Ative a virtual env

```bash
source .venv/bin/activate
```

- Instale as bibliotecas

```bash
python -m pip install -r requirements.txt
```

Incluir as variáveis de ambiente:

```bash
* export VCENTER_HOST=IP (Exemplo: 127.0.0.1)
* export VCENTER_USERNAME=usuario (Exemplo: administrator@vsphere.local)
* export VCENTER_USERNAME=senha (Exemplo: admin123)
* export DATASTORE_NAME=datastore_name (Exemplo: Datastore_sf10hv10_01)
* export FOLDER_NAME=folder_name (Exemplo: vcenter_folder)
```

