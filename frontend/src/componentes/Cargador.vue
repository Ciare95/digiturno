<template>
  <div class="flex justify-center items-center" :class="containerClass">
    <div class="animate-spin rounded-full" :class="tamanoClase" :style="estiloColor"></div>
  </div>
</template>

<script>
export default {
  name: 'Cargador',
  props: {
    tamano: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    color: {
      type: String,
      default: 'blue'
    },
    grosor: {
      type: String,
      default: 'normal',
      validator: (value) => ['delgado', 'normal', 'grueso'].includes(value)
    },
    altura: {
      type: String,
      default: 'auto'
    }
  },
  computed: {
    tamanoClase() {
      const tamanos = {
        sm: 'h-4 w-4',
        md: 'h-8 w-8',
        lg: 'h-12 w-12',
        xl: 'h-16 w-16'
      };
      
      const grosorBorde = {
        delgado: 'border',
        normal: 'border-2',
        grueso: 'border-4'
      };
      
      return `${tamanos[this.tamano]} ${grosorBorde[this.grosor]}`;
    },
    estiloColor() {
      const colores = {
        blue: '#3B82F6',
        red: '#EF4444',
        green: '#10B981',
        yellow: '#F59E0B',
        purple: '#8B5CF6',
        gray: '#6B7280'
      };
      
      const colorSeleccionado = colores[this.color] || colores.blue;
      
      return {
        borderColor: `${colorSeleccionado} transparent transparent transparent`
      };
    },
    containerClass() {
      return this.altura !== 'auto' ? `h-${this.altura}` : '';
    }
  }
};
</script>
