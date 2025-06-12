# Análisis de Ecuaciones Diferenciales Exactas

Esta aplicación en Python, utilizando Streamlit, permite analizar y resolver ecuaciones diferenciales de la forma \(M(x, y)\,dx + N(x, y)\,dy = 0\). La aplicación verifica si la ecuación es exacta y, en caso de no serlo, intenta encontrar un factor integrante (para los Casos 1, 2 y 3) para transformarla en una ecuación exacta.

## Características

-   Verificación de exactitud de la ecuación diferencial.
-   Búsqueda de factor integrante (dependiente de x, de y, o de la forma \(x^m y^n\)).
-   Visualización de los pasos intermedios y resultados en formato LaTeX.
-   Interfaz web interactiva para introducir las ecuaciones.

## Requisitos

Asegúrate de tener Python 3.8 o superior instalado.

## Instalación

1.  Clona este repositorio (si no lo has hecho ya) o navega a la carpeta de tu proyecto.
2.  Instala las dependencias necesarias. Puedes hacerlo usando `pip`:

    ```bash
    pip install streamlit sympy st-mathlive
    ```

## Uso de la Aplicación Web (Interfaz Gráfica)

Para ejecutar la aplicación web, abre tu terminal en la raíz del proyecto y ejecuta el siguiente comando:

```bash
streamlit run app.py
```

Esto abrirá la aplicación en tu navegador web predeterminado. Podrás introducir las funciones \(M(x, y)\) y \(N(x, y)\) utilizando notación LaTeX.

### Notas sobre la entrada LaTeX

La aplicación utiliza un componente `mathfield` para la entrada de ecuaciones, que soporta notación LaTeX. Aquí algunos ejemplos de cómo escribir las expresiones:

-   **Potencias**: `x^2` para \(x^2\), `y^3` para \(y^3\).
-   **Multiplicación**: `x*y` para \(xy\). La multiplicación implícita (`xy`) también puede funcionar en muchos casos, pero se recomienda usar `*` para mayor claridad y precisión.
-   **Fracciones**: `\frac{numerador}{denominador}`. Ejemplo: `\frac{x}{y}` para \( \frac{x}{y} \).
-   **Funciones Trigonométricas**: `\sin(x)`, `\cos(y)`, `\tan(xy)`.
-   **Exponenciales y Logaritmos**: `\exp(x)` o `e^x`, `\ln(x)` o `\log(x)`.
-   **Raíces**: `\sqrt{x}` para \( \sqrt{x} \), `\sqrt[n]{x}` para \( \sqrt[n]{x} \).

## Uso de la Versión de Consola (Ejemplos Predefinidos)

El proyecto también incluye un script para ejecutar la lógica de resolución en la consola con ejemplos predefinidos. Para usarlo:

```bash
python run_solver.py
```

Este comando ejecutará una serie de ejemplos y mostrará los resultados directamente en la terminal.

--- 