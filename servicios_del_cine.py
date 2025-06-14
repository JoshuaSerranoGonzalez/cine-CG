import sqlite3
from datetime import datetime
from database_manager import DatabaseManager

class CinemaServices:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def ver_peliculas_horarios(self):
        """Ver películas disponibles y sus horarios"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        query = """
        SELECT H.idHorario, P.titulo, H.fecha, H.hora, S.nombreSala
        FROM Pelicula P
        JOIN Horario H ON P.idPelicula = H.idPelicula
        JOIN Sala S ON H.idSala = S.idSala
        ORDER BY H.fecha, H.hora
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def ver_asientos_disponibles(self, id_horario):
        """Ver asientos disponibles para un horario específico"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            A.idAsiento,
            A.codigo AS Asiento,
            S.nombreSala
        FROM Asiento A
        JOIN Sala S ON A.idSala = S.idSala
        WHERE A.idAsiento NOT IN (
            SELECT E.idAsiento
            FROM Entrada E
            WHERE E.idHorario = ?
        )
        AND A.idSala = (
            SELECT H.idSala
            FROM Horario H
            WHERE H.idHorario = ?
        )
        ORDER BY A.codigo
        """
        
        cursor.execute(query, (id_horario, id_horario))
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def obtener_info_horario(self, id_horario):
        """Obtener información de un horario específico"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        query = """
        SELECT P.titulo, H.fecha, H.hora, S.nombreSala
        FROM Horario H
        JOIN Pelicula P ON H.idPelicula = P.idPelicula
        JOIN Sala S ON H.idSala = S.idSala
        WHERE H.idHorario = ?
        """
        
        cursor.execute(query, (id_horario,))
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado
    
    def comprar_entrada(self, id_horario, id_usuario, id_asiento, precio=8.50):
        """Comprar una entrada"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar que el asiento esté disponible
            cursor.execute("""
                SELECT COUNT(*) FROM Entrada 
                WHERE idHorario = ? AND idAsiento = ?
            """, (id_horario, id_asiento))
            
            if cursor.fetchone()[0] > 0:
                conn.close()
                return None, "El asiento ya está ocupado"
            
            # Insertar entrada
            cursor.execute("""
                INSERT INTO Entrada (idHorario, idUsuario, idAsiento, precio)
                VALUES (?, ?, ?, ?)
            """, (id_horario, id_usuario, id_asiento, precio))
            
            id_entrada = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return id_entrada, "Entrada comprada exitosamente"
            
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            return None, f"Error al comprar entrada: {e}"
    
    def crear_boleta(self, id_entrada, id_metodo_pago, total):
        """Crear boleta para una entrada"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Boleta (idEntrada, idMetodoPago, fechaCompra, total)
                VALUES (?, ?, ?, ?)
            """, (id_entrada, id_metodo_pago, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total))
            
            id_boleta = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return id_boleta, "Boleta creada exitosamente"
            
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            return None, f"Error al crear boleta: {e}"
    
    def ver_boleta_completa(self, id_boleta):
        """Ver información completa de una boleta"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            B.idBoleta,
            U.nombreUsuario,
            P.titulo AS Pelicula,
            H.fecha,
            H.hora,
            S.nombreSala,
            A.codigo AS Asiento,
            B.total,
            B.fechaCompra,
            MP.descripcion AS MetodoPago
        FROM Boleta B
        JOIN Entrada E ON B.idEntrada = E.idEntrada
        JOIN Usuario U ON E.idUsuario = U.idUsuario
        JOIN Horario H ON E.idHorario = H.idHorario
        JOIN Pelicula P ON H.idPelicula = P.idPelicula
        JOIN Sala S ON H.idSala = S.idSala
        JOIN Asiento A ON E.idAsiento = A.idAsiento
        JOIN MetodoPago MP ON B.idMetodoPago = MP.idMetodoPago
        WHERE B.idBoleta = ?
        """
        
        cursor.execute(query, (id_boleta,))
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado
    
    def obtener_usuarios(self):
        """Obtener lista de usuarios"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT idUsuario, nombreUsuario, tipoUsuario FROM Usuario")
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def obtener_metodos_pago(self):
        """Obtener métodos de pago disponibles"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT idMetodoPago, descripcion FROM MetodoPago")
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def verificar_usuario(self, nombre_usuario, clave):
        """Verificar credenciales de usuario"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT idUsuario, tipoUsuario 
            FROM Usuario 
            WHERE nombreUsuario = ? AND clave = ?
        """, (nombre_usuario, clave))
        
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado
    
    # Nuevos métodos para el administrador
    
    def obtener_generos(self):
        """Obtener lista de géneros"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT idGenero, nombreGenero FROM Genero")
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def obtener_tipos_audiencia(self):
        """Obtener tipos de audiencia"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT idAudiencia, descripcion FROM TipoAudiencia")
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def agregar_pelicula(self, titulo, duracion, id_genero, id_audiencia):
        """Agregar una nueva película"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Pelicula (titulo, duracion, idGenero, idAudiencia)
                VALUES (?, ?, ?, ?)
            """, (titulo, duracion, id_genero, id_audiencia))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.rollback()
            conn.close()
            return False
    
    def obtener_peliculas(self):
        """Obtener lista de películas con sus detalles"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            P.idPelicula,
            P.titulo,
            P.duracion,
            G.nombreGenero,
            TA.descripcion
        FROM Pelicula P
        JOIN Genero G ON P.idGenero = G.idGenero
        JOIN TipoAudiencia TA ON P.idAudiencia = TA.idAudiencia
        ORDER BY P.titulo
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def obtener_salas(self):
        """Obtener lista de salas"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT idSala, nombreSala, capacidad FROM Sala")
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def obtener_asientos_sala(self, id_sala):
        """Obtener asientos de una sala específica"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT idAsiento, codigo
            FROM Asiento
            WHERE idSala = ?
            ORDER BY codigo
        """, (id_sala,))
        
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def eliminar_asiento(self, id_asiento):
        """Eliminar un asiento"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar si el asiento está en uso
            cursor.execute("""
                SELECT COUNT(*) FROM Entrada
                WHERE idAsiento = ?
            """, (id_asiento,))
            
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False
            
            # Eliminar asiento
            cursor.execute("DELETE FROM Asiento WHERE idAsiento = ?", (id_asiento,))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.rollback()
            conn.close()
            return False
    
    def agregar_horario(self, id_pelicula, id_sala, fecha, hora):
        """Agregar un nuevo horario"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar si ya existe un horario en la misma sala y fecha/hora
            cursor.execute("""
                SELECT COUNT(*) FROM Horario
                WHERE idSala = ? AND fecha = ? AND hora = ?
            """, (id_sala, fecha, hora))
            
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False
            
            # Insertar horario
            cursor.execute("""
                INSERT INTO Horario (idPelicula, idSala, fecha, hora)
                VALUES (?, ?, ?, ?)
            """, (id_pelicula, id_sala, fecha, hora))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.rollback()
            conn.close()
            return False
    
    def obtener_horarios(self):
        """Obtener todos los horarios con detalles"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            H.idHorario,
            P.titulo,
            S.nombreSala,
            H.fecha,
            H.hora
        FROM Horario H
        JOIN Pelicula P ON H.idPelicula = P.idPelicula
        JOIN Sala S ON H.idSala = S.idSala
        ORDER BY H.fecha, H.hora
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        conn.close()
        
        return resultados
    
    def eliminar_horario(self, id_horario):
        """Eliminar un horario"""
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        
        try:
            # Verificar si hay entradas vendidas para este horario
            cursor.execute("""
                SELECT COUNT(*) FROM Entrada
                WHERE idHorario = ?
            """, (id_horario,))
            
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False
            
            # Eliminar horario
            cursor.execute("DELETE FROM Horario WHERE idHorario = ?", (id_horario,))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.rollback()
            conn.close()
            return False