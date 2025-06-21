import json
from datetime import datetime
from django import setup
from django.test import TestCase, Client
from django.urls import reverse

from tracker.forms import TransactionForm, MoneyTransferForm
from tracker.models import *
from django.core.exceptions import ValidationError


# Create your tests here.

class BudgetTrackerTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='jhon@doe.com', password='testUserCreation')
        self.profile = Profile.objects.create(user=self.user, job_position='Software Engineer', main_currency='USD',
                                              age=24)
        self.login = self.client.login(email='jhon@doe.com', password='testUserCreation')

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

    def test_views_display(self):
        Transaction.objects.create(date=datetime.now(), value_cad=10.0, value_usd=7.0, description='Test Transaction')
        MoneyTransfer.objects.create(date=datetime.now(), usd_value=7.0, platform='Wise', commission=1.50,
                                     cad_value=10.0, change_rate=1.37, processing_days=1)
        view_urls = {
            # reverse('login') : 'registration/login.html',
            reverse('register'): 'registration/registration.html',
            reverse('profile'): 'app/profile.html',
            reverse('transactions'): 'app/transactions.html',
            reverse('transaction-create'): 'app/transaction-create.html',
            reverse('transaction-update', args=[1]): 'app/transaction-edit.html',
            reverse('money-transfer'): 'app/money-transfer.html',
            reverse('money-transfer-create'): 'app/money-transfer-create.html',
            reverse('money-transfer-update', args=[1]): 'app/money-transfer-edit.html',

        }

        for key, value in view_urls.items():
            response = self.client.get(key)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, value)

    def test_api_returns_json(self):
        Transaction.objects.create(date=datetime.now(), value_cad=10.0, value_usd=7.0, description='Test Transaction')
        MoneyTransfer.objects.create(date=datetime.now(), usd_value=7.0, platform='Wise', commission=1.50,
                                     cad_value=10.0, change_rate=1.37, processing_days=1)
        api_urls = [
            reverse('expenses-summary'),
            reverse('incoming-summary'),
            reverse('history-summary'),
            reverse('transaction-api'),
            reverse('transaction-details', args=[1]),
            reverse('money-transfer-api'),
            reverse('money-transfer-detail', args=[1]),
        ]

        for url in api_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            data = json.loads(response.content)
            self.assertGreater(len(data), 0)

    def test_new_transaction_form(self):
        form_data = {
            'value_cad': 10.0,
            'value_usd': 7.0,
            'description': 'Test Transaction',
            'shop': 'Walmart',
            'transaction_type': 'Expenses',
            'category': 'Groceries',
            'payment_type': 'Debit Card CAD',
            'isd': 0.0,
            'tax_ec': 0.0,
            'date': datetime.now(),
        }

        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_money_transfer_form(self):
        form_data = {
            'platform': 'Wise',
            'usd_value': 7.0,
            'cad_value': 10.0,
            'commission': 1.50,
            'date': datetime.now(),
            'change_rate': 1.37,
            'processing_days': 1,
            'isd': 0.0,
            'tax': 0.0,
        }

        form = MoneyTransferForm(data=form_data)
        self.assertTrue(form.is_valid())