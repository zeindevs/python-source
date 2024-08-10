import asyncio
import requests
import websockets
import json
from decouple import config
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig

SECRET_KEY = config("SECRET_KEY")
PUBLIC_KEY = config("PUBLIC_KEY")
API_KEY = config("API_KEY")


async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        payload = {"method": "subscribeNewToken"}
        await websocket.send(json.dumps(payload, indent=2))

        # subscribe to token creation events
        # payload = {
        #     "method": "subscribeAccountTrade",
        #     "keys": ["AArPXm8JatJiuyEffuC1un2Sc835SULa4uQqDcaGpAjV"], # array of accounts to watch
        # }

        # Subscribing to trandes made by accounts
        # await websocket.send(json.dumps(payload))
        #

        # Subscribing to trades on tokens
        # payload = {
        #     "method": "subscribeTokenTrade",
        #     "keys": ["91WNez8D22NwBssQbkzjy4s2ipFrzpmn5hfvWVe2aY5p"], # array of token CAs to watch
        # }
        # await websocket.send(json.dumps(payload))

        # Unsubscribing frim new token events
        # payload = {"method": "unsubscribeNewToken"}
        # await websocket.send(json.dumps(payload))

        async for message in websocket:
            print(json.dumps(json.loads(message), indent=2))


def trade():
    uri = "https://pumpportal.fun/api/trade?api-key=your-api-key-here"
    payload = {
        "action": "buy",  # "buy" or "sell"
        "mint": "",  # contract address of the token you want to trade
        "amount": 10000,  # amount of SOL or tokens to trade
        "denominatedInSol": "false",  # "true" if amount is amount of SOL, "false" if amount is number of tokens
        "slippage": 10,  # percent slippage allowed
        "priorityFee": 0.005,  # amount to use as Jito tip or priority fee
        "pool": "pump",  # exchange to trade on. "pump" or "raydium"
    }

    response = requests.post(url=uri, data=payload)
    data = response.json()

    print(data)


def localTrade():
    uri = "https://pumpportal.fun/api/trade-local"
    payload = {
        "publicKey": "Your public key here",
        "action": "buy",  # "buy" or "sell"
        "mint": "token CA here",  # contract address of the token you want to trade
        "amount": 100000,  # amount of SOL or tokens to trade
        "denominatedInSol": "false",  # "true" if amount is amount of SOL, "false" if amount is number of tokens
        "slippage": 10,  # percent slippage allowed
        "priorityFee": 0.005,  # amount to use as priority fee
        "pool": "pump",  # exchange to trade on. "pump" or "raydium"
    }

    response = requests.post(url=uri, data=payload)

    keypair = Keypair.from_base58_string("API KEY")
    tx = VersionedTransaction(
        VersionedTransaction.from_bytes(response.content).message, [keypair]
    )

    commmitment = CommitmentLevel.Confirmed
    config = RpcSendTransactionConfig(preflight_commitment=commmitment)
    txPayload = SendVersionedTransaction(tx, config)

    response = requests.post(
        url="Your RPC Endpoint here - Eg: https://api.mainnet-beta.solana.com/",
        headers={"Content-Type": "application/json"},
        data=SendVersionedTransaction(tx, config).to_json(),
    )
    txSignature = response.json()["result"]
    print(f"Transaction: https://solscan.io/tx/{txSignature}")


def createWallet():
    response = requests.get(url="https://pumpportal.fun/api/create-wallet")
    data = response.json()
    print(data)


def sendLocalCreateTx():
    signer_keypair = Keypair.from_base58_string("")

    # Generate a random keypair for token
    mint_keypair = Keypair()

    # Define token metadata
    form_data = {
        "name": "PPTest",
        "symbol": "TEST",
        "description": "This is an example token created via PumpPortal.fun",
        "twitter": "https://x.com/a1lon9/status/1812970586420994083",
        "telegram": "https://x.com/a1lon9/status/1812970586420994083",
        "website": "https://pumpportal.fun",
        "showName": "true",
    }

    # Read the image file
    with open("./example.png", "rb") as f:
        file_content = f.read()
        f.close()

    files = {
        "file": ("example.png", file_content, "image/png"),
    }

    # Create IPFS metadata storage
    metadata_response = requests.post(
        "https://pump.fun/api/ipfs", data=form_data, files=files
    )
    metadata_response_json = metadata_response.json()

    # Token metadata
    token_metadata = {
        "name": form_data["name"],
        "symbol": form_data["symbol"],
        "uri": metadata_response_json["metadataUri"],
    }

    # Generate the create transaction
    response = requests.post(
        "https://pumpportal.fun/api/trade-local",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "publicKey": str(signer_keypair.pubkey()),
                "action": "create",
                "tokenMetadata": token_metadata,
                "mint": str(mint_keypair.pubkey()),
                "denominatedInSol": "true",
                "amount": 1,  # Dev buy of 1 SOL
                "slippage": 10,
                "priorityFee": 0.0005,
                "pool": "pump",
            }
        ),
    )

    tx = VersionedTransaction(
        VersionedTransaction.from_bytes(response.content).message,
        [mint_keypair, signer_keypair],
    )

    commitment = CommitmentLevel.Confirmed
    config = RpcSendTransactionConfig(preflight_commitment=commitment)
    txPayload = SendVersionedTransaction(tx, config)

    response = requests.post(
        url="Your RPC endpoint - Eg: https://api.mainnet-beta.solana.com/",
        headers={"Content-Type": "application/json"},
        data=SendVersionedTransaction(tx, config).to_json(),
    )
    txSignature = response.json()["result"]
    print(f"Transaction: https://solscan.io/tx/{txSignature}")


def send_create_tx():
    mint_keypair = Keypair()

    # Define token metadata
    form_data = {
        "name": "PPTest",
        "symbol": "TEST",
        "description": "This is an example token created via PumpPortal.fun",
        "twitter": "https://x.com/a1lon9/status/1812970586420994083",
        "telegram": "https://x.com/a1lon9/status/1812970586420994083",
        "website": "https://pumpportal.fun",
        "showName": "true",
    }

    # Read the image file
    with open("./example.png", "rb") as f:
        file_content = f.read()

    files = {"file": ("example.png", file_content, "image/png")}

    # Create IPFS metadata storage
    metadata_response = requests.post(
        "https://pump.fun/api/ipfs", data=form_data, files=files
    )
    metadata_response_json = metadata_response.json()

    # Token metadata
    token_metadata = {
        "name": form_data["name"],
        "symbol": form_data["symbol"],
        "uri": metadata_response_json["metadataUri"],
    }

    # Send the create transaction
    response = requests.post(
        "https://pumpportal.fun/api/trade?api-key=your-api-key",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "action": "create",
                "tokenMetadata": token_metadata,
                "mint": str(mint_keypair),
                "denominatedInSol": "true",
                "amount": 1,  # Dev buy of 1 SOL
                "slippage": 10,
                "priorityFee": 0.0005,
                "pool": "pump",
            }
        ),
    )

    if response.status_code == 200:  # successfully generated transaction
        data = response.json()
        print(f"Transaction: https://solscan.io/tx/{data['signature']}")
    else:
        print(response.reason)  # log error


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(subscribe())
    except KeyboardInterrupt:
        print("exiting program...")
