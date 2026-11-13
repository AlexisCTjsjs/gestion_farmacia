# FarmaSalud — Sistema Integral de Gestión Farmacéutica (Django + MariaDB)

Sistema de gestión para farmacias, dispensación de medicamentos, control de recetas médicas, clientes y profesionales de la salud.

**Módulos del Sistema:**
- 💊 **Medicamentos y Fármacos:** Catálogo, presentación, concentración e inventario activo.
- 📋 **Recetas y Dispensación:** Emisión e impresión oficial de recetas con posología, dosis y duración.
- 👥 **Clientes y Pacientes:** Registro y consulta de titulares.
- 🐾 **Fichas de Pacientes:** Fichas de atención y seguimiento clínico.
- 👨‍⚕️ **Médicos Prescriptores:** Registro de profesionales médicos y número de colegiatura.
- 📅 **Citas y Consultas:** Agenda y estados de atención (Pendiente, Confirmada, Atendida, Cancelada).
- 🩺 **Diagnósticos Clínicos:** Cuadro sintomático y tratamientos farmacéuticos recomendados.
- 📊 **Reportes y Auditoría:** Filtros por fecha y estado con exportación/impresión en PDF.

---

## Cuentas de Acceso

El sistema cuenta con roles diferenciados:

1. **👑 Administrador:**
   - **Usuario:** `admin`
   - **Contraseña:** (La que configuraste con `createsuperuser`)
   - **Permisos:** Acceso completo al sistema y al panel Django Admin (`/admin/`).

2. **🧑‍💼 Empleado de Farmacia:**
   - **Usuario:** `empleado`
   - **Contraseña:** `empleado123`
   - **Permisos:** Operación y gestión en el portal web (`/login/`).

---

## Ejecución del Proyecto

1. **Activar el entorno virtual:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Aplicar migraciones:**
   ```powershell
   python manage.py migrate
   ```

3. **Iniciar el servidor local:**
   ```powershell
   python manage.py runserver
   ```

4. **Acceder en el navegador:**
   - Portal Farmacia: `http://127.0.0.1:8000/login/`
   - Panel de Administración: `http://127.0.0.1:8000/admin/`

---

## Ejecutar Pruebas Automatizadas

```powershell
python manage.py test apps
```
