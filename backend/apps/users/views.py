from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Contactos, WebUsuarios
from .serializers import ContactosSerializer, WebUsuariosListSerializer, WebUsuariosCreateUpdateSerializer
# Create your views here.


class ContactosViewSet(viewsets.ModelViewSet):  # Solo permite GET
    serializer_class = ContactosSerializer

    def get_queryset(self):
        return Contactos.objects.all() 
    
class WebUsuariosViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return WebUsuarios.objects.all()
    
    def get_serializer_class(self):
        # Devuelve un serializer diferente según la acción
        if self.action in ['list', 'retrieve']:
            return WebUsuariosListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WebUsuariosCreateUpdateSerializer
        # Serializer por defecto si no coincide con ninguna acción específica
        return WebUsuariosListSerializer
    
    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        print(request.data)
        with transaction.atomic():
            # Aquí puedes agregar lógica personalizada para la creación
            # Por ejemplo, crear primero el contacto y luego el usuario web
            contacto = self._crear_contacto(request.data)
            print(f"contacto al salir de self._crear_contacto: {contacto}")
            codigo = contacto.nrocon
            print(f"codigo: {codigo}")
            nombre = contacto.nombre
            clave = request.data.get('clave', '1234')
            email = contacto.e_mail
            catusu = request.data.get('catusu', 'C')
            gposeg = request.data.get('gposeg', 0)
            telcel = contacto.telcel
            nrodoc = contacto.nrodoc
            try:
                web_usuario = WebUsuarios.objects.create(codigo=codigo,
                                                    nombre=nombre,
                                                    clave=clave,
                                                    email=email,
                                                    catusu=catusu,
                                                    gposeg=gposeg,
                                                    telcel=telcel,
                                                    nrodoc=nrodoc)
                serializer = WebUsuariosListSerializer(web_usuario)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except Exception as e:
                raise e
            # self.perform_create(serializer)
        
    
    # def perform_create(self, serializer):

    #     serializer.save()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Lógica personalizada para la actualización
            self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        serializer.save()

    
    def _crear_contacto(self, data):
        # Lógica para crear un contacto
        print('Creando contacto')
        print(f"Data: {data}")
        nro_emp = data.get('nroemp', 1)
        nrocon = Contactos.objects.all().order_by('-nrocon').first().nrocon + 1
        # print(f"nrocon: {nrocon}")
        nombre= data.get('nombre', 'Sin nombre')
        domCalle= data.get('domcalle', 'Sin calle')
        domnro= data.get('domnro', 'SN')
        dompis= data.get('dompis', 'SP')
        domdep= data.get('domdep', 'Sdep')
        locali= data.get('locali', 8000) # Si no indica, por defecto es Bahia Blanca
        # print(f"locali: {locali}")
        cp= data.get('cp', str(locali)[-4:])
        # print(f"cp: {cp}")
        provin = data.get('provin', 1) # Si no indica, por defecto es Buenos Aires
        telefo = data.get('telefo', 'Sin telefono')
        fax = data.get('fax', 'Sin fax')
        telcel = data.get('telcel', 'Sin celular')
        e_mail = data.get('e_mail', 'Sin email')
        fecnac = data.get('fecnac', '1900-01-01')
        cuit = data.get('cuit', 'Sin cuit')
        cativa = data.get('cativa', None)
        porcib = data.get('porcib', 0)
        catgan = data.get('catgan', '0')
        observ = data.get('observ', 'Contacto creado desde la web')
        escli = data.get('escli', 1)
        espro = data.get('espro', 0)
        obspos = data.get('obspos', 'Sin observaciones')
        ingbto = data.get('ingbto', 'Sin ingresos brutos')
        dirweb = data.get('dirweb', 'Sin direccion web')
        calenv = data.get('calenv', 'Sin calle envio')
        nroenv = data.get('nroenv', 'SN')
        locenv = data.get('locenv', 8000) # Si no indica, por defecto es Bahia Blanca
        codenv = data.get('codenv', str(locenv)[-4:])
        # print(f"codenv: {codenv}")
        telenv = data.get('telenv', 'Sin telefono envio')
        transp = data.get('transp', 'Sin transporte')
        pordes = data.get('pordes', 0)
        vtocta = data.get('vtocta', 30)
        vtopro = data.get('vtopro', 0)
        nroven = data.get('nroven', 0)
        vtoins = data.get('vtoins', '1900-01-01')
        descu1 = data.get('descu1', 0)
        descu2 = data.get('descu2', 0)
        nrodoc = data.get('nrodoc', None)
        porfle = data.get('porfle', 0)
        nrocbu = data.get('nrocbu', 'Sin nro cbu')
        nrolis = data.get('nrolis', 0)
        sincta = data.get('sincta', 0)
        cheque = data.get('cheque', 'Sin cheque')
        exeley = data.get('exeley', 0)
        calcli = data.get('calcli', 0)
        clifac = data.get('clifac', 0)
        dto567 = data.get('dto567', False)
        nomdes = data.get('nomdes', 'Sin nombre destino')
        docdes = data.get('docdes', 'Sin doc')
        obstra = data.get('obstra', 'Sin observaciones transporte')
        grande = data.get('grande', False)
        cbuinf = data.get('cbuinf', False)
        periva = data.get('periva', 0)

        if nrodoc is None:
            raise ValueError('El DNI es obligatorio es obligatorio')
        if cativa != 'CF' and cuit is None:
            raise ValueError('La categoria de iva es obligatoria')

        contacto, creado = Contactos.objects.get_or_create(nroemp=nro_emp,
                                            nrocon=nrocon,
                                            nombre=nombre, 
                                            domcal=domCalle, 
                                            domnro=domnro, 
                                            dompis=dompis, 
                                            domdep=domdep, 
                                            locali=locali, 
                                            cp=cp, 
                                            provin=provin, 
                                            telefo=telefo, 
                                            fax=fax,
                                            telcel=telcel,
                                            e_mail=e_mail,
                                            fecnac=fecnac,
                                            cuit=cuit,
                                            cativa=cativa,
                                            porcib=porcib,
                                            catgan=catgan,
                                            observ=observ,
                                            escli=escli, 
                                            espro=espro, 
                                            obspos=obspos, 
                                            ingbto=ingbto, 
                                            dirweb=dirweb, 
                                            calenv=calenv, 
                                            nroenv=nroenv, 
                                            locenv=locenv, 
                                            codenv=codenv,
                                            telenv=telenv,
                                            transp=transp,
                                            pordes=pordes,
                                            vtocta=vtocta,
                                            vtopro=vtopro,
                                            nroven=nroven,
                                            vtoins=vtoins,
                                            descu1=descu1,
                                            descu2=descu2,
                                            nrodoc=nrodoc,
                                            porfle=porfle,
                                            nrocbu=nrocbu,
                                            nrolis=nrolis,
                                            sincta=sincta,
                                            cheque=cheque,
                                            exeley=exeley,
                                            calcli=calcli,
                                            clifac=clifac,
                                            dto567=dto567,
                                            nomdes=nomdes,
                                            docdes=docdes,
                                            obstra=obstra,
                                            grande=grande,
                                            cbuinf=cbuinf,
                                            periva=periva)
        if creado:
            print(f"Contacto creado: {contacto}")
        else:
            print(f"Contacto ya existente: {contacto}")    
        return contacto

        

