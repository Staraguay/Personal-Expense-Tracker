from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
import requests
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import render, redirect, reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import *
from .models import *
from .serializers import *
from django.urls import reverse_lazy
from decimal import Decimal
from django.http import JsonResponse
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from collections import OrderedDict


# Create your views here.

class CustomLogin(LoginView):
    redirect_authenticated_user = True


def register_user(request):
    if request.method == 'POST':
        form = UserCreationFormModfy(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationFormModfy()

    return render(request, 'registration/registration.html', {'form': form})


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now()
        current_month_start = today.replace(day=1)

        currency = self.request.GET.get('currency')
        valid_currencies = {'USD': 'value_usd', 'CAD': 'value_cad'}
        data_currency = valid_currencies.get(currency, 'value_cad')
        if currency:
            if currency == 'USD':
                data_currency = 'value_usd'
            else:
                data_currency = 'value_cad'


        expenses_this_month = Transaction.objects.filter(is_deleted=False, date__gte=current_month_start, transaction_type='Expenses').aggregate(total=Sum(data_currency))['total'] or 0
        incoming_this_month = Transaction.objects.filter(is_deleted=False, date__gte=current_month_start, transaction_type='Incomings').aggregate(total=Sum(data_currency))['total'] or 0
        biggest_expense = Transaction.objects.filter(is_deleted=False, date__gte=current_month_start, transaction_type='Expenses').order_by('-'+data_currency).first()
        context['expenses_this_month'] = expenses_this_month
        context['incoming_this_month'] = incoming_this_month
        context['biggest_expense'] = biggest_expense.value_cad if biggest_expense and data_currency == 'value_cad' else biggest_expense.value_usd if biggest_expense else 0
        context['currency'] = 'USD' if data_currency == 'value_usd' else 'CAD'

        return context

class ExpensesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): #obtener luego el CAD O USD con un boton dinamico

        currency = request.GET.get('currency')
        valid_currencies = {'USD': 'value_usd', 'CAD': 'value_cad'}
        data_currency = valid_currencies.get(currency, 'value_cad')

        summary = (Transaction.objects
                   .filter(is_deleted=False, transaction_type = 'Expenses')
                   .values('category')
                   .annotate(total=Sum(data_currency))
                   .order_by('category'))

        labels = [item['category'] for item in summary]
        data = [float(item['total']) for item in summary]

        return Response({'labels': labels, 'data': data})

class IncomeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        currency = self.request.GET.get('currency')
        valid_currencies = {'USD': 'value_usd', 'CAD': 'value_cad'}
        data_currency = valid_currencies.get(currency, 'value_cad')

        summary = (Transaction.objects
                   .filter(is_deleted=False, transaction_type = 'Incomings')
                   .values('category')
                   .annotate(total=Sum(data_currency))
                   .order_by('category'))
        labels = [item['category'] for item in summary]
        data = [float(item['total']) for item in summary]

        return Response({'labels': labels, 'data': data})

class HistoryAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        today = now().date()
        six_months_ago = today - relativedelta(months=6)

        currency = self.request.GET.get('currency')
        valid_currencies = {'USD': 'value_usd', 'CAD': 'value_cad'}
        data_currency = valid_currencies.get(currency, 'value_cad')

        transactions = (Transaction.objects
                        .filter(is_deleted=False, date__gte=six_months_ago)
                        .annotate(month=TruncMonth('date'))
                        .values('month','transaction_type')
                        .annotate(total=Sum(data_currency))
                        .order_by('month'))
        result = {
            'Expenses': {},
            'Incomings': {}
        }

        for entry in transactions:
            month = entry['month'].strftime('%Y-%m')
            transaction_type = entry['transaction_type']
            total = float(entry['total']) if entry['total'] else 0.0

            if transaction_type == 'Expenses':
                result['Expenses'][month] = total
            elif transaction_type == 'Incomings':
                result['Incomings'][month] = total

        current_date = six_months_ago
        while current_date <= today:
            month_str = current_date.strftime('%Y-%m')
            if month_str not in result['Expenses']:
                result['Expenses'][month_str] = 0.0
            if month_str not in result['Incomings']:
                result['Incomings'][month_str] = 0.0
            current_date += relativedelta(months=1)

        def sort_by_date(d):
            return OrderedDict(sorted(d.items(), key=lambda x: x[0]))

        sorted_data = {
            'Expenses': sort_by_date(result['Expenses']),
            'Incomings': sort_by_date(result['Incomings']),
        }

        return Response(sorted_data)
