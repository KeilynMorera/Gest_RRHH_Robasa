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
    


# =========================================================
# TABLA: Salario_Empleado
# =========================================================
class SalarioEmpleado(models.Model):

    idSalarioEmpleado = models.AutoField(
        primary_key=True
    )

    Fecha_Inicio = models.DateField()

    Fecha_Fin = models.DateField(
        null=True,
        blank=True
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

    Compensacion_Total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )

    Observaciones = models.CharField(
        max_length=5000,
        null=True,
        blank=True
    )

    idEmpleado = models.ForeignKey(
        'Empleado',
        on_delete=models.CASCADE,
        db_column='idEmpleado',
        related_name='salarios'
    )

    class Meta:
        db_table = 'Salario_Empleado'
        verbose_name = 'Salario Empleado'
        verbose_name_plural = 'Salarios Empleados'

    # ✅ CORRECTO — calcula Compensacion_Total antes de guardar
    def save(self, *args, **kwargs):
        self.Compensacion_Total = (
            (self.Salario_Bruto     or 0) +
            (self.Comision_Base     or 0) +
            (self.Variable_Base     or 0) +
            (self.Viaticos_Alimenticios or 0) +
            (self.Kilometraje_Base  or 0) +
            (self.Bono_Base         or 0)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.idEmpleado.idPersona.Nombre_Completo} "
            f"- {self.Compensacion_Total}"
        )



# =========================================================
# Tabla: Estatus
# Registro estatus de la vacante
# =========================================================
class Estatus(models.Model):

    id_Estatus_Vacante = models.AutoField(
        primary_key=True,
        db_column='id_Estatus_Vacante'
    )

    TipoEstatus = models.CharField(
        max_length=20
    )

    class Meta:
        db_table = 'Estatus'
        verbose_name = 'Estatus'
        verbose_name_plural = 'Estatus'

    def __str__(self):
        return self.TipoEstatus


# =========================================================
# Tabla: Vacante
# Información principal de la vacante
# =========================================================
class Vacante(models.Model):

    id_Vacante = models.AutoField(
        primary_key=True,
        db_column='id_Vacante'
    )

    Fecha_Registro = models.DateField()

    TituloPublicacion = models.CharField(
        max_length=150
    )

    Motivo = models.CharField(
        max_length=200
    )

    Expe_Requerida = models.CharField(
        max_length=500
    )

    Salario_Bruto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Compensacion_Total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Cierre_Proceso = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'Vacante'


# =========================================================
# Tabla: Vacante_Asig
# Relación de la vacante con empleados y puesto
# =========================================================
class Vacante_Asig(models.Model):

    id_Vacante_Asig = models.AutoField(
        primary_key=True,
        db_column='id_Vacante_Asig'
    )

    id_Estatus_Vacante = models.ForeignKey(
        Estatus,
        on_delete=models.PROTECT,
        db_column='id_Estatus_Vacante',
        related_name='vacantes_asignadas'
    )

    id_Vacante = models.ForeignKey(
        Vacante,
        on_delete=models.CASCADE,
        db_column='id_Vacante',
        related_name='asignaciones'
    )

    idEmpleado_Aut = models.ForeignKey(
        'Empleado',
        on_delete=models.PROTECT,
        db_column='idEmpleado_Aut',
        related_name='vacantes_autorizadas'
    )

    idEmpleado_Rel_Ev = models.ForeignKey(
        'Empleado',
        on_delete=models.PROTECT,
        db_column='idEmpleado_Rel_Ev',
        related_name='vacantes_evaluador'
    )

    idEmpleado_Sus = models.ForeignKey(
        'Empleado',
        on_delete=models.PROTECT,
        db_column='idEmpleado_Sus',
        related_name='vacantes_sustitucion',
        null=True,
        blank=True
    )

    idEmpleado_Jef_Puest = models.ForeignKey(
        'Empleado',
        on_delete=models.PROTECT,
        db_column='idEmpleado_Jef_Puest',
        related_name='vacantes_jefatura'
    )

    idPuesto = models.ForeignKey(
        'Puesto',
        on_delete=models.PROTECT,
        db_column='idPuesto',
        related_name='vacantes'
    )

    class Meta:
        db_table = 'Vacante_Asig'
        verbose_name = 'Asignación de Vacante'
        verbose_name_plural = 'Asignaciones de Vacantes'

    def __str__(self):
        return f'Vacante #{self.id_Vacante_id} - {self.idPuesto}'
    


# =========================================================

# FASE DEL CANDIDATO

# =========================================================

class FaseCandidato(models.Model):
    id_Fase = models.AutoField(
        primary_key=True,
        db_column='id_Fase'
    )

    Fase_Actual = models.CharField(
        max_length=25,
        db_column='Fase_Actual'
    )

    class Meta:
        managed = False
        db_table = 'FaseCandidato'

    def __str__(self):
        return self.Fase_Actual


# =========================================================
# RESULTADO DEL PROCESO
# =========================================================

class ProcesoFase(models.Model):
    id_Proceso = models.AutoField(
        primary_key=True,
        db_column='id_Proceso'
    )

    Resultado_Av = models.CharField(
        max_length=80,
        db_column='Resultado_Av'
    )

    class Meta:
        managed = False
        db_table = 'ProcesoFase'

    def __str__(self):
        return self.Resultado_Av


class Vacante_Candidato(models.Model):

    id_Candidato = models.AutoField(primary_key=True)

    Activo = models.BooleanField(default=True)

    Observaciones = models.CharField(max_length=400)

    id_Vacante = models.ForeignKey(
        Vacante,
        db_column='id_Vacante',
        on_delete=models.CASCADE
    )

    idPersona = models.ForeignKey(
        Persona,
        db_column='idPersona',
        on_delete=models.CASCADE
    )

    id_Fase = models.ForeignKey(
        FaseCandidato,
        db_column='id_Fase',
        on_delete=models.CASCADE
    )

    id_Proceso = models.ForeignKey(
        ProcesoFase,
        db_column='id_Proceso',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "Vacante_Candidato"
        managed = False