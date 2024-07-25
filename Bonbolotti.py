import sqlite3
import tkinter as tk
from tkinter import messagebox
import yagmail


#Impostazione email
SENDER_EMAIL = "it.barry1997@gmail.com"
SENDER_PASSWORD ="ezjq ipns vngn tvwx"
RECEIVER_EMAIL = "momo1997moha@gmail.com"


#la soglia per il livello di scorte dasse
THRESHOLD = 20

conn = sqlite3.connect("inventario.db")#nome
#creation du tableau
cursor = conn.cursor()
cursor.execute(""" 
   CREATE TABLE IF NOT EXISTS bombolotti_inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        misura_750x805 INTEGER,
        misura_750x515 INTEGER,
        misura_500x580 INTEGER,
        misura_550x685 INTEGER,
        misura_750x965 INTEGER
   )
""")


conn.commit()
conn.close()


#Dati Iniziali
def insert_initial_data():
   conn = sqlite3.connect("inventario.db")
   cursor = conn.cursor() 
   cursor.execute("""
       INSERT INTO bombolotti_inventario (misura_750x805, misura_750x515, misura_500x580, misura_550x685, misura_750x965)
     VALUES (100, 232, 225, 125, 73)
""")
   conn.commit()
   conn.close()

#inserire i dati iniziali se il database e vuoto
insert_initial_data()

#Prelievo dei dati
def update_inventario(column, quantity):
   conn = sqlite3.connect("inventario.db")
   cursor = conn.cursor()
   cursor.execute(f"""
        UPDATE bombolotti_inventario
        SET {column} = {column} - ?
        WHERE id = 1
""", (quantity,))

   conn.commit()
   conn.close()

#visualizazione dati
def get_inventory():
   conn = sqlite3.connect("inventario.db")
   cursor = conn.cursor()
   cursor.execute("""SELECT * FROM bombolotti_inventario WHERE id = 1""")
   result = cursor.fetchone()
   conn.commit()

   if result is None:
      return resul(1,0,0,0,0,0)

   return result

# Visualizzare l'inventario attuale
inventory = get_inventory()
print(inventory)

#funzione per inviare email
def send_email(subject, body):
   try:
      yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
      yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
      print("Email inviato con successo")
   except Exception as e:
      print(f"Errore nel invio dell'email: {e}")

#funzione per controllo di livellodi livello di ordine
def check_inventory_levels():
   inventory = get_inventory()
   low_stock_items =[]
   if inventory[1] < THRESHOLD:
      low_stock_items.append(f"750X805: {inventory[1]}")
   if inventory[2] < THRESHOLD:
      low_stock_items.append(f"750X515: {inventory[2]}")
   if inventory[3] < THRESHOLD:
      low_stock_items.append(f"500X580: {inventory[3]}")
   if inventory[4] < THRESHOLD:
      low_stock_items.append(f"550X685: {inventory[4]}")
   if inventory[5] < THRESHOLD:
      low_stock_items.append(f"750X965: {inventory[5]}")

   if low_stock_items:
      body = "i seguenti articoli hanno un livello di scorta piu bassa:\n" + "\n".join(low_stock_items)
      send_email("Avviso di scorte basse", body)

#funzione per l'interfaccia utente
def show_inventory():
   inventory = get_inventory()
   inventory_str =f""" 
       750X805:{inventory[1]}
       750X515:{inventory[2]}
       500X580:{inventory[3]}
       550X685:{inventory[4]}
       75aX965:{inventory[5]}
   """
   messagebox.showinfo("Inventario attuale", inventory_str)

def Prelievo():
   misura = misura_var.get()
   quantita = int(quantita_entry.get())
   update_inventario(misura, quantita)
   messagebox.showinfo("Sucesso", "Prelievo ettuato con sucesso!")
   quantita_entry.delete(0, tk.END)
   check_inventory_levels()

#Interfaccia utente
root = tk.Tk()
root.title("Gestione inventario")

tk.Label(root, text="misura").grid(row=0, column=0)
tk.Label(root, text="quantita").grid(row=1, column=0)

misura_var = tk.StringVar()
misura_entry = tk.OptionMenu(root, misura_var,"misura_750X805", "misura_750x515", "misura_500x580", "misura_550x685", "misura_750x965")
misura_entry.grid(row=0, column=1)

quantita_entry = tk.Entry(root)
quantita_entry.grid(row=1, column=1)

tk.Button(root, text="Prelievo", command=Prelievo).grid(row=2, column=0)
tk.Button(root, text="visualizza inventario", command=show_inventory).grid(row=2,column=1)

root.mainloop()