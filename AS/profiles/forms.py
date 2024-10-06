from django import forms
from core.models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
