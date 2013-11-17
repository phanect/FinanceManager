from django.test import TestCase
from django.test.client import Client
from book.models import Purchase, RecentRegistry
from datetime import datetime


class UITest(TestCase):
	"""Views tests & Selenium functional tests"""

	def setUp(self):
		self.client = Client()

	def test_register_view(self):
		"""register view test"""

		# FIXME change category specification when specification of category is decided
		datasets = [
				{"data": {"amount": "2000", "date": "2013/04/02", "category": "0"}, "status": 200, "should_success": True},
				{"data": {"amount": "3,500", "date": "2013/04/02", "category": "0"}, "status": 200, "should_success": True},
				# Wrong point of comma is accepted in amount
				{"data": {"amount": "42,00", "date": "2013/04/02", "category": "0"}, "status": 200, "should_success": True},
				# Wrong point and number of comma is accepted in amount
				{"data": {"amount": "29,4068,0", "date": "2013/04/02", "category": "0"}, "status": 200, "should_success": True},
				# Wrong Date Format; Only YYYY/MM/DD is accepted
				{"data": {"amount": "7200", "date": "2013-04-02", "category": "0"}, "status": 400, "should_success": False},
		]

		Purchase.objects.all().delete()

		for dataset in datasets:
			response = self.client.post("/book/register/", data=dataset["data"])

			# 1. If data is registered when valid data is given and 
			# rejected when invalid data is given
			registered_item = Purchase.objects.all()

			if dataset["should_success"] and registered_item:
				pass  # Success
			elif not dataset["should_success"] and not registered_item:
				pass  # Success
			elif dataset["should_success"] and not registered_item:
				self.fail("Purchasing data is not successfully registered.")
				return
			else: #  if not dataset["should_success"] and registered_item
				self.fail("Purchasing data is registered although it should be rejected.\nInput:\n%s\nRegistered:\n%s"
						% (dataset["data"], registered_item.values()))
				return

			# 2. Confirm if registered Purchase item is also added to RecentRegistry
			if registered_item:
				recentreg = RecentRegistry.objects.all()[0]

				self.assertEqual(recentreg.purchase, registered_item[0],
						msg="Tried to register: %s, Actually Registered: %s" % ( str(registered_item), str(recentreg.purchase)))

			Purchase.objects.all().delete()

			# 3. Status code confirmation
			self.assertEqual(response.status_code, dataset["status"],
							msg="Actual: %s, Expected: %s\nGiven data is:\n%s\nContent:\n%s\n%s"
							% (response.status_code, dataset["status"], dataset, response.content, response))

class ModelsTest(TestCase):
	def test_RecentRegistry(self):
		purchase = Purchase(amount=2000, date=datetime.strptime("2013/04/03", "%Y/%m/%d"), category=0)
		purchase.save()

		recentreg = RecentRegistry.objects.all()[0]
		self.assertEqual(recentreg.purchase, purchase)

		# TODO assert if registration time is correct

	def test_Purchase(self):
		pass  # FIXME
