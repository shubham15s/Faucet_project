from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from .custom_throttle import WalletAddressThrottle
from web3 import Web3
import datetime
from django.conf import settings
from .models import Transaction

w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))


@api_view(["POST"])
@throttle_classes([WalletAddressThrottle])
def fund_faucet(request):
    wallet_address = request.data.get("wallet_address")

    # Check if the wallet address is provided
    if not wallet_address or not w3.is_address(wallet_address):
        return Response(
            {"error": "Invalid wallet address"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Get the nonce for the faucet wallet address (pending transactions included)
        nonce = w3.eth.get_transaction_count(settings.FAUCET_ADDRESS)

        # Prepare the transaction to send 0.0001 Sepolia ETH
        transaction = {
            "to": wallet_address,
            "value": w3.to_wei(0.0001, "ether"),
            "gas": 21000,
            # "gasPrice": w3.to_wei("100", "gwei"),
            "gasPrice": int(w3.eth.gas_price * 3),
            "nonce": nonce,
        }

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(
            transaction, settings.FAUCET_PRIVATE_KEY
        )

        # Send the transaction
        tx = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for transaction receipt 
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx)

        # Return transaction hash
        tx_hash = tx_receipt["transactionHash"].hex()
        # Record successful transaction in the database
        Transaction.objects.create(
            wallet_address=wallet_address,
            tx_hash=tx_receipt["transactionHash"].hex(),
            status="success",
        )

        return Response({"transaction_id": tx_hash}, status=status.HTTP_200_OK)

    except Exception as e:
        Transaction.objects.create(wallet_address=wallet_address, status="failed", error_message=str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def faucet_stats(request):
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(hours=24)

    recent_successful = Transaction.objects.filter(status="success", timestamp__gte=one_day_ago).count()
    recent_failed = Transaction.objects.filter(status="failed", timestamp__gte=one_day_ago).count()

    stats = {
        "successful_transactions": recent_successful,
        "failed_transactions": recent_failed,
    }
    return Response(stats)
