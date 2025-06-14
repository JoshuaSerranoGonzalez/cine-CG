import sqlite3

class DatabaseManager:
    def __init__(self, db_name="cine.db"):
        self.db_name = db_name
        self.crear_base_datos()
    
    def conectar(self):
        """Crear conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def crear_base_datos(self):
        """Crear todas las tablas e insertar datos iniciales"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Activar claves foráneas
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Crear tablas
        self._crear_tablas(cursor)
        
        # Insertar datos iniciales si no existen
        self._insertar_datos_iniciales(cursor)
        
        conn.commit()
        conn.close()
    
    def _crear_tablas(self, cursor):
        """Crear todas las tablas del sistema"""
        tablas_sql = """
        CREATE TABLE IF NOT EXISTS Usuario (
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreUsuario TEXT NOT NULL,
            clave TEXT NOT NULL,
            tipoUsuario TEXT NOT NULL CHECK (tipoUsuario IN ('Cliente', 'Administrador'))
        );
        
        CREATE TABLE IF NOT EXISTS Genero (
            idGenero INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreGenero TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS TipoAudiencia (
            idAudiencia INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS Pelicula (
            idPelicula INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            idGenero INTEGER,
            idAudiencia INTEGER,
            FOREIGN KEY (idGenero) REFERENCES Genero(idGenero),
            FOREIGN KEY (idAudiencia) REFERENCES TipoAudiencia(idAudiencia)
        );
        
        CREATE TABLE IF NOT EXISTS Sala (
            idSala INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreSala TEXT,
            capacidad INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS Asiento (
            idAsiento INTEGER PRIMARY KEY AUTOINCREMENT,
            idSala INTEGER,
            codigo TEXT NOT NULL,
            FOREIGN KEY (idSala) REFERENCES Sala(idSala)
        );
        
        CREATE TABLE IF NOT EXISTS Empleado (
            idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT,
            idUsuario INTEGER UNIQUE,
            rol TEXT NOT NULL,
            FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
        );
        
        CREATE TABLE IF NOT EXISTS Horario (
            idHorario INTEGER PRIMARY KEY AUTOINCREMENT,
            idPelicula INTEGER,
            idSala INTEGER,
            fecha TEXT,
            hora TEXT,
            FOREIGN KEY (idPelicula) REFERENCES Pelicula(idPelicula),
            FOREIGN KEY (idSala) REFERENCES Sala(idSala)
        );
        
        CREATE TABLE IF NOT EXISTS Entrada (
            idEntrada INTEGER PRIMARY KEY AUTOINCREMENT,
            idHorario INTEGER,
            idUsuario INTEGER,
            idAsiento INTEGER,
            precio REAL,
            FOREIGN KEY (idHorario) REFERENCES Horario(idHorario),
            FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
            FOREIGN KEY (idAsiento) REFERENCES Asiento(idAsiento)
        );
        
        CREATE TABLE IF NOT EXISTS MetodoPago (
            idMetodoPago INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT
        );
        
        CREATE TABLE IF NOT EXISTS Boleta (
            idBoleta INTEGER PRIMARY KEY AUTOINCREMENT,
            idEntrada INTEGER,
            idMetodoPago INTEGER,
            fechaCompra TEXT DEFAULT CURRENT_TIMESTAMP,
            total REAL,
            FOREIGN KEY (idEntrada) REFERENCES Entrada(idEntrada),
            FOREIGN KEY (idMetodoPago) REFERENCES MetodoPago(idMetodoPago)
        );
        
        CREATE TABLE IF NOT EXISTS Confite (
            idConfite INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL
        );
        
        CREATE TABLE IF NOT EXISTS BoletaConfite (
            idBoleta INTEGER,
            idConfite INTEGER,
            cantidad INTEGER,
            PRIMARY KEY (idBoleta, idConfite),
            FOREIGN KEY (idBoleta) REFERENCES Boleta(idBoleta),
            FOREIGN KEY (idConfite) REFERENCES Confite(idConfite)
        );
        """
        
        cursor.executescript(tablas_sql)
    
    def _insertar_datos_iniciales(self, cursor):
        """Insertar datos iniciales si las tablas están vacías"""
        # Verificar si ya existen datos
        cursor.execute("SELECT COUNT(*) FROM Genero")
        if cursor.fetchone()[0] == 0:
            # Insertar datos iniciales
            datos_iniciales = """
            INSERT INTO Genero (nombreGenero) VALUES ('Acción'), ('Comedia'), ('Terror');
            
            INSERT INTO TipoAudiencia (descripcion) VALUES ('Toda Audiencia'), ('+14'), ('+18');
            
            INSERT INTO Pelicula (titulo, duracion, idGenero, idAudiencia)
            VALUES ('Matrix', 120, 1, 2), ('Toy Story', 90, 2, 1);
            
            INSERT INTO Sala (nombreSala, capacidad)
            VALUES ('Sala 1', 100), ('Sala 2', 50);
            
            INSERT INTO Usuario (nombreUsuario, clave, tipoUsuario)
            VALUES ('juan123', 'pass123', 'Cliente'), ('admin1', 'adminpass', 'Administrador');
            
            INSERT INTO Horario (idPelicula, idSala, fecha, hora)
            VALUES (1, 1, '2025-06-10', '18:00'), (2, 2, '2025-06-10', '16:00');
            
            INSERT INTO Confite (nombre, precio)
            VALUES ('Popcorn', 3.50), ('Coca Cola', 2.00);
            
            INSERT INTO MetodoPago (descripcion) VALUES
            ('Efectivo'), ('Tarjeta Débito'), ('Tarjeta Crédito'), ('Transferencia'), ('Pago QR');
            
            INSERT INTO Asiento (idSala, codigo) VALUES
            (1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
            (1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5'),
            (1, 'C1'), (1, 'C2'), (1, 'C3'), (1, 'C4'), (1, 'C5'),
            (2, 'A1'), (2, 'A2'), (2, 'A3'), (2, 'A4'), (2, 'A5'),
            (2, 'B1'), (2, 'B2'), (2, 'B3'), (2, 'B4'), (2, 'B5'),
            (2, 'C1'), (2, 'C2'), (2, 'C3'), (2, 'C4'), (2, 'C5');
            
            INSERT INTO Empleado (idUsuario, rol) VALUES (2, 'Administrador General');
            """
            