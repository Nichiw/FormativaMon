from fastapi import FastAPI, status, Response
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR
from time import sleep, time
from random import randint
import psutil  # para medir saturação (CPU e memória)
import os


logger = getLogger("api_pedidos")
logger.setLevel(DEBUG)

formato = Formatter("%(asctime)s | %(levelname)s | %(message)s")

handler_terminal = StreamHandler()
handler_terminal.setFormatter(formato)

handler_arquivo = FileHandler("pedidos.log", encoding="utf-8")
handler_arquivo.setFormatter(formato)

logger.addHandler(handler_terminal)
logger.addHandler(handler_arquivo)

LIMITE_LATENCIA_MS = 1000

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
Pedidos_errados = 0


def simula_latencia(tempo_min: int, tempo_max: int) -> float:
    t = randint(tempo_min, tempo_max) / 10
    sleep(t)
    return t


def loga_saturacao():
    cpu = psutil.cpu_percent(interval=None)       # % de CPU em uso
    mem = psutil.virtual_memory().percent         # % de RAM em uso
    logger.info(f"Saturação — CPU: {cpu}% | Memória: {mem}%")


def loga_latencia(endpoint: str, duracao_s: float):
    duracao_ms = duracao_s * 1000 

    if duracao_ms > LIMITE_LATENCIA_MS:
        logger.warning(
            f"Latência alta em [{endpoint}] — {duracao_ms:.0f}ms "
            f"(limite: {LIMITE_LATENCIA_MS}ms)"
        )
    else:
        logger.info(f"Latência de [{endpoint}] — {duracao_ms:.0f}ms")


@API.get("/produtos")
def produtos():
    inicio = time()  
    logger.info("Tráfego — GET /produtos recebido")
    loga_saturacao()

    t = simula_latencia(0, 20)

    duracao_total = time() - inicio
    loga_latencia("GET /produtos", duracao_total)

    logger.info(f"GET /produtos — {len(PRODUTOS)} produtos retornados com sucesso")
    return PRODUTOS


@API.post("/produtos", status_code=status.HTTP_201_CREATED)
def pedido(nome_produto: str, response: Response):
    inicio = time()

    logger.info(f"Tráfego — POST /produtos recebido | produto solicitado: '{nome_produto}'")
    loga_saturacao()

    t = simula_latencia(0, 15)

    if nome_produto not in PRODUTOS.keys():
        global Pedidos_errados
        Pedidos_errados += 1
        response.status_code = status.HTTP_400_BAD_REQUEST

        duracao_total = time() - inicio
        loga_latencia("POST /produtos", duracao_total)

        logger.error(
            f"Erro — Produto '{nome_produto}' não encontrado no catálogo "
            f"(HTTP 400)"
            f"| Produtos não existentes solicitados até agora: {Pedidos_errados}"
        )
        return {"status": "Produto não existe"}

    PEDIDOS.append(PRODUTOS[nome_produto])

    duracao_total = time() - inicio
    loga_latencia("POST /produtos", duracao_total)

    logger.info(
        f"POST /produtos — Pedido de '{nome_produto}' realizado com sucesso "
        f"| Total de pedidos: {len(PEDIDOS)}"
    )
    return {"status": "Pedido realizado com sucesso"}


@API.get("/pedidos", status_code=status.HTTP_200_OK)
def listar_pedidos():
    inicio = time()

    logger.info("Tráfego — GET /pedidos recebido")
    loga_saturacao()

    t = simula_latencia(0, 10)

    duracao_total = time() - inicio
    loga_latencia("GET /pedidos", duracao_total)

    logger.info(f"GET /pedidos — {len(PEDIDOS)} pedidos retornados com sucesso")
    return PEDIDOS