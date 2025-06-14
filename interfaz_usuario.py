from servicios_del_cine import CinemaServices

class UserInterface:
    def __init__(self, cinema_services):
        self.cinema_services = cinema_services
        self.usuario_actual = None
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal"""
        print("\n" + "="*50)
        print("🎬 SISTEMA DE CINE 🎬")
        print("="*50)
        print("1. Iniciar sesión")
        print("2. Ver cartelera")
        print("3. Salir")
        print("-"*50)
    
    def mostrar_menu_cliente(self):
        """Mostrar menú para clientes"""
        print("\n" + "="*50)
        print(f"🎬 BIENVENIDO {self.usuario_actual[1]} 🎬")
        print("="*50)
        print("1. Ver cartelera")
        print("2. Comprar entrada")
        print("3. Ver mis boletas")
        print("4. Cerrar sesión")
        print("-"*50)
    
    def mostrar_menu_administrador(self):
        """Mostrar menú para administradores"""
        print("\n" + "="*50)
        print(f"👑 PANEL DE ADMINISTRACIÓN - {self.usuario_actual[1]} 👑")
        print("="*50)
        print("1. Gestionar Películas")
        print("2. Gestionar Asientos")
        print("3. Gestionar Horarios")
        print("4. Ver cartelera")
        print("5. Cerrar sesión")
        print("-"*50)
    
    def gestionar_peliculas(self):
        """Gestionar películas"""
        while True:
            print("\n" + "="*50)
            print("🎬 GESTIÓN DE PELÍCULAS 🎬")
            print("="*50)
            print("1. Agregar película")
            print("2. Ver películas")
            print("3. Volver")
            print("-"*50)
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.agregar_pelicula()
            elif opcion == "2":
                self.ver_peliculas()
            elif opcion == "3":
                break
            else:
                print("❌ Opción inválida")
    
    def agregar_pelicula(self):
        """Agregar una nueva película"""
        print("\n=== AGREGAR PELÍCULA ===")
        titulo = input("Título de la película: ")
        duracion = input("Duración (en minutos): ")
        
        # Mostrar géneros disponibles
        generos = self.cinema_services.obtener_generos()
        print("\nGéneros disponibles:")
        for genero in generos:
            print(f"{genero[0]}. {genero[1]}")
        
        id_genero = input("Selecciona el género (ID): ")
        
        # Mostrar tipos de audiencia
        audiencias = self.cinema_services.obtener_tipos_audiencia()
        print("\nTipos de audiencia:")
        for audiencia in audiencias:
            print(f"{audiencia[0]}. {audiencia[1]}")
        
        id_audiencia = input("Selecciona el tipo de audiencia (ID): ")
        
        try:
            resultado = self.cinema_services.agregar_pelicula(
                titulo, int(duracion), int(id_genero), int(id_audiencia)
            )
            if resultado:
                print("✅ Película agregada exitosamente")
            else:
                print("❌ Error al agregar la película")
        except ValueError:
            print("❌ Por favor ingresa valores numéricos válidos")
    
    def ver_peliculas(self):
        """Ver lista de películas"""
        peliculas = self.cinema_services.obtener_peliculas()
        
        if not peliculas:
            print("No hay películas registradas")
            return
        
        print("\n" + "="*80)
        print("🎬 LISTA DE PELÍCULAS 🎬")
        print("="*80)
        print(f"{'ID':<4} {'TÍTULO':<30} {'DURACIÓN':<10} {'GÉNERO':<15} {'AUDIENCIA':<15}")
        print("-"*80)
        
        for pelicula in peliculas:
            print(f"{pelicula[0]:<4} {pelicula[1]:<30} {pelicula[2]:<10} {pelicula[3]:<15} {pelicula[4]:<15}")
    
    def gestionar_asientos(self):
        """Gestionar asientos"""
        while True:
            print("\n" + "="*50)
            print("🪑 GESTIÓN DE ASIENTOS 🪑")
            print("="*50)
            print("1. Ver asientos por sala")
            print("2. Eliminar asiento")
            print("3. Volver")
            print("-"*50)
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.ver_asientos_sala()
            elif opcion == "2":
                self.eliminar_asiento()
            elif opcion == "3":
                break
            else:
                print("❌ Opción inválida")
    
    def ver_asientos_sala(self):
        """Ver asientos por sala"""
        salas = self.cinema_services.obtener_salas()
        
        if not salas:
            print("No hay salas registradas")
            return
        
        print("\nSalas disponibles:")
        for sala in salas:
            print(f"{sala[0]}. {sala[1]} (Capacidad: {sala[2]})")
        
        try:
            id_sala = int(input("\nSelecciona una sala (ID): "))
            asientos = self.cinema_services.obtener_asientos_sala(id_sala)
            
            if not asientos:
                print("No hay asientos en esta sala")
                return
            
            print("\n" + "="*50)
            print(f"🪑 ASIENTOS - SALA {id_sala} 🪑")
            print("="*50)
            print(f"{'ID':<4} {'CÓDIGO':<10}")
            print("-"*50)
            
            for asiento in asientos:
                print(f"{asiento[0]:<4} {asiento[1]:<10}")
                
        except ValueError:
            print("❌ Por favor ingresa un ID válido")
    
    def eliminar_asiento(self):
        """Eliminar un asiento"""
        self.ver_asientos_sala()
        
        try:
            id_asiento = int(input("\nIngresa el ID del asiento a eliminar: "))
            resultado = self.cinema_services.eliminar_asiento(id_asiento)
            
            if resultado:
                print("✅ Asiento eliminado exitosamente")
            else:
                print("❌ Error al eliminar el asiento")
        except ValueError:
            print("❌ Por favor ingresa un ID válido")
    
    def gestionar_horarios(self):
        """Gestionar horarios"""
        while True:
            print("\n" + "="*50)
            print("⏰ GESTIÓN DE HORARIOS ⏰")
            print("="*50)
            print("1. Agregar horario")
            print("2. Ver horarios")
            print("3. Eliminar horario")
            print("4. Volver")
            print("-"*50)
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.agregar_horario()
            elif opcion == "2":
                self.ver_horarios()
            elif opcion == "3":
                self.eliminar_horario()
            elif opcion == "4":
                break
            else:
                print("❌ Opción inválida")
    
    def agregar_horario(self):
        """Agregar un nuevo horario"""
        print("\n=== AGREGAR HORARIO ===")
        
        # Mostrar películas
        self.ver_peliculas()
        id_pelicula = input("\nSelecciona la película (ID): ")
        
        # Mostrar salas
        salas = self.cinema_services.obtener_salas()
        print("\nSalas disponibles:")
        for sala in salas:
            print(f"{sala[0]}. {sala[1]} (Capacidad: {sala[2]})")
        
        id_sala = input("Selecciona la sala (ID): ")
        fecha = input("Fecha (YYYY-MM-DD): ")
        hora = input("Hora (HH:MM): ")
        
        try:
            resultado = self.cinema_services.agregar_horario(
                int(id_pelicula), int(id_sala), fecha, hora
            )
            if resultado:
                print("✅ Horario agregado exitosamente")
            else:
                print("❌ Error al agregar el horario")
        except ValueError:
            print("❌ Por favor ingresa valores válidos")
    
    def ver_horarios(self):
        """Ver todos los horarios"""
        horarios = self.cinema_services.obtener_horarios()
        
        if not horarios:
            print("No hay horarios registrados")
            return
        
        print("\n" + "="*100)
        print("⏰ HORARIOS DISPONIBLES ⏰")
        print("="*100)
        print(f"{'ID':<4} {'PELÍCULA':<30} {'SALA':<10} {'FECHA':<12} {'HORA':<8}")
        print("-"*100)
        
        for horario in horarios:
            print(f"{horario[0]:<4} {horario[1]:<30} {horario[2]:<10} {horario[3]:<12} {horario[4]:<8}")
    
    def eliminar_horario(self):
        """Eliminar un horario"""
        self.ver_horarios()
        
        try:
            id_horario = int(input("\nIngresa el ID del horario a eliminar: "))
            resultado = self.cinema_services.eliminar_horario(id_horario)
            
            if resultado:
                print("✅ Horario eliminado exitosamente")
            else:
                print("❌ Error al eliminar el horario")
        except ValueError:
            print("❌ Por favor ingresa un ID válido")
    
    def iniciar_sesion(self):
        """Proceso de inicio de sesión"""
        print("\n=== INICIAR SESIÓN ===")
        nombre_usuario = input("Usuario: ")
        clave = input("Contraseña: ")
        
        usuario = self.cinema_services.verificar_usuario(nombre_usuario, clave)
        
        if usuario:
            self.usuario_actual = (usuario[0], nombre_usuario, usuario[1])
            print(f"¡Bienvenido {nombre_usuario}!")
            return True
        else:
            print("❌ Usuario o contraseña incorrectos")
            return False
    
    def mostrar_cartelera(self):
        """Mostrar películas y horarios"""
        print("\n" + "="*80)
        print("🎭 CARTELERA 🎭")
        print("="*80)
        
        peliculas = self.cinema_services.ver_peliculas_horarios()
        
        if not peliculas:
            print("No hay películas disponibles")
            return
        
        print(f"{'ID':<4} {'PELÍCULA':<20} {'FECHA':<12} {'HORA':<8} {'SALA':<10}")
        print("-"*80)
        
        for pelicula in peliculas:
            print(f"{pelicula[0]:<4} {pelicula[1]:<20} {pelicula[2]:<12} {pelicula[3]:<8} {pelicula[4]:<10}")
    
    def seleccionar_asientos(self):
        """Proceso de selección de asientos y compra"""
        self.mostrar_cartelera()
        
        try:
            id_horario = int(input("\nIngresa el ID de la función: "))
            
            # Verificar que el horario existe
            info_horario = self.cinema_services.obtener_info_horario(id_horario)
            if not info_horario:
                print("❌ Horario no encontrado")
                return
            
            print(f"\n🎬 {info_horario[0]} - {info_horario[1]} {info_horario[2]} - {info_horario[3]}")
            
            # Mostrar asientos disponibles
            asientos = self.cinema_services.ver_asientos_disponibles(id_horario)
            
            if not asientos:
                print("❌ No hay asientos disponibles para esta función")
                return
            
            print("\n🪑 ASIENTOS DISPONIBLES:")
            print(f"{'ID':<4} {'ASIENTO':<8} {'SALA':<10}")
            print("-"*25)
            
            for asiento in asientos:
                print(f"{asiento[0]:<4} {asiento[1]:<8} {asiento[2]:<10}")
            
            # Seleccionar asiento
            id_asiento = int(input("\nIngresa el ID del asiento: "))
            
            # Verificar que el asiento existe y está disponible
            asiento_valido = any(asiento[0] == id_asiento for asiento in asientos)
            if not asiento_valido:
                print("❌ Asiento no válido o no disponible")
                return
            
            precio = 8.50
            print(f"\n💰 Precio de la entrada: ${precio}")
            
            # Confirmar compra
            confirmar = input("¿Confirmar compra? (s/n): ").lower()
            if confirmar != 's':
                print("Compra cancelada")
                return
            
            # Procesar compra
            self.procesar_compra(id_horario, id_asiento, precio)
            
        except ValueError:
            print("❌ Por favor ingresa números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def procesar_compra(self, id_horario, id_asiento, precio):
        """Procesar la compra de entrada"""
        # Comprar entrada
        id_entrada, mensaje = self.cinema_services.comprar_entrada(
            id_horario, self.usuario_actual[0], id_asiento, precio
        )
        
        if not id_entrada:
            print(f"❌ {mensaje}")
            return
        
        print(f"✅ {mensaje}")
        
        # Mostrar métodos de pago
        print("\n💳 MÉTODOS DE PAGO:")
        metodos_pago = self.cinema_services.obtener_metodos_pago()
        
        for metodo in metodos_pago:
            print(f"{metodo[0]}. {metodo[1]}")
        
        try:
            id_metodo_pago = int(input("Selecciona método de pago: "))
            
            # Verificar método de pago válido
            metodo_valido = any(metodo[0] == id_metodo_pago for metodo in metodos_pago)
            if not metodo_valido:
                print("❌ Método de pago no válido")
                return
            
            # Crear boleta
            id_boleta, mensaje_boleta = self.cinema_services.crear_boleta(id_entrada, id_metodo_pago, precio)
            
            if id_boleta:
                print(f"✅ {mensaje_boleta}")
                print(f"🎫 Número de boleta: {id_boleta}")
                
                # Mostrar boleta
                input("\nPresiona Enter para ver tu boleta...")
                self.mostrar_boleta(id_boleta)
            else:
                print(f"❌ {mensaje_boleta}")
                
        except ValueError:
            print("❌ Método de pago inválido")
    
    def mostrar_boleta(self, id_boleta):
        """Mostrar información de la boleta"""
        boleta = self.cinema_services.ver_boleta_completa(id_boleta)
        
        if not boleta:
            print("❌ Boleta no encontrada")
            return
        
        print("\n" + "="*50)
        print("🎫 BOLETA DE ENTRADA 🎫")
        print("="*50)
        print(f"Boleta #: {boleta[0]}")
        print(f"Cliente: {boleta[1]}")
        print(f"Película: {boleta[2]}")
        print(f"Fecha: {boleta[3]}")
        print(f"Hora: {boleta[4]}")
        print(f"Sala: {boleta[5]}")
        print(f"Asiento: {boleta[6]}")
        print(f"Método de pago: {boleta[9]}")
        print(f"Fecha de compra: {boleta[8]}")
        print("-"*50)
        print(f"TOTAL: ${boleta[7]}")
        print("="*50)
    
    def ver_mis_boletas(self):
        """Ver boletas del usuario actual"""
        print("\n=== MIS BOLETAS ===")
        id_boleta = input("Ingresa el número de boleta (o 'q' para volver): ")
        
        if id_boleta.lower() == 'q':
            return
        
        try:
            self.mostrar_boleta(int(id_boleta))
        except ValueError:
            print("❌ Número de boleta inválido")
    
    def ejecutar(self):
        """Ejecutar el programa principal"""
        print("🎬 ¡Bienvenido al Sistema de Cine! 🎬")
        
        while True:
            if not self.usuario_actual:
                self.mostrar_menu_principal()
                opcion = input("Selecciona una opción: ")
                
                if opcion == "1":
                    self.iniciar_sesion()
                elif opcion == "2":
                    self.mostrar_cartelera()
                    input("\nPresiona Enter para continuar...")
                elif opcion == "3":
                    print("¡Hasta luego! 👋")
                    break
                else:
                    print("❌ Opción inválida")
            
            else:
                # Usuario logueado
                if self.usuario_actual[2] == 'Administrador':
                    self.mostrar_menu_administrador()
                    opcion = input("Selecciona una opción: ")
                    
                    if opcion == "1":
                        self.gestionar_peliculas()
                    elif opcion == "2":
                        self.gestionar_asientos()
                    elif opcion == "3":
                        self.gestionar_horarios()
                    elif opcion == "4":
                        self.mostrar_cartelera()
                        input("\nPresiona Enter para continuar...")
                    elif opcion == "5":
                        print(f"¡Hasta luego {self.usuario_actual[1]}! 👋")
                        self.usuario_actual = None
                    else:
                        print("❌ Opción inválida")
                else:
                    self.mostrar_menu_cliente()
                    opcion = input("Selecciona una opción: ")
                    
                    if opcion == "1":
                        self.mostrar_cartelera()
                        input("\nPresiona Enter para continuar...")
                    elif opcion == "2":
                        self.seleccionar_asientos()
                        input("\nPresiona Enter para continuar...")
                    elif opcion == "3":
                        self.ver_mis_boletas()
                        input("\nPresiona Enter para continuar...")
                    elif opcion == "4":
                        print(f"¡Hasta luego {self.usuario_actual[1]}! 👋")
                        self.usuario_actual = None
                    else:
                        print("❌ Opción inválida")