from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from .custom_throttle import WalletAddressThrottle
from web3 import Web3
import datetime
from django.conf import settings


# Setup Web3 connection
w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))


@api_view(["POST"])
@throttle_classes([WalletAddressThrottle])
def fund_faucet(request):
    wallet_address = request.data.get("wallet_address")

    # Check if the wallet address is provided
    if not wallet_address or not w3.isAddress(wallet_address):
        return Response(
            {"error": "Invalid wallet address"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Prepare transaction to send 0.0001 Sepolia ETH
        transaction = {
            "to": wallet_address,
            "value": w3.toWei(0.0001, "ether"),
            "gas": 21000,
            "gasPrice": w3.toWei("50", "gwei"),
            "nonce": w3.eth.getTransactionCount(settings.FAUCET_ADDRESS),
        }

        # Sign the transaction
        signed_txn = w3.eth.account.signTransaction(
            transaction, settings.FAUCET_PRIVATE_KEY
        )
        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Return transaction ID
        return Response({"transaction_id": tx_hash.hex()}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# In-memory tracking of transactions (replace with persistent storage if needed)
successful_transactions = []
failed_transactions = []


@api_view(["GET"])
def faucet_stats(request):
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(hours=24)

    # Filter transactions from the last 24 hours
    recent_successful = [tx for tx in successful_transactions if tx >= one_day_ago]
    recent_failed = [tx for tx in failed_transactions if tx >= one_day_ago]

    stats = {
        "successful_transactions": len(recent_successful),
        "failed_transactions": len(recent_failed),
    }
    return Response(stats)
