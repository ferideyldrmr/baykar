from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, LoginForm, RentalRecordForm
from .models import UAV, RentalRecord
from .forms import UAVForm, RentalForm, LeaseForm
from .models import UAV, RentalRecord, Lease
from core.forms import LeaseForm


def index(request):
    return render(request, 'index.html')


def uavs(request):
    return render(request, 'uavs.html', {})

def about(request):
    return render(request, 'about.html', {})
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid form. Please check the fields and try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered and logged in successfully!')
            return redirect('index')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('index')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'change_password.html', context)


def add_uav(request):
    if request.method == 'POST':
        form = UAVForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'UAV added successfully!')
            return redirect('list_uavs')
    else:
        form = UAVForm()

    context = {'form': form}
    return render(request, 'add_uav.html', context)


def delete_uav(request, uav_id):
    uav = get_object_or_404(UAV, pk=uav_id)
    uav.delete()
    messages.success(request, 'UAV deleted successfully!')
    return redirect('list_uavs')


def update_uav(request, uav_id):
    uav = get_object_or_404(UAV, pk=uav_id)
    if request.method == 'POST':
        form = UAVForm(request.POST, instance=uav)
        if form.is_valid():
            form.save()
            messages.success(request, 'UAV updated successfully!')
            return redirect('list_uavs')
    else:
        form = UAVForm(instance=uav)

    context = {'form': form, 'uav': uav}
    return render(request, 'update_uav.html', context)


def list_uavs(request):
    uavs = UAV.objects.all()
    return render(request, 'list_uavs.html', {'uavs': uavs})


def rent_uav(request, uav_id=None):
    if uav_id is not None:
        uav = get_object_or_404(UAV, pk=uav_id)
    else:
        uav = None

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            if uav is not None:
                rental.uav = uav
            rental.save()
            messages.success(request, 'UAV rented successfully!')
            return redirect('list_uavs')
    else:
        form = RentalForm()

    context = {'form': form, 'uav': uav}
    return render(request, 'rent_uav.html', context)


def lease_uav(request, uav_id, rental_id):
    uav = get_object_or_404(UAV, pk=uav_id)
    rental = get_object_or_404(RentalRecord, pk=rental_id)
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.uav = uav
            lease.rental = rental
            lease.save()
            messages.success(request, 'Lease created successfully!')
            return redirect('list_leases', pk=uav_id)
    else:
        form = LeaseForm()

    context = {'form': form, 'uav': uav, 'rental': rental}
    return render(request, 'lease_uav.html', context)


def list_leases(request, pk):
    uav = get_object_or_404(UAV, pk=pk)
    leases = Lease.objects.filter(uav=uav)
    return render(request, 'list_leases.html', {'uav': uav, 'leases': leases})


def rental_list(request):
    rentals = RentalRecord.objects.all()
    return render(request, 'rental_list.html', {'rentals': rentals})


def rental_update(request, pk):
    rental = get_object_or_404(RentalRecord, pk=pk)
    form = RentalRecordForm(instance=rental)
    if request.method == 'POST':
        form = RentalRecordForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            return redirect('rental_list')
    return render(request, 'rental_form.html', {'form': form})


def rental_delete(request, pk):
    rental = get_object_or_404(RentalRecord, pk=pk)
    if request.method == 'POST':
        rental.delete()
        return redirect('rental_list')
    return render(request, 'rental_confirm_delete.html', {'rental': rental})


def delete_lease(request, pk, lease_id):
    uav = get_object_or_404(UAV, pk=pk)
    lease = get_object_or_404(Lease, pk=lease_id)
    if request.method == 'POST':
        lease.delete()
        return redirect('list_leases', pk=pk)
    return render(request, 'delete_lease.html', {'uav': uav, 'lease': lease})


def update_lease(request, pk, lease_id):
    uav = get_object_or_404(UAV, pk=pk)
    lease = get_object_or_404(Lease, pk=lease_id)
    form = LeaseForm(request.POST or None, instance=lease)
    if form.is_valid():
        form.save()
        return redirect('list_leases', pk=pk)
    return render(request, 'update_lease.html', {'form': form, 'uav': uav, 'lease': lease})


def list_leases(request, pk):
    uav = get_object_or_404(UAV, pk=pk)
    leases = Lease.objects.filter(uav=uav)
    return render(request, 'list_leases.html', {'uav': uav, 'leases': leases})

