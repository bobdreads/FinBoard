from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Importe F para referenciar campos
from django.db.models import Sum, Case, When, F, Min, Max
from decimal import Decimal  # Importe Decimal para cálculos precisos

# --- NOVOS MODELOS ---


class Account(models.Model):
    CURRENCY_CHOICES = [
        ('BRL', 'Real Brasileiro'),
        ('USD', 'Dólar Americano'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário")
    name = models.CharField("Nome da Carteira", max_length=100,
                            help_text="Ex: Corretora XP, Binance Futures")
    currency = models.CharField(
        "Moeda", max_length=3, choices=CURRENCY_CHOICES, default='BRL')
    initial_balance = models.DecimalField(
        "Saldo Inicial", max_digits=12, decimal_places=2, default=0.0)
    is_active = models.BooleanField("Ativa", default=True)

    @property
    def current_balance(self):
        """Calcula o saldo atual dinamicamente."""
        # 1. Começa com o saldo inicial
        balance = self.initial_balance

        # 2. Processa depósitos e saques
        # Usamos Case/When para somar depósitos e subtrair saques
        transaction_total = self.transactions.aggregate(
            total=Sum(
                Case(
                    When(type='DEPOSITO', then='amount'),
                    When(type='SAQUE', then=F('amount') * -1),
                    default=Decimal('0.0'),
                    output_field=models.DecimalField()
                )
            )
        )['total'] or Decimal('0.00')

        balance += transaction_total

        # 3. Adiciona o resultado líquido das operações fechadas
        operations_pl = self.operation_set.filter(status='FECHADA').aggregate(
            total_pl=Sum('net_financial_result')
        )['total_pl'] or Decimal('0.00')

        balance += operations_pl

        return round(balance, 2)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSITO', 'Depósito'),
        ('SAQUE', 'Saque'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                related_name='transactions', verbose_name="Carteira")
    type = models.CharField("Tipo", max_length=10,
                            choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    date = models.DateTimeField("Data")
    description = models.CharField(
        "Descrição", max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} de {self.amount} em {self.account.name}"

# --- MODELOS EXISTENTES (COM AJUSTE NA 'Operation') ---


class Asset(models.Model):
    # ... (sem alterações aqui)
    MARKET_CHOICES = [('B3_ACOES', 'B3 - Ações'), ('B3_FUTUROS', 'B3 - Mercado Futuro'), ('FOREX_PARES',
                                                                                          'Forex - Pares de Moedas'), ('FOREX_COMMODITIES', 'Forex - Commodities'), ('FOREX_INDICES', 'Forex - Índices')]
    CURRENCY_CHOICES = [('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano')]
    ticker = models.CharField(
        "Ticker", max_length=20, unique=True, help_text="Ex: PETR4, WDOFUT, EURUSD")
    name = models.CharField("Nome", max_length=100)
    market = models.CharField("Mercado", max_length=20, choices=MARKET_CHOICES)
    currency = models.CharField(
        "Moeda", max_length=3, choices=CURRENCY_CHOICES)
    description = models.TextField("Descrição", blank=True, null=True)
    def __str__(self): return f"{self.ticker} ({self.get_market_display()})"


class Strategy(models.Model):
    # ... (sem alterações aqui)
    name = models.CharField("Nome da Estratégia", max_length=100, unique=True)
    description = models.TextField("Descrição do Setup")
    def __str__(self): return self.name


class Tag(models.Model):
    # ... (sem alterações aqui)
    name = models.CharField("Nome da Tag", max_length=50, unique=True)
    def __str__(self): return self.name


class Operation(models.Model):
    # ... (outros campos continuam iguais)
    STATUS_CHOICES = [('ABERTA', 'Aberta'), ('FECHADA', 'Fechada')]
    INITIAL_TYPE_CHOICES = [('COMPRA', 'Compra'), ('VENDA', 'Venda')]
    SENTIMENT_CHOICES = [('CONFIANTE', 'Confiante'), ('ANSIOSO', 'Ansioso'),
                         ('COM_MEDO', 'Com Medo'), ('FOCADO', 'Focado'), ('EFORICO', 'Eufórico')]

    # <<< AJUSTE IMPORTANTE AQUI >>>
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, verbose_name="Carteira")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário")
    asset = models.ForeignKey(
        Asset, on_delete=models.PROTECT, verbose_name="Ativo")
    strategy = models.ForeignKey(
        Strategy, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Estratégia")
    initial_stop_price = models.DecimalField(
        "Preço de Stop Planejado", max_digits=10, decimal_places=5, blank=True, null=True)
    initial_target_price = models.DecimalField(
        "Preço de Alvo Planejado", max_digits=10, decimal_places=5, blank=True, null=True)
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

    def __str__(
        self): return f"Operação #{self.id} - {self.asset.ticker} - {self.user.username}"

    def update_calculated_fields(self):
        """
        Calcula e atualiza os campos da operação com base em seus movimentos.
        """
        movements = self.movements.all().order_by('datetime')

        if not movements.exists():
            # Se não há movimentos, reseta os campos
            self.start_date = None
            self.end_date = None
            self.status = 'ABERTA'  # Ou outro status padrão que queira
            self.save()
            return

        # Define a data de início com base no primeiro movimento
        self.start_date = movements.first().datetime

        # Calcula a quantidade total de entradas e saídas
        quantities = movements.aggregate(
            total_entry=Sum('quantity', filter=models.Q(type='ENTRADA')),
            total_exit=Sum('quantity', filter=models.Q(type='SAIDA'))
        )
        total_entry = quantities['total_entry'] or 0
        total_exit = quantities['total_exit'] or 0

        # Atualiza o status e a data de fim
        if total_entry == total_exit and total_entry > 0:
            self.status = 'FECHADA'
            # A data de fim é a data do último movimento de saída
            last_exit = movements.filter(type='SAIDA').last()
            self.end_date = last_exit.datetime if last_exit else None
        else:
            self.status = 'ABERTA'
            self.end_date = None

        self.save()


class Movement(models.Model):
    # ... (sem alterações aqui)
    TYPE_CHOICES = [('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')]
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name='movements', verbose_name="Operação")
    type = models.CharField("Tipo", max_length=10, choices=TYPE_CHOICES)
    datetime = models.DateTimeField("Data e Hora")
    quantity = models.DecimalField(
        "Quantidade", max_digits=12, decimal_places=2)
    price = models.DecimalField("Preço", max_digits=12, decimal_places=5)
    costs = models.DecimalField(
        "Custos", max_digits=10, decimal_places=2, default=0.0)

    def __str__(
        self): return f"{self.type} de {self.quantity} em {self.operation.asset.ticker}"

    def save(self, *args, **kwargs):
        # Primeiro, salva o próprio movimento
        super().save(*args, **kwargs)
        # Em seguida, aciona a atualização na operação pai
        self.operation.update_calculated_fields()

    def delete(self, *args, **kwargs):
        # Armazena a referência da operação pai antes de se deletar
        operation = self.operation
        super().delete(*args, **kwargs)
        # Aciona a atualização na operação pai
        operation.update_calculated_fields()


class Attachment(models.Model):
    # ... (sem alterações aqui)
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name='attachments', verbose_name="Operação")
    file = models.ImageField("Arquivo", upload_to='trade_attachments/')
    description = models.CharField("Descrição", max_length=150)
    def __str__(self): return f"Anexo para a Operação #{self.operation.id}"
