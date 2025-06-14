def main():
    """Main con bucle para probar múltiples ecuaciones diferenciales ordinarias"""
    from dev.parsear_edo import parsear_edo
    from dev.exacta import exacta
    from dev.casos.caso1 import caso1
    from dev.casos.caso2 import caso2
    from dev.casos.caso3 import caso3
    from sympy import symbols

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
    x, y = symbols('x y')

    while True:
        print(f"\n[ECUACIÓN #{contador}]")
        entrada = input("Ingresa la EDO: ").strip()

        if entrada.lower() in ['salir', 'exit', 'quit', 's', 'q']:
            print("\n🚪 Saliendo del programa...")
            break

        if not entrada:
            print("⚠️  Entrada vacía. Intenta de nuevo.")
            continue

        try:
            print(f"\n🔍 Procesando: {entrada}")
            M, N = parsear_edo(entrada)
            print(f"\n📋 Resultado del parseo:")
            print(f"   M(x,y) = {M}")
            print(f"   N(x,y) = {N}")

            # 1. Verificar exactitud
            es_exacta = exacta(M, N, x, y)
            print(f"\n🎯 RESULTADO:")
            if es_exacta:
                print("   ✅ La ecuación ES EXACTA")
            else:
                print("   ❌ La ecuación NO ES EXACTA")
                # 2. Caso 1: factor integrante función de x
                factor1, exacta1 = caso1(M, N, x, y)
                if exacta1:
                    print("   ✅ Se encontró factor integrante en el CASO 1 y la ecuación es exacta.")
                else:
                    # 3. Caso 2: factor integrante función de y
                    factor2, exacta2 = caso2(M, N, x, y)
                    if exacta2:
                        print("   ✅ Se encontró factor integrante en el CASO 2 y la ecuación es exacta.")
                    else:
                        # 4. Caso 3: factor integrante x^m*y^n
                        factor3, exacta3 = caso3(M, N, x, y)
                        if exacta3:
                            print("   ✅ Se encontró factor integrante en el CASO 3 y la ecuación es exacta.")
                        else:
                            print("   ❌ No se encontró factor integrante por ninguno de los 3 métodos. La EDO no puede hacerse exacta por estos métodos.")

        except ValueError as e:
            print(f"\n❌ ERROR DE FORMATO: {e}")
            print("   Verifica la sintaxis de tu ecuación")
        except Exception as e:
            print(f"\n💥 ERROR INESPERADO: {e}")
            print("   Algo salió mal durante el procesamiento")

        contador += 1
        print("-" * 60)

    print(f"\n📊 Total de ecuaciones procesadas: {contador - 1}")
    print("¡Gracias por usar el probador de EDOs! 👋")

if __name__ == "__main__":
    main()