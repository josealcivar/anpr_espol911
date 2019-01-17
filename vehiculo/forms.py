from django import forms
from vehiculo.models import Lista_negra_vehiculos, Vehiculo

class ListaNegraForm(forms.ModelForm):

    class Meta:
        model = Lista_negra_vehiculos


        fields = [
        'comentario',
        ]
        labels = {
            'comentario'          : 'comentario',
      
        }

        widgets = {
            'comentario'     : forms.TextInput(attrs={'class':'form-control'}),

        }

class VehiculoProfile(forms.ModelForm):
    
    class Meta:
        model = Vehiculo

        fields = [
            'placa',
            'marca',
            'modelo',
            'anio_vehiculo',
            'servicio',
            
        ]
        labels={
            'placa' : 'Placa:',
            'marca' : 'Marca:',
            'modelo': 'Modelo:',
            'anio_vehiculo' : 'Año:',
            'servicio' : 'servicio:',
            
        }

        widgets = {
            'placa'         : forms.TextInput(attrs={'class':'form-control'}),
            'marca'         : forms.TextInput(attrs={'class':'form-control','disabled':'True'}),
            'modelo'        : forms.TextInput(attrs={'class':'form-control','disabled':'True'}),
            'anio_vehiculo' : forms.TextInput(attrs={'class':'form-control','disabled':'True'}),
            'servicio'      : forms.TextInput(attrs={'class':'form-control','disabled':'True'}),

        }
