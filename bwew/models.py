from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class DonationReceipt(models.Model):
    donor_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    donation_date = models.DateField()
    receipt_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Meta:
        db_table = 'bwew_donationreceipt'