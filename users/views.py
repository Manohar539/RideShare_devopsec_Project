# users/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  # redirect after success

        return render(request, "register.html", {"form": form})

    form = UserCreationForm()
    return render(request, "register.html", {"form": form})