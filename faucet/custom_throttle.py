# faucet/throttles.py
from rest_framework.throttling import BaseThrottle
import time

wallet_request_times = {}  # Store wallet request timestamps in-memory. Consider using a persistent store like Redis.

class WalletAddressThrottle(BaseThrottle):
    THROTTLE_TIMEOUT = 60  # 1 minute in seconds

    def allow_request(self, request, view):
        wallet_address = request.data.get("wallet_address")
        if not wallet_address:
            return False  # No wallet address provided

        current_time = time.time()

        # Check if the wallet address has requested funds within the timeout
        if wallet_address in wallet_request_times:
            last_request_time = wallet_request_times[wallet_address]
            if current_time - last_request_time < self.THROTTLE_TIMEOUT:
                return False  # Deny request (throttled)

        # Allow the request and update the last request time for the wallet address
        wallet_request_times[wallet_address] = current_time
        return True

    def wait(self):
        # Return the number of seconds to wait before making another request
        return self.THROTTLE_TIMEOUT
