# Import all schemas to make them available when importing from app.schemas
from app.schemas.personal import (
    PersonalCreate,
    PersonalRead,
    PersonalUpdate,
    PersonalProyectoCreate,
    PersonalProyectoRead,
)
from app.schemas.publicaciones import (
    PublicacionCreate,
    PublicacionRead,
    PublicacionUpdate,
)
from app.schemas.proyectos import (
    ProyectoCreate,
    ProyectoRead,
    ProyectoUpdate,
    ProyectoPersonalRead,
    ProyectoPersonalCreate,
)
from app.schemas.equipamiento import (
    EquipamientoCreate,
    EquipamientoRead,
    EquipamientoUpdate,
    EquipamientoActividadCreate,
    EquipamientoActividadRead,
)
from app.schemas.servicios import (
    ServicioCreate,
    ServicioRead,
    ServicioUpdate,
    ServicioEquipamientoCreate,
    ServicioEquipamientoRead,
)
from app.schemas.academico import (
    CarreraCreate,
    CarreraRead,
    CarreraUpdate,
    MateriaCreate,
    MateriaRead,
    MateriaUpdate,
    RequisitoCreate,
    RequisitoRead,
    RequisitoUpdate,
    CarreraWithMateriasRead,
    MateriaWithRelacionesRead,
)
from app.schemas.blog import (
    BlogPostCreate,
    BlogPostRead,
    BlogPostUpdate,
)
