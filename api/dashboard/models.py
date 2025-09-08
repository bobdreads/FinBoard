# api/dashboard/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Mantivemos a lógica de conversão de moeda, pode ser útil
from .currency_converter import convert_to_brl

# --- Modelos Principais baseados no seu Diagrama ER ---


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='BRL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Strategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Trade(models.Model):
    SIDE_CHOICES = (
        ('BUY', 'Compra'),
        ('SELL', 'Venda'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)
    side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    # Campos que serão calculados com base nas entradas/saídas
    # Podemos adicionar lógica para os calcular depois
    net_result = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"Trade #{self.id} - {self.symbol} ({self.side})"

# --- Modelos de Suporte ao Trade ---


class TradeEntry(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='entries', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    entry_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Entrada em Trade #{self.trade.id} @ {self.price}"


class TradeStop(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='stops', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    # Data em que o stop foi atingido
    stop_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Stop para Trade #{self.trade.id} @ {self.price}"


class TradeTarget(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='targets', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    # Quantidade a ser realizada
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    # Data em que o alvo foi atingido
    target_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Alvo para Trade #{self.trade.id} @ {self.price}"


class TradeManualClose(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='manual_closes', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    close_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Fecho Manual em Trade #{self.trade.id} @ {self.price}"

# --- Outros Modelos do Diagrama ---


class JournalNote(models.Model):
    trade = models.ForeignKey(
        Trade, on_delete=models.CASCADE, null=True, blank=True)
    strategy = models.ForeignKey(
        Strategy, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField()
    confidence_level = models.IntegerField(default=5)  # Ex: de 1 a 10
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de Journal para Trade #{self.trade_id}"


class PortfolioTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Depósito'),
        ('WITHDRAWAL', 'Saque'),
    )
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.type} de {self.value} em {self.portfolio.name}"

# E assim por diante para os outros modelos como SupportTicket, TaxReturn, etc.
# Começamos com estes que são o núcleo da lógica de trading.
