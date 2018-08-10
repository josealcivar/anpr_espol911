from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView, View
from vehiculo.models import Vehiculo, Flujo_vehicular, Lista_negra_vehiculos
from django.urls import reverse_lazy
from django.utils.formats import get_format
import datetime, json
from functools import reduce
from django.db.models import Q, Count
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.

def index(request):
    return render(request, 'index.html')

class VehiculoChart(ListView):
    model           = Vehiculo
    template_name   = 'index.html'

    def get_context_data(self, *args,**kwargs):
        context = super(VehiculoChart, self).get_context_data(**kwargs)

        fecha_actual=datetime.datetime.now()
        dias=datetime.timedelta(days=30)
        fecha_anterior=fecha_actual-dias
        print(fecha_anterior)
        # a= Vehiculo.objects.filter(fecha__gte=fecha_anterior,fecha__lte=fecha_actual).values('fecha').annotate(carros=Count('placa'))
        a= Flujo_vehicular.objects.filter(fecha__gte=fecha_anterior,fecha__lte='2018-08-30').values('fecha').annotate(carros=Count('vehiculo_id'))
        fechas=[]
        flujo_carros=[]
        print(a)
        for valores in a:
            fechas.append((valores['fecha']).strftime("%d-%b"))
            flujo_carros.append(valores['carros'])
        dates_json = json.dumps(list(fechas), cls=DjangoJSONEncoder) # las fechas pasa en json

        context.update({'dates_json': dates_json})  #agrega los datos de fechas como un arreglo independiente
        context.update({'carros': flujo_carros})    #agrega los datos de carros en un arreglo de forma independiente
        print(fechas)
        print(flujo_carros)
        return context

    def get_queryset(self):
        result= super(VehiculoChart, self).get_queryset()
        a = Vehiculo.objects.filter().select_related()
        print(a)
        return result

class VehiculoList(ListView):
    model         = Flujo_vehicular
    template_name = 'vehiculo/consult.html'
    paginate_by   = 10

    def get_context_data(self, *args,**kwargs):
        context = super(VehiculoList, self).get_context_data(**kwargs)

        fecha_actual=datetime.datetime.now().strftime('%d/%b/%Y')
        busqueda = self.get_queryset()
        context.update({'fecha_actual': fecha_actual})
        context.update({'busqueda': busqueda})
        print("ALGO")
        print(context)
        print("contexto")
        return context

    def get_queryset(self):
        result= super(VehiculoList, self).get_queryset()
        # query = self.request.GET.get['plate']

        fecha_actual=datetime.datetime.now()
        datesince       = self.request.GET.get('datesince')
        datefrom        = self.request.GET.get('datefrom')
        caracteristica  = self.request.GET.get('caracteristica')


        # plate = 'GOU0065'
        print("aqui toma el dato del template")
        print(datesince)
        print(datefrom)
        print(caracteristica)
        print("supuestamente mostro algo")
        # a = Flujo_vehicular.objects.all()
        # a = Vehiculo.objects.values('id','placa','caracteristica__marca','caracteristica__modelo','caracteristica__color','caracteristica__servicio','fecha','horacaptura','camara').filter(fecha__lte=fecha_actual).order_by('fecha')

        if caracteristica:
             # query_list = query.split()
             # b = Flujo_vehicular.objects.filter(vehiculo__placa__icontains=caracteristica)
             result= Flujo_vehicular.objects.filter(Q(vehiculo__placa__icontains=caracteristica) | Q(vehiculo__marca__icontains=caracteristica) | Q(vehiculo__modelo__icontains=caracteristica))

             # User.objects.filter(userprofile__level__gte=0)
             # result = result.filter(reduce(Vehiculo(fecha__gte=datesince,fecha__lte=datefrom)))
             # result = Vehiculo.objects.filter(fecha__range=[datesince,datefrom])
        # elif plate:
            # result = Vehiculo.objects.filter(placa__contains=plate)

        print(result)
        return result

class VehiculoDenunciar(DeleteView):
      model = Vehiculo
      template_name = 'vehiculo/vehiculo_reportar.html'
      success_url = reverse_lazy('consultar')

      # def get_context_data(self, *args, **kwargs):
      #     context = super (VehiculoDenunciar, self).get_context_data(**kwargs)
      #
      #     coment=self.request.GET.post('comentario')
      #     print(coment)
      #     context['comentario']=coment
      #     return HttpResponseRedirect(self.get_success_url())


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
        print("ALGO")
        print(context)
        print("contexto")
        return context

    def get_queryset(self):
        result= super(VehiculoReportadoList, self).get_queryset()
        caracteristica  = self.request.GET.get('caracteristica')

        print(caracteristica)
        print("supuestamente mostro algo")
        if caracteristica:
             result= Lista_negra_vehiculos.objects.filter(Q(vehiculo__placa__icontains=caracteristica) | Q(vehiculo__marca__icontains=caracteristica) | Q(vehiculo__modelo__icontains=caracteristica))

        print(result)
        return result
