from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_read = cleaned_data.get('is_read')
        message = cleaned_data.get('message')

        # Validation: A notification cannot be marked as read without a message
        if is_read and not message:
            raise forms.ValidationError("A read notification must have a message.")

        return cleaned_data
