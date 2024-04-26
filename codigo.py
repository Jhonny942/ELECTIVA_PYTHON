import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos
cnx = sqlite3.connect('Ventas.db')
cursor = cnx.cursor()

# Definición de las tablas si no existen
products_table = '''
    CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY, 
        name_producto TEXT NOT NULL,
        cantidad TEXT NOT NULL,
        id_categoria INTEGER 
    );
'''

categories_table = '''
    CREATE TABLE IF NOT EXISTS categorias(
        id INTEGER PRIMARY KEY, 
        name_categoria TEXT NOT NULL
    );
'''
cursor.execute(products_table)
cursor.execute(categories_table)
cnx.commit()  # Crea la tabla

# Funciones para operaciones CRUD
def insertar_categoria():
    nombre = categoria_entry.get()
    if nombre:
        cursor.execute(f"INSERT INTO categorias (name_categoria) VALUES('{nombre}')")
        cnx.commit()
        messagebox.showinfo("Éxito", "Categoría creada exitosamente.")
        categoria_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Por favor ingresa un nombre para la categoría.")

def insertar_producto():
    nombre = producto_entry.get()
    cantidad = cantidad_entry.get()
    categoria_id = categoria_id_entry.get()
    if nombre and cantidad and categoria_id:
        cursor.execute(f"INSERT INTO productos (name_producto, cantidad, id_categoria) VALUES('{nombre}', '{cantidad}', '{categoria_id}')")
        cnx.commit()
        messagebox.showinfo("Éxito", "Producto creado exitosamente.")
        producto_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        categoria_id_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Por favor ingresa todos los campos.")

def listar_categorias():
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    if categorias:
        messagebox.showinfo("Categorías", "\n".join([f"ID: {categoria[0]}, Nombre: {categoria[1]}" for categoria in categorias]))
    else:
        messagebox.showinfo("Categorías", "No hay categorías registradas.")

def listar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if productos:
        messagebox.showinfo("Productos", "\n".join([f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, ID Categoría: {producto[3]}" for producto in productos]))
    else:
        messagebox.showinfo("Productos", "No hay productos registrados.")

def generar_reportes():
    query_reporte1 = '''
        SELECT 
            c.name_categoria, 
            SUM(p.cantidad) as total_productos
        FROM 
            productos p INNER JOIN 
                categorias c
            ON p.id_categoria = c.id
        GROUP BY 
            c.name_categoria 
    '''
    cursor.execute(query_reporte1)
    data = cursor.fetchall()

    # Preparar los datos para la primera gráfica
    categorias = [resultado[0] for resultado in data]
    total_productos = [resultado[1] for resultado in data]

    # Crear la primera gráfica
    plt.figure(figsize=(10, 6))
    plt.bar(categorias, total_productos, color='skyblue')
    plt.xlabel('Categorías')
    plt.ylabel('Total de productos')
    plt.title('Total de productos por categoría')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Segunda consulta para la segunda gráfica
    query_reporte2 = '''
        SELECT 
            c.name_categoria, 
            p.name_producto
        FROM 
            productos p INNER JOIN 
                categorias c
            ON p.id_categoria = c.id
        ORDER BY 
            c.name_categoria
    '''
    cursor.execute(query_reporte2)
    data_products = cursor.fetchall()

    # Preparar los datos para la segunda gráfica
    categories_products = {}
    for categoria, producto in data_products:
        if categoria not in categories_products:
            categories_products[categoria] = []
        categories_products[categoria].append(producto)

    # Crear la segunda gráfica
    plt.figure(figsize=(10, 6))
    for categoria, productos in categories_products.items():
        plt.barh(productos, len(categoria), color='lightgreen')
    plt.xlabel('Cantidad de Productos')
    plt.ylabel('Categorías')
    plt.title('Productos por categoría')
    plt.tight_layout()

    # Mostrar ambas gráficas
    plt.show()

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Ventas")

# Crear widgets
categoria_label = tk.Label(root, text="Nombre de la Categoría:")
categoria_entry = tk.Entry(root, width=30)
categoria_button = tk.Button(root, text="Crear Categoría", command=insertar_categoria)

producto_label = tk.Label(root, text="Nombre del Producto:")
producto_entry = tk.Entry(root, width=30)
cantidad_label = tk.Label(root, text="Cantidad:")
cantidad_entry = tk.Entry(root, width=10)
categoria_id_label = tk.Label(root, text="ID de Categoría:")
categoria_id_entry = tk.Entry(root, width=10)
producto_button = tk.Button(root, text="Crear Producto", command=insertar_producto)

listar_categorias_button = tk.Button(root, text="Listar Categorías", command=listar_categorias)
listar_productos_button = tk.Button(root, text="Listar Productos", command=listar_productos)
generar_reportes_button = tk.Button(root, text="Generar Reportes", command=generar_reportes)
salir_button = tk.Button(root, text="Salir", command=root.quit)

# Organizar widgets en la ventana
categoria_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
categoria_entry.grid(row=0, column=1, padx=10, pady=5)
categoria_button.grid(row=0, column=2, padx=10, pady=5)

producto_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
producto_entry.grid(row=1, column=1, padx=10, pady=5)
cantidad_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")
cantidad_entry.grid(row=1, column=3, padx=10, pady=5)
categoria_id_label.grid(row=1, column=4, padx=10, pady=5, sticky="e")
categoria_id_entry.grid(row=1, column=5, padx=10, pady=5)
producto_button.grid(row=1, column=6, padx=10, pady=5)

listar_categorias_button.grid(row=2, column=0, padx=10, pady=5)
listar_productos_button.grid(row=2, column=1, padx=10, pady=5)
generar_reportes_button.grid(row=2, column=2, padx=10, pady=5)
salir_button.grid(row=2, column=3, columnspan=2, padx=10, pady=5)

# Ejecutar el bucle principal
root.mainloop()

# Cerrar la conexión a la base de datos
cnx.close()