# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Articulos(models.Model):
    codigo = models.CharField(db_column='Codigo', primary_key=True, max_length=20)  # Field name made lowercase.
    equiva = models.CharField(db_column='Equiva', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nrouni = models.IntegerField(db_column='NroUni', blank=True, null=True)  # Field name made lowercase.
    nrogru = models.IntegerField(db_column='NroGru', blank=True, null=True)  # Field name made lowercase.
    nrosub = models.IntegerField(db_column='NroSub', blank=True, null=True)  # Field name made lowercase.
    nroenv = models.IntegerField(db_column='NroEnv', blank=True, null=True)  # Field name made lowercase.
    fecpre = models.DateTimeField(db_column='FecPre', blank=True, null=True)  # Field name made lowercase.
    precio = models.FloatField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    poruti = models.FloatField(db_column='PorUti', blank=True, null=True)  # Field name made lowercase.
    incide = models.FloatField(db_column='Incide', blank=True, null=True)  # Field name made lowercase.
    ivaexe = models.IntegerField(db_column='IvaExe', blank=True, null=True)  # Field name made lowercase.
    tabiva = models.IntegerField(db_column='TabIva', blank=True, null=True)  # Field name made lowercase.
    percib = models.FloatField(db_column='PercIB', blank=True, null=True)  # Field name made lowercase.
    constk = models.IntegerField(db_column='ConStk', blank=True, null=True)  # Field name made lowercase.
    fecstk = models.DateTimeField(db_column='FecStk', blank=True, null=True)  # Field name made lowercase.
    stkini = models.FloatField(db_column='StkIni', blank=True, null=True)  # Field name made lowercase.
    ptoped = models.FloatField(db_column='PtoPed', blank=True, null=True)  # Field name made lowercase.
    stkmax = models.FloatField(db_column='StkMax', blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    ubicac = models.CharField(db_column='Ubicac', max_length=20, blank=True, null=True)  # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo', blank=True, null=True)  # Field name made lowercase.
    nrorev = models.CharField(db_column='NroRev', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecrev = models.DateTimeField(db_column='FecRev', blank=True, null=True)  # Field name made lowercase.
    modulo = models.IntegerField(db_column='Modulo', blank=True, null=True)  # Field name made lowercase.
    observ = models.TextField(db_column='Observ', blank=True, null=True)  # Field name made lowercase.
    comisi = models.FloatField(db_column='Comisi', blank=True, null=True)  # Field name made lowercase.
    publi1 = models.FloatField(db_column='Publi1', blank=True, null=True)  # Field name made lowercase.
    publi2 = models.FloatField(db_column='Publi2', blank=True, null=True)  # Field name made lowercase.
    nromar = models.IntegerField(db_column='NroMar', blank=True, null=True)  # Field name made lowercase.
    aplica = models.CharField(db_column='Aplica', max_length=35, blank=True, null=True)  # Field name made lowercase.
    esbien = models.IntegerField(db_column='EsBien', blank=True, null=True)  # Field name made lowercase.
    esfavo = models.IntegerField(db_column='EsFavo', blank=True, null=True)  # Field name made lowercase.
    totitc = models.FloatField(db_column='TotITC', blank=True, null=True)  # Field name made lowercase.
    impco2 = models.FloatField(db_column='ImpCO2', blank=True, null=True)  # Field name made lowercase.
    coddgr = models.CharField(db_column='CodDGR', max_length=6, blank=True, null=True)  # Field name made lowercase.
    dto567 = models.IntegerField(db_column='Dto567', blank=True, null=True)  # Field name made lowercase.
    codncm = models.CharField(db_column='CodNCM', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nrofam = models.TextField(db_column='NroFam', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'articulos'
