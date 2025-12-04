from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_catalog_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('city', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=255, verbose_name='Адрес/пункт выдачи')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('processing', 'В обработке'), ('shipped', 'Отправлен'), ('completed', 'Завершён'), ('cancelled', 'Отменён')], default='new', max_length=20)),
                ('delivery_method', models.CharField(max_length=80)),
                ('payment_method', models.CharField(max_length=80)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='carbrand',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='cargeneration',
            unique_together={('name', 'car_model')},
        ),
        migrations.AlterUniqueTogether(
            name='carmodel',
            unique_together={('name', 'car_brand')},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100, unique=True, verbose_name='Артикул / OEM')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.URLField(blank=True, max_length=500, null=True, verbose_name='Фото')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.brand')),
                ('car_models', models.ManyToManyField(blank=True, related_name='products', to='shop.CarModel')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.category')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price_at_order', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='shop.product')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиции заказов',
            },
        ),
    ]