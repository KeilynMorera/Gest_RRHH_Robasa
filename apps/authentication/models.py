from django.db import models

#Se definen las tablas de la base de datos

# =========================================================
# TABLA: PersonaSexo
# =========================================================
class PersonaSexo(models.Model): #Esta clase representa una tabla de la base de datos
    idSexo = models.AutoField(primary_key=True) #AutoField = entero autoincrementable
    Sexo = models.CharField(max_length=20)

    #Sirve para que Django use exactamente ese nombre de tabla en SQL Server.
    class Meta:
        db_table = 'PersonaSexo'

    def __str__(self):
        return self.Sexo
    
# =========================================================
# TABLA: Persona
# =========================================================
class Persona(models.Model):

    idPersona = models.AutoField(primary_key=True)
    Nombre_Completo = models.CharField(max_length=200)
    Cedula = models.CharField(max_length=20)
    Fecha_Nacimiento = models.DateField()
    Telefono = models.CharField(max_length=20)
    Celular = models.CharField(max_length=20)
    Correo = models.EmailField(max_length=200)
    Direccion = models.CharField(max_length=400)

    # Para guardar imágenes/fotos
    Foto = models.ImageField(
        upload_to='fotos_personas/',
        null=True,
        blank=True
    )

    # Foreign Key hacia PersonaSexo
    idSexo = models.ForeignKey(
        PersonaSexo,
        on_delete=models.CASCADE, #Si eliminas un sexo, también se eliminan las personas relacionadas.
        db_column='idSexo'
    )

    class Meta:
        db_table = 'Persona'

    def __str__(self):
        return self.Nombre

