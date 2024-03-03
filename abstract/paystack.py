from django.conf import settings
import requests

class Paystack:
	"""
    A class for interacting with the Paystack API for transaction verification.
    """
	PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
	base_url = "https://api.paystack.co/"

	def verify_payment(self, ref, *args, **kwarges):
		"""
        Verifies a Paystack transaction by its reference code.

        Args:
            ref (str): The reference code of the transaction to be verified.

        Returns:
            tuple[str, dict]: A tuple containing the transaction status and data
                if successful (status code 200), otherwise the transaction status
                and a generic message.

        """
		path = f'transaction/verify/{ref}'
		headers = {
		"Authorization": f'Bearer {self.PAYSTACK_SK}',
		'Content-Type': 'application/json'
		}

		url = self.base_url + path
		response = requests.get(url, headers=headers)
		print(f'Transaction with ref: {ref} has a response {response} and status code of {response.status_code}')
		if response.status_code == 200:
			response_data = response.json()
			return response_data['status'], response_data['data']

		response_data = response.json()
		return response_data['status'], response_data['message']