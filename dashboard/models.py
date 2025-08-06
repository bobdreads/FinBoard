# Em dashboard/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo 1: Ativo


class Asset(models.Model):
    MARKET_CHOICES = [
        ('B3_ACOES', 'B3 - Ações'),
        ('B3_FUTUROS', 'B3 - Mercado Futuro'),
        ('FOREX_PARES', 'Forex - Pares de Moedas'),
        ('FOREX_COMMODITIES', 'Forex - Commodities'),
        ('FOREX_INDICES', 'Forex - Índices'),
    ]
    CURRENCY_CHOICES = [
        ('BRL', 'Real Brasileiro'),
        ('USD', 'Dólar Americano'),
    ]

    ticker = models.CharField(
        "Ticker", max_length=20, unique=True, help_text="Ex: PETR4, WDOFUT, EURUSD")
    name = models.CharField("Nome", max_length=100)
    market = models.CharField("Mercado", max_length=20, choices=MARKET_CHOICES)
    currency = models.CharField(
        "Moeda", max_length=3, choices=CURRENCY_CHOICES)
    description = models.TextField("Descrição", blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} ({self.get_market_display()})"

# Modelo 2: Estratégia


class Strategy(models.Model):
    name = models.CharField("Nome da Estratégia", max_length=100, unique=True)
    description = models.TextField("Descrição do Setup")

    def __str__(self):
        return self.name

# Modelo 3: Tag


class Tag(models.Model):
    name = models.CharField("Nome da Tag", max_length=50, unique=True)

    def __str__(self):
        return self.name

# Modelo 4: Operação (O Trade Completo)


class Operation(models.Model):
    STATUS_CHOICES = [('ABERTA', 'Aberta'), ('FECHADA', 'Fechada')]
    INITIAL_TYPE_CHOICES = [('COMPRA', 'Compra'), ('VENDA', 'Venda')]
    SENTIMENT_CHOICES = [
        ('CONFIANTE', 'Confiante'), ('ANSIOSO', 'Ansioso'),
        ('COM_MEDO', 'Com Medo'), ('FOCADO', 'Focado'), ('EFORICO', 'Eufórico')
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário")
    asset = models.ForeignKey(
        Asset, on_delete=models.PROTECT, verbose_name="Ativo")
    strategy = models.ForeignKey(
        Strategy, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Estratégia")

    # --- NOVOS CAMPOS ADICIONADOS AQUI ---
    # Plano de Trade
    initial_stop_price = models.DecimalField(
        "Preço de Stop Planejado", max_digits=10, decimal_places=5, blank=True, null=True)
    initial_target_price = models.DecimalField(
        "Preço de Alvo Planejado", max_digits=10, decimal_places=5, blank=True, null=True)
    # --- FIM DOS NOVOS CAMPOS ---

    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    status = models.CharField("Status", max_length=10,
                              choices=STATUS_CHOICES, default='ABERTA')
    initial_operation_type = models.CharField(
        "Tipo da Operação Inicial", max_length=10, choices=INITIAL_TYPE_CHOICES)
    start_date = models.DateTimeField("Data de Início")
    end_date = models.DateTimeField("Data de Fim", null=True, blank=True)

    net_financial_result = models.DecimalField(
        "Resultado Financeiro Líquido", max_digits=12, decimal_places=2, null=True, blank=True)
    points_pips_result = models.DecimalField(
        "Resultado em Pontos/Pips", max_digits=12, decimal_places=2, null=True, blank=True)

    entry_reason = models.TextField("Motivo da Entrada")
    general_notes = models.TextField(
        "Observações Gerais (Lições Aprendidas)", blank=True, null=True)
    entry_sentiment = models.CharField(
        "Sentimento na Entrada", max_length=10, choices=SENTIMENT_CHOICES, blank=True, null=True)
    execution_rating = models.IntegerField("Qualidade da Execução (1-5)", validators=[
                                           MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    def __str__(self):
        return f"Operação #{self.id} - {self.asset.ticker} - {self.user.username}"

# Modelo 5: Movimentação (Cada Compra ou Venda)


class Movement(models.Model):
    TYPE_CHOICES = [('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')]

    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name='movements', verbose_name="Operação")
    type = models.CharField("Tipo", max_length=10, choices=TYPE_CHOICES)
    datetime = models.DateTimeField("Data e Hora")
    quantity = models.DecimalField(
        "Quantidade", max_digits=12, decimal_places=2)
    # Aumentando a precisão do preço para acomodar o Forex
    price = models.DecimalField(
        "Preço", max_digits=12, decimal_places=5)  # <--- MUDANÇA AQUI
    costs = models.DecimalField(
        "Custos", max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.type} de {self.quantity} em {self.operation.asset.ticker}"

# Modelo 6: Anexo (Screenshots)


class Attachment(models.Model):
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name='attachments', verbose_name="Operação")
    file = models.ImageField("Arquivo", upload_to='trade_attachments/')
    description = models.CharField("Descrição", max_length=150)

    def __str__(self):
        return f"Anexo para a Operação #{self.operation.id}"
