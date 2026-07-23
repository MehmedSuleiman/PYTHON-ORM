from django.db import models

from main_app.querysets import AstronautQueryset


class AstronautManager(models.Manager.from_queryset(AstronautQueryset)):
    ...