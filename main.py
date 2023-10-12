import requests 
import time
import json

file = 'wal.txt'

def nonse_(adress):
    response = requests.get(f'https://voyager.online/api/contract/{adress}')
    if response.status_code == 200:
        res = json.loads(response.text)
        nonce = int(res['nonce'],16)
        time.sleep(3)
        return nonce
    else:
        return 0

class Token:
    def __init__(self,symbol,balanse,okrug) -> None:
        self.symbol = symbol
        self.balanse = balanse
        self.okrug = okrug

    def balanse_(self,amount):
        self.balanse = round(float(amount),self.okrug)

def balanse(adress):
    response = requests.get(f'https://voyager.online/api/contract/{adress}/balances')
    if response.status_code == 200:
        res = json.loads(response.text)
        eth = Token('ETH',0,4)
        dai = Token('DAI',0,1)
        usdc = Token('USDC',0,1)
        usdt = Token('USDT',0,1)
        zeth = Token('zETH',0,4)
        tokens = [eth,dai,usdc,usdt,zeth]
        nonse = nonse_(adress)
        for i in res:
            for token in tokens:
                if token.symbol == i['symbol']:
                    token.balanse_(i['formattedBalance'])
        res = f'{adress} : {nonse} : {eth.balanse} : {dai.balanse} : {usdc.balanse}: {usdt.balanse} : {zeth.balanse}'
    else:
        res = f'{adress} : 0'
    print(res)
    time.sleep(3)

def wallett(file):
    private = open(file,'r').read().splitlines()
    wallet = private[00]
    return wallet

def wallett_del(file):
    ish = open(file,'r').readlines()
    del ish[00]
    with open(file, "w") as file:
        file.writelines(ish)

def main():
    while True:
        adress_ = wallett(file)
        balanse(adress_)
        wallett_del(file)

main()