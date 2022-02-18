# Teste Zax

Este é um teste de conhecimento da linguagem Python para a empresa [Zax](https://www.zaxapp.com.br/)

Para saber as opções do programa basta digitar:

    python3 main.py -h
    ou
    python3 main.py --help
    usage: main.py [-h] [--pedidos PEDIDOS] [--entregadores ENTREGADORES]

    Processa pedidos

    options:
    -h, --help            show this help message and exit
    --pedidos PEDIDOS     Arquivo CSV com os pedidos
    --entregadores ENTREGADORES
                            Arquivo CSV com os entregadores

O formato dos arquivos deve ser o seguinte:

    pedidos.csv

    Loja,Valor,Percentual
    1,50.0,5
    1,50.0,5
    1,50.0,5
    2,50.0,5
    2,50.0,5
    2,50.0,5
    2,50.0,5
    3,50.0,15
    3,50.0,15
    3,100.0,15

Para o arquivo de entregadores o formato é o seguinte:

    Numero,Valor,Loja
    1,2.00
    2,2.00
    3,2.00
    4,2.00,1
    5,2.00

Este projeto não usa nenhuma biblioteca externa, apenas o Python.