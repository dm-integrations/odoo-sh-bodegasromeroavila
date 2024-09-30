# Nombre del Módulo Odoo

En este módulo limitamos la visualizacion de determinados menus, si el usuario no tiene lo permisos necesarios.
Anulamos en la plantilla de correo el añadido de Odoo de "Powered by Odoo".

## Tabla de Contenidos

1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Configuración](#configuración)    
5. [Changelog](#changelog) 

## Descripción

Este módulo **[Nombre del Módulo]** proporciona la siguiente funcionalidad:
- Limitamos el acceso a determinados menus a usuarios sin permisos especificos para acceder
- Eliminamos de la plantilla de correo mail_notification_light el añadido de Odoo "Powered by Odoo"
- ...


## Requisitos

- Odoo versión 17
- Otros módulos dependientes, si los hay:
  - `hr`
  - `mail`
  - `spreadsheet_dashboard`
  - `web`

## Instalación

Instalación del módulo en el sistema.


## Configuración

No requiere de ninguna configuración especial para su instalación.


## Changelog
 
[17.0.1.0] - 2024-09-30

    Primera versión del módulo.
    Ocultamos en las plantillas de correo, en el footer el apartado Powered by Odoo.
    Añadimos permisos superiores a los menus de Tableros, Empleados, Website para que los usuarios estandar no vean esos menus.

