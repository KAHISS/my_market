from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuário")
    position = models.CharField(max_length=100, verbose_name="Cargo")
    hire_date = models.DateField(verbose_name="Data de Contratação")
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Salário")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.position}"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"


class WorkSchedule(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Funcionário")
    start_time = models.TimeField(verbose_name="Hora de Início")
    end_time = models.TimeField(verbose_name="Hora de Fim")
    overtime = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Horas Extras", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name = "Horário de Trabalho"
        verbose_name_plural = "Horários de Trabalho"


class Payment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Funcionário")
    payment_method = models.CharField(
        max_length=100,
        choices=[('dinheiro', 'Dinheiro'), ('cartão', 'Cartão'),
                 ('cheque', 'Cheque'), ('pix', 'Pix')],
        verbose_name="Método de Pagamento")
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Desconto", default=0)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor do Pagamento")
    proof = models.ImageField(
        "Comprovante", upload_to='employee/payments/%Y/%m/%d/', blank=True, default="")
    payment_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Data do Pagamento")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.payment_date}"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def total_amount(self):
        self.amount = self.employee.salary - self.discount
        self.save()
