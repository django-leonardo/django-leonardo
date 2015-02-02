
from horizon import forms

class DummyForm(forms.SelfHandlingForm):

    def handle(self, request, data):
        pass