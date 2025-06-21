"""
Sistema de Cine - Programa Principal
====================================

Este es el archivo principal que ejecuta el sistema de cine.
Para ejecutar el programa, usa: python main.py

Estructura del proyecto:
- main.py: Archivo principal
- database_manager.py: Gestión de la base de datos
- servicios_del_cine.py: Servicios y lógica de negocio
- interfaz_usuario.py: Interfaz de usuario

Usuarios de prueba:
- Cliente: usuario 'juan123', contraseña 'pass123'
- Admin: usuario 'admin1', contraseña 'adminpass adadada'
"""

import sys
import logging
from interfaz_usuario import UserInterface
from database_manager import DatabaseManager
from servicios_del_cine import CinemaServices

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cine.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    """Función principal del programa"""
    try:
        print("\n🎬 Bienvenido al Sistema de Cine 🎬")
        print("=====================================")
        
        # Inicializar componentes con manejo de errores
        try:
            db_manager = DatabaseManager()
            if not db_manager.verificar_conexion():
                raise Exception("No se pudo conectar a la base de datos")
            
            cinema_services = CinemaServices(db_manager)
            if not cinema_services:
                raise Exception("Error al inicializar los servicios del cine")
            
            # Crear instancia de la interfaz de usuario
            app = UserInterface(cinema_services)
            if not app:
                raise Exception("Error al inicializar la interfaz de usuario")
            
            # Ejecutar la aplicación
            app.ejecutar()
            
        except Exception as e:
            error_msg = f"Error en la inicialización del sistema: {str(e)}"
            print(f"\n❌ {error_msg}")
            logging.error(error_msg, exc_info=True)
            return
        
    except KeyboardInterrupt:
        print("\n\n🛑 Programa interrumpido por el usuario")
        logging.info("Programa interrumpido por el usuario")
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"\n❌ {error_msg}")
        logging.error(error_msg, exc_info=True)
        print("Por favor, reporta este error al administrador")
    finally:
        print("\n👋 ¡Gracias por usar el Sistema de Cine!")

if __name__ == "__main__":
    main()