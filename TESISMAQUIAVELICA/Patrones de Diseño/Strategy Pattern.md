 Estrategia
**Intención:**

El patrón de diseño de comportamiento Strategy te permite definir una familia de algoritmos, poner cada uno de ellos en una clase separada y hacer que sus objetos sean intercambiables.

### ![[Pasted image 20241128175045.png]]
## Problema

Un día decidiste crear una aplicación de navegación para viajeros casuales. La aplicación se centraba en un hermoso mapa que ayudaba a los usuarios a orientarse rápidamente en cualquier ciudad.

Una de las características más solicitadas para la aplicación era la planificación automática de rutas. Un usuario debería poder ingresar una dirección y ver la ruta más rápida hacia ese destino mostrada en el mapa.

La primera versión de la aplicación solo podía construir rutas sobre carreteras. Las personas que viajaban en coche estaban encantadas. Pero, al parecer, no a todos les gusta conducir en sus vacaciones. Así que en la siguiente actualización agregaste una opción para construir rutas a pie. Justo después de eso, agregaste otra opción para permitir que las personas usen el transporte público en sus rutas.

Sin embargo, eso fue solo el comienzo. Más tarde planeaste agregar la construcción de rutas para ciclistas. Y aún más tarde, otra opción para construir rutas a través de todos los puntos turísticos de una ciudad.

El código del navegador se volvió muy inflado.
![[Pasted image 20241129133914.png]]
Desde una perspectiva comercial, la aplicación fue un éxito, pero la parte técnica te causó muchos dolores de cabeza. Cada vez que agregabas un nuevo algoritmo de enrutamiento, la clase principal del navegador duplicaba su tamaño. En algún momento, la bestia se volvió demasiado difícil de mantener.

Cualquier cambio en uno de los algoritmos, ya sea una simple corrección de errores o un ligero ajuste del puntaje de las calles, afectaba a toda la clase, aumentando la posibilidad de crear un error en el código que ya funcionaba.

Además, el trabajo en equipo se volvió ineficiente. Tus compañeros, que fueron contratados justo después del lanzamiento exitoso, se quejaban de que pasaban demasiado tiempo resolviendo conflictos de fusión. Implementar una nueva característica requería que cambiaras la misma clase enorme, entrando en conflicto con el código producido por otras personas.

### Solución:

El patrón de Strategy sugiere que tomes una clase que haga algo específico de muchas maneras diferentes y extraigas todos estos algoritmos en clases separadas llamadas estrategias.

La clase original, llamada contexto, debe tener un campo para almacenar una referencia a una de las estrategias. El contexto delega el trabajo a un objeto de estrategia vinculado en lugar de ejecutarlo por sí mismo.

El contexto no es responsable de seleccionar un algoritmo adecuado para el trabajo. En cambio, el cliente pasa la estrategia deseada al contexto. De hecho, el contexto no sabe mucho sobre las estrategias. Funciona con todas las estrategias a través de la misma interfaz genérica, que solo expone un método para activar el algoritmo encapsulado dentro de la estrategia seleccionada.

De esta manera, el contexto se vuelve independiente de estrategias concretas, por lo que puedes agregar nuevos algoritmos o modificar los existentes sin cambiar el código del contexto o de otras estrategias.

![[Pasted image 20241129134021.png]]
### Estructura del Patrón Strategy:

