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
 
[17.0.1.1] - 2024-10-2

    Añadimos campos personalizados en el modelo de crm.lead 
    Añadimos campos personalizados en el modelo de res.partner
    Extendemos la vista de crm.lead para añadir los campos personalizados y un atajo en el buscador
    Extendemos la vista de res.partner para añadir los campos personalizados y modificamos la vista para reorganizad la visual


[17.0.1.2] - 2024-11-12

    Añadimos campos personalizados en el modelo de crm.lead 
    Añadimos campos personalizados en el modelo de res.partner
    Añadimos minuatura de imagen del producto en las lineas de pedido a nivel de formulario
    Extendemos la vista de crm.lead para añadir los campos personalizados y un atajo en el buscador
    Extendemos la vista de res.partner para añadir los campos personalizados y modificamos la vista para reorganizad la visual
    Creamos modelo crm.lead.fuente para indicar por que fuente entra un cliente u oportunidad