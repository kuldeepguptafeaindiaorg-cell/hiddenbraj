from django import forms
from .models import Registration, TOUR_TYPE_CHOICES


class RegistrationForm(forms.ModelForm):
    """Mirrors the fields in the HiddenBraj HTML form."""

    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'id': 'fname', 'placeholder': 'Aapka poora naam'}),
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'id': 'phone', 'placeholder': '+91 XXXXX XXXXX'}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'aapka@email.com'}),
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'id': 'city', 'placeholder': 'Aap kahan se hain?'}),
    )
    tour_type = forms.ChoiceField(
        choices=[('', '— Tour prakar chunein —')] + list(TOUR_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'id': 'tourtype'}),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'msg',
            'rows': 4,
            'placeholder': 'Koi vishesh iccha ya prashn?',
        }),
    )

    class Meta:
        model = Registration
        fields = ['name', 'phone', 'email', 'city', 'tour_type', 'message']
