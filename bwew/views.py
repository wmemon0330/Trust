from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from.models import*
from django.shortcuts import get_object_or_404, redirect
import uuid
from .models import DonationReceipt
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "index.html")
    
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("fname", None)
        last_name = request.POST.get("lname", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        age = request.POST.get("age", None)
        phone_number = request.POST.get("phone", None)

        user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=password)
        return redirect("login")
    
    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        print("Username:", username)
        print("Password:", password)
        print("Authenticated user:", user)

        if user is not None:
            print("User Found, Logged In")
            auth_login(request, user)
            return redirect("create_receipt")
        else:
            print("Invalid login credentials.")
            messages.error(request, "Invalid Username or Password")
    
    return render(request, "login.html")


@login_required
def create_receipt(request):
    if request.method == 'POST':
        donor_name = request.POST.get("donor_name")
        contact_no = request.POST.get("contact_no")
        donation_date = request.POST.get("donation_date")
        amount = request.POST.get("amount")
        remarks = request.POST.get("remarks")

        receipt_number = str(uuid.uuid4())[:8]

        receipt = DonationReceipt.objects.create(
            donor_name=donor_name,
            contact_no=contact_no,
            donation_date=donation_date,
            amount=amount,
            remarks=remarks,
            receipt_number=receipt_number,
            issued_by=request.user
        )

        # ✅ Redirect to viewreceipt instead of rendering it directly
        return redirect("viewreceipt")

    return render(request, "create_receipt.html")


@login_required
def viewreceipt(request):
    receipts = DonationReceipt.objects.filter(issued_by=request.user).order_by('-donation_date')
    return render(request, "viewreceipt.html", {"receipts": receipts})


def deletereceipt(request, receipt_id):
    receipt = get_object_or_404(DonationReceipt, id=receipt_id)
    receipt.delete()
    return redirect('viewreceipt')