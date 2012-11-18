from django.db import models
from django.db.models import F
from django.utils import timezone


class Domain(models.Model):
    """
    Model to represent hostnames and domains
    """
    name = models.CharField(max_length=300, db_index=True)
    wildcard = models.BooleanField(
        default=False,
        help_text='Include all subdomains e.g. *.example.com',
    )

    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class Redirect(models.Model):
    """
    Model to define old_domain/old_path to new_domain/new_paths
    """
    old_domain = models.ForeignKey(Domain, related_name='old_urls')
    old = models.CharField('Old Path', max_length=1000, db_index=True)
    new_domain = models.ForeignKey(Domain, related_name='new_urls')
    new = models.CharField('New Path', max_length=1000)

    class Meta:
        verbose_name = 'Redirect'
        verbose_name_plural = 'Redirects'
        ordering = ('old_domain', 'old')

    def __unicode__(self):
        return "%s/%s Redirect" % (self.old_domain.name, self.old)


class Ignore404(models.Model):
    """
    Patterns to ignore in 404s
    """
    domain = models.ForeignKey(Domain, related_name='ignores')
    name = models.CharField(max_length=100)

    starts_with = models.CharField(
        max_length=100,
        blank=True,
        help_text='Ignore if path begins with this.',
    )

    ends_with = models.CharField(
        max_length=200,
        blank=True,
        help_text='Ignore if path ends with this.',
    )

    pattern = models.CharField(
        'Pattern',
        max_length=500,
        blank=True,
        help_text='Ignore if path matches this regexp pattern',
    )

    class Meta:
        verbose_name = 'Ignore 404'
        verbose_name_plural = 'Ignore 404s'
        ordering = ('domain', 'name')

    def __unicode__(self):
        return "%s Ignore for %s" % (self.name, self.domain.name)


class Seen404(models.Model):
    """
    Model to store a count of 404s that are not redirected or ignored
    """
    domain = models.ForeignKey(Domain, related_name='seen_404s')
    path = models.CharField(max_length=1000, db_index=True)
    count = models.IntegerField(default=1, db_index=True)
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Seen 404'
        verbose_name_plural = 'Seen 404s'
        ordering = ('count', 'domain', 'path')

    def __unicode__(self):
        return "Seen 404 for %s/%s" % (self.domain.name, self.path)

    def increment(self, count=1):
        """ Increment the seen count """
        self.count = F('count') + count
        self.save()

    def save(self, *args, **kwargs):
        self.last_seen = timezone.now()
        super(Seen404, self).save(*args, **kwargs)
