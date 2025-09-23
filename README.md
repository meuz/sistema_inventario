Estructura de la base de datos:
<img width="219" height="176" alt="image" src="https://github.com/user-attachments/assets/486fc071-85c5-457b-b5ca-c7363423ee5f" />

Ejecucion del comando "python manage.py migrate" luego de una correcion en los modelos (Faltaba el modelo de Bodegas)
<img width="625" height="75" alt="Captura de pantalla 2025-09-23 180139" src="https://github.com/user-attachments/assets/67b35a6d-cec0-4fe6-bd3b-e24526342557" />

Descripcion de los modelos:
Como modelo principal tenemos a Producto, el cual se relaciona con Categoria, Proveedor y Bodega para ser clasificado y descrito mediante relaciones de uno a muchos. A su vez, el modelo Movimiento funciona como un registro historico, que documenta cada entrada y salida de stock. Este enfoque garantiza un orden y organizacion de productos.

Se debe activar el entorno virtual antes de iniciar el servicio:
.\venv\Scripts\activate

luego:
python manage.py runserver

De no funcionar, probar con:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

y luego los otros comandos.


Profesora le ofrezco una disculpa, se que este trabajo no tiene ni pies ni cabeza, en la proxima entrega me esforzare más.


