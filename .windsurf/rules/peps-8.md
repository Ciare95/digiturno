---
trigger: manual
---

Todo el código Python del proyecto debe seguir las convenciones del estilo PEP 8 para garantizar legibilidad, mantenibilidad y coherencia, además debes tener en cuenta el primer principio de los principios SOLID que es El Principio de responsabilidad única (Single Responsibility Principle).

El Principio de Responsabilidad Única dice que una clase debe hacer una cosa y, por lo tanto, debe tener una sola razón para cambiar.

Para enunciar este principio más técnicamente: Solo un cambio potencial (lógica de base de datos, lógica de registro, etc.) en la especificación del software debería poder afectar la especificación de la clase.

Esto significa que si una clase es un contenedor de datos, como una clase Libro o una clase Estudiante, y tiene algunos campos relacionados con esa entidad, debería cambiar solo cuando cambiamos el modelo de datos.
Aplica tambien el principio DRY (Dont Repeat Yourself) al código