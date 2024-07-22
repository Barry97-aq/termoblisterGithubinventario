import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import yagmail
from threading import Timer

#imposta email
SENDER_EMAIL= "it.barry1997@gmail.com"
SENDER_PASSWORD= "ezjq ipns vngn tvwx"
RECEIVER_EMAIL= "momo1997moha@gmail.com"

THRESHOLD = 20

app = Flask(__name__)

def get_inventory():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bombolotti_inventario WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result

def update_inventario(column, quantity):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE bombolotti_inventario SET {column} = {column} - ? WHERE id = 1", (quantity,))
    conn.commit
    conn.close()    

def send_email(subject, body):
    try: 
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
        print("Email inviato con successo")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

def check_inventory_levels():
    inventory = get_inventory()
    low_stock_items = []
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
        body = "I seguenti articoli hanno un livello di scorta basso:\n" + "\n".join(low_stock_items)
        send_email("Avviso di scorte", body)

def schedule_inventory_check():
    check_inventory_levels()
    Timer(3600, schedule_inventory_check).start() #

@app.route('/')
def index():
    inventory = get_inventory()
    return render_template('index.html', inventory=inventory)

@app.route('/prelievo', methods=['POST'])
def prelievo():
    misura = request.form['misura']
    quantita = int(request.form['quantita'])
    update_inventario(misura, quantita)
    check_inventory_levels()
    return redirect(url_for('index'))

if __name__ == '__main__':
    schedule_inventory_check()
    app.run(debug=True)
    