from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from rembg import remove
from pdf2docx import Converter
from werkzeug.utils import secure_filename
import time
import pdfplumber
import pandas as pd
import fitz  # PyMuPDF
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

USERNAME = 'admin'
PASSWORD = 'rahasia'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Login salah!")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/remove-bg', methods=['GET', 'POST'])
def remove_bg():
    if not session.get('logged_in'):
        return redirect('/')

    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = f'removed-{filename}'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        start_time = time.time()
        with open(input_path, 'rb') as i, open(output_path, 'wb') as o:
            o.write(remove(i.read()))
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        return render_template('tools/remove_bg.html',
                               original=filename,
                               result=output_filename,
                               duration=duration)

    return render_template('tools/remove_bg.html', original=None, result=None, duration=None)

@app.route('/pdf-to-word', methods=['GET', 'POST'])
def pdf_to_word():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        file = request.files['pdf']
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_path = input_path.replace('.pdf', '.docx')
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        return render_template('tools/pdf_to_word.html', result=output_path)
    return render_template('tools/pdf_to_word.html', result=None)

@app.route('/pdf-to-excel', methods=['GET', 'POST'])
def pdf_to_excel():
    if not session.get('logged_in'):
        return redirect('/')

    if request.method == 'POST':
        file = request.files['pdf']
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        output_filename = filename.rsplit('.', 1)[0] + '.xlsx'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Ekstrak tabel dari PDF ke Excel
        all_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df)

        if all_tables:
            full_df = pd.concat(all_tables, ignore_index=True)
            full_df.to_excel(output_path, index=False)

            return render_template('tools/pdf_to_excel.html', result=output_filename)
        else:
            return render_template('tools/pdf_to_excel.html', result=None, error="Tidak ada tabel yang ditemukan.")

    return render_template('tools/pdf_to_excel.html', result=None)

@app.route('/filter-jadwal', methods=['GET', 'POST'])
def filter_jadwal():
    if not session.get('logged_in'):
        return redirect('/')
    # [Fungsi ini tetap sama seperti sebelumnya, tidak dimodifikasi di sini]
    return render_template('tools/filter_jadwal.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
