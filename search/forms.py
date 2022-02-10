from django import forms


class SearchForm(forms.Form):
    origin = forms.CharField(max_length=72, label="From", min_length=3)
    destination = forms.CharField(max_length=72, label="To")
    departure_date = forms.DateField(label="Departure", widget=forms.DateInput(attrs={'type': 'date'}),)
    return_date = forms.DateField(label="Return", widget=forms.DateInput(attrs={'type': 'date'}),)
