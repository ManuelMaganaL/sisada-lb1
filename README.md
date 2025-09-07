# Laboratorio 1 - Sistemas Adaptativos
Simulación de calle con coches, junto con un sistema de autoajuste para cambiar el color de los semaforos

La formula para autoajustar la duración de la luz verde de los semaforos es la siguiente:
> duracion(seg) = duracion_minima(seg) + números_de_coches * 2(seg)

## Requisitos
Para ejecutar el programa ten descargado:
- Python
- PIP

## Ejecución
```sh
# Clona el repositorio
git clone https://github.com/ManuelMaganaL/sisada-lb1

# Entra en el repo
cd sisada-lb1

# Instala las dependencias necesarias
pip install -r requirements.txt

# Ejecuta el archivo main.py para ver la simulación
python src/main.py
```

## Ejemplo
![Foto de ejemplo](./img/demo.gif)
