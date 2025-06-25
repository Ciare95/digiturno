---
trigger: manual
---

# Guía de estilo para Python (PEP 8) + Principios de diseño

## ✨ PEP 8 - Estándares de estilo Python

Todo el código Python del proyecto debe seguir las convenciones del estilo **PEP 8** para garantizar:
- ✅ Legibilidad
- ✅ Mantenibilidad
- ✅ Coherencia

Recomendaciones clave:
- Usa `snake_case` para nombres de funciones y variables.
- Usa `CamelCase` para clases.
- Limita las líneas a 79 caracteres.
- Usa 4 espacios por nivel de indentación.
- Comenta con claridad y usa docstrings en funciones y clases.

---

## 🧠 Principio SOLID: Responsabilidad Única (S)

> “Una clase debe tener una única razón para cambiar.”

Esto significa que:
- Cada clase debe encargarse de **una sola tarea** dentro del sistema.
- Evita mezclar responsabilidades, por ejemplo, lógica de base de datos con lógica de validación.

**Ejemplo bueno**:
```python
# Clase con una única responsabilidad: manejar libros
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor