from sympy import symbols
from dev.parsear_edo import parsear_edo
from dev.exacta import exacta

def main():
    print("=== VERIFICADOR DE ECUACIONES DIFERENCIALES EXACTAS ===")
    print("Ejemplos: 2xy dx + x^2 dy = 0")
    print("         (x - y + 1) dx - dy = 0")
    print("         3x^2 dx + 2y dy = 0")
    print("Escribe 'salir', 'exit' o 'q' para terminar\n")
    
    while True:
        try:
            # Solicitar entrada
            entrada = input("EDO: ").strip()
            
            # Comandos para salir
            if entrada.lower() in ['salir', 'exit', 'q', 'quit']:
                print("¡Hasta luego! 👋")
                break
            
            # Validar que no esté vacía
            if not entrada:
                print("⚠️  Por favor ingresa una ecuación diferencial.\n")
                continue
            
            # Procesar la EDO
            M, N = parsear_edo(entrada)
            
            print("\nVerificando si la ecuación es exacta...")
            if exacta(M, N):
                print("✅ La ecuación es exacta.")
            else:
                print("❌ La ecuación NO es exacta.")
                
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! 👋")
            break
        except Exception as e:
            print(f"[ERROR] Fallo al procesar la EDO: {e}")
        
        # Separador visual
        print("-" * 50)

if __name__ == "__main__":
    main()