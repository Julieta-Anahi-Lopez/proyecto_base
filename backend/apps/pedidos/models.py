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