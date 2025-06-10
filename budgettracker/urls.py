"""
URL configuration for budgettracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tracker import views as tracker_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tracker_views.CustomLogin.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout' ),
    path('register', tracker_views.register_user, name='register'),
    path('home/', tracker_views.Home.as_view(), name='home'),
    path('api/expenses-summary/', tracker_views.ExpensesAPI.as_view(), name='expenses-summary'),
    path('api/incoming-summary/', tracker_views.IncomeAPI.as_view(), name='incoming-summary'),
    path('api/history/', tracker_views.HistoryAPI.as_view(), name='history-summary'),
    path('profile/', tracker_views.ProfileView.as_view(), name='profile'),
    path('transactions/', tracker_views.TransactionsView.as_view(), name='transactions'),
    path('api/transactions/', tracker_views.TransactionListAPI.as_view(), name='transaction-api'),
    path('transactions/create/', tracker_views.TransactionCreate.as_view(), name='transaction-create'),
    path('transactions/<int:pk>', tracker_views.TransactionViewAPI.as_view(), name='transaction-details'),
    path('transactions/edit/<int:pk>', tracker_views.TransactionUpdate.as_view(), name='transaction-update'),
    path('transactions/delete/<int:pk>', tracker_views.TransactionDelete.as_view(), name='transaction-delete'),
    path('money-transfer/', tracker_views.MoneyTransferList.as_view(), name='money-transfer'),
    path('api/money-transfer', tracker_views.MoneyTransferListAPI.as_view(), name='money-transfer-api'),
    path('money-transfer/create/', tracker_views.MoneyTransferCreate.as_view(), name='money-transfer-create'),
    path('money-transfer/<int:pk>', tracker_views.MoneyTransferDetailsAPI.as_view(), name='money-transfer-detail'),
    path('money-transfer/edit/<int:pk>', tracker_views.MoneyTransferUpdate.as_view(), name='money-transfer-update'),
    path('money-transfer/delete/<int:pk>', tracker_views.MoneyTransferDelete.as_view(), name='money-transfer-delete'),
]
