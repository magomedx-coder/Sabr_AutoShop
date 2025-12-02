from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Bank(models.Model):
    name = models.CharField(max_length=255)
    bic = models.CharField(max_length=15, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self):
        return self.name


class Contractor(models.Model):
    name = models.CharField(max_length=255)
    bank = models.ForeignKey('Bank', models.DO_NOTHING, verbose_name='Банк', blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    okonh = models.CharField(max_length=5, blank=True, null=True)
    okpo = models.CharField(max_length=10, blank=True, null=True)
    inn = models.CharField(max_length=23, blank=True, null=True)
    is_supplier = models.BooleanField()
    comment = models.CharField(max_length=150, blank=True, null=True)


class Country(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    group = models.ForeignKey('Group', models.CASCADE, verbose_name='Группа товаров')
    supplier_price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Закуп. цена')
    retail_price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Розн. цена')
    unit = models.ForeignKey('Unit', models.DO_NOTHING, verbose_name='Единица')
    minimal_amount = models.BigIntegerField(verbose_name='Норма запаса')
    all_amount = models.BigIntegerField(verbose_name='Кол-во')
    weight = models.IntegerField(verbose_name='Масса')
    countries = models.ManyToManyField('Country')
    actual = models.BooleanField(verbose_name='Актуальный')

    class Meta:
        ordering = ('-pk',)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Группа товаров"
        verbose_name_plural = "Группы товаров"

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Единица"
        verbose_name_plural = "Единицы"

    def __str__(self):
        return self.name


class GoodItem(models.Model):
    item = models.ForeignKey('Good', on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name


class Invoice(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=250, default='Simple sale', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at) + (str(' ' + self.comment) if self.comment else '')

    def get_absolute_url(self):
        return reverse('invoice_detail', kwargs={'invoice_id': self.pk})

    def get_total_cost(self):
        total_cost = 0
        for i in self.gooditem_set.all():
            total_cost += i.price * i.quantity
        return total_cost

    class Meta:
        ordering = ('-pk',)
