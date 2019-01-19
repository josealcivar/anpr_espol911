from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View, TemplateView
from vehiculo.models import Vehiculo, Flujo_vehicular, Lista_negra_vehiculos
from django.urls import reverse_lazy
from django.utils.formats import get_format
import datetime, json
from functools import reduce
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from vehiculo.forms import ListaNegraForm, VehiculoProfile  # formulario de ListaNegra y Actualizarplaca vehiculo
from django.contrib import messages
import urllib
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
    return render(request, 'index.html')

#clase que permite borrar vehiculos que estan en lista negra
class ReportadoDelete(DeleteView):
    model         = Lista_negra_vehiculos
    template_name = 'vehiculo/delete_listanegra.html'
    success_url   = reverse_lazy('vehiculos_reportados')


#renderiza el grafico estadistico
class VehiculoChart(ListView):
    model           = Vehiculo
    template_name   = 'index.html'

    def get_context_data(self, *args,**kwargs):
        context = super(VehiculoChart, self).get_context_data(**kwargs)

        fecha_actual=datetime.datetime.now()
        dias=datetime.timedelta(days=30)
        print(dias)
        fecha_anterior=fecha_actual-dias
        print(fecha_anterior)
        # gte == fecha > 2000-23-14     lte fecha < 2000-12-12
        a= Flujo_vehicular.objects.filter(fecha__gte=fecha_anterior,fecha__lte=fecha_actual).values('fecha').annotate(carros=Count('vehiculo_id'))
        fechas=[]
        flujo_carros=[] 
        print(a)
        for valores in a:
            fechas.append((valores['fecha']).strftime("%d-%b"))
            flujo_carros.append(valores['carros'])
        dates_json = json.dumps(list(fechas), cls=DjangoJSONEncoder) # las fechas pasa en json
        print(fechas) 
        print(dates_json)
        context.update({'dates_json': dates_json})  #agrega los datos de fechas como un arreglo independiente
        context.update({'carros': flujo_carros})    #agrega los datos de carros como un arreglo independiente
        print(fechas)
        print(flujo_carros)
        return context

    def get_queryset(self):
        request= super(VehiculoChart, self).get_queryset()
        #request= super(VehiculoChart, self).get_queryset()
        print("hola")
        
      
        date_since       = self.request.GET.get('datesince')
        date_from        = self.request.GET.get('datefrom')
        print(date_since)
        print(date_from)
        # gte == fecha > 2000-23-14     lte fecha < 2000-12-12
        #a= Flujo_vehicular.objects.filter(fecha__gte=date_since,fecha__lte=date_from).values('fecha').annotate(carros=Count('vehiculo_id'))
        print("holaaa consultas")
        #print(a)
        fechas=[]
        flujo_carros=[]
        #for valores in a:
         #   fechas.append((valores['fecha']).strftime("%d-%b"))
         #   flujo_carros.append(valores['carros'])
        #dates_json = json.dumps(list(fechas), cls=DjangoJSONEncoder) # las fechas pasa en json
        print("imprime la consulta")
        print(fechas)
        print(flujo_carros)
        #request.update({'dates_json': dates_json})  #agrega los datos de fechas como un arreglo independiente
        #request.update({'carros': flujo_carros})    #agrega los datos de carros como un arreglo independiente
        
        return request


#muestra la lista de todos los vehiculos