class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'app/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            profile = Profile.objects.get(user=self.request.user)
            kwargs['instance'] = profile
        except Profile.DoesNotExist:
            pass
        return kwargs

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)


class TransactionsView(LoginRequiredMixin,TemplateView):
    template_name = 'app/transactions.html'


class TransactionListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        transactions = Transaction.objects.filter(is_deleted=False)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionCreate(LoginRequiredMixin,CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'app/transaction-create.html'
    success_url = reverse_lazy('transactions')

    def form_valid(self, form):
        value_cad = form.cleaned_data['value_cad']
        value_usd = form.cleaned_data['value_usd']

        if value_cad is None and value_usd is None:
            form.add_error('value_cad', 'You must provide a valid value in CAD or USD')
            form.add_error('value_usd', 'You must provide a valid value in USD or CAD.')
            return self.form_invalid(form)

        if value_cad is None or value_usd is None:
            base_currency = 'CAD' if value_cad is not None else 'USD'
            target_currency = 'USD' if base_currency == 'CAD' else 'CAD'
            amount = value_cad if base_currency == 'CAD' else value_usd

            try:
                url = f'https://api.frankfurter.app/latest?amount={amount}&from={base_currency}&to={target_currency}'
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                rate = data.get('rates', {}).get(target_currency)
                if rate is None:
                    raise ValueError('Invalid API response')

                if base_currency == 'CAD':
                    form.instance.value_usd = Decimal(rate)
                else:
                    form.instance.value_cad = Decimal(rate)

            except requests.RequestException as e:
                form.add_error(None, 'Error querying the exchange rate.')
                print(e)
                return self.form_invalid(form)
            except (ValueError, KeyError) as e:
                form.add_error(None, 'Unexpected response from the exchange service.')
                print(e)
                return self.form_invalid(form)

        if form.instance.payment_type in ['Credit Card EC', 'Debit Card EC']:
            usd_value = form.instance.value_usd or Decimal('0')
            form.instance.isd = round(usd_value * Decimal('0.05'), 2)
            form.instance.tax_ec = round(usd_value * Decimal('0.12'), 2)

        return super(TransactionCreate, self).form_valid(form)


class TransactionViewAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class TransactionUpdate(LoginRequiredMixin,UpdateView):
    model = Transaction
    template_name = 'app/transaction-edit.html'
    success_url = reverse_lazy('transactions')
    form_class = TransactionForm

class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


class MoneyTransferList(LoginRequiredMixin, TemplateView):
    template_name = 'app/money-transfer.html'


class MoneyTransferListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        transfers = MoneyTransfer.objects.filter(is_deleted=False)
        serializer = MoneyTransferSerializer(transfers, many=True)
        return Response(serializer.data)


class MoneyTransferCreate(LoginRequiredMixin,CreateView):
    model = MoneyTransfer
    form_class = MoneyTransferForm
    template_name = 'app/money-transfer-create.html'
    success_url = reverse_lazy('money-transfer')


    def form_valid(self, form):
        usd_value = form.cleaned_data['usd_value']
        if isinstance(usd_value, Decimal):
            if form.instance.isd is None:
                form.instance.isd = round(usd_value * Decimal(0.05), 2)
            if form.instance.tax is None:
                form.instance.tax = round(usd_value * Decimal(0.12), 2)

        return super(MoneyTransferCreate, self).form_valid(form)


class MoneyTransferDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        transfers = MoneyTransfer.objects.get(pk=pk)
        serializer = MoneyTransferSerializer(transfers)
        return Response(serializer.data)


class MoneyTransferUpdate(LoginRequiredMixin, UpdateView):
    model = MoneyTransfer
    form_class = MoneyTransferForm
    template_name = 'app/money-transfer-edit.html'
    success_url = reverse_lazy('money-transfer')



class MoneyTransferDelete(LoginRequiredMixin, DeleteView):
    model = MoneyTransfer

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
