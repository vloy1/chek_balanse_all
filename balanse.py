import time
from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.account.account import Account
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
import asyncio

class Wallet:

    def __init__(self,file_wallet) -> None:

        self.file_wallet = file_wallet
        self.adress,self.seed,self.private_key = self.wallett()

    def write_fife(self,name_file):
        with open(f'{name_file}.txt', 'a') as f:
            f.write(f'{self.adress}:{self.seed}:{self.private_key}# {self.account_balance}\n')

    def wallett(self):

        private = open(self.file_wallet,'r').readlines()#.read().splitlines()
        wallet = private[00].splitlines()[0]
        del private[00]
        with open(self.file_wallet, "w") as file:
            file.writelines(private)
        return wallet.split(':')
    
    async def balanse(self):

        privat_key  = int(self.private_key, 16)
        self.starknet_account = Account(
            client=FullNodeClient('https://starknet-mainnet.core.chainstack.com/0a1bf194ad26817e1b6d2a00063b4dc2'),
            address=self.adress,
            key_pair=KeyPair.from_private_key(key=privat_key),
            chain=StarknetChainId.MAINNET,)
        
        call = Call(
            to_addr=0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
            selector=get_selector_from_name("balanceOf"),
            calldata=[self.starknet_account.address],
        )

        self.account_balance = round(((await self.starknet_account.client.call_contract(call))[0]/10**18),6)
        if self.account_balance > 0.0008:
            self.write_fife('norm')
        elif 0.0008 >self.account_balance and self.account_balance > 0.00005:
            self.write_fife('bomg')
        else: 
            self.write_fife('false')
        print(f'{self.adress} # {self.account_balance} # {self.account_balance*3700} $')
        
if __name__ == '__main__':
    while True:
        wal = Wallet('wal.txt')
        asyncio.run(wal.balanse())
        1

