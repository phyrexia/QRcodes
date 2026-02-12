#!/usr/bin/env python3
"""
Script interactivo para personalizar la generación de códigos QR
"""

from generate_qr import MGQRGenerator
import json
from pathlib import Path

def load_products_from_csv(csv_path):
    """
    Carga productos desde un archivo CSV
    
    Formato CSV esperado:
    id,name,color
    001-L,camisa_azul_L,blue
    002-M,pantalon_negro_M,purple
    """
    import csv
    
    products = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                "id": row['id'],
                "name": row['name'],
                "color": row.get('color', 'blue')
            })
    
    return products

def load_products_from_json(json_path):
    """
    Carga productos desde un archivo JSON
    
    Formato JSON esperado:
    [
        {"id": "001-L", "name": "camisa_azul_L", "color": "blue"},
        {"id": "002-M", "name": "pantalon_negro_M", "color": "purple"}
    ]
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def interactive_mode():
    """Modo interactivo para crear un solo QR"""
    print("\n" + "="*60)
    print("🎨 GENERADOR INTERACTIVO DE CÓDIGOS QR MG")
    print("="*60 + "\n")
    
    # Solicitar información del producto
    product_id = input("📦 ID del producto (ej: 007-XL): ").strip()
    product_name = input("🏷️  Nombre para el archivo (ej: jersey_verde_XL): ").strip()
    
    # Mostrar opciones de color
    print("\n🎨 Esquemas de color disponibles:")
    colors = ["blue", "green", "red", "purple", "orange", "teal"]
    for i, color in enumerate(colors, 1):
        print(f"  {i}. {color}")
    
    color_choice = input("\nSelecciona un color (1-6) [1]: ").strip() or "1"
    try:
        color_index = int(color_choice) - 1
        if 0 <= color_index < len(colors):
            color_scheme = colors[color_index]
        else:
            color_scheme = "blue"
    except ValueError:
        color_scheme = "blue"
    
    # Crear generador y generar QR
    generator = MGQRGenerator()
    
    print(f"\n🚀 Generando código QR...")
    filename = generator.create_product_qr(
        product_id=product_id,
        product_name=product_name,
        color_scheme=color_scheme
    )
    
    print(f"\n✅ ¡Código QR generado exitosamente!")
    print(f"📁 Ubicación: {filename}")
    print("="*60 + "\n")

def batch_mode():
    """Modo batch desde archivo"""
    print("\n" + "="*60)
    print("📦 GENERADOR BATCH DE CÓDIGOS QR MG")
    print("="*60 + "\n")
    
    print("Formatos soportados:")
    print("  1. CSV (id,name,color)")
    print("  2. JSON (lista de objetos)\n")
    
    file_path = input("Ruta del archivo: ").strip()
    
    if not Path(file_path).exists():
        print(f"❌ Error: El archivo '{file_path}' no existe")
        return
    
    # Detectar tipo de archivo
    if file_path.endswith('.csv'):
        products = load_products_from_csv(file_path)
    elif file_path.endswith('.json'):
        products = load_products_from_json(file_path)
    else:
        print("❌ Error: Formato no soportado. Usa .csv o .json")
        return
    
    # Generar códigos
    generator = MGQRGenerator()
    generator.batch_generate(products)

def main():
    """Menú principal"""
    print("\n" + "="*60)
    print("🔷 SISTEMA DE CÓDIGOS QR MG")
    print("="*60 + "\n")
    
    print("Selecciona una opción:")
    print("  1. Modo interactivo (crear un QR)")
    print("  2. Modo batch (desde archivo CSV/JSON)")
    print("  3. Generar productos de ejemplo")
    print("  4. Salir\n")
    
    choice = input("Opción [1]: ").strip() or "1"
    
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        batch_mode()
    elif choice == "3":
        # Generar ejemplos por defecto
        from generate_qr import main as generate_examples
        generate_examples()
    elif choice == "4":
        print("\n👋 ¡Hasta luego!\n")
        return
    else:
        print("\n❌ Opción inválida\n")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
