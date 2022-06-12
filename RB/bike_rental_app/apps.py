from django.apps import AppConfig


class BikeRentalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bike_rental_app'





class NAppConfig(AppConfig):
    name = 'bike_rental_app'

    def ready(self):
        import bike_rental_app.signals