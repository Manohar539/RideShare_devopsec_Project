from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # auto login after register
            login(request, user)

            return JsonResponse({
                "success": True
            })

        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            })

    return JsonResponse({"success": False})