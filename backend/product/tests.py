import datetime
from django.test import TestCase
from django.utils import timezone

from production.models import *

class DeliveryDateTest(TestCase):

  def test_is_delivery_after_order_for_late_delivery(self):
    today = timezone.now()
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    delivery_in_future = Production(date_ordered = today, date_of_delivery = tomorrow)
    self.assertIs(delivery_in_future.is_delivery_date_after_order(), True)

  def test_is_delivery_after_order_for_early_delivery(self):

    today = timezone.now()
    yesterday = timezone.now() - datetime.timedelta(days=1)
    delivery_in_the_past = Production(date_ordered = today, date_of_delivery = yesterday)
    self.assertIs(delivery_in_the_past.is_delivery_date_after_order(), False)

  def test_is_delivery_after_order_for_same_dates(self):
    today = timezone.now()
    delivery_in_the_same_day = Production(date_ordered = today, date_of_delivery = today)
    self.assertIs(delivery_in_the_same_day.is_delivery_date_after_order(), True)