
from django.db.models import QuerySet, Count


class AstronautQueryset(QuerySet):
    def get_astronauts_by_missions_count(self) -> QuerySet:
        return self.prefetch_related('mission').annotate(
            mission_count=Count('mission')
        ).order_by(
            '-mission_count',
            'phone_number'
        )