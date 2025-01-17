from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from django.shortcuts import get_object_or_404


# CRUD for Account
class AccountListCreateView(APIView):
    # Handle GET (list all accounts) and POST (create an account)
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailView(APIView):
    # Handle GET, PUT, and DELETE for a single account
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        account.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# CRUD for Destination
class DestinationListCreateView(APIView):
    # Handle GET (list all destinations) and POST (create a destination)
    def get(self, request):
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #print('before serialize:',request.data)
        serializer = DestinationSerializer(data=request.data)
        #print('After Serializing',serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestinationDetailView(APIView):
    # Handle GET, PUT, and DELETE for a single destination
    def get(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        serializer = DestinationSerializer(destination)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        serializer = DestinationSerializer(destination, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        destination.delete()
        return Response({"message": "Destination deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Get destinations for a given account ID
class AccountDestinationsView(APIView):
    def get(self, request, account_id):
        try:
            account = Account.objects.get(account_id=account_id)
            destinations = Destination.objects.filter(account=account)
            serializer = DestinationSerializer(destinations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)









#### Incoming Data

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Account, Destination


class IncomingDataHandlerView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate the incoming JSON payload
        app_secret_token = request.data.get('app_secret_token')
        data = request.data.get('data')

        if not app_secret_token or not data:
            return Response(
                {"error": "Missing app_secret_token or data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Identify the account using the app secret token
        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response(
                {"error": "Invalid app_secret_token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Retrieve all destinations associated with the account
        destinations = Destination.objects.filter(account=account)

        if not destinations.exists():
            return Response(
                {"message": "No destinations configured for this account."},
                status=status.HTTP_200_OK
            )

        # Send data to destinations
        transmission_results = []
        for destination in destinations:
            try:
                # Send the request to the destination
                response = requests.request(
                    method=destination.http_method,
                    url=destination.url,
                    headers=destination.headers,
                    json=data  # Send the payload as JSON
                )

                # Log the result
                transmission_results.append({
                    "url": destination.url,
                    "status_code": response.status_code,
                    "response": response.text
                })

            except Exception as e:
                # Handle any errors during the request
                transmission_results.append({
                    "url": destination.url,
                    "error": str(e)
                })

        # Return the transmission results
        return Response({"transmissions": transmission_results}, status=status.HTTP_200_OK)
