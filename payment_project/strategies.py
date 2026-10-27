# Import asyncio
# Used to simulate asynchronous payment processing
import asyncio



# ESEWA STRATEGY


class EsewaStrategy:

    async def pay(self, amount):

        # Simulate waiting for external eSewa API
        await asyncio.sleep(1)

        return {
            "status": "SUCCESS",
            "message": f"Rs. {amount} paid using eSewa"
        }



# KHALTI STRATEGY


class KhaltiStrategy:

    async def pay(self, amount):

        # Simulate Khalti API call
        await asyncio.sleep(1)

        return {
            "status": "SUCCESS",
            "message": f"Rs. {amount} paid using Khalti"
        }



# CARD STRATEGY


class CardStrategy:

    async def pay(self, amount):

        # Simulate card payment API
        await asyncio.sleep(1)

        return {
            "status": "SUCCESS",
            "message": f"Rs. {amount} paid using Card"
        }