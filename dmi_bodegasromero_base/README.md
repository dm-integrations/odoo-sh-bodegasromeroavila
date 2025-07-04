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

[17.0.1.3] - 2024-11-13

    Creamos una actividad al usuario Ana (id=2) cada vez que se cree un nuevo cliente de tipo compañia, para que revise los datos
    Traduccion del boton de actividades a Recordatorios
    Añadimos dependencias de módulo de cupones y fidelidad (sale_loyalty) 
    Personalizamos la funcionalidad para poder asignar tarjeta de fidelidad a los clientes y poder gestionar las promociones personlizadas
    Añadimos control de promociones a nivel de cliente, para compobrar si ese cliente cumple con las condiciones de la promocion
    Añadimos la linea de promocion en verde para que resalte la linea con la promocion aplicada.
    Al confirmar el pedido comprobamos si hay que aplicar promocion y si hay que hacerlo se aplica

[17.0.1.4] - 2024-12-20

    En campo cliente vinculado no dejar crear en caliente
    Añadir al cliente vinculado solo clientes a los que tengan acceso el comercial que lo crea 
    (O que sea el comercial o que sea el usuario seguidor)
    Campo fuente contacto que sea requerido, las fuentes solo se pueden crear desde su menu de configuracion. 
    Etiquetas de contacto ordenar por secuencia en vez de por nombre

[17.0.1.4] - 2024-12-20

    El campo fuente lo hacemos requerido en los contactos
    Añadimos el campo fuente en la vista de lista de contactos
    Quitamos el campo fuente antiguo de la vista de oportunidades (el de tipo texto)

[17.0.1.5] - 2025-02-04

    Cambiar literal de cliente vinculado a contacto vinculado
    Si en la tarea la fecha limite se pasa, crear una actividad recordando a la persona que la tiene asignada
    En las listas de precios añadir check no_mostrar_listado para marcar tarifas de un unico cliente y no mostrarlas en el many2many de tarifas en contacto
    Pedir la fuente solo para contactos de tipo compañia o que no tenga un parent_id asociado
    Sincronizar las tareas de un proyecto en el calendario general si tiene inicio y fin

[17.0.1.6] - 2025-02-24

    Hacemos requerido el campo country_id de res_partner

[17.0.1.7] - 2025-03-03

    Por defecto el campo l10n_es_edi_facturae_checkbox_xml se pone a False en el wizard para el envio de facturas por email

[17.0.1.8] - 2025-03-03

    Modificamos la vista de los leads. Ya que al activar la opcion de crear leads, el campo fuente no aparece en la vista y es obligatorio
    Hacemos obligatorio el campo motivo de perdida al perder una oportunidad

[17.0.1.9] - 2025-04-09

    añadimos un campo de grados en facturas y ventas, que multiplica el numero introducio por la cantidad, lo que afecta a los precios
    Hacemos el campo name de los empaquetados traducible

[17.0.1.10] - 2025-04-09

    Hacemos que el campo email del contacto solo sea obligatorio para las compañias o usuarios sin parent_id

[17.0.1.11] - 2025-04-23

    Modificamos los calculos de la factura para que el campo de grados afecte al precio total cant * grados / 100
    Al registrar los pagos evitamos el control del VAT para que no salte la restriccion

[17.0.1.12] - 2025-04-30

    Ocultamos en el website el Powered by Odoo que se encuentra en la vista frontend_layout, ocultando el valor ya que
    muchas las vistas la heredan y da error si lo reemplazamos

[17.0.1.13] - 2025-05-14

    Añadimos en los contactos un método para poder archivar los contactos dentro de una compañía cuando se archive la compañia
    

[17.0.1.14] - 2025-06-30

    Actualice el código de campo dmi_grados, agregue el campo dmi_alcohol_grados_discount a la venta y la cuenta, y anule el método _convert_to_tax_line_dict para administrar el cálculo de impuestos
    

[17.0.1.14] - 2025-06-30
    Actualizar los métodos de impuestos.