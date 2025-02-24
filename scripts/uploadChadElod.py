chat_elod = """
''IiiIiiiii::     ''    '':'''''''''''''::'::::::':i
''iiiJJJIii::':'' :: :::'':i::'::::::':'::'::::::::'
IIIII$$$$:$i::::''''''''''':'':''''''':::i:::'::::::
$IIII''I$$$ii:::::::::'   '':$$i:iIJ$IIII$$Ii:iJ$$Ii
$$Ii$'$::IIiiiiii:J::        '$IIIII$$IIIIIIIIIIiIJI
:$iiJ'J$$iIiIIIIIi':' '''    ':IiIiJJ$IIIIIIIiiiiiII
'::'::$$IiiiIIiIIi:: ':'''    ':I''IIiIIIIII:iII''' 
''''I'$$iiIIIiiIIi:: ':::''::'''::''''IIIII:''::''''
''''$'I$IiiiiiiII:I: :::::::::::iIIIJJIIIIIi::::::::
''''i'i$$i::::iiJ'''''' ''' 'i:::     IIIII'        
''''::i$$I::':ii$'''''' '' ''i:::::::'IIIII         
'':: :I$$$:iiiIii::''::':::::i:''::' 'IIIII         
IJJIiiI$$$i:::::'''':':'::::::iI'':  'IIIII         
IJJIIii$$$:i:::' ''':''''':::'::i':' 'IIIII '      '
:IIIIi$$$:i:::ii':'::'''''':: ''i:'' :iIIII:i'''  'i
iIIII:ii:::iiii:':'::''''''': ':  ': :IIIII  '  '::i
iiIII:JI'::iiiiii:::::''''''i':I '''' IIJJI ''i'   '
$iIIIiJI'iiiiiII:III::'  ''::ii' ':'' IJJJ$ ''''' :'
:$IIJ''' I'':'I:::::::''''':::iii  ' :JJJ$$:::Ii'':'
 ''   '  '     '::::::''''':::iiii''JIJJJJJJ' 'i'I::
  I'  ''':'' ':i:::::'''''':::i:iiIIiIiIIII::'':''::
' I'''''::'ii:::::::::''''':iiii::iiiiIIJJJ:''''':::
 i     ii:i:::::::::::::::::::ii::::iiiI$$J''    '''
'    ''''':::::::::::::::::::::iii::::iiI$$'    '   
 I    'iI::::::::::::::::::::::i:i::::::i$$    '    
:::''''''::::::::::::::::::::::::::::::::I$'':::::: 
'i''  'I:''''''::::::::::::::::::::::::::iI ''''''  
JiI:'J:::'''''':::::::::::::::::::::''::::iii::'::  
i'iI'I:::'''' :::::::::::'::::::::::'::ii:iii:i'''' 
i:''''::::::''':::::::::''::::::::: ''::ii:ii:':''''
'''''':::::''  :::::::::''::::::::'' '':::::i'::''::
'   '':::::''  '''''''::''''''':::'' '''::::i''     
'''II:::::'''  '''''''''''''''''::''ii'':::::iiiiii 
'':Ii:::''''   '''''''':::''''':::':'I'''''::iiIIii'
'':::::'''':'' ''''''':::::::'::::':i'''''''::iiiii 
i':i:::''':i   '''''''::''::::::::':i:':''''::iiIIi'
''ii::::':i:    '''::::::':::::::: :iI'$I'':::iI:ii:
Iiii:::::ii':   '''':::::::::::::i ::i' ':'::::II:ii
iIII:::::II::I ''''''''':''''::::' :::   ''::::IIiiI
IIII:::::iIi:IIi'''':''''::''':::: :::   ''::::iIIii
iIIi:::::iI::III'''''''':'''':::::'':'    '':::iII'I
:':::::::i::'iii:''''''''':::::::::':''   '':::iII I
''':::::::''''::::'''::::::::::::::::' i  '::::iII'I
::':::::ii::::::''''''''':'::::::::::: :' '::::'iiIi
iiiii::::::::::: '''''':::::::::''::::'i'  ::::iiii:
iiiii' ''i:''':i  '''''''':::::' ::'::::''    :iiii:
iiiii  :'ii':iii    '''''''':'  '':::::::::   'iiiii
iiiii :iiii'iIi''    :'''''       i'iiiiiii    iiiii
iiiiiiiii:i'ii:            i      :'iiiiiii:'  iiiii
iiiiiiiii':'ii' '  ' ' ' ':i      ':iiiiiiiii:iiiiii
iiiiii::i':':i:     '  :   :      ''' iii::iiiiiiiii
' ''':'':'iiiJ'        :   '          :ii'':iiiiiiii
       '':'  '         '          '   'i:'i:::iiiiii
        :ii' '     '       '      '   IIIi:'':IIIIII
    iI'' iii       '       '      ''  iII'''iIIIIIII
    iiI: ':: '             '       ' ':IIIIIIIIIIIII
     :':''': :    ' ''             ''':IIIIIIIIIIIii
     '':::i'':      '       '      '  'IIIIIIIIIIIII
     ''iIII:::              :      ''''iIIIIIIIIIIII
     '::::iii:              i     ''''''IIIIIIIIIIII
                '    '      '  '''':::''IIIIIIIIIIII
:               '        '     '''':::''IIIIIIIIIIII
"""



