from django.db import models
from django.conf import settings

# Create your models here.

STATES = [
    ('OPN', 'Open'),
    ('BLK', 'Blocked'),
    ('MRG', 'Merged'),
    ('RES', 'Resolved'),
    ('CLS', 'Closed'),
]

SEVERITY_LEVELS = [
    (5, 'Blocker'),
    (4, 'Critical'),
    (3, 'Major'),
    (2, 'Minor'),
    (1, 'Trivial'),
    (-1, 'Not Categorized')
]

ISSUE_TYPE = [
    ('IMP', 'Improvement'),
    ('NEW', 'New Feature'),
    ('BUG', 'Bug'),
    ('TST', 'Test'),
    ('TSK', 'Task'),
    ('NOT', 'Not Categorized')
]


class Ticket(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Created by',
        related_name='created_tickets',
    )
    created_at = models.DateTimeField(
        'Created at', auto_now_add=True,
    )
    subject = models.CharField(
        'Subject', max_length=100,
    )
    details = models.TextField(
        'Details', max_length=1000,
        blank=True
    )
    severity = models.IntegerField(
        'Severity', choices=SEVERITY_LEVELS,
        null=True, default=-1,
    )
    issue_type = models.CharField(
        'Issue Type', max_length=16, choices=ISSUE_TYPE,
        null=False, default='NOT'
    )
    state = models.CharField(
        'State', max_length=16, choices=STATES,
        null=False, default='OPN',
    )
    other_ticket = models.ForeignKey(
        'Ticket', models.PROTECT, null=True, blank=True,
        related_name='related',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, verbose_name='Assigned to',
        related_name='assigned_tickets', null=True, blank=True,
    )

    def __str__(self):
        return '#{0}: {1}'.format(self.id, self.subject)

    def blocked_tickets(self):
        return self.related.filter(state='Blocked')

    def merged_tickets(self):
        return self.related.filter(state='Merged')

    def update(self, **kwargs):
        self.severity = kwargs.get('severity', self.severity)
        self.state = kwargs.get('state', self.state)
        self.save()

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class TicketComments(models.Model):
    ticket = models.ForeignKey(
        Ticket, models.CASCADE, verbose_name='Ticket', related_name='entries'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.PROTECT, verbose_name='Created by',
    )
    created_at = models.DateTimeField(
        'Created at', auto_now_add=True,
    )
    body = models.CharField(
        'Body', max_length=1000,
    )

    class Meta:
        verbose_name = 'TicketComment'
        verbose_name_plural = 'TicketComments'
