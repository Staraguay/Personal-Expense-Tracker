from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from tracker.models import *
from django.core.exceptions import ValidationError


# Create your tests here.

class BudgetTrackerTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='jhon@doe.com', password='testUserCreation')
        self.profile = Profile.objects.create(user=self.user, job_position='Software Engineer', main_currency='USD', age=24)
        self.login = self.client.login(username='jhon@doe.com', password='testUserCreation')

    def test_transaction_str_partiall(self):
        tx = Transaction(date=datetime.now())
        tx.full_clean()

    def test_transaction_str_full(self):
        tx = Transaction.objects.create(value_cad=10.0, value_usd=7.0, description='Test Transaction',
                                        date=datetime.now(), shop='Walmart', transaction_type='Expenses',
                                        category='Groceries', payment_type='Debit Card CAD')
        self.assertIsNotNone(tx.id)
        self.assertEqual(tx.shop, "Walmart")
        self.assertEqual(tx.transaction_type, "Expenses")
        self.assertEqual(str(tx), '10.0 - 7.0 - Test Transaction')

    def test_moneyTransfer_str_partiall(self):
        mt = MoneyTransfer(date=datetime.now())
        mt.full_clean()

    def test_moneyTransfer_str_full(self):
        mt = MoneyTransfer.objects.create(usd_value=7.0, platform='Wise', commission=1.50, cad_value=10.0,
                                          change_rate=1.37, processing_days=1, date=datetime.now())
        self.assertEqual(str(mt), '7.0 - Wise')

    def test_profile_str(self):
        prof = Profile.objects.get(user=self.user)
        self.assertIsNotNone(prof.id)
        self.assertEqual(str(prof), 'jhon@doe.com - Software Engineer')

    def test_views_requires_login(self):
        self.client.logout()

        protected_urls = [
            reverse('home'),
            reverse('profile'),
            reverse('transactions'),
            reverse('transaction-create'),
            reverse('transaction-update', args=[1]),
            reverse('money-transfer'),
            reverse('money-transfer-update', args=[1]),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/?next={url}')

    def test_apiViews_requires_login(self):
        self.client.logout()
        protected_urls = [
            reverse('expenses-summary'),
            reverse('incoming-summary'),
            reverse('history-summary'),
            reverse('transaction-api'),
            reverse('transaction-details', args=[1]),
            reverse('money-transfer-api'),
            reverse('money-transfer-detail', args=[1]),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
