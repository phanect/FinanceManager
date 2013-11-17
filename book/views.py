from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from datetime import datetime
from book.models import Purchase

# @login_required
def register(request):
	if request.method != "POST":
		return HttpResponseBadRequest("Request method must be POST.")

	#
	# Receive parameters and validate
	#
	try:
		amount = request.POST["amount"]
		amount = amount.replace(",", "")  # remove all commas

		if "." in amount:
			return HttpResponseBadRequest("Decimal is not supported.")

		amount = int(amount)
		date = datetime.strptime(request.POST["date"], "%Y/%m/%d")
		category = request.POST["category"]
	except KeyError as e:
		# In case required parameters are not given
		return HttpResponseBadRequest("%s" % e.strerror)
	except ValueError:
		# in case date is given in wrong data format
		return HttpResponseBadRequest("Only YYYY/MM/DD format is accepted for date.")

	#
	# Register Purchase data
	#
	purchase = Purchase(amount=amount, date=date, category=category)
	purchase.save()

	return HttpResponse()
