# Paleta de Colores del Sistema

Este documento describe la paleta de colores utilizada en toda la aplicación y cómo modificarla.

## Colores Principales

La aplicación utiliza una paleta de 4 colores principales:

- **#22D3EE** - Cyan brillante (Primary)
  - Uso: Botones principales, enlaces, elementos de acción
  
- **#63B3ED** - Azul cielo (Primary Dark)
  - Uso: Hovers, estados secundarios, elementos destacados
  
- **#1F2937** - Gris oscuro (Dark)
  - Uso: Textos principales, fondos oscuros, navegación
  
- **#DBF9FA** - Cyan muy claro (Light Accent)
  - Uso: Fondos de secciones, destacados suaves, estados activos

## Ubicación de los Colores

Los colores están definidos en dos lugares principales:

### 1. CSS Variables (`static/css/colors.css`)
```css
:root {
    --color-primary: #22D3EE;
    --color-primary-dark: #63B3ED;
    --color-dark: #1F2937;
    --color-light: #DBF9FA;
}
```

### 2. Configuración de Tailwind (`templates/base.html`)
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'primary': '#22D3EE',
                'primary-dark': '#63B3ED',
                'dark': '#1F2937',
                'light-accent': '#DBF9FA',
            }
        }
    }
}
```

## Cómo Modificar los Colores

Para cambiar la paleta de colores en toda la aplicación:

1. **Editar `static/css/colors.css`**: Cambiar los valores en `:root`
2. **Editar `templates/base.html`**: Actualizar la configuración de Tailwind
3. **Buscar y reemplazar**: Si hay colores hardcodeados, buscar con:
   - `#22D3EE`, `#63B3ED`, `#1F2937`, `#DBF9FA`
   - `bg-[#22D3EE]`, `text-[#22D3EE]`, etc.

## Uso en Templates

### Botones Principales
```html
<button class="bg-gradient-to-r from-[#22D3EE] to-[#63B3ED] hover:from-[#63B3ED] hover:to-[#22D3EE] text-white">
    Acción
</button>
```

### Textos y Enlaces
```html
<a href="#" class="text-[#22D3EE] hover:text-[#63B3ED]">Enlace</a>
```

### Fondos
```html
<div class="bg-[#DBF9FA]">Contenido</div>
```

### Navegación
```html
<nav class="bg-[#1F2937] text-white">
    Navegación
</nav>
```

## Colores de Estado

Además de los colores principales, se utilizan colores estándar para estados:

- **Éxito**: Verde (#10B981)
- **Advertencia**: Amarillo (#F59E0B)
- **Error**: Rojo (#EF4444)
- **Información**: Azul (#3B82F6)

Estos colores se mantienen independientes de la paleta principal para mantener la consistencia semántica.
