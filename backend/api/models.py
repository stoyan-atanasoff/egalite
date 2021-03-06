from django.db import models
import math

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=100)
    siret = models.CharField(max_length=100, null = True, blank = True)
    created_date = models.DateTimeField('date created')
    last_iegh = models.FloatField(blank = True, null = True)

    def __unicode__(self):
        return self.name

    def last_data(self):
        data = OrganizationData.objects.filter(organization = self).order_by('year')
        if data:
            return data[0]
        else:
            return None

    def latest_data_id(self):
        data = self.last_data()
        if not data:
            return None
        return data.pk

    def last_iegh(self):
        data = self.last_data()
        return data.get_iegh()


class OrganizationData(models.Model):
    created_date = models.DateTimeField('date created')
    year = models.PositiveIntegerField(null = True)
    direction_male = models.PositiveIntegerField(null = True)
    direction_female = models.PositiveIntegerField(null = True)
    global_male_ratio = models.FloatField()
    employees_count =  models.PositiveIntegerField(null = True, blank = True)
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)
    iehg = models.FloatField()
    # TODO approved and author 

    def __init__(self, *args, **kwargs):
        super(OrganizationData, self).__init__(*args, **kwargs)
        self.iehg = self.get_iegh()

    def get_direction_female_ratio(self):
        if self.direction_female == 0:
            return 0
        return self.direction_female / (self.direction_female + self.direction_male)

    def get_iegh(self):
        if self.pk is not None:
            return 100 * (1 - math.sqrt(math.fabs(1 - self.global_male_ratio / 100 - self.get_direction_female_ratio())))
        else:
            return None

    def __unicode__(self):
        return self.organization.name + " " + self.year
