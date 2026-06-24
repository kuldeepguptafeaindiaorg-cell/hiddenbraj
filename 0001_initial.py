from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Full Name')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('email', models.EmailField(blank=True, verbose_name='Email')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='City')),
                ('tour_type', models.CharField(
                    blank=True,
                    choices=[
                        ('weekend', 'Weekend Yatra (Sat–Sun)'),
                        ('extended', 'Extended Yatra (3–5 days)'),
                        ('custom', 'Custom / Private Yatra'),
                        ('school', 'School / Group Visit'),
                    ],
                    max_length=20,
                    verbose_name='Tour Type',
                )),
                ('message', models.TextField(blank=True, verbose_name='Message / Special Request')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Registered At')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Registration',
                'verbose_name_plural': 'Registrations',
                'ordering': ['-created_at'],
            },
        ),
    ]
