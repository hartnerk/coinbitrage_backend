from django.urls import path
from . import views

urlpatterns = [
    path('alerts', views.get_alerts, name="get_alerts"),
    path('alerts/<int:alert_id>', views.get_alert_by_id, name="get_alert_by_id"),
    path('alerts/new', views.new_alert, name='new_alert'),
    path('alerts/<int:alert_id>/edit', views.edit_alert, name='edit_alert'),
    path('alerts/<int:alert_id>/delete', views.delete_alert, name='delete_alert'),

    path('coinio/<str:coin_id>/best', views.best_arbitrage, name='best_arbitrage'),
    ]