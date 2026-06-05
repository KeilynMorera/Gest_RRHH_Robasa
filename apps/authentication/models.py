from django.db import models



    

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

    id_Departamento = models.AutoField(
        primary_key=True,
        db_column='id_Depertamento'
    )

    Nombre = models.CharField(max_length=150)

    idGerencia = models.ForeignKey(
        Gerencia,
        on_delete=models.CASCADE,
        db_column='idGerencia'
    )

    class Meta:
        db_table = 'Departamento'

    def __str__(self):
        return self.Nombre



# =========================================================
# MODELO: Puesto
# Catálogo de puestos de la organización
# =========================================================
class Puesto(models.Model):

    idPuesto = models.AutoField(
        primary_key=True
    )

    Nombre = models.CharField(
        max_length=150
    )

    Descripcion = models.CharField(
        max_length=400
    )

    idDepartamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        db_column='id_Depertamento'
    )

    class Meta:
        db_table = 'Puesto'
        

    def __str__(self):
        return self.Nombre
    

# =========================================================
# MODELO: Compensacion_Puesto
# Historial de compensaciones por puesto
# =========================================================
class Compensacion_Puesto(models.Model):

    idCompensacion = models.AutoField(
        primary_key=True
    )

    Salario_Bruto = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    Salario_Sem_Neto = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    Comision_Base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Variable_Base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Viaticos_Alimenticios = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Kilometraje_Base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Bono_Base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Vigencia = models.DateField()

    idPuesto = models.ForeignKey(
        Puesto,
        on_delete=models.CASCADE,
        db_column='idPuesto'
    )

    class Meta:

        db_table = 'Compensacion_Puesto'

        ordering = ['-Vigencia']

        constraints = [

            models.UniqueConstraint(
                fields=[
                    'idPuesto',
                    'Vigencia'
                ],
                name='uq_puesto_vigencia'
            )

        ]

    def __str__(self):

        return (
            f'{self.idPuesto.Nombre}'
            f' - {self.Vigencia}'
        )



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
# TABLA: Contrato
# Solo lectura — los datos vienen definidos en la BD.
# No se registran desde el sistema.
# =========================================================
class Contrato(models.Model):

    idContrato    = models.AutoField(primary_key=True)
    Tipo_Contrato = models.CharField(max_length=50)   # VARCHAR(50) en SQL

    class Meta:
        db_table = 'Contrato'
        managed  = False   # Django no toca esta tabla (no crea ni altera)
        

    def __str__(self):
        return self.Tipo_Contrato


# =========================================================
# TABLA: Empleado
# =========================================================
class Empleado(models.Model):

    idEmpleado    = models.AutoField(primary_key=True)
    Fecha_Ingreso = models.DateField()
    Activo        = models.BooleanField(default=True)  # BIT: True=1 Activo, False=0 Inactivo

    idContrato    = models.ForeignKey(
                        Contrato,
                        on_delete=models.CASCADE,
                        db_column='idContrato'
                    )
    idPersona     = models.ForeignKey(
                        Persona,
                        on_delete=models.CASCADE,
                        db_column='idPersona'
                    )
    idPuesto      = models.ForeignKey(
                        Puesto,
                        on_delete=models.CASCADE,
                        db_column='idPuesto'
                    )

    class Meta:
        db_table = 'Empleado'

    def __str__(self):
        return f"{self.idPersona.Nombre_Completo} — {self.idPuesto.Nombre}"
    


# =========================================================
# TABLA: Pasante
# =========================================================
class Pasante(models.Model):

    idPasante            = models.AutoField(primary_key=True)
    Fecha_Inicio         = models.DateField()
    Fecha_Fin            = models.DateField(null=True, blank=True)  # NULL permitido
    Univercidad          = models.CharField(max_length=200)
    Carrera              = models.CharField(max_length=200)
    Tutor_Univercitario  = models.CharField(max_length=200)
    Activo               = models.BooleanField(default=True)  # BIT: True=1 Activo, False=0 Inactivo

    idPersona            = models.ForeignKey(
                               Persona,
                               on_delete=models.CASCADE,
                               db_column='idPersona'
                           )
    idPuesto             = models.ForeignKey(
                               Puesto,
                               on_delete=models.CASCADE,
                               db_column='idPuesto'
                           )
    idEmpleado_Sup       = models.ForeignKey(
                               Empleado,
                               on_delete=models.CASCADE,
                               db_column='idEmpleado_Sup',
                               related_name='pasantes_supervisados'
                           )

    class Meta:
        db_table = 'Pasante'

    def __str__(self):
        return f"{self.idPersona.Nombre_Completo} — {self.idPuesto.Nombre}"