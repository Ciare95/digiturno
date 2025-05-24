#!/usr/bin/env python
"""Utilidad de línea de comandos de Django para tareas administrativas."""
import os
import sys


def ejecutar_tareas_administrativas():
    """Ejecutar tareas administrativas principales."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiturno.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Error de importación: ¿Está instalado Django y disponible en su "
            "variable de entorno PYTHONPATH? ¿Activó el entorno virtual?"
        ) from exc
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    ejecutar_tareas_administrativas()
