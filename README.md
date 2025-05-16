# SauceDemo Test Automation Framework

## 📋 Descripción
Framework de automatización de pruebas E2E para [SauceDemo](https://www.saucedemo.com) implementando el patrón Page Object Model (POM). Este proyecto utiliza Selenium WebDriver con Python y está diseñado para realizar pruebas automatizadas de las principales funcionalidades de la aplicación.

## 🏗️ Estructura del Proyecto


```
saucedemo-automation/ 
├── config/ 
│ └── config.py # Configuraciones globales y ambientes 
├── pages/ 
│ ├── base_page.py # Clase base para Page Objects 
│ ├── login_page.py # Page Object de Login 
│ ├── inventory_page.py # Page Object de Inventario 
│ └── cart_page.py # Page Object de Carrito 
├── tests/ 
│ ├── test_login.py # Pruebas de autenticación 
│ └── test_cart.py # Pruebas de carrito de compras 
├── reports/ 
│ ├── allure-results/ # Resultados de pruebas en formato Allure 
│ └── screenshots/ # Capturas de pantalla de fallos 
├── requirements.txt # Dependencias del proyecto 
├── Makefile # Comandos de automatización 
└── README.md

```
## 🔧 Requisitos Previos
- Python 3.12.2
- Google Chrome (última versión estable)
- ChromeDriver (compatible con tu versión de Chrome)
- Java 8+ (para Allure Report)

## ⚙️ Configuración del Entorno


1. Clonar el repositorio:

```bash
bash git clone [https://github.com/yourusername/saucedemo-automation.git](https://github.com/yourusername/saucedemo-automation.git) cd saucedemo-automation
```
2. Crear y activar entorno virtual:

```bash
bash python -m venv venv source venv/bin/activate # En Windows: venv\Scripts\activate
```
3. Instalar dependencias:

```bash
bash make install
```

## 🚀 Ejecución de Pruebas

### Ejecutar todas las pruebas


```bash
bash make test
```

### Ejecutar pruebas específicas
```bash
# Ejecutar solo pruebas de login
pytest tests/test_login.py
# Ejecutar solo pruebas de carrito
pytest tests/test_cart.py
# Ejecutar pruebas con un marcador específico
pytest -m "critical"

```
### Generar y ver reporte Allure

```bash
bash make allure-report
```
## 📊 Reportes
Los reportes se generan en dos formatos:
- **Allure Report**: `reports/allure-report/index.html`
- **Screenshots**: `reports/screenshots/` (en caso de fallos)

## 🔍 Funcionalidades Cubiertas
- [x] Login (éxito y fallo)
- [x] Agregar productos al carrito
- [x] Remover productos del carrito
- [x] Verificación de precios
- [x] Proceso de checkout
- [x] Filtrado de productos
- [x] Ordenamiento de productos

## 🧪 Ambientes Soportados
El framework soporta múltiples ambientes configurables en `config/config.py`:
- Development (`dev`)
- Testing (`qa`)
- Production (`prod`)

Para cambiar de ambiente, modifica `CURRENT_ENV` en `config/config.py`.

## 📝 Convenciones de Código
- Seguimos PEP 8 para Python
- Nombres de pruebas descriptivos usando `snake_case`
- Documentación en español
- Comentarios explicativos en código complejo

## 🎯 Estrategias de Localización de Elementos

En este proyecto utilizamos tres métodos principales para localizar elementos en la interfaz web:

### 1. ID (Recomendado)
```python
elemento = driver.find_element(By.ID, "user-name")
```
**Ventajas:**
- ✅ Rendimiento óptimo (más rápido)
- ✅ Único por definición en el DOM
- ✅ Menor probabilidad de cambio
- ✅ Sintaxis simple y clara

**Cuándo usarlo:**
- Primera opción siempre que el elemento tenga un ID
- Ideal para elementos críticos como botones de login/submit

### 2. CSS Selector
```python
elemento = driver.find_element(By.CSS_SELECTOR, "input[data-test='username']")
```
**Ventajas:**
- ✅ Más rápido que XPath
- ✅ Sintaxis concisa y flexible
- ✅ Soporta múltiples atributos

**Cuándo usarlo:**
- Cuando el elemento no tiene ID
- Para seleccionar elementos por clase o atributos data-*
- En estructuras CSS complejas

### 3. XPath
```python
elemento = driver.find_element(By.XPATH, "//input[@id='user-name']")
```
**Ventajas:**
- ✅ Máxima flexibilidad
- ✅ Puede navegar hacia arriba en el DOM
- ✅ Soporta lógica condicional
- ✅ Útil para elementos dinámicos complejos

**Desventajas:**
- ❌ Más lento que ID y CSS
- ❌ Puede ser frágil si cambia la estructura HTML
- ❌ Sintaxis más compleja
### 📌 Jerarquía de Uso Recomendada
1. **ID** (Primera opción)
   - Más rápido y confiable
   - Ejemplo: `id="login-button"`

2. **CSS Selector** (Segunda opción)
   - Cuando no hay ID disponible
   - Ejemplo: `input[data-test='username']`

3. **XPath** (Última opción)
   - Solo cuando las opciones anteriores no son viables
   - Ejemplo: `//div[@class='login-box']//input`

### 💡 Buenas Prácticas

1. **Priorizar IDs**
```python
# Bien
elemento = driver.find_element(By.ID, "login-button")

# Evitar si hay ID disponible
elemento = driver.find_element(By.XPATH, "//input[@type='submit']")
```
2. **Usar selectores específicos**

```python
# Bien
elemento = driver.find_element(By.CSS_SELECTOR, "#login-form input[type='submit']")

# Evitar
elemento = driver.find_element(By.CSS_SELECTOR, "input")
```
3. **Mantener selectores actualizados**
   - Documentar cambios en los selectores
   - Revisar periódicamente la validez de los selectores
   - Usar atributos estables (como data-test)

4. **Evitar selectores frágiles**

```python
# Evitar
elemento = driver.find_element(By.XPATH, "//div[3]/span[2]")

# Preferir
elemento = driver.find_element(By.CSS_SELECTOR, "[data-test='username']")
```
### 🔍 Ejemplos en Nuestro Proyecto
```python
# Ejemplo con ID (mejor opción)
USERNAME_INPUT = driver.find_element(By.ID, "user-name")

# Ejemplo con CSS (segunda mejor opción)
PASSWORD_INPUT = driver.find_element(By.CSS_SELECTOR, "input[data-test='password']")

# Ejemplo con XPath (usar solo si es necesario)
LOGIN_BUTTON = driver.find_element(By.XPATH, "//input[@value='Login']")
```

## 🤝 Contribución
1. Fork el proyecto
2. Crea tu rama de feature
   ```bash
   git checkout -b feature/NuevaCaracteristica
   ```
3. Commit tus cambios
   ```bash
   git commit -m 'Agrega nueva característica'
   ```
4. Push a la rama
   ```bash
   git push origin feature/NuevaCaracteristica
   ```
5. Crea un Pull Request

## 🐛 Reporte de Bugs
Si encuentras un bug, por favor crea un issue con:
- Descripción detallada del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots (si aplica)

## 📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles

## 🙋‍♂️ Autor
[Javier Villalta](https://github.com/javice)

## 🔗 Enlaces Útiles
- [Documentación de Selenium](https://www.selenium.dev/documentation/)
- [Documentación de Pytest](https://docs.pytest.org/)
- [Documentación de Allure](https://docs.qameta.io/allure/)
- [SauceDemo](https://www.saucedemo.com)