class VehiculoList(ListView):
    model         = Flujo_vehicular
    template_name = 'vehiculo/consult.html'
    paginate_by   = 10

    def get_context_data(self, *args,**kwargs):
        context = super(VehiculoList, self).get_context_data(**kwargs)
        # context = super().get_context_data(**kwargs)
        fecha_actual=datetime.datetime.now().strftime('%d/%b/%Y')
        busqueda = self.get_queryset()
        context.update({'fecha_actual': fecha_actual})
        context.update({'busqueda': busqueda})
        print("ALGO")
        # print(context)
        # print("contexto")
        return context

    def get_queryset(self):
        request= super(VehiculoList, self).get_queryset()

        fecha_actual    = datetime.datetime.now()
        datesince       = self.request.GET.get('datesince')
        datefrom        = self.request.GET.get('datefrom')
        caracteristica  = self.request.GET.get('caracteristica')

        if caracteristica: # or datesince or datefrom:
            print("FILTRADO")
             # query_list = query.split()
             # b = Flujo_vehicular.objects.filter(vehiculo__placa__icontains=caracteristica)
            request= self.model.objects.filter(Q(vehiculo__placa__icontains=caracteristica) | Q(vehiculo__marca__icontains=caracteristica) | Q(vehiculo__modelo__icontains=caracteristica)) #| Q(fecha__gte=datesince) & Q(fecha__lte=datefrom) )
            # request= self.model.objects.filter((Q(fecha__gte=datesince) & Q(fecha__lte=datefrom) ))
            print(request.query)
            print(request)
        elif datesince or datefrom:
            print("TODO")
            request= self.model.objects.filter((Q(fecha__gte=datesince) & Q(fecha__lte=datefrom) ))


        else:
            request = self.model.objects.all().order_by('-fecha','-horacaptura')
    
        return request

#Reportar un vehiculo a lista negra
class VehiculoDenunciar(CreateView):
    model             = Flujo_vehicular
    second_model      = Vehiculo
    template_name     = 'vehiculo/vehiculo_reportar.html'
    form_class        = ListaNegraForm
    success_url       = reverse_lazy('consultar')



# pintar el formulario en el html
    def get_context_data(self, **kwargs):
        context = super(VehiculoDenunciar, self).get_context_data(**kwargs)
        pk=self.kwargs['pk']
        
        #verifica que el vehiculo no este en lista negra
        lista_negra = Lista_negra_vehiculos.objects.filter(vehiculo_id=pk).exists()
        # si no esta en lista negra, permite guardar el registro
        if not lista_negra:
           
            carro=self.second_model.objects.filter(id=pk).values('placa','marca','modelo')
            if carro:
                context['vehiculo']=carro[0]
        else:
            print("")
            # messages.error(request, 'Registro No existe o ya fue registrado', extra_tags='alert')
        if 'form' not in context:
           context['form'] = self.form_class(self.request.GET)
        print(context['form'])
        print("hola")
        print(context)
        return context


    # funcion para guardar en la base de datos de lista negra
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        #llena el formulario con los datos que estan en el template
        pk=self.kwargs['pk']
        form = self.form_class(request.POST)
        estado='ACTIVO'
        fecha=datetime.datetime.now()

        if request.method == 'POST':#para guardar los datos una vez modificados
            comentario = request.POST['comentario']
            
            lista=Lista_negra_vehiculos.objects.create(comentario=comentario, fecha=fecha, estado=estado,vehiculo_id=pk)
            lista.save()
            messages.success(request, 'Registro Fue Enviado a Lista Negra', extra_tags='alert')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.warning(request, 'No registro a lista negra')
            return self.render_to_response(self.get_context_data(form=form))


# Muestra la lista de todos los vehiculos reportados

class VehiculoReportadoList(ListView):
    model         = Lista_negra_vehiculos
    template_name = 'vehiculo/report.html'
    paginate_by   = 10

    def get_context_data(self, *args,**kwargs):
        context = super(VehiculoReportadoList, self).get_context_data(**kwargs)

        fecha_actual=datetime.datetime.now().strftime('%d/%b/%Y')
        busqueda = self.get_queryset()
        context.update({'fecha_actual': fecha_actual})
        context.update({'busqueda': busqueda})
     
        return context

    def get_queryset(self):
        result= super(VehiculoReportadoList, self).get_queryset()
        caracteristica  = self.request.GET.get('caracteristica')
        print(caracteristica)
        print("supuestamente mostro algo")
        if caracteristica:
            result= self.model.objects.filter(Q(vehiculo__placa__icontains=caracteristica) | Q(vehiculo__marca__icontains=caracteristica) | Q(vehiculo__modelo__icontains=caracteristica))

        print(result)
        return result

