from coinbitrage_api.models import Alert
from django.forms import ModelForm

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ['alert_name', 'coin', 'threshold', 'user', 'enabled']