# api/dashboard/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# --- Modelos de Suporte ---


class Tag(models.Model):
    """Sugestão 2: Modelo para as Tags das Estratégias"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# --- Modelos Principais ---


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
    # Sugestão 2: Adicionando a relação Muitos-para-Muitos com Tags
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Trade(models.Model):
    # Sugestão 1: Novas escolhas para o campo 'status'
    STATUS_CHOICES = (
        ('OPEN', 'Em Aberto'),
        ('CLOSED_TARGET', 'Fechado no Alvo'),
        ('CLOSED_STOP', 'Fechado no Stop'),
        ('CLOSED_MANUAL', 'Fechado Manualmente'),
    )
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
    net_result = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)

    # Sugestão 1: Substituindo 'is_open' por 'status'
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return f"Trade #{self.id} - {self.symbol} ({self.get_status_display()})"


class JournalNote(models.Model):
    # Sugestão 3: Adicionando a ligação direta e obrigatória ao User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # A ligação ao Trade agora é opcional, permitindo notas gerais
    trade = models.ForeignKey(
        Trade, on_delete=models.CASCADE, null=True, blank=True)
    strategy = models.ForeignKey(
        Strategy, on_delete=models.SET_NULL, null=True, blank=True)

    notes = models.TextField()
    confidence_level = models.IntegerField(default=5)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.trade:
            return f"Nota de Journal para Trade #{self.trade.id}"
        return f"Nota Geral de Journal ({self.user.username}) em {self.created_at.strftime('%d/%m/%Y')}"

# --- Outros Modelos (sem alterações, mas mantidos) ---


class TradeEntry(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='entries', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    entry_date = models.DateTimeField(default=timezone.now)


class TradeStop(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='stops', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    stop_date = models.DateTimeField(blank=True, null=True)


class TradeTarget(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='targets', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    target_date = models.DateTimeField(blank=True, null=True)


class TradeManualClose(models.Model):
    trade = models.ForeignKey(
        Trade, related_name='manual_closes', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=5)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    close_date = models.DateTimeField(default=timezone.now)


class PortfolioTransaction(models.Model):
    TRANSACTION_TYPES = (('DEPOSIT', 'Depósito'), ('WITHDRAWAL', 'Saque'))
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
