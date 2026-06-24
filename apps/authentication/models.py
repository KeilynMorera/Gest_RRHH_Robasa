from django.db import models
from django.db.models import Sum
from datetime import datetime, date, timedelta, time



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
    Carrera              = models.CharField(max_length=100, default="Sin especificar")
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
# Solo lectura — los datos vienen definidos en la BD.
# No se registran desde el sistema.
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
# Solo lectura — los datos vienen definidos en la BD.
# No se registran desde el sistema.
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


# =========================================================
# CANDIDATO DE LA VACANTE
# =========================================================
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



# =========================================================
# SOLICITUD DE VACACIONES
# =========================================================
class VacacionSolicitud(models.Model):

    idSolicitud = models.AutoField(
        primary_key=True
    )

    Fecha_Solicitud = models.DateField()

    Fecha_Inicio = models.DateField()

    Fecha_Fin = models.DateField()

    Dias_Solicitud = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    id_Estatus_Vacante = models.ForeignKey(
        Estatus,
        on_delete=models.PROTECT,
        db_column='id_Estatus_Vacante',
        related_name='solicitudes_vacaciones'
    )

    idEmpleado_Sol_Vac = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        db_column='idEmpleado_Sol_Vac',
        related_name='vacaciones_solicitadas'
    )

    idEmpleado_Respon = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        db_column='idEmpleado_Respon',
        related_name='vacaciones_aprobadas'
    )

    class Meta:
        managed = False
        db_table = 'Vacacion_Solicitud'

    def __str__(self):
        return f"Solicitud #{self.idSolicitud}"



# =========================================================
# CONSULTAR SALDO DE VACACIONES
# =========================================================
class VacacionSaldo(models.Model):

    idSaldo = models.AutoField(primary_key=True)

    Anio = models.IntegerField()

    Dias_Acumulados = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    Dias_Tomado = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    Dias_Disponibles = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    idEmpleado_Sal_Vac = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        db_column='idEmpleado_Sal_Vac',
        related_name='saldo_vacaciones'
    )

    class Meta:
        db_table = 'Vacacion_Saldo'

    def __str__(self):
        return f"{self.idEmpleado_Sal_Vac} - {self.Anio}"
    


    def calcular_dias_acumulados(self):

        fecha_ingreso = self.idEmpleado_Sal_Vac.Fecha_Ingreso

        hoy = date.today()

        anios = hoy.year - fecha_ingreso.year

        if anios < 1:
            return 0

        elif anios == 1:
            return 12

        elif anios == 2:
            return 14

        elif anios == 3:
            return 16

        elif anios == 4:
            return 18

        else:
            return 20
        

    def calcular_dias_tomados(self):

        total = VacacionSolicitud.objects.filter(

            idEmpleado_Sol_Vac=self.idEmpleado_Sal_Vac,

            Fecha_Inicio__year=self.Anio,

            id_Estatus_Vacante__TipoEstatus__iexact="Aprobada"

        ).aggregate(

            total=Sum('Dias_Solicitud')

        )

        return total['total'] or 0
    

    def save(self, *args, **kwargs):

        self.Dias_Acumulados = self.calcular_dias_acumulados()

        self.Dias_Tomado = self.calcular_dias_tomados()

        self.Dias_Disponibles = (
            self.Dias_Acumulados -
            self.Dias_Tomado
        )

        super().save(*args, **kwargs)




# =========================================================
# ESTADO DE ASISTENCIA
# =========================================================
class AsistenciaEstado(models.Model):

    idAsis_Estado = models.AutoField(
        primary_key=True
    )

    TipoEstado = models.CharField(
        max_length=20
    )

    class Meta:
        db_table = 'Asistencia_Estado'

    def __str__(self):

        return self.TipoEstado


# =========================================================
# ASISTENCIA
# =========================================================
class Asistencia(models.Model):

    idAsistencia = models.AutoField(
        primary_key=True
    )

    Fecha = models.DateField()

    Hora_Entrada = models.TimeField()

    Hora_Salida = models.TimeField()

    Horas_Extra = models.TimeField(
        null=True,
        blank=True
    )

    idAsis_Estado = models.ForeignKey(
        AsistenciaEstado,
        on_delete=models.PROTECT,
        db_column='idAsis_Estado',
        related_name='asistencias'
    )

    idEmpleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        db_column='idEmpleado',
        related_name='asistencias'
    )

    class Meta:

        db_table = 'Asistencia'

        ordering = ['-Fecha']

    def __str__(self):

        return f"{self.idEmpleado} - {self.Fecha}"


    # =====================================================
    # CALCULAR HORAS EXTRA
    # Jornada laboral = 8 horas
    # =====================================================

    def calcular_horas_extra(self):

        entrada  = datetime.combine(date.today(), self.Hora_Entrada)
        salida   = datetime.combine(date.today(), self.Hora_Salida)
        jornada  = timedelta(hours=8)
        trabajado = salida - entrada
        extra    = trabajado - jornada

        if extra.total_seconds() <= 0:
            return time(0, 0, 0)   # ← time en lugar de int 0

        total_seg = int(extra.total_seconds())
        horas     = total_seg // 3600
        minutos   = (total_seg % 3600) // 60
        return time(horas, minutos, 0)   # ← time en lugar de int


    # =====================================================
    # GUARDAR
    # =====================================================

    def save(self, *args, **kwargs):

        self.Horas_Extra = self.calcular_horas_extra()

        super().save(*args, **kwargs)


