from django.db import models


# =========================================================
# TABLA: PersonaSexo
# =========================================================
class PersonaSexo(models.Model):
    idSexo = models.AutoField(primary_key=True)
    Sexo   = models.CharField(max_length=20)

    class Meta:
        db_table = 'PersonaSexo'

    def __str__(self):
        return self.Sexo


# =========================================================
# TABLA: Persona
# =========================================================
class Persona(models.Model):
    idPersona        = models.AutoField(primary_key=True)
    Nombre_Completo  = models.CharField(max_length=200)
    Cedula           = models.CharField(max_length=20)
    Fecha_Nacimiento = models.DateField()
    Telefono         = models.CharField(max_length=20)
    Celular          = models.CharField(max_length=20)
    Correo           = models.EmailField(max_length=200)
    Direccion        = models.CharField(max_length=400)
    Foto             = models.ImageField(
                           upload_to='fotos_personas/',
                           null=True,
                           blank=True
                       )
    idSexo           = models.ForeignKey(
                           PersonaSexo,
                           on_delete=models.CASCADE,
                           db_column='idSexo'
                       )

    class Meta:
        db_table = 'Persona'

    def __str__(self):
        return self.Nombre_Completo   # ← era self.Nombre (no existe ese campo)
    

# =========================================================
# TABLA: Empresas
# =========================================================
class Empresa(models.Model):
    idEmpresa = models.AutoField(primary_key=True)

    Nombre = models.CharField(max_length=150)

    Descripcion = models.TextField()

    class Meta:
        db_table = 'Empresas'

    def __str__(self):
        return self.Nombre
    

# =========================================================
# TABLA: Gerencia
# =========================================================
class Gerencia(models.Model):
    idGerencia = models.AutoField(
        primary_key=True
    )

    Nombre = models.CharField(
        max_length=150
    )

    idEmpresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE, #on_delete=models.CASCADE significa que si se elimina una empresa, también se eliminarán las gerencias asociadas a esa empresa.
        db_column='idEmpresa'
    )

    class Meta:
        db_table = 'Gerencia'

    def __str__(self):
        return self.Nombre
    

# =========================================================
# MODELO: Departamento
# Departamentos que pertenecen a una Gerencia
# =========================================================
class Departamento(models.Model):

    idDepartamento = models.AutoField(
        primary_key=True,
        db_column='id_Departamento'
    )

    Nombre = models.CharField(
        max_length=150
    )

    idGerencia = models.ForeignKey(
        'Gerencia',
        on_delete=models.CASCADE, #on_delete=models.CASCADE significa que si se elimina una gerencia, también se eliminarán los departamentos asociados a esa gerencia.
        db_column='idGerencia'
    )

    class Meta:
        db_table = 'Departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.Nombre