from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import CreerUtilisateur, ModifierUtilisateur, ContactForm
from .models import User



@csrf_protect
def inscriptionPage(request):
    form = CreerUtilisateur()
    if request.method == 'POST':
        form = CreerUtilisateur(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            new_password1 = form.cleaned_data['password1']
            new_password2 = form.cleaned_data['password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
            messages.success(request, f'Compte créé avec succès pour {user.username}')
            return redirect('connexion')
    context = {'form': form}
    return render(request, 'users/inscription.html', context)

@login_required(login_url='connexion')
def profilUtilisateur(request, user_id=int):
    print("in profilUtilisateur to user id:", user_id)
    context={}
    return render(request, 'users/profil.html', context)

@login_required(login_url='connexion')
def modifierUtilisateur(request, user_id=int):
    print("in modifierUtilisateur to user id:", user_id)
    print(request)
    title = "Modification du profil"
    context = {'title': title}
    users = User.objects.all()
    print("all users:", users)
    user = User.objects.get(id__exact=user_id)
    if request.method == 'GET':
        form = ModifierUtilisateur(instance=user)
        print("form1: ", form)
        context = {'title': title, 'form': form}
    if request.method == 'POST':
        form = ModifierUtilisateur(request.POST, request.FILES)
        print("form2: ", form)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            new_password1 = form.cleaned_data['password1']
            new_password2 = form.cleaned_data['password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                messages.success(request, f"Ton profil a bien été modifié {user.username}")
                return redirect('recipes')
            else:
                messages.warning(request, f"Les mots de passe ne correspondent pas {user.username}")
        else:
            print("form3: ", form) 
            print("form.errors: ", form.errors)
            for field in form:
                print("Field Error:", field.name,  field.errors)
            print("get request to get profile ok but form seems not be valid")
            messages.warning(request, f"Les mots de passe ne correspondent pas {user.username}")
            # return render(request, 'users/modify_user_view.html', context)
    return render(request, 'users/modify_user_view.html', context)

@login_required(login_url='connexion')
def desactiverUtilisateur(request, user_id=int):
    print("in desactiverUtilisateur to user id:", user_id)
    print(request)
    title = "suppression du profil"
    context = {'title': title}
    user = User.objects.get(id__exact=user_id)
    user.is_active=False
    user.save()
    return redirect('connexion')

# @login_required(login_url='connexion')
# def modifierUtilisateur(request, user_id=int):
#     print("in modifierUtilisateur to user id:", user_id)
#     print(request)
#     context = {}
#     users = User.objects.all()
#     print(users)
#     print(users[2])
#     user = User.objects.get(id__exact=user_id)
#     if request.method == 'GET':
#         form = ModifierUtilisateur(instance=user)
#         context = {'form': form}
#     if request.method == 'POST':
#         form = ModifierUtilisateur(request.POST, request.FILES)
#         if form.is_valid():
#             user.username = form.cleaned_data['username']
#             user.email = form.cleaned_data['email']
#             new_password1 = form.cleaned_data['password']
#             new_password2 = form.cleaned_data['password']
#             if new_password1 == new_password2:
#                 user.set_password(new_password2)
#                 user.save()
#             else:
#                 messages.warning(request, f"Les mots de passe ne correspondent pas {user.username}")
#                 return render(request, 'users/modify_user_view.html', context)
#             messages.success(request, f"Ton profil a bien été modifié {user.username}")
#         return redirect('recipes')
    # return render(request, 'users/modify_user_view.html', context)

@csrf_protect
def accesPage(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipes')
        else:
            messages.info(request, "email ou mot de passe incorrect")
    return render(request, 'users/acces.html', context)


def logoutUser(request):
    logout(request)
    return redirect('connexion')


class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)