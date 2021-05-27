from django.test import TestCase
from .models import Deal, Response, User, Transport, Pay_method
import datetime

# Create your tests here.
class ResponseTastCase(TestCase):

    def setUp(self):
        u1 = User.objects.create(username='user1', password="1")
        u2 = User.objects.create(username='user2', password="2")

        Response.objects.create(rating='1', author=u1, on_user=u2)
        Response.objects.create(rating='3', author=u2, on_user=u1)
        Response.objects.create(rating='1', author=u1, on_user=u1)

        tr1 = Transport.objects.create(name='a', description='d', owner=u1)
        tr1.clients.add(u1)

        pm1 = Pay_method.objects.create(pay_method_name = "PayPal")
        d1 = Deal.objects.create(rent_transport=tr1, owner=u1, client=u1, start_date=datetime.date.today(), close_date=datetime.date.today() + datetime.timedelta(days=1), pay_method=pm1)
        d2 = Deal.objects.create(rent_transport=tr1, owner=u1, client=u2, start_date=datetime.date.today(), close_date=datetime.date.today(), pay_method=pm1)
        d3 = Deal.objects.create(rent_transport=tr1, owner=u1, client=u2, start_date=datetime.date.today(), close_date=datetime.date.today() + datetime.timedelta(days=1), pay_method=pm1)

    def test_response_author_resiver__diferent_users(self):
        u1 = User.objects.get(username='user1')
        u2 = User.objects.get(username='user2')
        resp = Response.objects.get(author=u1, on_user=u2)
        self.assertTrue(resp.is_valid_response())

    def test_response_author_resiver_one_user(self):
        u1 = User.objects.get(username='user1')
        resp = Response.objects.get(author=u1, on_user=u1)
        self.assertFalse(resp.is_valid_response())
  
    def test_owner_client_one_user(self):
        u1 = User.objects.get(username='user1')
        resp = Transport.objects.get(owner=u1)
        self.assertFalse(resp.is_valid_transport())

    def test_deal_owner_client_same(self):
        u1 = User.objects.get(username='user1')
        d = Deal.objects.get(owner=u1, client=u1)
        self.assertFalse(d.is_valid_deal())

    def test_deal_start_close_in_one_day(self):
        u1 = User.objects.get(username='user1')
        u2 = User.objects.get(username='user2')
        d = Deal.objects.get(owner=u1, client=u2, close_date=datetime.date.today())
        self.assertFalse(d.is_valid_deal())

    def test_deal_norm(self):
        u1 = User.objects.get(username='user1')
        u2 = User.objects.get(username='user2')
        d = Deal.objects.get(owner=u1, client=u2, close_date=datetime.date.today() + datetime.timedelta(days=1))
        self.assertTrue(d.is_valid_deal())