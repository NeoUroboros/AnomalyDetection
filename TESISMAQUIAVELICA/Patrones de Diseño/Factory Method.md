# Método de Fábrica (Factory Method)
**También conocido como:** Constructor Virtual

---

## **Intención**
El **Método de Fábrica** es un patrón de diseño creacional que proporciona una interfaz para crear objetos en una clase base, pero permite que las subclases modifiquen el tipo de objetos que se crearán.
![[Pasted image 20241127160112.png]]

---

## **Problema**
Imagina que estás creando una aplicación para la gestión logística. La primera versión solo maneja transporte terrestre con camiones, y la mayor parte del código depende de la clase `Truck`.
![[Pasted image 20241127160141.png]]

Con el tiempo, recibes solicitudes para incluir transporte marítimo. Sin embargo, tu código está acoplado a la clase `Truck`. Agregar la clase `Ship` requeriría modificar gran parte del código existente, creando problemas de mantenimiento y escalabilidad.

---

## **Solución**
El patrón **Método de Fábrica** sugiere reemplazar las llamadas directas al constructor de objetos (usando el operador `new`) por llamadas a un método de fábrica especial. No te preocupes: los objetos aún se crean mediante el operador `new`, pero la llamada se realiza dentro del método de fábrica. Los objetos devueltos por un método de fábrica suelen denominarse **productos**.
![[Pasted image 20241127160246.png]]
A primera vista, este cambio puede parecer inútil: simplemente movimos la llamada al constructor de una parte del programa a otra. Sin embargo, considera esto: ahora puedes sobrescribir el método de fábrica en una subclase y cambiar la clase de productos que el método crea.

Hay una pequeña limitación, sin embargo: las subclases pueden devolver diferentes tipos de productos solo si estos productos tienen una clase base o una interfaz común. Además, el método de fábrica en la clase base debe declarar su tipo de retorno como esta interfaz.
![[Pasted image 20241127160356.png]]
Por ejemplo, tanto las clases `Truck` como `Ship` deben implementar la interfaz `Transport`, que declara un método llamado `deliver`. Cada clase implementa este método de manera diferente: los camiones entregan la carga por tierra, mientras que los barcos la entregan por mar. El método de fábrica en la clase `RoadLogistics` devuelve objetos `Truck`, mientras que el método de fábrica en la clase `SeaLogistics` devuelve objetos `Ship`.
![[Pasted image 20241127160407.png]]
El código que utiliza el método de fábrica (a menudo llamado **código cliente**) no ve la diferencia entre los productos reales devueltos por las diversas subclases. El cliente trata a todos los productos como objetos abstractos del tipo `Transport`. El cliente sabe que todos los objetos de transporte deben tener el método `deliver`, pero no le importa exactamente cómo funciona.

---

## **Estructura**
![[Pasted image 20241127160536.png]]

1. **Producto:**
   - Declara la interfaz común que comparten todos los objetos creados por la fábrica.
2. **Productos Concretos:**
   - Implementaciones específicas de la interfaz del producto.
3. **Creador:**
   - Clase base que declara el método de fábrica. Puede tener una implementación por defecto o ser abstracto.
4. **Creadores Concretos:**
   - Sobrescriben el método de fábrica para devolver un tipo específico de producto.

---

## **Pseudocódigo**
Ejemplo: Crear botones de interfaz gráfica compatibles con diferentes sistemas operativos.

```java
// Clase base del creador
abstract class Dialog {
    abstract method createButton(): Button;

    method render() {
        Button okButton = createButton();
        okButton.onClick(closeDialog);
        okButton.render();
    }
}

// Creadores concretos
class WindowsDialog extends Dialog {
    method createButton(): Button {
        return new WindowsButton();
    }
}

class WebDialog extends Dialog {
    method createButton(): Button {
        return new HTMLButton();
    }
}

// Interfaz del producto
interface Button {
    method render();
    method onClick(f);
}

// Productos concretos
class WindowsButton implements Button {
    method render() {
        // Renderiza un botón al estilo Windows
    }
    method onClick(f) {
        // Vincula el evento de clic
    }
}

class HTMLButton implements Button {
    method render() {
        // Representa un botón en HTML
    }
    method onClick(f) {
        // Vincula un evento de clic del navegador
    }
}

// Cliente
class Application {
    field dialog: Dialog;

    method initialize() {
        if (config.OS == "Windows") {
            dialog = new WindowsDialog();
        } else if (config.OS == "Web") {
            dialog = new WebDialog();
        } else {
            throw new Exception("Sistema operativo desconocido.");
        }
    }

    method main() {
        initialize();
        dialog.render();
    }
}

```

