# PaymentsService

### Microservicio de Payments en Python

**DesignDoc del Microservicio**
https://docs.google.com/document/d/1HwPicopfwutkZlpRVY0wSh7wZv3hl9smyWe4YFwi0gs/edit?usp=sharing

#### Dependencias 

Para instalar las dependencias 
* PIP: pip install -r requirements.txt
* Conda: conda env create -f environment.yml

Es necesario tener RabbitMQ y MongoDB instalados.

**Estructura del Proyecto**

* app/domain
    * modulos que aglutinan funcionalidad y servicios relacionados a entidades del dominio (payments y transactions)
* app/gateways
    * modulos para el manejo de la comunicacion mediante RabbitMQ y MercadoPago (no terminado, "simulado")
* app/utils
    * modulos para validacion de schema, conexion a bd, manejo de errores, y autenticacion con microservicio auth.

