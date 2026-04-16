from fastapi import FastAPI, status, Response
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG

from time import sleep
from random import randint

API = FastAPI()

PRODUTOS = {
    "NVIDIA RTX 4090": {"categoria": "GPU", "preco": 12500.00},
    "Intel Core i9-14900K": {"categoria": "CPU", "preco": 4200.00},
    "AMD Ryzen 7 7800X3D": {"categoria": "CPU", "preco": 2800.00},
    "ASUS ROG Strix Z790-E": {"categoria": "Placa-mãe", "preco": 3500.00},
    "Corsair Vengeance RGB 32GB DDR5": {"categoria": "RAM", "preco": 1100.00},
    "Samsung 990 Pro 2TB NVMe": {"categoria": "Armazenamento", "preco": 1400.00},
    "Corsair RM1000x 1000W": {"categoria": "Fonte", "preco": 1200.00},
    "Lian Li PC-O11 Dynamic": {"categoria": "Gabinete", "preco": 1300.00},
    "NZXT Kraken Elite 360": {"categoria": "Cooler", "preco": 1800.00},
    "Logitech G Pro X Superlight": {"categoria": "Periférico", "preco": 800.00},
    "Razer BlackWidow V4 Pro": {"categoria": "Periférico", "preco": 1500.00},
    "Seagate IronWolf 8TB HDD": {"categoria": "Armazenamento", "preco": 1200.00},
    "Gigabyte B650 AORUS Elite": {"categoria": "Placa-mãe", "preco": 1800.00},
    "Noctua NH-D15": {"categoria": "Cooler", "preco": 750.00},
    "Crucial P3 1TB M.2": {"categoria": "Armazenamento", "preco": 450.00},
    "Kingston FURY Beast 16GB DDR4": {"categoria": "RAM", "preco": 350.00},
    "EVGA SuperNOVA 750 G6": {"categoria": "Fonte", "preco": 850.00},
    "AMD Radeon RX 7900 XTX": {"categoria": "GPU", "preco": 7200.00},
    "MSI MAG B550 Tomahawk": {"categoria": "Placa-mãe", "preco": 1100.00},
    "Western Digital Black 4TB": {"categoria": "Armazenamento", "preco": 900.00},
    "Arctic MX-6 (Pasta Térmica)": {"categoria": "Acessório", "preco": 60.00},
    "Be Quiet! Silent Wings 4": {"categoria": "Cooler", "preco": 180.00},
    "TP-Link Archer TX3000E Wi-Fi 6": {"categoria": "Rede", "preco": 380.00},
    "DeepCool AK620": {"categoria": "Cooler", "preco": 400.00},
    "Cooler Master TD500 Mesh": {"categoria": "Gabinete", "preco": 650.00}
}

PEDIDOS = []

def simula_latencia(tempo_min: int, tempo_max: int) -> int:
    t = randint(tempo_min, tempo_max) / 10
    sleep(t)
    return t

@API.get("/produtos")
def produtos():
    t = simula_latencia(0, 20)
    
    print("Produtos listados")

    return PRODUTOS


@API.post("/produtos", status_code=status.HTTP_201_CREATED)
def pedido(nome_produto: str, response: Response):
    # Simulando latência
    t = simula_latencia(0, 15)

    if nome_produto not in PRODUTOS.keys():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ({"status": "Produto não existe"})

    print(f"Produto {nome_produto} selecionado")

    PEDIDOS.append(PRODUTOS[nome_produto])

    return {"status": "Pedido realizado com sucesso"}

@API.get("/pedidos", status_code=status.HTTP_200_OK)
def listar_pedidos():
    # Simulando latência
    t = simula_latencia(0, 10)

    return PEDIDOS