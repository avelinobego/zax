"""
Aplicação teste para a Teste ZAX - vaga: Desenvolvedor Python
"""
import argparse
from decimal import Decimal
from typing import Iterable, List, Tuple
from xmlrpc.client import Boolean
import csv

"""
Classe Pedido
"""
class Pedido:
    def __init__(self, loja: int, valor: Decimal, percentual: Decimal = None) -> None:
        self.loja = loja
        self.valor: Decimal = valor
        self.retirado = False
        self.percentual = percentual or Decimal(5)

    def percentual_pago(self) -> Decimal:
        return Decimal(self.valor * self.percentual / 100)

    def __lt__(self, other) -> bool:
        return self.valor < other.valor or self.percentual < other.percentual

    def __str__(self) -> str:
        return f'Pedido(loja={self.loja}, valor={self.valor}, percentual={self.percentual})'

"""
Classe Entregador
"""
class Entregador:
    def __init__(self, numero: int, valor_cobrado: Decimal, loja_prioritaria: int = -1) -> None:
        self.numero = numero
        self.entregas: Pedido = []
        self.loja_prioritaria = loja_prioritaria
        self.valor_cobrado = valor_cobrado

    def calcular_valor(self) -> Decimal:
        total_das_entregas: Decimal = Decimal(0.0)
        for entrega in self.entregas:
            total_das_entregas += entrega.percentual_pago()

        return total_das_entregas + self.valor_cobrado

    def lojas(self) -> str:
        return ','.join(str(pedido.loja) for pedido in self.entregas)

    def __lt__(self, other) -> bool:
        return self.loja_prioritaria < other.loja_prioritaria

    def __str__(self) -> str:
        return f'Entregador: {self.numero}, lojas: {self.lojas()}, valor: R$ {self.calcular_valor():<10.2f}, prioridade: {self.loja_prioritaria}'

"""
Função que processa os pedidos
"""
def processar_pedidos(motoboy: Entregador, pedido: Pedido) -> None:
    if pedido and not pedido.retirado:
        pedido.retirado = True
        motoboy.entregas.append(pedido)

"""
Função que processa os pedidos
"""
def make_motoboys_generator(motoboys: Iterable[Entregador]) -> Entregador:
    while True:
        for motoboy in motoboys:
            yield motoboy

"""
Função que processa os pedidos.
O gerador de pedidos é usado para processar os pedidos em ordem.
A cada vez que os pedidos forem retirados eles passam a não fazer parte do looping
"""
def make_pedidos_generator(pedidos: Iterable[Pedido]) -> Pedido:
    continuar: Boolean = True
    while continuar:
        continuar = False
        for pedido in pedidos:
            if pedido.retirado:
                continue
            continuar = True
            yield pedido

"""
Função que processa os pedidos
"""
def run() -> None:

    parser = argparse.ArgumentParser(description='Processa pedidos')
    parser.add_argument('--pedidos', type=str, dest='pedidos',
                        help='Arquivo CSV com os pedidos')
    parser.add_argument('--entregadores', type=str,
                        dest='entregadores', help='Arquivo CSV com os entregadores')
    args = parser.parse_args()

    if not args.pedidos or not args.entregadores:
        print('''
        Você precisa informar os arquivos de entrada:
        --pedidos: arquivo CSV com os pedidos
        --entregadores: arquivo CSV com os entregadores

        O arquivo de pedidos deve estar no formato:
        Loja,Valor,Percentual
        1,50.0,15

        O arquivo de entregadores deve estar no formato:

        Numero,Valor,Loja
        1,2.00
        2,3.00,1

        ''')
        return

    # Carregar os pedidos
    with open(args.entregadores, 'r') as f:
        linhas = csv.DictReader(f, delimiter=',')
        ENTREGADORES: Tuple[Pedido] = tuple(Entregador(int(linha['Numero']), Decimal(
            linha['Valor']), int(linha['Loja'] or -1)) for linha in linhas)

    # Carregar os entregadores
    with open(args.pedidos, 'r') as f:
        linhas = csv.DictReader(f, delimiter=',')
        PEDIDOS: Tuple[Pedido] = tuple(
            Pedido(int(linha['Loja']), Decimal(linha['Valor']), Decimal(linha['Percentual'])) for linha in linhas)

    # Ordenando os pedidos por valor/percentual pois serão estes os critérios de prioridade
    PEDIDOS_CLASSIFICADOS = sorted(PEDIDOS, reverse=True)
    # Ordenando os entregadores por prioridade de loja
    ENTREGADORES_PRIORIZADOS = sorted(ENTREGADORES, reverse=True)

    pedidos_disponivel = make_pedidos_generator(PEDIDOS_CLASSIFICADOS)
    motoboys = make_motoboys_generator(ENTREGADORES_PRIORIZADOS)

    pedido = next(pedidos_disponivel, None)

    for motoboy in motoboys:

        if motoboy.loja_prioritaria > 0 and motoboy.loja_prioritaria != pedido.loja:
            continue

        processar_pedidos(motoboy, pedido)

        pedido = next(pedidos_disponivel, None)
        if not pedido:
            break

    for motoboy in ENTREGADORES_PRIORIZADOS:
        print(motoboy)


if __name__ == '__main__':
    run()
