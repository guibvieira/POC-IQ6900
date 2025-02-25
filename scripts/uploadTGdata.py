from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv
import json
import pandas as pd
from tqdm import tqdm
import time
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


def create_chunks(messages, max_chunk_size=500):
    chunks = []
    current_chunk = []
    current_size = 0
    
    for message in messages:
        # Skip empty messages
        if not isinstance(message, str) or not message.strip():
            continue
            
        message_size = len(message)
        
        # If a single message is larger than max_chunk_size, split it
        if message_size > max_chunk_size:
            if current_chunk:  # First save any existing chunk
                chunks.append(' || '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split long message into sub-chunks
            for i in range(0, message_size, max_chunk_size):
                chunks.append(message[i:i + max_chunk_size])
            continue
            
        # If adding this message would exceed chunk size, start a new chunk
        if current_size + len(message) + 4 > max_chunk_size:  # 4 accounts for ' || ' separator
            chunks.append(' || '.join(current_chunk))
            current_chunk = []
            current_size = 0
            
        # Add message to current chunk
        current_chunk.append(message)
        current_size += len(message) + 4  # Add length of message plus separator
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' || '.join(current_chunk))
    
    return chunks

def upload_tg_messages():
    # Split the chat_elod into chunks
    tg_data = pd.read_csv("/Users/gui/dev/iq69000/foundry-example/df_clean_minus_spams_2025-01-26_2025-02-03_subset.csv")
    chunks = create_chunks(tg_data['text'].values)
    
    for i, chunk in tqdm(enumerate(chunks)):
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
        time.sleep(0.2)
        # Wait for transaction receipt
        # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        # print("🐍 File: scripts/uploadChatElod.py | Line: 136 | upload_chat_elod ~ receipt",receipt)

        # print(f"Chunk {i+1}/{len(chunks)} uploaded. Transaction hash: {receipt['transactionHash'].hex()}")
    # return receipt['transactionHash'].hex()

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
    print("🐍 File: scripts/uploadChatElod.py | Line: 166 | reconstruct_chat_elod ~ userDataConnectTxReceipt",user_data_connect_tx_receipt)

    mapping_wallet = dict()
    mapping_wallet[account.address] = user_data_connect_tx_receipt['transactionHash'].hex()

    print("🐍 File: scripts/uploadChatElod.py | Line: 166 | reconstruct_chat_elod ~ mapping_wallet",mapping_wallet)


if __name__ == "__main__":
    tx_hash = upload_tg_messages()
    reconstruct_data(tx_hash)