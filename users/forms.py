from django import forms
from .models import FarmerProfile

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_approved = cleaned_data.get('is_approved')
        rejection_reason = cleaned_data.get('rejection_reason')

        if is_approved and rejection_reason:
            raise forms.ValidationError(
                "You cannot provide a rejection reason for an approved farmer."
            )

        return cleaned_data
