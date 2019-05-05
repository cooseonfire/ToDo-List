from django import forms


class TodolistForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=150, label='List title')


class TodoForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    description = forms.CharField(max_length=2000, widget=forms.Textarea,
                                  label='Description', required=False)
    priority = forms.ChoiceField(choices=((1, 'Low'), (2, 'Medium'),
                                          (3, 'High')),
                                 required=False, label='Priority')
    deadline = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                               required=False, label='Deadline')
