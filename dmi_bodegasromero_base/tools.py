# -*- coding: utf-8 -*-
import re


def strip_size_suffix(name):
    """
    Elimina los sufijos de talla habituales (S, M, L, XL, talla 42, (M), - L, / XS, etc.)
    del final del nombre de un producto, CONSERVANDO el formato/mayúsculas original.
    Se usa para mostrar el título limpio en la tienda web.
    """
    if not name:
        return ""
    name = name.strip()

    # Soportamos números de 1 o 2 dígitos para tallas de vestir (38, 40, etc.) sin de-duplicar años como "2024"
    size_terms = r'xs|s|m|l|xl|xxl|xxxl|pequeño|pequeña|mediano|mediana|grande|grandes|talla\s*\d+|talla\s*[a-zA-Z]+|\d{1,2}'

    # 1. Paréntesis con talla o número: " (s)", " (m)", " (l)", " (xl)", " (42)", " (talla s)"
    name = re.sub(rf'\s*\((talla\s+)?({size_terms})\)\s*$', '', name, flags=re.IGNORECASE)

    # 2. Guión, barra o coma con talla o número: " - s", " - m", " / s", " , s"
    name = re.sub(rf'\s*[\-/,]\s*(talla\s+)?({size_terms})\s*$', '', name, flags=re.IGNORECASE)

    # 3. Talla de texto explícita: "talla s", "talla m", "talla 42"
    name = re.sub(rf'\s+talla\s*({size_terms})\s*$', '', name, flags=re.IGNORECASE)

    # 4. Talla suelta al final precedida por un espacio (letras individuales o palabras comunes)
    name = re.sub(rf'\s+(xs|s|m|l|xl|xxl|xxxl|pequeño|pequeña|mediano|mediana|grande|grandes)\s*$', '', name, flags=re.IGNORECASE)

    return name.strip()


def clean_product_name(name):
    """
    Normaliza el nombre de un producto (minúsculas + sin sufijos de talla) para poder
    agrupar variantes o plantillas que representan el mismo artículo en la tienda web.
    """
    if not name:
        return ""
    return strip_size_suffix(name).strip().lower()
