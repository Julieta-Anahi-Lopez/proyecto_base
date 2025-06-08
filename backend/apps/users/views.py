from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, views
from django.db import transaction
from .models import Contactos, WebUsuarios
from .serializers import ContactosSerializer, WebUsuariosListSerializer, WebUsuariosCreateUpdateSerializer
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


class ContactosViewSet(viewsets.ModelViewSet):  # Solo permite GET
    serializer_class = ContactosSerializer

    def get_queryset(self):
        return Contactos.objects.all() 
    
class WebUsuariosViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
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
        with transaction.atomic():
            try:
                # Validación previa de datos críticos
                if not request.data.get('nrodoc'):
                    return Response({'error': 'El DNI es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
                if not request.data.get('e_mail'):
                    return Response({'error': 'El email es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Verificación previa de duplicados en WebUsuarios
                nrodoc = request.data.get('nrodoc')
                email = request.data.get('e_mail')
                
                if WebUsuarios.objects.filter(nrodoc=nrodoc).exists():
                    return Response({'error': 'Ya existe un usuario web con este DNI'}, status=status.HTTP_400_BAD_REQUEST)
                
                if WebUsuarios.objects.filter(e_mail=email).exists():
                    return Response({'error': 'Ya existe un usuario web con este email'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Crear contacto primero
                contacto = self._crear_contacto(request.data)
                    
                # Preparar datos para el usuario web
                usuario_data = {
                    'codigo': contacto.nrocon,
                    'nombre': contacto.nombre,
                    'clave': request.data.get('clave', '1234'),  # Texto plano según requerimiento
                    'e_mail': contacto.e_mail,
                    'catusu': request.data.get('catusu', 'C'),
                    'gposeg': request.data.get('gposeg', 0),
                    'telcel': contacto.telcel,
                    'nrodoc': contacto.nrodoc
                }
                
                # Crear usuario web
                web_usuario = WebUsuarios.objects.create(**usuario_data)
                serializer = WebUsuariosListSerializer(web_usuario)
                headers = self.get_success_headers(serializer.data)
                
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                
            except ValueError as e:
                # Error de validación (controlado)
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Error inesperado (no controlado)
                return Response(
                    {'error': f'Error inesperado: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
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

    def _es_localidad_lista_cero(self, codigo_postal: str) -> bool:
        # Lista de códigos postales válidos (como strings)
        codigos_validos = {
            "8000",  # Bahía Blanca
            "8105",  # General Daniel Cerri
            "8109",  # Punta Alta
            "8150",  # Coronel Dorrego
            "8153",  # Monte Hermoso
            "8103",  # Ingeniero White
            "8160",  # Tornquist
            "7530",  # Coronel Pringles
            "8168",  # Sierra de la Ventana
            "8118",  # Cabildo
            "8170",  # Pigue
        }

        return str(codigo_postal) in codigos_validos

    
    def _crear_contacto(self, data):
        # Lógica para crear un contacto
        # print('Creando contacto')
        # print(f"Data: {data}")
        nro_emp = data.get('nroemp', 1)
        nrocon = Contactos.objects.all().order_by('-nrocon').first().nrocon + 1
        # print(f"nrocon: {nrocon}")
        nombre= data.get('nombre', 'Sin nombre')
        domCalle= data.get('domcalle', 'Sin calle')
        domnro= data.get('domnro', 'SN')
        dompis= data.get('dompis', 'SP')
        domdep= data.get('domdep', 'Sdep')
        locali= data.get('locali', None) # Si no indica, None para forzar que indiquen localidad en la validacion
        print(f"locali: {locali}")
        cp= data.get('cp', str(locali)[-4:])
        print(f"cp: {cp}")
        provin = data.get('provin', 1) # Si no indica, por defecto es Buenos Aires
        telefo = data.get('telefo', 'Sin telefono')
        fax = data.get('fax', 'Sin fax')
        telcel = data.get('telcel', 'Sin celular')
        e_mail = data.get('e_mail', None)
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
        locenv = data.get('locali', 8000) # Si no indica, por defecto es Bahia Blanca ---> Se asume que la localid de envio es la misma que la de registracion.
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

        if not locali:
            raise ValueError('El campo localidad es obligatorio')

        # Asino numero de lista en funcion del codigo postal.
        localidad_lista_cero = self._es_localidad_lista_cero(locali)
        if localidad_lista_cero:
            print("Entre a lista 0")
            nrolis = 0
        else:
            print("Entre a lista 1")
            nrolis = 1

        if nrodoc is None:
            raise ValueError('El DNI es obligatorio es obligatorio')
        if e_mail is None:
            raise ValueError('El email es obligatorio')
        if cativa != 'CF' and cuit is None:
            raise ValueError('La categoria de iva es obligatoria')
        dni_existente = Contactos.objects.filter(nrodoc=nrodoc).exists()
        e_mail_existente = Contactos.objects.filter(e_mail=e_mail).exists()
        if dni_existente or e_mail_existente:
            raise ValueError('El DNI o el email ya existen en la lista de contactos.')

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






from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import WebUsuarios
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

class LoginView(views.APIView):
    """
    Vista para login de usuarios web.
    Recibe email y contraseña, valida credenciales y devuelve tokens JWT.
    """
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    
    def post(self, request):
        # Obtener credenciales
        email = request.data.get('email')
        clave = request.data.get('clave')
        
        # Validar que se proporcionaron ambos campos
        if not email or not clave:
            return Response(
                {'error': 'Debe proporcionar email y contraseña'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Buscar usuario por email
            user = WebUsuarios.objects.get(e_mail=email)
            
            # Verificar contraseña (texto plano según requerimiento)
            if user.clave != clave:
                return Response(
                    {'error': 'Credenciales inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Generar tokens JWT para el usuario
            refresh = RefreshToken.for_user(user)
            
            # Devolver tokens y datos básicos del usuario
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'codigo': user.codigo,
                    'nombre': user.nombre,
                    'email': user.e_mail,
                    'catusu': user.catusu
                }
            })
            
        except WebUsuarios.DoesNotExist:
            # Por seguridad, no especificamos si el email no existe o la contraseña es incorrecta
            return Response(
                {'error': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class CustomTokenRefreshView(TokenRefreshView):
    """
    Vista personalizada para refrescar tokens JWT
    Usa nuestro serializador personalizado
    """
    serializer_class = CustomTokenRefreshSerializer