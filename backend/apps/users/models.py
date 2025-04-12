from django.db import models

# Create your models here.
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
class Contactos(models.Model):
    nroemp = models.IntegerField(db_column='NroEmp', blank=True, null=True)  # Field name made lowercase.
    nrocon = models.IntegerField(db_column='NroCon', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=60, blank=True, null=True)  # Field name made lowercase.
    domcal = models.CharField(db_column='DomCal', max_length=30, blank=True, null=True)  # Field name made lowercase.
    domnro = models.CharField(db_column='DomNro', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dompis = models.CharField(db_column='DomPis', max_length=3, blank=True, null=True)  # Field name made lowercase.
    domdep = models.CharField(db_column='DomDep', max_length=5, blank=True, null=True)  # Field name made lowercase.
    locali = models.IntegerField(db_column='Locali', blank=True, null=True)  # Field name made lowercase.
    cp = models.CharField(db_column='CP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    provin = models.IntegerField(db_column='Provin', blank=True, null=True)  # Field name made lowercase.
    telefo = models.CharField(db_column='Telefo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=25, blank=True, null=True)  # Field name made lowercase.
    telcel = models.CharField(db_column='TelCel', max_length=25, blank=True, null=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='e-mail', max_length=120, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    fecnac = models.DateTimeField(db_column='FecNac', blank=True, null=True)  # Field name made lowercase.
    cuit = models.CharField(db_column='Cuit', max_length=13, blank=True, null=True)  # Field name made lowercase.
    cativa = models.CharField(db_column='CatIva', max_length=3, blank=True, null=True)  # Field name made lowercase.
    porcib = models.IntegerField(db_column='PorcIB', blank=True, null=True)  # Field name made lowercase.
    catgan = models.CharField(db_column='CatGan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    observ = models.TextField(db_column='Observ', blank=True, null=True)  # Field name made lowercase.
    escli = models.IntegerField(db_column='EsCli', blank=True, null=True)  # Field name made lowercase.
    espro = models.IntegerField(db_column='EsPro', blank=True, null=True)  # Field name made lowercase.
    obspos = models.CharField(db_column='ObsPos', max_length=120, blank=True, null=True)  # Field name made lowercase.
    ingbto = models.CharField(db_column='IngBto', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dirweb = models.CharField(db_column='DirWeb', max_length=50, blank=True, null=True)  # Field name made lowercase.
    calenv = models.CharField(db_column='CalEnv', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nroenv = models.CharField(db_column='NroEnv', max_length=5, blank=True, null=True)  # Field name made lowercase.
    locenv = models.IntegerField(db_column='LocEnv', blank=True, null=True)  # Field name made lowercase.
    codenv = models.CharField(db_column='CodEnv', max_length=8, blank=True, null=True)  # Field name made lowercase.
    telenv = models.CharField(db_column='TelEnv', max_length=25, blank=True, null=True)  # Field name made lowercase.
    transp = models.CharField(db_column='Transp', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pordes = models.FloatField(db_column='PorDes', blank=True, null=True)  # Field name made lowercase.
    vtocta = models.IntegerField(db_column='VtoCta', blank=True, null=True)  # Field name made lowercase.
    vtopro = models.IntegerField(db_column='VtoPro', blank=True, null=True)  # Field name made lowercase.
    nroven = models.IntegerField(db_column='NroVen', blank=True, null=True)  # Field name made lowercase.
    vtoins = models.DateTimeField(db_column='VtoIns', blank=True, null=True)  # Field name made lowercase.
    descu1 = models.FloatField(db_column='Descu1', blank=True, null=True)  # Field name made lowercase.
    descu2 = models.FloatField(db_column='Descu2', blank=True, null=True)  # Field name made lowercase.
    nrodoc = models.CharField(db_column='NroDoc', max_length=8, blank=True, null=True)  # Field name made lowercase.
    porfle = models.FloatField(db_column='PorFle', blank=True, null=True)  # Field name made lowercase.
    nrocbu = models.CharField(db_column='NroCBU', max_length=22, blank=True, null=True)  # Field name made lowercase.
    nrolis = models.IntegerField(db_column='NroLis', blank=True, null=True)  # Field name made lowercase.
    sincta = models.IntegerField(db_column='SinCta', blank=True, null=True)  # Field name made lowercase.
    cheque = models.CharField(db_column='Cheque', max_length=40, blank=True, null=True)  # Field name made lowercase.
    exeley = models.IntegerField(db_column='ExeLey', blank=True, null=True)  # Field name made lowercase.
    calcli = models.IntegerField(db_column='CalCli', blank=True, null=True)  # Field name made lowercase.
    clifac = models.IntegerField(db_column='CliFac', blank=True, null=True)  # Field name made lowercase.
    dto567 = models.BooleanField(db_column='Dto567', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    nomdes = models.CharField(db_column='NomDes', max_length=80, blank=True, null=True)  # Field name made lowercase.
    docdes = models.CharField(db_column='DocDes', max_length=13, blank=True, null=True)  # Field name made lowercase.
    obstra = models.CharField(db_column='ObsTra', max_length=255, blank=True, null=True)  # Field name made lowercase.
    grande = models.BooleanField(db_column='Grande', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cbuinf = models.BooleanField(db_column='CBUInf', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    periva = models.IntegerField(db_column='PerIVA', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'contactos' 




class WebUsuarios(models.Model):
    codigo = models.IntegerField(db_column='Codigo', primary_key=True)  # Field name made lowercase. The composite primary key (Codigo, CatUsu, NroDoc) found, that is not supported. The first column is selected.
    nombre = models.CharField(db_column='Nombre', max_length=40, blank=True, null=True)  # Field name made lowercase.       
    clave = models.CharField(db_column='Clave', max_length=20, blank=True, null=True)  # Field name made lowercase.
    e_mail = models.CharField(db_column='email',max_length=255, blank=True, null=True)
    catusu = models.CharField(db_column='CatUsu', max_length=1)  # Field name made lowercase.
    gposeg = models.IntegerField(db_column='GpoSeg', blank=True, null=True)  # Field name made lowercase.
    telcel = models.CharField(db_column='TelCel', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nrodoc = models.CharField(db_column='NroDoc', max_length=15)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'web_usuarios'
        unique_together = (('codigo', 'catusu', 'nrodoc'),)  



     # --- MÉTODOS AÑADIDOS PARA COMPATIBILIDAD CON JWT ---
    
    @property
    def is_anonymous(self):
        """
        Requerido por JWT - Siempre devuelve False ya que un usuario cargado nunca es anónimo
        """
        return False
        
    @property
    def is_authenticated(self):
        """
        Requerido por JWT - Siempre devuelve True ya que si tenemos una instancia del usuario,
        ya lo consideramos autenticado
        """
        return True
    
    def get_username(self):
        """
        Requerido por JWT - Devuelve un identificador único para el usuario
        """
        return self.e_mail
    # Añade este método a tu clase WebUsuarios en models.py si no lo tiene ya

    def get_id(self):
        """
        Método necesario para que RefreshToken pueda obtener el ID del usuario
        """
        return self.codigo
        
    def __str__(self):
        """
        Representación en string del usuario
        """
        return f"{self.nombre} ({self.e_mail})"
        