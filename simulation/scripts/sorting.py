# Python imports
import django.db.models as models
from django.db.models import Q

# Django imports


# Local imports


class PlayerListParams:

    def __init__(self, request):
        self.request = request
        self.query = Q()
        self.ordering = "sim_rating"
        self.order_direction = "-"
        self.prefix = "" # Prefix for adding "player__" to fields

    def name_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        name_filter = self.request.POST.get("name-filter")
        if name_filter:
            name_parts = name_filter.split()
            name_query = Q()
            for part in name_parts:
                name_query &= Q(**{self.prefix + "first_name__icontains": part}) | Q(**{self.prefix + "last_name__icontains": part})
            self.query &= name_query

    def position_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        position_filter = self.request.POST.getlist("position-filter")
        if position_filter:
            positions = ["PG", "SG", "SF", "PF", "C"]
            position_query = Q()
            for position in positions:
                if position in position_filter:
                    position_query |= Q(**{self.prefix + "position": position})
            self.query &= position_query

    def league_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        league_filter = self.request.POST.get("league-filter")
        if league_filter:
            if league_filter == "main_league_only":
                self.query &= Q(**{self.prefix + "team__surge": False})
            elif league_filter == "surge_league_only":
                self.query &= Q(**{self.prefix + "team__surge": True})
            elif league_filter == "both_leagues":
                self.query &= Q(**{self.prefix + "team__surge": False}) | Q(**{self.prefix + "team__surge": True})

    def anomaly_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        anomaly_filter = self.request.POST.get("anomaly-filter")
        if anomaly_filter:
            if anomaly_filter == "only_anomalies":
                self.query &= Q(**{self.prefix + "anomaly": True})
            elif anomaly_filter == "exclude_anomalies":
                self.query &= Q(**{self.prefix + "anomaly": False})

    def custom_filter(self): # Input must be configured as is in 'templates/players/player_list.html' template
        custom_filter = self.request.POST.get("custom-filter")
        custom_filter_type = self.request.POST.get("custom-filter-type")
        custom_filter_value = self.request.POST.get("custom-filter-value")
        if custom_filter_value:
            if custom_filter_type == "gt":
                self.query &= Q(**{self.prefix + f"{custom_filter}__gte": custom_filter_value})
            elif custom_filter_type == "lt":
                self.query &= Q(**{self.prefix + f"{custom_filter}__lte": custom_filter_value})
            elif custom_filter_type == "eq":
                self.query &= Q(**{self.prefix + custom_filter: custom_filter_value})

    def get_ordered_queryset(self, queryset):
        filtered_queryset = queryset.filter()
        if self.ordering:
            filtered_queryset = filtered_queryset.order_by(f"{self.order_direction}{self.ordering}")
        return filtered_queryset

    def build_player_list_query(self):
        self.name_filter()
        self.position_filter()
        self.league_filter()
        self.anomaly_filter()
        self.custom_filter()
        return self.query
    
class AveragesListParams(PlayerListParams):

    def __init__(self, request):
        # Call parent constructor
        super().__init__(request)
        # Set child-specific attributes
        self.prefix = "player__"
        self.ordering = "average_game_score"

    def stat_filter(self):

        # Fields:
            # Field Name: 'field_name'
            # GTE, LTE, EQ: 'field_name__gte', 'field_name__lte', 'field_name'
            # Field Value: 'field_value'
            # Ascending, Descending: 'field_name', '-field_name'

        stat_filter = self.request.POST.get("stat-filter")
        stat_filter_type = self.request.POST.get("stat-filter-type")
        stat_filter_value = self.request.POST.get("stat-filter-value")
        stat_filter_order = self.request.POST.get("stat-filter-order")
        stat_filter_order_by = self.request.POST.get("stat-filter-order-by")

        # Add filter to query
        if stat_filter_value:
            # Add GTE, LTE, or EQ filter to query
            if stat_filter_type == "gt":
                self.query &= Q(**{f"{stat_filter}__gte": stat_filter_value})
            elif stat_filter_type == "lt":
                self.query &= Q(**{f"{stat_filter}__lte": stat_filter_value})
            elif stat_filter_type == "eq":
                self.query &= Q(**{stat_filter: stat_filter_value})
        # Add order to query
        if stat_filter_order_by:
            self.ordering = stat_filter_order_by.strip()
            if stat_filter_order == "asc":
                self.order_direction = "" # It's descending by default

    def build_averages_list_query(self):
        self.stat_filter()
        self.name_filter()
        self.position_filter()
        self.league_filter()
        self.custom_filter()

def build_player_list_params(request):
    params = PlayerListParams(request)
    params.build_player_list_query()
    return params, params.query

def build_averages_list_params(request):
    params = AveragesListParams(request)
    params.build_averages_list_query()
    return params, params.query
