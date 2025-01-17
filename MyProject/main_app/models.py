import uuid
from django.db import models




class Account(models.Model):
    email = models.EmailField(unique=True)  # Mandatory & unique
    account_id = models.CharField(max_length=10, unique=True, editable=False)  # Custom format: ACC1001
    account_name = models.CharField(max_length=100)  # Mandatory
    app_secret_token = models.CharField(max_length=64, unique=True, editable=False)  # Auto-generated secret token
    website = models.URLField(blank=True, null=True)  # Optional

    def save(self, *args, **kwargs):
        # Generate account_id in the format ACC1001, ACC1002, etc.
        if not self.account_id:
            # Get the last account_id and increment it
            last_account = Account.objects.order_by('-id').first()
            if last_account and last_account.account_id:
                # Extract the numeric part, increment, and format
                last_number = int(last_account.account_id.replace('ACC', ''))
                new_number = last_number + 1
            else:
                # Start from ACC1001 if no accounts exist
                new_number = 1001
            self.account_id = f"ACC{new_number}"  # Set the new account_id

        # Generate app secret token if not already set
        if not self.app_secret_token:
            import uuid
            self.app_secret_token = uuid.uuid4().hex

        super().save(*args, **kwargs)  # Call the base class save()

    def __str__(self):
        return self.account_name





class Destination(models.Model):
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)
    url = models.URLField()  # Mandatory
    http_method = models.CharField(
        max_length=10,
        choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')],  # HTTP method options
    )
    headers = models.JSONField()  # Stores multiple key-value pairs

    def __str__(self):
        return f"Destination for {self.account.account_name}: {self.url}"
