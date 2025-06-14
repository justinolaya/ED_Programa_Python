def main():
    """Main con bucle para probar múltiples ecuaciones diferenciales ordinarias"""
    
    # Importar las funciones necesarias
    from dev.parsear_edo import parsear_edo
    from dev.exacta import exacta
    
    print("=" * 60)
    print("PROBADOR DE ECUACIONES DIFERENCIALES EXACTAS")
    print("=" * 60)
    print("Formato: M(x,y) dx + N(x,y) dy = 0")
    print("Ejemplos:")
    print("  • 2xy dx + x^2 dy = 0")
    print("  • (3x^2 + 2y) dx + (2x + 4y) dy = 0")
    print("  • y dx + x dy = 0")
    print("  • (2x + y) dx + (x + 2y) dy = 0")
    print("Escribe 'salir' para terminar")
    print("-" * 60)
    
    contador = 1
    
    while True:
        print(f"\n[ECUACIÓN #{contador}]")
        entrada = input("Ingresa la EDO: ").strip()
        
        # Condición de salida
        if entrada.lower() in ['salir', 'exit', 'quit', 's', 'q']:
            print("\n🚪 Saliendo del programa...")
            break
            
        # Verificar entrada vacía
        if not entrada:
            print("⚠️  Entrada vacía. Intenta de nuevo.")
            continue
            
        try:
            print(f"\n🔍 Procesando: {entrada}")
            
            # Parsear la ecuación
            M, N = parsear_edo(entrada)
            print(f"\n📋 Resultado del parseo:")
            print(f"   M(x,y) = {M}")
            print(f"   N(x,y) = {N}")
            
            # Verificar exactitud
            es_exacta = exacta(M, N)
            
            print(f"\n🎯 RESULTADO:")
            if es_exacta:
                print("   ✅ La ecuación ES EXACTA")
            else:
                print("   ❌ La ecuación NO ES EXACTA")
                
        except ValueError as e:
            print(f"\n❌ ERROR DE FORMATO: {e}")
            print("   Verifica la sintaxis de tu ecuación")
            
        except Exception as e:
            print(f"\n💥 ERROR INESPERADO: {e}")
            print("   Algo salió mal durante el procesamiento")
            
        finally:
            contador += 1
            print("-" * 60)
    
    print(f"\n📊 Total de ecuaciones procesadas: {contador - 1}")
    print("¡Gracias por usar el probador de EDOs! 👋")

if __name__ == "__main__":
    main()