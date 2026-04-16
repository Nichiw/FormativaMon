from requests import get, post
from time import sleep
from random import randint, choice

from threading import Thread

def testa_produtos_get(addr: str):
    for _ in range(50):
        req = get(f"http://{addr}/produtos")
        print("GET", req.status_code)

def testa_produtos_post(addr: str, todos_produtos: dict):
    for _ in range(50):
        produto = choice([*todos_produtos.keys(), "mouse", "GPU"])
        req = post(url=f"http://{addr}/produtos", params=f"nome_produto={produto}")
        print("POST", req.status_code)

def main():
    addr = "localhost:8000"
    todos_produtos = get(f"http://{addr}/produtos").json()

    t1 = Thread(target=testa_produtos_get, args=(addr,))
    t2 = Thread(target=testa_produtos_post, args=(addr, todos_produtos))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("Fim!")

if __name__ == "__main__":
    main()