## **Cuándo Usarlo**

1. **Desacoplamiento:** Cuando no conoces los tipos específicos de objetos con los que trabajará tu código.
2. **Extensibilidad:** Cuando necesitas extender una biblioteca o marco, permitiendo a los usuarios personalizar componentes internos.
3. **Reutilización:** Para reutilizar recursos existentes (como conexiones de base de datos) en lugar de crear nuevos objetos cada vez.

---

## **Cómo Implementarlo**

1. Asegúrate de que todos los productos sigan la misma interfaz.
2. Agrega un método de fábrica vacío en la clase base del creador. Su tipo de retorno debe coincidir con la interfaz del producto.
3. Encuentra las llamadas directas a constructores en tu código y cámbialas por llamadas al método de fábrica.
4. Crea subclases del creador, sobrescribe el método de fábrica y define el código de construcción para cada tipo de producto.
5. Si el método de fábrica queda vacío en la clase base, conviértelo en abstracto.

---

## **Ventajas**

- **Desacoplamiento:** Reduce la dependencia entre el creador y los productos concretos.
- **Principio de Responsabilidad Única:** Centraliza la lógica de creación de productos.
- **Principio Abierto/Cerrado:** Puedes agregar nuevos tipos de productos sin modificar el código existente.

---

## **Desventajas**

- Puede aumentar la complejidad al introducir muchas subclases para implementar el patrón.

---

## **Relaciones con Otros Patrones**

- **Fábrica Abstracta:** A menudo se basa en un conjunto de métodos de fábrica.
- **Prototipo:** Puede usarse como una alternativa para la creación de objetos, pero requiere inicialización compleja.
- **Método Plantilla:** El método de fábrica puede ser un paso dentro de un Método Plantilla.

La diferencia principal entre **usar el patrón Factory Method** (con `CreateDocumentObject`) y **crear directamente
clases que hereden de `Document`** radica en la **flexibilidad** y el **desacoplamiento** que obtienes al emplear el
patrón de diseño. A continuación, te explico por qué usar un Factory Method podría ser mejor en ciertos contextos,
comparado con heredar directamente de `Document`:

### 1. **Desacoplamiento entre la creación y el uso de objetos**
   - **Con Factory Method**: El código cliente (quien usa los documentos) **no necesita conocer las clases
   concretas** (como `CSV`, `JSON`, etc.) que está utilizando. El cliente solo conoce la clase abstracta
   `CreateDocumentObject`, que se encarga de crear el documento apropiado.

     - Ventaja: Si en el futuro necesitas cambiar la forma en que creas un documento (por ejemplo, cambiar
     el backend de lectura o escritura de documentos CSV), lo puedes hacer en la clase `CreateCSV`, sin modificar
      el código que usa esos documentos.

   - **Sin Factory Method (herencia directa de `Document`)**: El cliente tendría que instanciar directamente las
   clases concretas (`CSV`, `JSON`, etc.). Esto implica que el código cliente debe saber exactamente qué clase
   instanciar dependiendo del tipo de documento.

     - Desventaja: Si en algún momento necesitas cambiar cómo se crea un documento, tendrías que hacer
     cambios en el código cliente. Esto va en contra del principio **abierto/cerrado (OCP)**, ya que tendrías
     que modificar el código existente.

### 2. **Escalabilidad y mantenimiento**
   - **Con Factory Method**: Si decides agregar nuevos tipos de documentos en el futuro (por ejemplo, `Excel`,
    `XML`), solo necesitas registrar esos nuevos formatos en la clase `DocumentFactory`, sin tocar el código de
     las clases o el código cliente que usa documentos. Además, puedes hacerlo de manera centralizada, desde una
      sola fábrica.

     - Ventaja: Tu código es más escalable porque agregar nuevas funcionalidades (nuevos tipos de documentos)
      no requiere modificar el código existente, solo lo extiendes.

   - **Sin Factory Method**: Cada vez que agregas un nuevo tipo de documento, tendrías que modificar el código
   cliente para que sepa cómo crear instancias de esa nueva clase. Esto puede ser tedioso y propenso a errores
   si hay muchas partes del código que utilizan documentos.

     - Desventaja: Esto no es escalable, ya que la lógica de creación de objetos está dispersa en todo el
     código cliente, y cualquier cambio requeriría actualizaciones en múltiples lugares.

