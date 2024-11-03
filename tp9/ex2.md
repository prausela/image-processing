La **transformada de Hough** para la detección de círculos es una técnica útil en procesamiento de imágenes para detectar formas circulares en una imagen. 
La idea principal es usar un espacio de parámetros que represente los posibles círculos y acumular evidencia en ese espacio. 

# Pasos para el uso de la Transformada de Hough para la Detección de Círculos
1. Preprocesamiento de la Imagen:
    - *Conversión a Escala de Grises*: Si la imagen de entrada está en color, convertirla a una imagen en escala de grises. Esto facilita el análisis porque reduce la cantidad de datos.
    - *Aplicación de Filtros*: Usar un filtro (por ejemplo, un filtro Gaussiano) para suavizar la imagen y reducir el ruido. Esto ayuda a evitar la detección de falsos positivos.
2. Detección de Bordes:
    - Utiliza un algoritmo de detección de bordes como el operador *Canny* para resaltar los bordes en la imagen, los cuales corresponden a cambios bruscos en la intensidad de la imagen y son los candidatos potenciales para los contornos de los círculos
3. Espacio de Parámetros para Círculos:
    - Un círculo en una imagen se puede definir por: el centro del círculo (𝑥_centro, 𝑦_centro) y el radio 𝑟
    - La transformada de Hough para círculos se basa en acumular evidencia para diferentes combinaciones de estos parámetros en un espacio tridimensional (o 2D si el radio es fijo o se busca en un rango específico)
4. Aplicación de la Transformada de Hough:
    - Recorre todos los puntos detectados en la imagen de bordes. Por cada punto (𝑥, 𝑦) que corresponde a un borde, asume que podría ser un punto en el borde de varios círculos con diferentes radios.
    - Para cada radio posible, calcula las coordenadas del centro del círculo utilizando las ecuaciones:
        𝑥_centro= 𝑥 − 𝑟.cos(𝜃)
        𝑦_centro= 𝑥 − 𝑟.sin(𝜃)
    donde 𝜃 varía de 0 a 360 grados.
    - Incrementa el valor en una acumuladora (una matriz tridimensional de acumulación) para cada posible (𝑥_centro, 𝑦_centro, 𝑟) calculado. Este proceso acumula evidencia de posibles centros de círculos.
5. Búsqueda de Máximos en el Espacio de Acumulación:
    - Identifica los picos en la matriz de acumulación. Un pico en este espacio sugiere que hay un círculo con los parámetros correspondientes.
    - Los picos representan los parámetros (𝑥_centro, 𝑦_centro, 𝑟) de los círculos detectados
6. Dibujar los Círculos Detectados:
    - Utilizar los parámetros de los círculos detectados para dibujar los círculos sobre la imagen original.

# Uso en Python
En Python, la transformada de Hough para la detección de círculos se implementa usando la biblioteca *OpenCV*. Se comienza cargando la imagen y convirtiéndola a escala de grises. Luego, se aplica un suavizado para reducir el ruido y se utiliza la función **cv2.HoughCircles** para detectar los círculos. Esta función busca círculos en la imagen basándose en la evidencia acumulada de diferentes combinaciones de centros y radios.

Una vez detectados, los círculos se dibujan sobre la imagen original para visualizarlos. Es importante ajustar algunos parámetros de la función, como el tamaño mínimo y máximo de los círculos, y los umbrales, para obtener resultados más precisos dependiendo de las características de la imagen.