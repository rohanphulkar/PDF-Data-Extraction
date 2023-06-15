from flask import Flask, render_template, redirect, url_for, request
import os
import csv
from script import extract_key_value_pair, save_to_csv

app = Flask(__name__)

# Configure a folder to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def index():
    # Rendering index paeg
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        # Save the uploaded file to UPLOAD_FOLDER
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract the key-value pairs from the file
        extracted_data = extract_key_value_pair(file_path)
        if isinstance(extracted_data,str):
            return extracted_data
        
        csv_filename = 'extracted_data.csv'
        # Saving the extracted data to the csv file
        save_to_csv(extracted_data,csv_filename)

        # Redirect to result page
        return redirect(url_for('result',csv_file=csv_filename))
    else:
        return "No file was uploaded"

@app.route("/result/<csv_file>")
def result(csv_file):
    data = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return render_template("result.html",data=data)

# Run the flask application
if __name__ == '__main__':
    app.run(debug=True)