### 3. **Cumplimiento de SOLID**
   - **Con Factory Method**:
     - **Principio de responsabilidad única (SRP)**: Separas claramente las responsabilidades: la creación de los
     documentos está en las clases creadoras (`CreateCSV`, `CreateJSON`), y la lógica del documento está en las
     clases `CSV`, `JSON`, etc. Esto facilita el mantenimiento, ya que si hay cambios en cómo se crea el documento,
      no tienes que modificar la clase `Document`.

     - **Principio abierto/cerrado (OCP)**: No necesitas modificar clases existentes para soportar nuevos formatos
      de documentos; simplemente creas una nueva clase creadora que herede de `CreateDocumentObject`.

   - **Sin Factory Method**:
     - **SRP violado**: El código que usa los documentos también sería responsable de instanciarlos, lo que mezcla
      responsabilidades (creación y uso) en un solo lugar.

     - **OCP violado**: Si agregas nuevos tipos de documentos, tendrías que modificar el código cliente para que
     sepa cómo crear esos nuevos tipos, lo que va en contra del principio abierto/cerrado.

### 4. **Testing más fácil**
   - **Con Factory Method**: Al separar la creación de objetos en una clase distinta, puedes **testear las clases
    de creación de documentos por separado**. Además, el uso de interfaces y clases abstractas (como
    `CreateDocumentObject`) hace más fácil mockear o simular diferentes comportamientos en los tests, sin necesidad
     de modificar el código real.

   - **Sin Factory Method**: Al no tener un desacoplamiento claro entre la creación y el uso de los documentos,
   el testing puede volverse más complicado, ya que el cliente está más estrechamente acoplado a las clases
   concretas de los documentos.

### 5. **Dinamismo**
   - **Con Factory Method**: Puedes hacer el código dinámico, como el caso que planteas donde decides qué tipo
    de documento crear basado en la extensión del archivo. Esto es posible gracias a la **DocumentFactory**,
    que delega la responsabilidad de crear el documento apropiado sin que el cliente tenga que saberlo.

   - **Sin Factory Method**: Tendrías que utilizar condicionales (`if` o `switch`) en el código cliente para
   verificar la extensión del archivo y crear manualmente la clase correspondiente. Esto no es tan dinámico
   ni escalable, y hace que el código sea más rígido y difícil de mantener.


### **Ejemplo Sin Factory Method:**
Si eliminamos el Factory Method y hacemos que las clases hereden directamente de `Document`, el código cliente
tendría que manejar manualmente la creación de objetos de acuerdo a la extensión del archivo, algo así:

```python
def get_document(filepath):
    extension = filepath.split('.')[-1]
    if extension == 'csv':
        return CSV(filepath)
    elif extension == 'json':
        return JSON(filepath)
    else:
        raise ValueError(f"No document handler for extension: {extension}")

# Uso en el código cliente
doc = get_document('data/raw/iris.csv')
df = doc.readDoc()
doc.writeDoc('data/output/iris.csv')
```

- **Desventaja**: Este enfoque obliga al código cliente a tomar decisiones sobre qué clase instanciar (violando SRP)
 y a modificar el código cada vez que se agregue un nuevo tipo de documento (violando OCP). Esto también puede hacer
  que el código sea más difícil de mantener y escalar a medida que se añaden más tipos de documentos.


### **Conclusión**:
- **Usar el Factory Method** es mejor en escenarios donde buscas flexibilidad, escalabilidad y un diseño desacoplado.
 Te permite cumplir con principios de diseño (SOLID), facilita la mantenibilidad y hace que tu sistema sea extensible
  sin cambiar el código existente.

- **No usar Factory Method** puede ser suficiente si tu sistema es muy pequeño, no va a escalar y no necesitas
agregar nuevos tipos de documentos. Pero en sistemas más complejos, donde esperas trabajar con múltiples tipos de
documentos o cambiar la lógica de creación en el futuro, el Factory Method es una mejor opción.


---

### **Descripción del Diagrama:**

1. **Creator (Clase Abstracta)**:
    
    - Define un método abstracto `createProduct()` que las subclases deben implementar.
    - Proporciona la lógica común (`someOperation()`) y delega la creación específica de productos a las subclases.
2. **ConcreteCreatorA y ConcreteCreatorB (Clases Concretas)**:
    
    - Implementan el método `createProduct()` para devolver una instancia específica de un producto (por ejemplo, `ConcreteProductA` o `ConcreteProductB`).
