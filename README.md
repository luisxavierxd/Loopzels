# Loopzels — Rompecabezas de Patrones Animados

> Juego de escritorio desarrollado en Python como herramienta de estimulacion cognitiva mediante rompecabezas visuales animados con dificultad progresiva.

---

## Descripcion del Proyecto (Expo Ingenierias)

### El Problema — Por que existe Loopzels

El deterioro de las capacidades cognitivas, en particular de la memoria visual, la atencion sostenida y el razonamiento espacial, representa una problematica creciente que no se limita a los adultos mayores. La exposicion prolongada a contenidos digitales pasivos —redes sociales, videos de formato corto, notificaciones constantes— genera en personas de todas las edades una reduccion en la capacidad de concentracion y en la habilidad de retener y procesar informacion visual compleja. Ante la ausencia de herramientas de estimulacion cognitiva accesibles, gratuitas y atractivas para el usuario cotidiano, existe una clara area de oportunidad para el desarrollo de software educativo-recreativo que combine entretenimiento con ejercitacion mental estructurada.

### El Objetivo

Desarrollar un software de entretenimiento educativo que estimule activamente la memoria visual, el reconocimiento de patrones y la agilidad mental, ofreciendo una experiencia de juego progresiva y motivadora que pueda ser utilizada de manera habitual como practica de mantenimiento cognitivo.

### La Solucion — Que es y Como funciona

**Loopzels** es una aplicacion de escritorio desarrollada en Python que presenta al usuario patrones visuales animados (en formato GIF) fragmentados aleatoriamente en piezas que deben ser reordenadas hasta reconstruir la imagen original. El jugador selecciona dos piezas por turno para intercambiarlas, guiandose unicamente por su memoria del patron completo y su capacidad de razonamiento espacial.

La metodologia del juego se basa en la **Teoria de la Carga Cognitiva** (Sweller, 1988): la dificultad escala de forma controlada desde grillas de 2x2 hasta 6x6, lo que permite al usuario construir competencia gradualmente sin saturar su memoria de trabajo. Adicionalmente, el uso de **patrones en movimiento** (GIFs animados en lugar de imagenes estaticas) introduce un desafio perceptual unico: el cerebro debe procesar simultaneamente la composicion espacial y el movimiento, activando mas recursos cognitivos que un rompecabezas convencional. El sistema de records por tiempo fomenta la **motivacion intrinseca** y la practica repetida, principios fundamentales del aprendizaje por refuerzo positivo.

Lo que diferencia a Loopzels de rompecabezas digitales existentes es precisamente la combinacion de animacion continua, escalabilidad de dificultad y registro de progreso personal, todo dentro de una interfaz visualmente inmersiva con fondo dinamico y musica ambiental, haciendo del entrenamiento cognitivo una experiencia genuinamente entretenida.

### Resultados Esperados

El uso regular de Loopzels busca fortalecer la memoria visual a corto plazo, mejorar la velocidad de procesamiento espacial y desarrollar la capacidad de atencion sostenida. Su diseno accesible y sin costo lo posiciona como una herramienta de estimulacion cognitiva disponible para cualquier persona con acceso a una computadora, democratizando el entrenamiento mental de una forma que los metodos tradicionales no logran.

---

## Caracteristicas Principales

| Caracteristica | Detalle |
|---|---|
| Patrones animados | 5 patrones GIF distintos, cada uno con su propia composicion y ritmo visual |
| Dificultad escalable | Grillas de 2x2, 3x3, 4x4, 5x5 y 6x6 (4 a 36 piezas) |
| Sistema de records | Top 3 mejores tiempos por patron y por tamano de grilla, persistidos en JSON |
| Fondo dinamico | El fondo de la pantalla de titulo rota entre los patrones con recolorizado en tiempo real |
| Audio ambiental | Musica de fondo con control de volumen persistente entre sesiones |
| Vista previa animada | Previsualizacion del patron elegido antes de comenzar la partida |
| Pantalla fullscreen | Lanza en pantalla completa automaticamente |

---

## Estructura del Proyecto

```
Rompecabezas/
├── Programa/
│   ├── Assets/
│   │   ├── Audio/
│   │   │   └── musica_fondo.mp3        # Musica ambiental del juego
│   │   ├── General/
│   │   │   ├── fondo.png               # Imagen de fondo de menus
│   │   │   ├── logo.gif                # Logo animado de la pantalla titulo
│   │   │   └── tamaño.png              # Grafico del selector de tamano
│   │   └── Patrones/
│   │       ├── Patron1.gif             # Patron 1 (usado como rompecabezas y fondo)
│   │       ├── Patron2.gif
│   │       ├── Patron3.gif
│   │       ├── Patron4.gif
│   │       └── Patron5.gif
│   └── Codigo/
│       ├── Main.py                     # Punto de entrada: crea ventana e inicia titulo
│       ├── pantalla_titulo.py          # Pantalla de bienvenida con fondo animado y logo
│       ├── menu_principal.py           # Selector de patron, tamano y gestion de records
│       ├── Rompecabezas.py             # Motor del juego: grid, animacion, logica de clic
│       ├── configuracion.py            # Pantalla de ajustes (volumen)
│       ├── audio.py                    # Manejo de musica con pygame
│       └── config.json                 # Persistencia de volumen y records
├── .venv/                              # Entorno virtual de Python
├── .gitignore
└── LICENSE
```

### Descripcion de cada modulo

#### `Main.py`
Punto de entrada del programa. Inicializa la ventana de tkinter en modo pantalla completa, arranca el sistema de audio y llama a la pantalla de titulo. Maneja el cierre limpio de la aplicacion.

