from flask import Flask, render_template, redirect, url_for, request
import logging
from logging import Formatter, FileHandler
import os
import adc1115
import createTransactions

app = Flask(__name__)

list_values = adc1115.main()
print(list_values)

# Route for handling the display page
@app.route('/route', methods=['GET', 'POST'])
def display():
    link = "https://devnet.thetangle.org/address/"
    if request.method == 'POST':
        result,address1 = createTransactions.main()
        link = link + str(address1)
        return render_template('transaction.html', val1 = result, val2 = link)
    else:
        return render_template('display.html', val1 = list_values[0], val2 = list_values[1], 
        val3 = list_values[2],val4 = list_values[3],val5 = list_values[4],val6 = list_values[5],val7 = list_values[6],
        val8 = list_values[7],val9 = list_values[8],val10 = list_values[9])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('display'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
