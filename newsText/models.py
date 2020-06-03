from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.



class SeaNewsCbhgV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_cbhg_v2'


class SeaNewsCultureV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_culture_v2'


class SeaNewsDomesticV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_domestic_v2'


class SeaNewsEconomicsV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_economics_v2'


class SeaNewsEduV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_edu_v2'


class SeaNewsInternationalV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_international_v2'


class SeaNewsMilV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_mil_v2'


class SeaNewsTechV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_tech_v2'


class SeaNewsTodayhotV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_todayhot_v2'


class SeaNewsTraveV2(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)
    news_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sea_news_trave_v2'


class Test(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    news_type = models.CharField(max_length=10, blank=True, null=True)
    news_date = models.DateField(blank=True, null=True)
    news_summary = models.CharField(max_length=100, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_web_url = models.CharField(max_length=100, blank=True, null=True)
    news_source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
