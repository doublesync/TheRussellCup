# Python imports
import django.db.models as models
from django.db.models import Q

# Django imports


# Local imports


class FilterListParams:

    def __init__(self, request):
        self.request = request
        self.query = Q()

    def name_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        name_filter = self.request.POST.get("name-filter")
        if name_filter:
            name_parts = name_filter.split()
            name_query = Q()
            for part in name_parts:
                name_query &= Q(first_name__icontains=part) | Q(last_name__icontains=part)
            self.query &= name_query

    def position_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        position_filter = self.request.POST.getlist("position-filter")
        if position_filter:
            positions = ["PG", "SG", "SF", "PF", "C"]
            position_query = Q()
            for position in positions:
                if position in position_filter:
                    position_query |= Q(position=position)
            self.query &= position_query

    def league_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        league_filter = self.request.POST.get("league-filter")
        if league_filter:
            if league_filter == "main_league_only":
                self.query &= Q(team__surge=False)
            elif league_filter == "surge_league_only":
                self.query &= Q(team__surge=True)

    def anomaly_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        anomaly_filter = self.request.POST.get("anomaly-filter")
        if anomaly_filter:
            if anomaly_filter == "only_anomalies":
                self.query &= Q(anomaly=True)
            elif anomaly_filter == "exclude_anomalies":
                self.query &= Q(anomaly=False)

    def custom_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        custom_filter = self.request.POST.get("custom-filter")
        custom_filter_type = self.request.POST.get("custom-filter-type")
        custom_filter_value = self.request.POST.get("custom-filter-value")
        if custom_filter_value:
            if custom_filter_type == "gt":
                self.query &= Q(**{f"{custom_filter}__gt": custom_filter_value})
            elif custom_filter_type == "lt":
                self.query &= Q(**{f"{custom_filter}__lt": custom_filter_value})
            elif custom_filter_type == "eq":
                self.query &= Q(**{custom_filter: custom_filter_value})

    def build_player_list_query(self):
        self.name_filter()
        self.position_filter()
        self.league_filter()
        self.anomaly_filter()
        self.custom_filter()
        return self.query
    

def build_player_list_params(request):
    params = FilterListParams(request)
    query = params.build_player_list_query()
    return query

def build_averages_list_params(request):
    params = FilterListParams(request)
    query = params.build_averages_list_query()
    return query
