# DMI Contact Access

En este módulo limitamos la visualizacion de contactos a determinados usuarios.

## Tabla de Contenidos

1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Configuración](#configuración)    
5. [Changelog](#changelog) 

## Descripción

Este módulo **[DMI Contact Access]** proporciona la siguiente funcionalidad:
En este módulo limitamos la visualizacion de contactos a los usuarios del grupo Commercial Own User y Deny All Partners.
Los usuario del grupo Commercial Own User podran ver todos los contactos en los que este como comercial, 
mientras que los usuarios del grupo Deny All Partners no podrán ver ningún contacto.
- Los usuarios del grupo Commercial Own User podran ver todos los contactos en los que este como comercial.
- Los usuarios del grupo Commercial All User podran ver todos los contactos.
- Por defecto si no se selecciona ningún grupo de los anteriores al usuario se le asignara el grupo Deny All Partners, y no podrá ver ningún contacto.



## Requisitos

- Odoo versión 17
- Otros módulos dependientes, si los hay:
  - `base`
  - `contacts`
  - `sale_management` 

## Instalación

Instalación del módulo en el sistema.


## Configuración

Es necesario revisar la configuración de los grupos asignados a cada usuario.


## Changelog
 
[17.0.1.1.0] - 2024-09-30

    Primera versión del módulo.
    Ocultamos en los contactos que no sean del comercial a usuarios del grupo Commercial Own User.
    

[17.0.1.1.1] - 2024-10-2

    Revisamos las reglas de registro de los contactos, debido a fallos al intentar a acceder a contactos propios del 
    sistema que son necesario para el acceso y manejo de determinados datos en algunos modelos. 
    Filtramos los contactos por el comercial asignado a cada contacto, y ademas si este pertenece al usuario conectado.
    

[17.0.1.1.2] - 2024-10-11

    Ampliamos la regla de registro para permitir a un usuario asignar seguidores de otros usuarios. 
    Odoo para asignar seguidores utilizad el contacto del usuario en cuestión. Debido a que estos contactos no 
    tiene asociados a los compañeros de trabajo, no se podía asignar seguidores a los contactos.
    Se amplia el filtro para permitir a los usuarios asignar seguidores a los contactos que no son suyos, 
    pero pertenecen o tienen asignados usuarios internos del sistema.

    

[17.0.1.1.3] - 2024-11-12

    - Añadimos control de permisos de ventas para solo mostrar aquellas pedido de clientes deonde se esta como seguidor o comercial
    - Permitimos ver contactos a usuario del grupo Commercial Own user si estan como seguidores

