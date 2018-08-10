from django import forms
from apps.adopcion.models import Persona, Solicitud

class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiulo


        fields = [
        'propietario',
        'placa',
        'fecha',
        'horacaptura',
        'camara',

        ]
        labels = {
            'nombre'          : 'Nombre',
            'apellido'        : 'Apellido',
            'edad'            : 'Edad',
            'telefono'        : 'Telefono',
            'email'           : 'Correo Electronico',

        }

        widgets = {
            'propietario'     : forms.TextInput(attrs={'class':'form-control'}),
            'placa'           : forms.TextInput(attrs={'class':'form-control'}),
            'fecha'           : forms.TextInput(attrs={'class':'form-control'}),
            'horacaptura'     : forms.TextInput(attrs={'class':'form-control'}),
            'camara'          : forms.TextInput(attrs={'class':'form-control'}),

        }

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud


        fields = [
        'numero_mascota',
        'razones',
        ]
        labels = {
            'numero_mascota' : 'Numero de mascotas',
            'razones'        : 'Razones para adoptar',
        }

        widgets = {
            'numero_mascota' : forms.TextInput(attrs={'class':'form-control'}),
            'razones'         : forms.Textarea(attrs={'class':'form-control'}),
        }



from django import forms
from vehiculo.models import Vehiculo, Caracteristica

class SearchForm(forms.Form):

    class Meta:
        model = Persona


        fields = [
        'nombre',
        'apellido',
        'edad',
        'telefono',
        'email',

        ]
        labels = {
            'nombre'          : 'Nombre',
            'apellido'        : 'Apellido',
            'edad'            : 'Edad',
            'telefono'        : 'Telefono',
            'email'           : 'Correo Electronico',

        }

        widgets = {
            'placa'          : forms.TextInput(attrs={'class':'form-control'}),
            'modelo'         : forms.TextInput(attrs={'class':'form-control'}),
            'marca'          : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_desde'    : forms.TextInput(attrs={'class':'form-control'}),
            'fecha_hasta'    : forms.TextInput(attrs={'class':'form-control'}),
            'hora_desde'    : forms.TextInput(attrs={'class':'form-control'}),
            'hora_desde'    : forms.TextInput(attrs={'class':'form-control'}),

        }


    placa       = forms.CharField(required=False)
    modelo      = forms.CharField(required=False)
    marca       = forms.CharField(required=False)
    fecha_desde = forms.CharField(required=False)
    fecha_hasta = forms.CharField(required=False)
    hora_desde  = forms.CharField(required=False)
    hora_hasta  = forms.CharField(required=False)
