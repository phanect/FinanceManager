from django.test import TestCase
from django.test.client import Client


class UITest(TestCase):
	"""Views tests & Selenium functional tests"""

	def setUp(self):
		self.client = Client()

	def test_register_view(self):
		"""register view test"""

		# FIXME change category specification when specification of category is decided
		datasets = [
				{"data": {"amount": "2000", "date": "2013/04/02", "category": "0"}, "status": 200},
				{"data": {"amount": "3,500", "date": "2013/04/02", "category": "0"}, "status": 200},
				{"data": {"amount": "42,00", "date": "2013/04/02", "category": "0"}, "status": 200},
				# Wrong Date Format; Only YYYY/MM/DD is accepted
				{"data": {"amount": "7200", "date": "2013-04-02", "category": "0"}, "status": 400}
		]

		for dataset in datasets:
			response = self.client.post("/register/", data=dataset["data"] )
			self.assertEqual(response.status_code, dataset["status"])
