from django import forms

class SearchForm(forms.Form):
    pick_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date','blank':'true'}))
    pick_time = forms.TimeField(widget = forms.TimeInput(attrs={'type': 'time','blank':'true'}))
    drop_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date','blank':'true'}))
    drop_time = forms.TimeField(widget = forms.TimeInput(attrs={'type': 'time','blank':'true'}))
