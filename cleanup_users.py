import sqlite3
import os

db_path = 'tutorias.sqlite'

def cleanup_users():
    if not os.path.exists(db_path):
        print(f"File {db_path} does not exist.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Identificar usuarios a borrar (sin división y que no sean 'admin')
    cursor.execute("SELECT ID FROM usuario WHERE (clave_division IS NULL OR clave_division = '') AND ID != 'admin';")
    users_to_delete = [row[0] for row in cursor.fetchall()]

    if not users_to_delete:
        print("No se encontraron usuarios sin división para borrar (exceptuando al admin).")
        conn.close()
        return

    print(f"Usuarios identificados para borrar: {users_to_delete}")

    try:
        # Borrar registros relacionados primero para mantener integridad
        for user_id in users_to_delete:
            # Borrar tutorías donde sea tutor o tutorado
            cursor.execute("DELETE FROM tutoria WHERE clave_tutor = ? OR clave_tutorado = ?;", (user_id, user_id))
            # Borrar solicitudes de baja donde esté involucrado
            cursor.execute("DELETE FROM solicitud_baja WHERE clave_tutor = ? OR clave_tutorado = ?;", (user_id, user_id))
            
        # Finalmente borrar a los usuarios
        placeholders = ', '.join(['?'] * len(users_to_delete))
        cursor.execute(f"DELETE FROM usuario WHERE ID IN ({placeholders});", users_to_delete)

        conn.commit()
        print(f"Éxito: Se han eliminado {len(users_to_delete)} usuarios y sus registros relacionados.")
    except Exception as e:
        conn.rollback()
        print(f"Error durante la eliminación: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    cleanup_users()
