from django.forms import ModelForm
from django import forms
from touristapp2.models import *

class Membershipform(ModelForm):
    class Meta:
        model=Membershipmodel
        fields=['name','email','phone_number','country','special_request']
    def clean(self):
        super().clean()
        return self.cleaned_data
        
class Bookingform(ModelForm):
    class Meta:
        model=Bookingmodel
        fields=['name','email','check_in_date_and_time','check_out_date_and_time',
                'destination','no_of_persons','have_you_availed_membership',
                'type_of_room'
                ]
        def clean(self):
            super().clean()
            return self.cleaned_data


        
