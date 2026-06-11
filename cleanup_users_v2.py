import sqlite3
import os
import time

db_path = 'tutorias.sqlite'

def cleanup_users():
    if not os.path.exists(db_path):
        print(f"File {db_path} does not exist.")
        return

    # Intentar hasta 5 veces si la base de datos está bloqueada
    for attempt in range(5):
        try:
            conn = sqlite3.connect(db_path, timeout=30) # Aumentar el timeout
            cursor = conn.cursor()

            # Identificar usuarios a borrar
            cursor.execute("SELECT ID FROM usuario WHERE (clave_division IS NULL OR clave_division = '') AND ID != 'admin';")
            users_to_delete = [row[0] for row in cursor.fetchall()]

            if not users_to_delete:
                print("No se encontraron usuarios sin división para borrar (exceptuando al admin).")
                conn.close()
                return

            print(f"Usuarios identificados para borrar: {users_to_delete}")

            # Borrar registros relacionados
            for user_id in users_to_delete:
                cursor.execute("DELETE FROM tutoria WHERE clave_tutor = ? OR clave_tutorado = ?;", (user_id, user_id))
                cursor.execute("DELETE FROM solicitud_baja WHERE clave_tutor = ? OR clave_tutorado = ?;", (user_id, user_id))
                
            # Borrar usuarios
            placeholders = ', '.join(['?'] * len(users_to_delete))
            cursor.execute(f"DELETE FROM usuario WHERE ID IN ({placeholders});", users_to_delete)

            conn.commit()
            print(f"Éxito: Se han eliminado {len(users_to_delete)} usuarios y sus registros relacionados.")
            conn.close()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print(f"Intento {attempt + 1}: La base de datos está bloqueada, esperando...")
                time.sleep(2)
            else:
                print(f"Error operativo: {e}")
                break
        except Exception as e:
            print(f"Error inesperado: {e}")
            break

if __name__ == "__main__":
    cleanup_users()
