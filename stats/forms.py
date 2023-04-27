from django import forms


class statsSearchForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
