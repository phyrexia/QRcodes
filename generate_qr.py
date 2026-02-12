#!/usr/bin/env python3
"""
Generador de códigos QR personalizados con logo MG
Inspirado en los códigos QR coloridos de Microsoft
"""

import segno
from PIL import Image
import os
from pathlib import Path

class MGQRGenerator:
    """Generador de códigos QR con branding MG"""
    
    def __init__(self, logo_path="logos/mg_logo.png", base_url="https://mg-brand.com/p/"):
        """
        Inicializa el generador de QR
        
        Args:
            logo_path: Ruta al logo MG
            base_url: URL base para los productos
        """
        self.logo_path = logo_path
        self.base_url = base_url
        self.output_dir = Path("generated")
        self.output_dir.mkdir(exist_ok=True)
        
    def create_product_qr(self, product_id, product_name, color_scheme="blue", 
                         size=10, border=2):
        """
        Crea un código QR para un producto específico
        
        Args:
            product_id: ID único del producto (ej: "001-L")
            product_name: Nombre del producto para el archivo
            color_scheme: Esquema de color ("blue", "green", "red", "purple", "orange")
            size: Tamaño del QR (escala)
            border: Borde del QR (módulos)
            
        Returns:
            Ruta del archivo generado
        """
        # URL del producto
        url = f"{self.base_url}{product_id}"
        
        # Crear el código QR con corrección de error alta (necesaria para logo)
        qr = segno.make(url, error='h', mode='byte')
        
        # Definir esquemas de color
        color_schemes = {
            "blue": {"dark": "#0078D4", "light": "#E6F2FF"},
            "green": {"dark": "#107C10", "light": "#E6F7E6"},
            "red": {"dark": "#D83B01", "light": "#FFE6E6"},
            "purple": {"dark": "#5C2D91", "light": "#F4E6FF"},
            "orange": {"dark": "#F7630C", "light": "#FFF0E6"},
            "teal": {"dark": "#008272", "light": "#E6F7F5"},
        }
        
        colors = color_schemes.get(color_scheme, color_schemes["blue"])
        
        # Nombre del archivo
        filename = self.output_dir / f"qr_{product_name}_{product_id}.png"
        
        # Guardar QR con colores personalizados
        qr.save(
            filename,
            scale=size,
            border=border,
            dark=colors["dark"],
            light=colors["light"]
        )
        
        # Añadir logo en el centro
        if os.path.exists(self.logo_path):
            self._add_logo(filename)
        
        print(f"✓ QR generado: {filename}")
        print(f"  URL: {url}")
        print(f"  Color: {color_scheme}")
        
        return filename
    
    def _add_logo(self, qr_path):
        """
        Añade el logo MG en el centro del código QR
        
        Args:
            qr_path: Ruta del archivo QR
        """
        # Abrir QR e imagen del logo
        qr_img = Image.open(qr_path).convert("RGBA")
        logo = Image.open(self.logo_path).convert("RGBA")
        
        # Calcular tamaño del logo (aproximadamente 20% del QR)
        qr_width, qr_height = qr_img.size
        logo_size = int(min(qr_width, qr_height) * 0.2)
        
        # Redimensionar logo manteniendo proporción
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Crear un fondo blanco para el logo
        logo_bg_size = int(logo_size * 1.2)
        logo_bg = Image.new('RGBA', (logo_bg_size, logo_bg_size), 'white')
        
        # Centrar logo en el fondo blanco
        logo_pos = ((logo_bg_size - logo.size[0]) // 2, 
                    (logo_bg_size - logo.size[1]) // 2)
        logo_bg.paste(logo, logo_pos, logo)
        
        # Calcular posición central en el QR
        pos = ((qr_width - logo_bg_size) // 2, (qr_height - logo_bg_size) // 2)
        
        # Pegar el logo con fondo en el QR
        qr_img.paste(logo_bg, pos, logo_bg)
        
        # Guardar
        qr_img.save(qr_path)
    
    def batch_generate(self, products):
        """
        Genera múltiples códigos QR de una vez
        
        Args:
            products: Lista de diccionarios con información del producto
                     Ejemplo: [{"id": "001-L", "name": "camisa_azul", "color": "blue"}]
        """
        print(f"\n🚀 Generando {len(products)} códigos QR...\n")
        
        generated = []
        for product in products:
            try:
                filename = self.create_product_qr(
                    product_id=product["id"],
                    product_name=product["name"],
                    color_scheme=product.get("color", "blue")
                )
                generated.append(filename)
            except Exception as e:
                print(f"✗ Error generando {product['name']}: {e}")
        
        print(f"\n✅ Proceso completado: {len(generated)}/{len(products)} códigos generados")
        return generated


def main():
    """Ejemplo de uso"""
    
    # Crear generador
    generator = MGQRGenerator()
    
    # Productos de ejemplo
    productos_ejemplo = [
        {"id": "001-L", "name": "camisa_azul_L", "color": "blue"},
        {"id": "001-M", "name": "camisa_azul_M", "color": "blue"},
        {"id": "001-S", "name": "camisa_azul_S", "color": "blue"},
        {"id": "002-L", "name": "pantalon_negro_L", "color": "purple"},
        {"id": "002-M", "name": "pantalon_negro_M", "color": "purple"},
        {"id": "003-L", "name": "chaqueta_roja_L", "color": "red"},
        {"id": "003-M", "name": "chaqueta_roja_M", "color": "red"},
        {"id": "004-L", "name": "zapatos_marron_L", "color": "orange"},
        {"id": "005-L", "name": "bufanda_verde_L", "color": "green"},
        {"id": "006-L", "name": "gorra_azul_L", "color": "teal"},
    ]
    
    # Generar todos los códigos
    generator.batch_generate(productos_ejemplo)
    
    print("\n" + "="*60)
    print("📱 Para escanear estos códigos:")
    print("   1. Usa cualquier app de lectura de QR")
    print("   2. El QR redirigirá a: https://mg-brand.com/p/[ID-PRODUCTO]")
    print("   3. Tu app puede capturar el ID del producto de la URL")
    print("="*60)


if __name__ == "__main__":
    main()
