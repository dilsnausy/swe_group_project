from django import forms
from .models import BuyerProfile

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['delivery_address']
    def save(self, commit=True):
    # Save the phone number from CustomUser
        user = self.instance.user # Get the CustomUser associated with the profile
        user.phone_number = self.cleaned_data.get('phone_number')  # Save phone_number to the CustomUser model
        if commit:
            user.save()  # Save the CustomUser instance
        return super().save(commit)