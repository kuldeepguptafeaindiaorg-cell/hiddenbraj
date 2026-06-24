from django.db import models


TOUR_TYPE_CHOICES = [
    ('weekend', 'Weekend Yatra (Sat–Sun)'),
    ('extended', 'Extended Yatra (3–5 days)'),
    ('custom', 'Custom / Private Yatra'),
    ('school', 'School / Group Visit'),
]


class Registration(models.Model):
    """Stores a visitor's tour registration from the HiddenBraj website."""

    name = models.CharField(max_length=200, verbose_name='Full Name')
    phone = models.CharField(max_length=20, verbose_name='Phone Number')
    email = models.EmailField(blank=True, verbose_name='Email')
    city = models.CharField(max_length=100, blank=True, verbose_name='City')
    tour_type = models.CharField(
        max_length=20,
        choices=TOUR_TYPE_CHOICES,
        blank=True,
        verbose_name='Tour Type',
    )
    message = models.TextField(blank=True, verbose_name='Message / Special Request')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Registered At')
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return f"{self.name} — {self.phone} ({self.created_at.strftime('%d %b %Y')})"
