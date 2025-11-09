import pandas as pd
import psycopg2

def insert_excel_to_postgresql(file_path, db_config, table_name):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path)

        # Conectarse a la base de datos PostgreSQL
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config.get('port', 5432)
        )
        cursor = connection.cursor()

        # Crear la consulta de inserción
        columns = ', '.join([f'"{col}"' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f'INSERT INTO "{table_name}" ("name", "category", "quantity", "unit", "gross_weight", "net_weight", "calories", "protein", "lipids", "carbohydrates") VALUES ({placeholders})'

        # Insertar cada fila en la tabla
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        # Confirmar los cambios
        connection.commit()
        print(f"Datos insertados exitosamente en la tabla '{table_name}'.")
    
    except Exception as e:
        print(f"Error al insertar datos: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Conexión a PostgreSQL cerrada.")

# Configuración de conexión a la base de datos
db_config = {
    'host': 'postgresql',     # Cambia según tu configuración
    'database': 'nutriswap',   # Nombre de tu base de datos
    'user': 'nutri-dev',      # Usuario de PostgreSQL
    'password': 'admin123',  # Contraseña de PostgreSQL
}

# Parámetros del archivo Excel y la tabla
file_path = "smaecsv-og.xlsx"  # Ruta completa al archivo Excel
table_name = "alimentos"            # Nombre de la tabla existente en PostgreSQL

# Ejecutar la función
insert_excel_to_postgresql(file_path, db_config, table_name)
