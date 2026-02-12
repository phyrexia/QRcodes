# articulos
# Sistema de Códigos QR MG

Sistema para generar códigos QR personalizados con el logo MG y esquemas de colores, similar a los códigos QR de Microsoft. Cada código contiene información específica del producto que puede ser escaneada desde una app móvil.

## 🎯 Características

- ✅ **Logo MG centralizado** en cada código QR
- ✅ **Códigos de colores** para diferenciar productos/categorías
- ✅ **URLs estructuradas** para facilitar el escaneo desde apps
- ✅ **Generación masiva** de códigos con un solo script
- ✅ **Alta corrección de errores** (permite el logo sin afectar la lectura)

## 📋 Requisitos

```bash
pip install -r requirements.txt
```

## 🚀 Uso Rápido

### Generar códigos de ejemplo

```bash
python generate_qr.py
```

Esto generará 10 códigos QR de ejemplo en la carpeta `generated/` con diferentes colores y productos.

### Uso Programático

```python
from generate_qr import MGQRGenerator

# Crear generador
generator = MGQRGenerator()

# Generar un código QR individual
generator.create_product_qr(
    product_id="007-XL",
    product_name="jersey_verde_XL",
    color_scheme="green"
)

# Generar múltiples códigos
productos = [
    {"id": "008-M", "name": "vestido_rosa", "color": "purple"},
    {"id": "009-L", "name": "sombrero_gris", "color": "blue"},
]
generator.batch_generate(productos)
```

## 🎨 Esquemas de Color Disponibles

- `blue` (azul) - Color por defecto
- `green` (verde)
- `red` (rojo)
- `purple` (morado/púrpura)
- `orange` (naranja)
- `teal` (azul verdoso)

## 📱 Uso en App Móvil

### 1. Estructura de la URL

Cada código QR contiene una URL con esta estructura:

```
https://mg-brand.com/p/{ID-PRODUCTO}
```

Ejemplo: `https://mg-brand.com/p/001-L`

### 2. Leer el código en tu App

#### iOS (Swift)

```swift
import AVFoundation

func metadataOutput(_ output: AVCaptureMetadataOutput, 
                   didOutput metadataObjects: [AVMetadataObject], 
                   from connection: AVCaptureConnection) {
    if let metadataObject = metadataObjects.first {
        guard let readableObject = metadataObject as? AVMetadataMachineReadableCodeObject else { return }
        guard let stringValue = readableObject.stringValue else { return }
        
        // Extraer ID del producto de la URL
        if let productId = extractProductId(from: stringValue) {
            loadProductInfo(productId: productId)
        }
    }
}

func extractProductId(from url: String) -> String? {
    // https://mg-brand.com/p/001-L -> "001-L"
    let components = url.components(separatedBy: "/")
    return components.last
}
```

#### Android (Kotlin)

```kotlin
import com.google.mlkit.vision.barcode.Barcode
import com.google.mlkit.vision.barcode.BarcodeScanning

fun processBarcode(barcode: Barcode) {
    val url = barcode.rawValue ?: return
    
    // Extraer ID del producto
    val productId = url.substringAfterLast("/")
    
    // Cargar información del producto
    loadProductInfo(productId)
}
```

#### React Native

```javascript
import { RNCamera } from 'react-native-camera';

const onBarCodeRead = (e) => {
  const url = e.data;
  
  // Extraer ID del producto: https://mg-brand.com/p/001-L
  const productId = url.split('/').pop();
  
  // Cargar información del producto
  loadProductInfo(productId);
};

<RNCamera
  onBarCodeRead={onBarCodeRead}
  barCodeTypes={[RNCamera.Constants.BarCodeType.qr]}
/>
```

### 3. Backend/API

Tu app puede consultar información del producto usando el ID extraído:

```javascript
async function loadProductInfo(productId) {
  const response = await fetch(
    `https://api.mg-brand.com/products/${productId}`
  );
  const productData = await response.json();
  
  // productData contendrá:
  // - Nombre del producto
  // - Talla
  // - Precio
  // - Stock
  // - Imágenes
  // - etc.
  
  displayProduct(productData);
}
```

## 📁 Estructura del Proyecto

```
QRcodes/
├── generate_qr.py          # Script principal
├── requirements.txt        # Dependencias
├── README.md              # Esta documentación
├── logos/
│   └── mg_logo.png        # Logo MG
└── generated/             # Códigos QR generados
    ├── qr_camisa_azul_L_001-L.png
    ├── qr_pantalon_negro_L_002-L.png
    └── ...
```

## 🔧 Personalización

### Cambiar URL base

```python
generator = MGQRGenerator(base_url="https://tu-dominio.com/producto/")
```

### Cambiar tamaño del QR

```python
generator.create_product_qr(
    product_id="001-L",
    product_name="producto",
    size=15,  # Más grande
    border=4  # Más borde
)
```

### Usar tu propio logo

1. Reemplaza `logos/mg_logo.png` con tu logo
2. El logo debe ser PNG con fondo transparente
3. Recomendado: 500x500px o similar (cuadrado)

## 💡 Consejos

1. **Corrección de errores**: Usamos nivel 'H' (alta) para que el logo no afecte la lectura
2. **Tamaño del logo**: El logo ocupa ~20% del QR, dejando suficiente información para escanear
3. **Contraste**: Usa colores con suficiente contraste para facilitar el escaneo
4. **Pruebas**: Siempre prueba los códigos en diferentes apps de escaneo antes de imprimirlos

## 📊 Casos de Uso

- **Etiquetas de productos** en tiendas físicas
- **Catálogos impresos** con información digital
- **Inventario y trazabilidad** de productos
- **Campañas de marketing** con productos específicos
- **Control de autenticidad** de productos originales

## 🆘 Solución de Problemas

**El QR no se escanea:**
- Verifica que el tamaño sea al menos 300x300px para impresión
- Asegúrate de que haya suficiente contraste
- Prueba con diferentes apps de escaneo

**El logo está muy grande:**
- Modifica `logo_size` en el método `_add_logo()`
- Por defecto es 20% del tamaño del QR

**Quiero más colores:**
- Añade más esquemas en `color_schemes` dentro de `create_product_qr()`

## 📄 Licencia

Proyecto para uso interno de MG Brand.