# carga la informacion del vehiculo registrado
class ProfileCar(DetailView):
    model = Flujo_vehicular
    template_name = 'vehiculo/Perfil_vehiculo.html'
    form_class = VehiculoProfile
    success_url  = reverse_lazy('consultar')

    def get_context_data(self, **kwargs):

        context = super(ProfileCar, self).get_context_data(**kwargs)
        #obtiene el id del vehiculo registrado
        pk = self.kwargs.get('pk', 0)
        vehiculo = Flujo_vehicular.objects.values('vehiculo_id').filter(id=pk)

        vehiculo2 = Vehiculo.objects.values('id','placa','marca','modelo','anio_vehiculo','servicio').filter(id=vehiculo[0]['vehiculo_id'])
        
        print(vehiculo2[0]['placa'])
        #guarda en un objeto para mostrarlo en el formulario
        context['object'] = vehiculo2[0]

        print("hola mundo")
        print(context)
        return context
    
        # fardado de datos del vehiculo 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        #llena el formulario con los datos que estan en el template
        pk=self.kwargs['pk']
        form = self.form_class(request.POST)
        
        if request.method == 'POST': #para guardar los datos una vez modificados
            placas = request.POST['placa'] # datos de placas que va a editar
            #carro=Lista_negra_vehiculos.objects.get(vehiculo_id=pk)
            # consulta el objeto a editar.
            carro=Vehiculo.objects.values('id','placa','marca','modelo','anio_vehiculo','servicio').filter(placa=placas)
            print("hola a todos")
            print(carro)
            if not carro:
                array_data=self.consultaPlaca(placas)
                
                if len(array_data)>1: # si es < 1 es porque tiene datos de vehiculo
                    car=Vehiculo.objects.create(placa=array_data[0], marca=array_data[1], color=array_data[2],anio_matricula=array_data[3], modelo=array_data[4], clase=array_data[5],fecha_matricula=array_data[6],anio_vehiculo=array_data[7], servicio=array_data[8],fecha_caducidad=array_data[9])
                    car.save() # guarda el vehiculo en la base de datos
                    car_with_id=Vehiculo.objects.values('id').filter(placa=placas)
                    print("MUESTRA LOS DATOS DE CARRO")
                    flujo_car=Flujo_vehicular.objects.get(id=pk)
                    print(flujo_car)
                    # proceso de actualizar name ruta imagen con placa
                    name_ruta_imagen=flujo_car.rutaimagen
                    print("ruta ant: ", name_ruta_imagen)
                    temp_image=str(name_ruta_imagen).split('_',1)
                    new_name=placas+'_'+temp_image[1]
                    print("ruta new: ", new_name)
                    flujo_car.rutaimagen=new_name
                    
                    flujo_car.vehiculo_id=car_with_id[0]['id']
                    flujo_car.save()
                    
                    messages.success(request, 'Vehiculo fue actualizado con placa: ' + placas , extra_tags='alert')

                else:
                    messages.error(request, 'NO existe Vehiculo con placa: '+ placas , extra_tags='alert')
                    
            else:
                flujo_car=Flujo_vehicular.objects.get(id=pk)
                # proceso de actualizar name ruta imagen con placa
                name_ruta_imagen=flujo_car.rutaimagen
                temp_image=str(name_ruta_imagen).split('_',1)
                new_name=placas+'_'+temp_image[1]
                flujo_car.rutaimagen=new_name
                flujo_car.vehiculo_id=carro[0]['id']
                flujo_car.save()
                messages.success(request, 'registro de flujo vehicular fue actualizado con placa: ' + placas , extra_tags='alert')
            
        else:
            messages.error(request, 'hubo un Error' , extra_tags='alert')
        return HttpResponseRedirect(self.success_url)
# funcion scrapping para traer datos de vehiculo
    def consultaPlaca(self, placa):
        data_vehicle=[]
        data_vehicle.append(placa)
        
        try:
            quote_page = 'http://consultas.atm.gob.ec/PortalWEB/paginas/clientes/clp_grid_citaciones.jsp?ps_tipo_identificacion=PLA&ps_identificacion='+ placa +'&ps_placa='
            page = urllib.request.urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find('table',{'cellpadding':"2"})
            rows = table.find_all('tr')
            for tr in rows:
                for wrapper in tr.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['detalle_formulario'] and tag.get('class') == ['detalle_formulario']):
                    data_vehicle.append(wrapper.text)
                    print (wrapper.text)

            print(data_vehicle)
            return data_vehicle
        except:
            print("no hay datos de vehiculo")
            return data_vehicle
