from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  # import messages
from django.contrib.auth.forms import AuthenticationForm

from .forms import CreateTicketForm, TicketUpdateForm, CommentForm

# Create your views here.

def index(request):

    return render(request, 'index.html')


def listTickets(request):

    return render(request, 'list.html')

def createTicket(request):
    if (request.user.is_authenticated):
        if request.method == "POST":
            form = CreateTicketForm(request.POST)
            if (form.is_valid()):
                t = form.save(commit=False)
                t.created_by = request.user
                t.save()
                # print(form.cleaned_data)
                return redirect('/ticket/' + str(t.id))
            else:
                messages.warning(request, "There was some problem with the form data.")
                return redirect('/create')

        else:
            form = CreateTicketForm()

        return render(request, 'create.html', {'form': form})

    messages.warning(request, "You need to be logged in to create a ticket.")
    return redirect('/login')

def ticketDetail(request, tid):
    return HttpResponse('This is the ticket view for ticket with id ' + str(tid))

def registerUser(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request=request, template_name="register.html", context={"register_form": form})


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logoutUser(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

