from django.db import models

# Create your models here.
class Pedidos(models.Model):
    compro = models.CharField(db_column='Compro', max_length=13,  primary_key=True)  # Field name made lowercase.
    nrocli = models.IntegerField(db_column='NroCli', blank=True, null=True)  # Field name made lowercase.
    fecped = models.DateTimeField(db_column='FecPed', blank=True, null=True)  # Field name made lowercase.
    plazo = models.CharField(db_column='Plazo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lugent = models.TextField(db_column='LugEnt', blank=True, null=True)  # Field name made lowercase.
    condic = models.CharField(db_column='Condic', max_length=50, blank=True, null=True)  # Field name made lowercase.
    observ = models.TextField(db_column='Observ', blank=True, null=True)  # Field name made lowercase.
    nrousu = models.IntegerField(db_column='NroUsu', blank=True, null=True)  # Field name made lowercase.
    nroven = models.IntegerField(db_column='NroVen', blank=True, null=True)  # Field name made lowercase.
    imputa = models.IntegerField(db_column='Imputa', blank=True, null=True)  # Field name made lowercase.
    nombpc = models.CharField(db_column='NombPC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=18, blank=True, null=True)  # Field name made lowercase.
    nroemp = models.IntegerField(db_column='NroEmp')  # Field name made lowercase. The composite primary key (NroEmp, Compro) found, that is not supported. The first column is selected.
    tipdep = models.IntegerField(db_column='TipDep', blank=True, null=True)  # Field name made lowercase.
    nroest = models.TextField(db_column='NroEst', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'pedidos'
        unique_together = (('nroemp', 'compro'),) 


class PedidosDetalle(models.Model):
    compro = models.CharField(db_column='Compro', max_length=13)  # Field name made lowercase.
    nroord = models.IntegerField(db_column='NroOrd')  # Field name made lowercase.
    codart = models.CharField(db_column='CodArt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantid = models.FloatField(db_column='Cantid', blank=True, null=True)  # Field name made lowercase.
    descri = models.CharField(db_column='Descri', max_length=255, blank=True, null=True)  # Field name made lowercase.
    penden = models.FloatField(db_column='PendEn', blank=True, null=True)  # Field name made lowercase.
    pendfc = models.FloatField(db_column='PendFC', blank=True, null=True)  # Field name made lowercase.
    precio = models.FloatField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    nrolis = models.IntegerField(db_column='NroLis', blank=True, null=True)  # Field name made lowercase.
    pordes = models.FloatField(db_column='PorDes', blank=True, null=True)  # Field name made lowercase.
    nroemp = models.IntegerField(db_column='NroEmp')  # Field name made lowercase. The composite primary key (NroEmp, Compro, NroOrd) found, that is not supported. The first column is selected.
    observ = models.CharField(db_column='Observ', max_length=25, blank=True, null=True)  # Field name made lowercase.
    poruni = models.FloatField(db_column='PorUni', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pedidos_detalle'
        unique_together = (('nroemp', 'compro', 'nroord'),)