#### `pantalla_titulo.py`
Muestra la pantalla de bienvenida. Implementa la clase `FondoAnimado` que carga los GIFs de patrones, los recoloriza en rojo/amarillo con `ImageOps.colorize` y los anima cuadro a cuadro. El fondo rota automaticamente entre patrones cada 10 segundos en un hilo separado para no bloquear la interfaz. El logo animado y los botones JUGAR / SALIR se superponen sobre el fondo.

#### `menu_principal.py`
Pantalla de configuracion previa a la partida. Permite seleccionar:
- **Tamano del grid**: botones de 2x2 a 6x6
- **Patron**: navegacion con botones `<` / `>` con previsualizacion animada

Cuando el usuario presiona "Jugar", construye el overlay de partida con tres columnas: panel de tiempo transcurrido (izquierda), rompecabezas interactivo (centro) y panel de records (derecha). Al completar el puzzle actualiza y persiste el top 3 de tiempos en `config.json`.

#### `Rompecabezas.py`
Motor central del juego. Responsabilidades:
- `mezclar_piezas()`: genera un orden aleatorio garantizando que nunca sea igual al correcto.
- `cargar_frames()`: abre el GIF, lo convierte a escala de grises y lo recorta en `GRID²` piezas, guardando todos los frames de animacion por pieza.
- `crear_grid()`: construye la cuadricula de Canvas widgets con los listeners de clic.
- `click_pieza()`: implementa la logica de seleccion de dos piezas e intercambio.
- `animar()`: loop de animacion a 80 ms/frame que actualiza todos los canvas y aplica recolorizado rojo/amarillo en tiempo real.
- `puzzle_completo()`: verifica si el orden actual coincide con el orden correcto y dispara el callback de victoria.

#### `configuracion.py`
Pantalla modal de ajustes con un slider de volumen. El valor se sincroniza en tiempo real con `pygame.mixer` y se persiste inmediatamente en `config.json`. Una burbuja flotante muestra el porcentaje actual sobre el knob del slider.

#### `audio.py`
Abstrae la inicializacion y control de `pygame.mixer`. Carga la musica de fondo, respeta el volumen guardado en `config.json` y expone funciones simples (`inicializar_audio`, `detener_musica`) al resto de los modulos.

---

## Flujo de la Aplicacion

```
Inicio
  └─> Main.py
        └─> pantalla_titulo.py  (fondo animado rotativo + logo + botones)
              └─> [JUGAR] → menu_principal.py
                    ├─> Selector de grid (2x2 – 6x6)
                    ├─> Selector de patron (1–5) con preview animada
                    └─> [Jugar] → overlay de partida
                          ├─> Rompecabezas.py  (motor de juego + animacion)
                          ├─> Timer en tiempo real
                          ├─> Records del patron/tamano seleccionado
                          └─> [Victoria] → actualiza records → volver al menu
```

---

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| tkinter | Framework de interfaz grafica (ventanas, widgets, canvas) |
| Pillow (PIL) | Procesamiento de imagenes: resize, crop, colorize, animacion GIF |
| customtkinter | Widget CTkLabel para el logo de la pantalla titulo |
| pygame | Reproduccion y control de musica de fondo |
| json | Persistencia de configuracion y records del jugador |
| threading | Precarga de frames GIF en segundo plano sin bloquear la UI |

---

## Instalacion y Ejecucion

### Requisitos previos

- Python 3.10 o superior
- pip

### Instalacion de dependencias

```bash
pip install pillow customtkinter pygame
```

O usando el entorno virtual incluido:

```bash
# Windows
.venv\Scripts\activate
pip install pillow customtkinter pygame
```

### Ejecutar el juego

```bash
cd Programa/Codigo
python Main.py
```

El juego se abre automaticamente en pantalla completa. Presiona `Alt+F4` para cerrar o usa el boton SALIR.

---

## Mecanica de Juego

1. En el menu principal elige el **tamano del grid** (cuanto mayor, mas dificil).
2. Navega entre los **5 patrones** disponibles con las flechas `<` / `>`.
3. Presiona **Jugar**. El patron se fragmenta aleatoriamente en el grid.
4. Haz clic en una pieza para seleccionarla (se resalta en blanco). Luego haz clic en otra para intercambiarlas.
5. Reconstruye el patron original lo mas rapido posible. El timer corre desde el primer momento.
6. Al completar el rompecabezas, tu tiempo se registra en el **top 3** si es suficientemente bueno.

---

## Niveles de Dificultad

| Grid | Piezas | Descripcion |
|---|---|---|
| 2x2 | 4 | Introductorio — ideal para familiarizarse |
| 3x3 | 9 | Facil — requiere atencion basica al patron |
| 4x4 | 16 | Intermedio — demanda memoria visual activa |
| 5x5 | 25 | Avanzado — exige planificacion de movimientos |
| 6x6 | 36 | Experto — maxima carga cognitiva y atencion |

---

## Sistema de Records

Los records se guardan en `Programa/Codigo/config.json` bajo la clave `top_tiempos`, organizados por patron y tamano de grilla. Se mantienen los **3 mejores tiempos** (menor tiempo = mejor resultado) para cada combinacion posible (5 patrones x 5 tamanos = 25 tablas independientes).

```json
"top_tiempos": {
    "Patron2": {
        "5": ["00:38", "00:41", "00:46"]
    }
}
```

Los records pueden borrarse individualmente desde la pantalla de partida con el boton **Borrar Records**.

---

## Autores

Desarrollado por estudiantes de ingenieria como proyecto para Expo-Ingenierias.

- Luis Xavier Garcia — Desarrollo principal

---

## Licencia

Distribuido bajo los terminos de la licencia incluida en el archivo `LICENSE`.
