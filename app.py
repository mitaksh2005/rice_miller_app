from flask import Flask, render_template, request, redirect
import MySQLdb
import os

app = Flask(__name__)

# Database config using environment variables
db_config = {
    "host": os.environ.get("MYSQL_HOST", "db4free.net"),
    "user": os.environ.get("MYSQL_USER", "mitaksh"),
    "passwd": os.environ.get("MYSQL_PASSWORD", "Mitaksh@2005"),
    "db": os.environ.get("MYSQL_DB", "rice_miller"),
    "port": int(os.environ.get("MYSQL_PORT", 3306))
}

@app.route('/')
def index():
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM miller_invoice ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', invoices=data)

@app.route('/add', methods=['POST'])
def add_invoice():
    form = request.form
    values = (
        form['seller_name'], form['vehicle_no'], form['inward_no'], form['rst_no'], form['description'],
        form['date'], form['due_date'], form['net_qty'], form['gunnies'], form['winnes'],
        form['quality'], form['settle'], form['final_qty'], form['gunny_balance'], form['bags'],
        form['rate'], form['amount'], form['market_no'], form['market_amt'], form['handling'],
        form['supervisor'], form['lf_adv'], form['wb_charges'], form['total']
    )

    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO miller_invoice (
            seller_name, vehicle_no, inward_no, rst_no, description,
            date, due_date, net_qty, gunnies, winnes,
            quality, settle, final_qty, gunny_balance, bags,
            rate, amount, market_no, market_amt, handling,
            supervisor, lf_adv, wb_charges, total
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/invoice/<int:invoice_id>')
def show_invoice(invoice_id):
    conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM miller_invoice WHERE id = %s", (invoice_id,))
    invoice = cursor.fetchone()
    conn.close()
    return render_template('pdf_view.html', invoice=invoice)

@app.template_filter('format_invoice')
def format_invoice(inv):
    return f"""
                               MILLERS COPY
                        {inv[1]}

Vehicle No. : {inv[2]:<20} Inward No. : {inv[3]}
Description : {inv[5]:<20} RST# : {inv[4]}
Date        : {inv[6]} Due Date   : {inv[7]}

-------------------------------------------------------------
Net Qty   : {float(inv[8]):.3f}
Gunnies   : {float(inv[9]):.3f}
Winnes    : {float(inv[10]):.3f}
Quality   : {float(inv[11]):.3f}
Settle    : {float(inv[12]):.3f}
Final Qty : {float(inv[13]):.3f}
-------------------------------------------------------------
Gunny Balance: {inv[14]}

Bags         : {inv[15]}
Rate         : {float(inv[16]):.2f}
Amount       : {float(inv[17]):.2f}
-------------------------------------------------------------
(+)
Market #{inv[18]:<16} : {float(inv[19]):>10.2f}
Handling                  : {float(inv[20]):>10.2f}
Supervisor Charges        : {float(inv[21]):>10.2f}
(-)
L.F. Adv.                 : {float(inv[22]):>10.2f}
W / B Charges             : {float(inv[23]):>10.2f}

TOTAL AMOUNT              : {float(inv[24]):>10.2f}
-------------------------------------------------------------"""

if __name__ == '__main__':
    app.run(debug=True)