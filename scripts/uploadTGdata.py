from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv
import json
import pandas as pd

# Load environment variables
load_dotenv()

# Connect to Taraxa network
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

# Contract details
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

def upload_tg_messages():
    # Split the chat_elod into chunks
    pd.read_csv("/Users/gui/dev/iq69000/foundry-example/df_clean_minus_spams_2025-01-26_2025-02-03.csv")
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
        return receipt['transactionHash'].hex()

def reconstruct_data(last_tx):

    tx = contract.functions.sendDbCode(
        account.address,
        "taraxa",
        last_tx,
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
    receipt_send_db_code = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("🐍 File: scripts/uploadChatElod.py | Line: 152 | reconstruct_chat_elod ~ receipt",receipt_send_db_code)

    user_data_connect_tx = contract.functions.userDataConnect(
        account.address,
        receipt_send_db_code['transactionHash'].hex(),
        "genesis"
    ).build_transaction({
        'from': account.address,
        'gas': 500000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 841,
    })

    signed_tx = w3.eth.account.sign_transaction(user_data_connect_tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    user_data_connect_tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("🐍 File: scripts/uploadChatElod.py | Line: 166 | reconstruct_chat_elod ~ userDataConnectTxReceipt",userDataConnectTxReceipt)

    mapping_wallet = dict()
    mapping_wallet[account.address] = user_data_connect_tx_receipt['transactionHash'].hex()

    print("🐍 File: scripts/uploadChatElod.py | Line: 166 | reconstruct_chat_elod ~ mapping_wallet",mapping_wallet)


if __name__ == "__main__":
    tx_hash = upload_tg_messages()
    reconstruct_data(tx_hash)