3. **Product (Interfaz o Clase Abstracta)**:
    
    - Define las operaciones comunes que todos los productos deben tener (`doStuff()`).
4. **ConcreteProductA y ConcreteProductB (Clases Concretas)**:
    
    - Implementan la interfaz o extienden la clase abstracta `Product`.

En tu implementación, el patrón **Factory Method** se usa para manejar la creación de diferentes documentos (`CSV`, `Excel`, `JSON`, etc.) basándote en su extensión.

---

### **Tu Implementación del Factory Method**:

#### 1. **Creator (Clase Base Abstracta):**

- En tu caso, esta sería la clase `CreateDocumentObject`, que define:
    - El método abstracto `createDocument()` para que cada subclase implemente.
    - La lógica común para leer documentos usando `readDocument()`.

```python
class CreateDocumentObject(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def createDocument(self):
        pass

    def readDocument(self):
        document = self.createDocument()  # Delegar a la subclase
        return document.readDoc()         # Operación común
```

---

#### 2. **ConcreteCreator (Subclases específicas):**

- Estas son las clases como `CreateCSV`, `CreateExcel`, etc. Cada una implementa `createDocument()` para devolver el tipo correcto de documento.

Ejemplo:

```python
class CreateCSV(CreateDocumentObject):
    def __init__(self, filepath):
        super().__init__(filepath)

    def createDocument(self):
        return CSV(self.filepath)
```

Cada subclase concreta sabe cómo crear su tipo de documento.

---

#### 3. **Product (Clase o Interfaz Base):**

- En tu caso, la clase base sería `Document`, que define el método abstracto `readDoc()`. Todas las clases concretas (`CSV`, `Excel`, etc.) heredan de esta.

```python
class Document(ABC):
    @abstractmethod
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def readDoc(self):
        pass
```

---

#### 4. **ConcreteProduct (Implementaciones Concretas):**

- Estas son las clases como `CSV`, `Excel`, `JSON`, etc., que implementan la lógica específica para leer cada tipo de documento.

Ejemplo:

```python
class CSV(Document):
    def __init__(self, filepath):
        super().__init__(filepath)

    def readDoc(self):
        return pd.read_csv(self.filepath)
```

---

#### 5. **Factory Manager (Document Factory):**

- Centraliza la lógica para asociar extensiones de archivo con sus respectivos creadores (`ConcreteCreator`).

```python
class DocumentFactory:
    def __init__(self):
        self.creators = {}

    def registerFormat(self, extension, creator):
        self.creators[extension] = creator

    def getDocument(self, filepath):
        extension = filepath.split(".")[-1]
        creator = self.creators.get(extension)
        if not creator:
            raise ValueError(f"No document handler for extension: {extension}")
        return creator(filepath)
```

Esto permite registrar nuevos formatos fácilmente, como:

```python
factory = DocumentFactory()
factory.registerFormat('csv', CreateCSV)
factory.registerFormat('xlsx', CreateExcel)
```

---

### **Cómo Funciona Todo Junto:**

Cuando necesitas procesar un archivo, el flujo es:

1. Llamas a `factory.getDocument(filepath)`.
    
    - La fábrica identifica el tipo de archivo (por extensión) y selecciona el creador adecuado (por ejemplo, `CreateCSV` para archivos CSV).
2. El método `createDocument()` del creador específico devuelve el producto concreto (por ejemplo, una instancia de `CSV`).
    
3. Usas el producto para realizar operaciones comunes, como `readDoc()`.
    

Ejemplo de uso:

```python
doc = factory.getDocument("data/raw/example.csv")
df = doc.readDocument()  # Llama a CSV.readDoc()
```

---

### **Ventajas del Factory Method en tu Contexto:**

1. **Extensibilidad**:
    
    - Si necesitas soportar un nuevo formato (por ejemplo, `XML`), solo necesitas crear un nuevo `ConcreteCreator` (como `CreateXML`) y registrarlo en la fábrica.
2. **Responsabilidad Única**:
    
    - Cada clase tiene una tarea específica: la fábrica administra los formatos, y los productos manejan la lógica para leer documentos.
3. **Flexibilidad**:
    
    - Puedes cambiar o mejorar la lógica de lectura de un formato sin afectar el resto del sistema.
4. **Desacoplamiento**:
    
    - El código que usa el sistema no necesita saber qué tipo de documento está manejando; solo usa la interfaz común `Document`.

¿Hay algo más que quieras detallar o algún punto específico en el código que te genere dudas?