from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Connect to Taraxa network
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

# Contract details
# CONTRACT_ADDRESS = "0x09e503e18ea530344c17d76c6eb3e2a0bba83ebc"  # Replace with your deployed contract address
CONTRACT_ADDRESS = Web3.to_checksum_address("0x09e503e18ea530344c17d76c6eb3e2a0bba83ebc")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Initialize account
account = Account.from_key(PRIVATE_KEY)

# Contract ABI - only including the functions we need
ABI = json.load(open("/Users/gui/dev/iq69000/foundry-example/out/code_in.sol/CodeIn.json"))['abi']

# Initialize contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def split_string(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def upload_chat_elod():
    # Split the chat_elod into chunks
    chunks = split_string(chat_elod.strip())
    
    for i, chunk in enumerate(chunks):
        # Prepare transaction
        tx = contract.functions.sendCode(
            account.address,  # user address
            chunk,           # code chunk
            str(i),         # beforeTx (using chunk index as reference)
            1,              # method (using 1 as default)
            0 if i < len(chunks)-1 else 1  # decodeBreak (1 for last chunk)
        ).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': w3.eth.gas_price ,
            'nonce': w3.eth.get_transaction_count(account.address),
            'chainId': 841,  
        })
        
        # Sign and send transaction
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # Wait for transaction receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("🐍 File: scripts/uploadChatElod.py | Line: 136 | upload_chat_elod ~ receipt",receipt)

        print(f"Chunk {i+1}/{len(chunks)} uploaded. Transaction hash: {receipt['transactionHash'].hex()}")

def reconstruct_chat_elod():
    lastTx = "0xef89e660aef0dda48a636292174259396737e51933c3c5ad1ef0075c2c73a8d1"

    tx = contract.functions.sendDbCode(
        account.address,
        "taraxa",
        lastTx,
        "string",
        "None"
    ).build_transaction({
        'from': account.address,
        'gas': 500000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 841,
    })
    

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("🐍 File: scripts/uploadChatElod.py | Line: 152 | reconstruct_chat_elod ~ receipt",receipt)

    userDataConnectTx = contract.functions.userDataConnect(
        account.address,
        receipt['transactionHash'].hex(),
        "genesis"
    ).build_transaction({
        'from': account.address,
        'gas': 500000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 841,
    })

    signed_tx = w3.eth.account.sign_transaction(userDataConnectTx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    userDataConnectTxReceipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("🐍 File: scripts/uploadChatElod.py | Line: 166 | reconstruct_chat_elod ~ userDataConnectTxReceipt",userDataConnectTxReceipt)

    mapping_wallet = dict()
    mapping_wallet[account.address] = userDataConnectTxReceipt['transactionHash'].hex()

    print("🐍 File: scripts/uploadChatElod.py | Line: 166 | reconstruct_chat_elod ~ mapping_wallet",mapping_wallet)


if __name__ == "__main__":
    # upload_chat_elod()
    reconstruct_chat_elod()