1. **Contexto**: Mantiene una referencia a una de las estrategias concretas y se comunica con este objeto solo a través de la interfaz de estrategia. [![Estructura del Patrón Strategy](https://refactoring.guru/images/patterns/diagrams/strategy/structure-2x.png)]

2. **Interfaz de Estrategia**: Es común a todas las estrategias concretas. Declara un método que el contexto usa para ejecutar una estrategia.

3. **Estrategias Concretas**: Implementan diferentes variaciones de un algoritmo que el contexto usa.

4. **Cliente**: Crea un objeto de estrategia específico y se lo pasa al contexto. El contexto expone un método setter que permite a los clientes reemplazar la estrategia asociada con el contexto en tiempo de ejecución.

### Pseudocódigo:

En este ejemplo, el contexto usa múltiples estrategias para ejecutar varias operaciones aritméticas.

```java
// La interfaz de estrategia declara operaciones comunes a todas
// las versiones compatibles de algún algoritmo. El contexto usa esta
// interfaz para llamar al algoritmo definido por las estrategias concretas.
interface Strategy {
    int execute(int a, int b);
}

// Las estrategias concretas implementan el algoritmo siguiendo
// la interfaz base de la estrategia. La interfaz las hace
// intercambiables en el contexto.
class ConcreteStrategyAdd implements Strategy {
    public int execute(int a, int b) {
        return a + b;
    }
}

class ConcreteStrategySubtract implements Strategy {
    public int execute(int a, int b) {
        return a - b;
    }
}

class ConcreteStrategyMultiply implements Strategy {
    public int execute(int a, int b) {
        return a * b;
    }
}

// El contexto define la interfaz de interés para los clientes.
class Context {
    // El contexto mantiene una referencia a uno de los objetos estrategia.
    // El contexto no conoce la clase concreta de una estrategia.
    // Debe trabajar con todas las estrategias a través de la interfaz
    // de la estrategia.
    private Strategy strategy;

    // Generalmente el contexto acepta una estrategia a través del
    // constructor, y también proporciona un setter para que la
    // estrategia pueda ser cambiada en tiempo de ejecución.
    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    // El contexto delega algo de trabajo al objeto estrategia
    // en lugar de implementar múltiples versiones del
    // algoritmo por sí mismo.
    public int executeStrategy(int a, int b) {
        return strategy.execute(a, b);
    }
}

// El código del cliente elige una estrategia concreta y se la pasa al contexto.
// El cliente debe conocer las diferencias entre las estrategias
// para poder hacer la elección correcta.
public class ExampleApplication {
    public static void main(String[] args) {
        Context context = new Context();

        int firstNumber = 5;
        int secondNumber = 3;
        String action = "addition"; // Imagina que esto viene de una entrada del usuario

        if (action.equals("addition")) {
            context.setStrategy(new ConcreteStrategyAdd());
        } else if (action.equals("subtraction")) {
            context.setStrategy(new ConcreteStrategySubtract());
        } else if (action.equals("multiplication")) {
            context.setStrategy(new ConcreteStrategyMultiply());
        }

        int result = context.executeStrategy(firstNumber, secondNumber);
        System.out.println("Resultado: " + result);
    }
}
```

### Aplicabilidad:

- Usa el patrón Strategy cuando quieras usar diferentes variantes de un algoritmo dentro de un objeto y puedas cambiar de un algoritmo a otro durante el tiempo de ejecución.
- Usa el patrón cuando tengas muchas clases similares que solo difieren en la forma en que ejecutan algún comportamiento.
- Usa el patrón para aislar la lógica de negocio de una clase de los detalles de implementación de algoritmos que pueden no ser tan importantes en el contexto de esa lógica.
- Usa el patrón cuando tu clase tenga una declaración condicional masiva que cambie entre diferentes variantes del mismo algoritmo.

### Pros y Contras:

**Pros**:
- Puedes intercambiar los algoritmos utilizados dentro de un objeto en tiempo de ejecución.
- Puedes aislar los detalles de implementación de un algoritmo del código que lo usa.
- Puedes reemplazar la herencia con la composición.
- Principio de Abierto/Cerrado. Puedes introducir nuevas estrategias sin tener que cambiar el contexto.

**Contras**:
- Si solo tienes un par de algoritmos y rara vez cambian, no hay una razón real para complicar el programa con nuevas clases e interfaces que vienen con el patrón.
- Los clientes deben estar al tanto de las diferencias entre las estrategias para poder seleccionar una adecuada.
