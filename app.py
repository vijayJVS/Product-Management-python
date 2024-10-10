from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

#Db Connection
app=Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="jose123*"
app.config["MYSQL_DB"]="catalog"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)


#Show Product

@app.route("/")
def home():

    con = mysql.connection.cursor()
    sql = "Select * from Product"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html", datas=res)
    

#Add Product

@app.route("/addProduct", methods=['GET', 'POST'])

def addProduct():
    if request.method == 'POST':

        id = request.form['id']
        Pname = request.form['pname']
        Pprice = request.form['pprice']
        qty = request.form['qty']
        Desc = request.form['desc']
        con = mysql.connection.cursor()
        sql = "insert into Product (id, Product_Name, Product_price, Quantity, P_Desc) values (%s, %s, %s, %s, %s)"
        res = con.execute(sql,(id, Pname, Pprice, qty, Desc))
        mysql.connection.commit()
        con.close()
        flash("Product Added Sucessfully...")
        return redirect(url_for('home'))
    return render_template("addProduct.html")

#Update

@app.route("/UpdateProduct/<string:id>", methods=['GET', 'POST'])
 
def UpdatePro(id):
        con = mysql.connection.cursor()
        if request.method == 'POST':
            Pname = request.form['pname']
            Pprice = request.form['pprice']
            qty = request.form['qty']
            Desc = request.form['desc']
            con = mysql.connection.cursor()
            sql = "Update Product set Product_Name=%s, Product_Price=%s, Quantity=%s, P_Desc=%s where ID=%s"
            res = con.execute(sql,[Pname, Pprice, qty, Desc, id])
            mysql.connection.commit()
            con.close()
            flash("Product Updated Sucessfully...")
            return redirect(url_for("home"))
     
        con = mysql.connection.cursor()
        sql = "Select * from Product where ID=%s"
        con.execute(sql,[id])
        res=con.fetchone()
        return render_template("editPro.html", datas=res)

#Delete Product

@app.route("/deletePro/<string:id>", methods=['GET', 'POST'])

def deletePro(id):
        con = mysql.connection.cursor()
        sql = "Delete from Product where ID=%s"
        con.execute(sql, (id,))
        mysql.connection.commit()
        con.close()
        flash("Product Deleted Sucessfully...")
        return redirect(url_for('home'))


if(__name__ == '__main__'):
    app.secret_key="abc123"
    app.run(debug=True)