from django.urls import path
from main_app.views import (
    AccountListCreateView,
    AccountDetailView,
    DestinationListCreateView,
    DestinationDetailView,
    AccountDestinationsView,
    IncomingDataHandlerView
)

urlpatterns = [
    # Account CRUD
    path('api/accounts/',          AccountListCreateView.as_view(), name='account-list-create'),
    path('api/accounts/<int:pk>/', AccountDetailView.as_view(),     name='account-detail'),

    # Destination CRUD
    path('api/destinations/',          DestinationListCreateView.as_view(), name='destination-list-create'),
    path('api/destinations/<int:pk>/', DestinationDetailView.as_view(),     name='destination-detail'),

    # Get destinations for a given account ID
    path('api/account/<str:account_id>/destinations/', AccountDestinationsView.as_view(), name='account-destinations'),

    # incoming Data
    path('server/incoming_data/', IncomingDataHandlerView.as_view(), name='incoming-data'),

]
