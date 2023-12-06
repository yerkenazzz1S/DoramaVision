from django import forms
from core.models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['text']