# =========================================================
# TABLA: TipoPermiso
# Catálogo de tipos de permisos
# =========================================================
class TipoPermiso(models.Model):

    id_TipoPermiso = models.AutoField(
        primary_key=True,
        db_column='id_TipoPermiso'
    )

    Tipo_Permiso = models.CharField(
        max_length=80,
        db_column='Tipo_Permiso'
    )

    class Meta:

        managed = False

        db_table = 'TipoPermiso'

    def __str__(self):

        return self.Tipo_Permiso
    

# =========================================================
# TABLA: Permiso
# Justificación o permiso asociado a una asistencia
# =========================================================
class Permiso(models.Model):

    idPermiso = models.AutoField(
        primary_key=True,
        db_column='idPermiso'
    )

    Activo = models.BooleanField(
        default=True,
        db_column='Activo'
    )

    Justificacion = models.CharField(
        max_length=5000,
        db_column='Justificacion'
    )

    id_TipoPermiso = models.ForeignKey(

        TipoPermiso,

        on_delete=models.CASCADE,

        db_column='id_TipoPermiso',

        related_name='permisos'
    )

    idAsistencia = models.ForeignKey(

        Asistencia,

        on_delete=models.CASCADE,

        db_column='idAsistencia',

        related_name='permisos_asistencia'
    )

    idEmpleado = models.ForeignKey(

        Empleado,

        on_delete=models.CASCADE,

        db_column='idEmpleado',

        related_name='permisos_empleado'
    )

    class Meta:

        managed = False

        db_table = 'Permiso'

    def __str__(self):

        return f"{self.idEmpleado} - {self.id_TipoPermiso}"
    


# =========================================================
# TABLA: Accion_Personal (Cabecera)
# =========================================================
class AccionPersonal(models.Model):
    idAccion = models.AutoField(
        primary_key=True, 
        db_column='idAccion'
    )
    Fecha = models.DateField(
        db_column='Fecha'
    )
    # Llave foránea directa al Empleado
    idEmpleado = models.ForeignKey(
        'Empleado',  # Cambiar por Empleado si está en el mismo archivo
        on_delete=models.CASCADE,
        db_column='idEmpleado',
        related_name='acciones_personal'
    )

    class Meta:
        managed = False  # Cambiar a True si quieres que Django controle las migraciones
        db_table = 'Accion_Personal'
        ordering = ['-Fecha']

    def __str__(self):
        return f"Folio: {self.idAccion} - Empleado: {self.idEmpleado_id} ({self.Fecha})"
    

# =========================================================
# TABLA: Detalle_Accion (Catálogo de Tipos de Acciones)
# =========================================================
class DetalleAccion(models.Model):
    id_Detalle_Accion = models.AutoField(
        primary_key=True, 
        db_column='id_Detalle_Accion'
    )
    Accion = models.CharField(
        max_length=80, 
        db_column='Accion'
    )

    class Meta:
        managed = False
        db_table = 'Detalle_Accion'

    def __str__(self):
        return self.Accion


# =========================================================
# TABLA: Accion_Tipo (Detalle del Movimiento)
# =========================================================
class AccionTipo(models.Model):
    idAccion_Tipo = models.AutoField(
        primary_key=True, 
        db_column='idAccion_Tipo'
    )
    Detalle = models.CharField(
        max_length=600, 
        db_column='Detalle'
    )
    # NUEVA COLUMNA: Aquí guardaremos el monto personalizado (Premio, Ajuste, Ascenso) o 0.00
    monto_ta = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        db_column='Monto_TA'
    )
    
    # RELACIONES (Foreign Keys)
    id_Detalle_Accion = models.ForeignKey(
        'DetalleAccion', 
        on_delete=models.PROTECT, 
        db_column='id_Detalle_Accion'
    )
    idAccion = models.ForeignKey(
        'AccionPersonal', 
        on_delete=models.CASCADE, 
        db_column='idAccion'
    )
    idSalarioEmpleado = models.ForeignKey(
        'SalarioEmpleado', 
        on_delete=models.PROTECT, 
        db_column='idSalarioEmpleado'
    )

    class Meta:
        managed = False  # Mantiene el control sobre tu tabla existente en SQL Server
        db_table = 'Accion_Tipo'

    def __str__(self):
        return f"Movimiento {self.idAccion_Tipo} - {self.id_Detalle_Accion.Accion} (₡{self.monto_ta})"