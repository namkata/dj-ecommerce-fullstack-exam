# Generated by Django 4.2 on 2025-02-23 13:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the record was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when the record was last updated.')),
                ('name', models.CharField(help_text='Product name', max_length=255)),
                ('slug', models.SlugField(help_text='Unique URL-friendly identifier', unique=True)),
                ('description', models.TextField(blank=True, help_text='Product description', null=True)),
                ('price', models.DecimalField(decimal_places=2, help_text='Product price', max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0, help_text='Available stock quantity')),
                ('main_image', models.ImageField(blank=True, help_text='Main product image', null=True, upload_to='product_images/')),
                ('specifications', models.JSONField(blank=True, help_text='Technical specifications', null=True)),
                ('rating', models.FloatField(default=0, help_text='Product rating', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('sold_count', models.PositiveIntegerField(default=0, help_text='Total products sold')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='categories.category')),
                ('created_by', models.ForeignKey(blank=True, help_text='The user who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, help_text='The user who last updated this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the record was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when the record was last updated.')),
                ('image', models.ImageField(help_text='Additional product image', upload_to='product_images/')),
                ('alt_text', models.CharField(blank=True, help_text='Alternative text for image', max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='The user who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
                ('updated_by', models.ForeignKey(blank=True, help_text='The user who last updated this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the record was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The date and time when the record was last updated.')),
                ('created_by', models.ForeignKey(blank=True, help_text='The user who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='products.product')),
                ('updated_by', models.ForeignKey(blank=True, help_text='The user who last updated this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
                'unique_together': {('user', 'product')},
            },
        ),
    ]
