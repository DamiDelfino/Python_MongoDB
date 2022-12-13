from pymongo import MongoClient
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId 



MONGO_URI = "mongodb://localhost"

client = MongoClient(MONGO_URI)

#Almacena la Base de Datos
db = client['river_plate']
#Almacena la coleccion
collection = db['jugadores']



'''
#Crear documentos
jugador_uno = {"nombre": "Franco", "apellido": "Armani", "posicion":"arquero", "edad":36}
jugador_dos = {"nombre": "Ezequiel", "apellido": "Centurion", "posicion":"arquero", "edad":25}
jugador_tres = {"nombre": "Milton", "apellido": "Casco", "posicion":"defensor", "edad":34}
#Insertar los documentos  a la coleccion
collection.insert_many([jugador_uno, jugador_dos, jugador_tres])
'''
resultados = collection.find()
ID_JUGADOR = ""
#Funciones
def mostrarDatos(nombre="", apellido="", posicion="", edad=""):
    objetoBuscar ={}
    if len(nombre)!=0:
       objetoBuscar["nombre"]=nombre
    elif len(apellido)!=0:
       objetoBuscar["apellido"]=apellido
    elif len(posicion)!=0:
       objetoBuscar["posicion"]=posicion
    elif len(edad)!=0:
       objetoBuscar["edad"]=edad
    #imprimir de a uno los documentos creados
    registros = tabla.get_children()
    for registro in registros:
        tabla.delete(registro)

    for r in collection.find(objetoBuscar):
        tabla.insert('',0,text=r["_id"], values=r["apellido"])
   
def crearJugador():
    if len(nombre.get())!=0 and len(apellido.get())!=0 and len(posicion.get())!=0 and len(edad.get())!=0:
        documento={"nombre": nombre.get(), "apellido": apellido.get(), "posicion":posicion.get(), "edad":edad.get()}
        collection.insert_one(documento)
        nombre.delete(0,END)
        apellido.delete(0,END)
        posicion.delete(0,END)
        edad.delete(0,END)
       
    else:
        pass

def dobleClickTabla(event):
    global  ID_JUGADOR
    ID_JUGADOR=str(tabla.item(tabla.selection())["text"])
    documento=collection.find({"_id":ObjectId(ID_JUGADOR)})[0]
    nombre.delete(0, END)
    nombre.insert(0, documento["nombre"])
    apellido.delete(0, END)
    apellido.insert(0, documento["apellido"])
    posicion.delete(0, END)
    posicion.insert(0, documento["posicion"])
    edad.delete(0, END)
    edad.insert(0, documento["edad"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"
#Funcion Editar
def editarJugador():
    if len(nombre.get())!=0 and len(apellido.get())!=0 and len(posicion.get())!=0 and len(edad.get())!=0:
        global ID_JUGADOR
        idBuscar={"_id":ObjectId(ID_JUGADOR)}
        nuevosValores={"nombre":nombre.get(), "apellido": apellido.get(), "posicion":posicion.get(), "edad":edad.get()}
        collection.update_one(idBuscar, nuevosValores)
        nombre.delete(0,END)
        apellido.delete(0,END)
        posicion.delete(0,END)
        edad.delete(0,END)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"

def borrarJugador():
    global ID_JUGADOR
    idBuscar ={"_id": ObjectId(ID_JUGADOR)}
    collection.delete_one(idBuscar)
    nombre.delete(0, END)
    apellido.delete
    posicion.delete
    edad.delete
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
    mostrarDatos()

def buscarJugador():
    mostrarDatos(buscarNombre.get(), buscarApellido.get(), buscarPosicion.get(), buscarEdad.get())


#Crear la ventana TKInter
ventana = Tk()
ventana.title("River Plate")
ventana.iconbitmap("river.ico")
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1, column=0,columnspan=2)
tabla.heading("#0", text="ID")
tabla.heading("#1", text="Apellido")

tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana, text="Nombre").grid(row=2, column=0)
nombre=Entry(ventana)
nombre.grid(row=2, column=1)
nombre.focus()

#Apellido
Label(ventana, text="Apellido").grid(row=3, column=0)
apellido=Entry(ventana)
apellido.grid(row=3, column=1)

#Posicion
Label(ventana, text="Posicion").grid(row=4, column=0)
posicion=Entry()
posicion.grid(row=4, column=1)

#Edad
Label(ventana, text="Edad").grid(row=5, column=0)
edad=Entry(ventana)
edad.grid(row=5, column=1)

#Buscar Nombre
Label(ventana, text="Buscar por Nombre").grid(row=9, column=0)
buscarNombre=Entry(ventana)
buscarNombre.grid(row=9, column=1)


#Buscar Apellido
Label(ventana, text="buscar por Apellido").grid(row=10, column=0)
buscarApellido=Entry(ventana)
buscarApellido.grid(row=10, column=1)

#Buscar Posicion
Label(ventana, text="buscar por Posicion").grid(row=11, column=0)
buscarPosicion=Entry()
buscarPosicion.grid(row=11, column=1)

#Buscar Edad
Label(ventana, text="buscar por Edad").grid(row=12, column=0)
buscarEdad=Entry(ventana)
buscarEdad.grid(row=12, column=1)



#Boton crear
crear=Button(ventana, text="Crear jugador", command=crearJugador,bg="green", fg="white")
crear.grid(row=6, columnspan=2)

#Boton editar
editar = Button(ventana, text="Editar Jugador", command=editarJugador, bg="yellow")
editar.grid(row=7, columnspan=2)
editar["state"]="disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar Jugador", command=borrarJugador, bg="orange", fg="white")
borrar.grid(row=8, columnspan=2)
borrar["state"]="disabled"

#Boton Buscar
buscar = Button(ventana, text="Buscar Jugador", command=buscarJugador, bg="blue", fg="white")
buscar.grid(row=13, columnspan=2)

mostrarDatos()
crearJugador()

ventana.mainloop()