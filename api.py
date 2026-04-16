# https://tinyurl.com/devsecops160426

from fastapi import FastAPI, status, Response
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG

from time import sleep, perf_counter
from random import randint

import psutil
import sys

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
QUANTIDADE_ERROS = {
    'except': 0,
    'erro_api': 0,
}
LATENCIA_MEDIA_ENDPOINT = {
    '/produtos': 0,
    '/pedidos': 0
}
QUANTIDADE_REQUISICOES = 0
QUANTIDADE_PEDIDOS = 0

LOGGER = getLogger(__name__)
LOGGER.setLevel(DEBUG)

FORMATTER = Formatter(fmt="%(asctime)s | %(levelname)s | %(message)s")

SH = StreamHandler(sys.stdout)
SH.setFormatter(FORMATTER)

FH = FileHandler("16_04_26.log")
FH.setFormatter(FORMATTER)

LOGGER.addHandler(SH)
LOGGER.addHandler(FH)

def coletar_saturacao():
    uso_cpu = psutil.cpu_percent()
    uso_memoria = psutil.virtual_memory().percent

    return uso_cpu, uso_memoria

def contabilizar_erro(tipo_erro: str):
    global QUANTIDADE_ERROS
    QUANTIDADE_ERROS[tipo_erro] += 1

def contabilizar_latencia(endpoint: str, latencia: float):
    global LATENCIA_MEDIA_ENDPOINT
    LATENCIA_MEDIA_ENDPOINT[endpoint] += latencia / QUANTIDADE_REQUISICOES

def contabilizar_requisicoes():
    global QUANTIDADE_REQUISICOES
    QUANTIDADE_REQUISICOES += 1

def simula_latencia(tempo_min: int, tempo_max: int) -> int:
    t = randint(tempo_min, tempo_max) / 10
    sleep(t)
    LOGGER.debug(f"Latência simulada: {t}")
    return t

@API.get("/produtos")
def produtos():
    inicio = perf_counter()
    try:
        t = simula_latencia(0, 20)
        
        LOGGER.info("Produtos listados")

        fim = perf_counter()

        cpu, mem = coletar_saturacao()
        LOGGER.info(f"Consumo GET /produtos CPU: {cpu}, Memória: {mem}")
        return PRODUTOS
    except Exception as e:
        LOGGER.error(e)
        contabilizar_erro('except')
        return {"status": "Erro interno"}
    finally:
        fim = perf_counter()

        LOGGER.info(f"Latência /produtos -> {fim - inicio:.3f}")
        contabilizar_requisicoes()
        contabilizar_latencia('/produtos', fim-inicio)


@API.post("/produtos", status_code=status.HTTP_201_CREATED)
def pedido(nome_produto: str, response: Response):
    global QUANTIDADE_PEDIDOS
    inicio = perf_counter()
    # Simulando latência
    t = simula_latencia(0, 15)

    try:
        if nome_produto not in PRODUTOS.keys():
            response.status_code = status.HTTP_400_BAD_REQUEST
            fim = perf_counter()
        
            LOGGER.info(f"Latência /produtos -> {fim - inicio:.3f}")
            contabilizar_erro('erro_api')
            LOGGER.debug(f"Produto: {nome_produto}")

            return ({"status": "Produto não existe"})
        

        LOGGER.info(f"Produto {nome_produto} selecionado")

        PEDIDOS.append(PRODUTOS[nome_produto])
        QUANTIDADE_PEDIDOS += 1
        fim = perf_counter()
        cpu, mem = coletar_saturacao()
        LOGGER.info(f"Consumo POST /produtos CPU: {cpu}, Memória: {mem}")

        latencia = fim - inicio

        if latencia > 0.5:
            LOGGER.warning(f"Pedido demorou {latencia}s")

        LOGGER.info(f"Latência /produtos -> {latencia:.3f}")

        return {"status": "Pedido realizado com sucesso"}
    except Exception as e:
        LOGGER.info(f"Latência /produtos -> {fim - inicio:.3f}")
        LOGGER.error(e)
        contabilizar_erro('except')
        contabilizar_latencia('/pedidos', t)
        return {"status": "Erro interno"}
    finally:
        contabilizar_latencia('/produtos', fim-inicio)
        contabilizar_requisicoes()


@API.get("/pedidos", status_code=status.HTTP_200_OK)
def listar_pedidos():
    inicio = perf_counter()

    try:
        # Simulando latência
        t = simula_latencia(0, 10)
        cpu, mem = coletar_saturacao()
        LOGGER.info(f"Consumo GET /pedidos CPU: {cpu}, Memória: {mem}")
        return PEDIDOS
    except Exception as e:
        LOGGER.error(e)
        contabilizar_erro('except')
        return {"status": "erro interno"}
    finally:
        fim = perf_counter()
        LOGGER.info(f"Latência /produtos -> {fim - inicio:.3f}")
        contabilizar_latencia('/pedidos', fim-inicio)
        contabilizar_requisicoes()

@API.get("/metricas")
def metricas():
    return {
        'quantidade_pedidos': QUANTIDADE_PEDIDOS,
        'quantidade_erros': QUANTIDADE_ERROS,
        'latencia_media': LATENCIA_MEDIA_ENDPOINT
    }