from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import os
from ai_engine import get_prediction
from report_gen import generate_medical_report
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['REPORTS_FOLDER'] = os.path.join('static', 'reports')

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        patient_name = request.form.get('patient_name', 'Unknown')
        patient_age = request.form.get('age', 'N/A')
        patient_gender = request.form.get('gender', 'N/A')
        cancer_type = request.form.get('cancer_type', 'Multi-Cancer')
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = str(uuid.uuid4()) + "_" + file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # AI Prediction
            res = get_prediction(filepath)
            res['image_url'] = url_for('static', filename='uploads/' + filename)
            res['patient_name'] = patient_name
            res['patient_age'] = patient_age
            res['patient_gender'] = patient_gender
            res['cancer_type'] = cancer_type
            
            # Generate Report
            report_filename = f"report_{str(uuid.uuid4())[:8]}.pdf"
            report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
            generate_medical_report(patient_name, patient_age, patient_gender, res, report_path)
            
            res['report_url'] = url_for('static', filename='reports/' + report_filename)
            
            return render_template('detect.html', result=res)
            
    return render_template('detect.html', result=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
