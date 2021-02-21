from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  # import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
import xlwt
import timeago
from dateutil import tz
from datetime import datetime, timezone

from .forms import CreateTicketForm, TicketUpdateForm, CommentForm
from .models import Ticket, STATES, SEVERITY_LEVELS, ISSUE_TYPE


# Create your views here.

def index(request):
    return render(request, 'index.html')


def listTickets(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to view the list")
        return redirect('/login')

    page = request.GET.get('page', 1)
    ticket_list = Ticket.objects.all().filter(Q(created_by=request.user) | Q(assigned_to=request.user)).order_by('-created_at')
    paginator = Paginator(ticket_list, 10)
    page_obj = paginator.get_page(page)

    time_lapsed = []
    ist_time = []
    format = "%d-%m-%Y %H:%M:%S"
    for ticket in page_obj:
        time_lapsed += [timeago.format(ticket.created_at, datetime.now().astimezone(tz=timezone.utc))]
        ist_time += [ticket.created_at.astimezone(tz.gettz('ITC')).strftime(format)]

    obj = zip(page_obj, time_lapsed, ist_time)

    return render(request, 'list.html', {'obj': obj, 'page_obj': page_obj})


def boardView(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to view the list")
        return redirect('/login')

    ticket_list = Ticket.objects.all().filter(Q(created_by=request.user) | Q(assigned_to=request.user)).order_by('-created_at')

    # Get from parameter how to group and group accordingly
    groups = {'state': STATES, 'severity': SEVERITY_LEVELS, 'issue_type': ISSUE_TYPE}
    group_by = request.GET.get('group_by', 'state')
    grouped_dict = {}
    for ticket in ticket_list:
        if group_by == 'state': grouped_dict.setdefault(ticket.get_state_display(), []).append(ticket)
        elif group_by == 'severity': grouped_dict.setdefault(ticket.get_severity_display(), []).append(ticket)
        else: grouped_dict.setdefault(ticket.get_issue_type_display(), []).append(ticket)

    if '' in grouped_dict: grouped_dict['Not Categorized'] += grouped_dict.pop('')

    print(grouped_dict)

    temp_dict = {}
    for key, tickets in grouped_dict.items():
        time_lapsed = []
        ist_time = []
        format = "%d-%m-%Y %H:%M:%S"
        for ticket in tickets:
            time_lapsed += [timeago.format(ticket.created_at, datetime.now().astimezone(tz=timezone.utc))]
            ist_time += [ticket.created_at.astimezone(tz.gettz('ITC')).strftime(format)]
        obj = zip(grouped_dict[key], time_lapsed, ist_time)

        temp_dict[key] = obj

    grouped_dict = temp_dict
    del temp_dict
    print(grouped_dict)

    return render(request, 'board_view.html', {'grouped_dict': grouped_dict, 'group_by': groups[group_by], 'sort_by': group_by})


def createTicket(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateTicketForm(request.POST)
            if form.is_valid():
                t = form.save(commit=False)
                t.created_by = request.user
                t.save()
                return redirect('/ticket/' + str(t.id))
            else:
                print(form)
                messages.warning(request, "There was some problem with the form data.")
                return redirect('/create')

        else:
            form = CreateTicketForm()

        return render(request, 'create.html', {'form': form})

    messages.warning(request, "You need to be logged in to create a ticket.")
    return redirect('/login')


def ticketDetail(request, tid):
    try:
        ticket_obj = Ticket.objects.get(id=tid)
    except:
        messages.warning(request, "The requested ticket is not available or has been deleted.")
        return redirect('/list')

    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to view the list.")
        return redirect('/login')

    if ticket_obj.created_by != request.user and ticket_obj.assigned_to != request.user:
        messages.warning(request, "You are not authorised to view this ticket.")
        return redirect('/list')

    if request.method == 'POST':
        form = TicketUpdateForm(instance=ticket_obj, data=request.POST)
        if form.is_valid():
            form.save()
            ticket_obj.created_at = datetime.now().astimezone(tz=timezone.utc)
            ticket_obj.save()
            messages.success(request, "Ticket has been updated.")
            return redirect(request.path_info)

    form = TicketUpdateForm(instance=ticket_obj)

    return render(request, 'ticket_detail.html', {'form': form, 'ticket_obj': ticket_obj})


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
    if request.user.is_authenticated:
        messages.warning('You are already logged in. Logout to sign in as different user.')
        return redirect('/')

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
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logoutUser(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def exportTicketsAsExcel(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to use this feature.")
        return redirect('/login')

    ticket_list = Ticket.objects.all().filter(Q(created_by=request.user) | Q(assigned_to=request.user)).order_by(
        '-created_at')

    time_lapsed = []
    ist_time = []
    format = "%d-%m-%Y %H:%M:%S"
    for ticket in ticket_list:
        time_lapsed += [timeago.format(ticket.created_at, datetime.now().astimezone(tz=timezone.utc))]
        ist_time += [ticket.created_at.astimezone(tz.gettz('ITC')).strftime(format)]

    obj = zip(ticket_list, time_lapsed, ist_time)

    response = HttpResponse(content_type='application/ms-excel')
    filename = "issues_"+ request.user.username
    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('LeaderBoard')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['S.no', 'Time Lapsed', 'Assigned To', 'Subject', 'Severity', 'State', 'Created By', 'Created at (IST)', 'Details']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    for ticket, time_elapsed, curr_time in obj:
        row_num += 1
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, time_elapsed, font_style)
        ws.write(row_num, 2, str(ticket.assigned_to), font_style)
        ws.write(row_num, 3, ticket.subject, font_style)
        ws.write(row_num, 4, ticket.get_severity_display(), font_style)
        ws.write(row_num, 5, ticket.get_state_display(), font_style)
        ws.write(row_num, 6, str(ticket.created_by), font_style)
        ws.write(row_num, 7, curr_time, font_style)
        ws.write(row_num, 8, ticket.details, font_style)
    wb.save(response)
    return response
