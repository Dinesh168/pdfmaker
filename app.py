from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file part in the request')
            return redirect(url_for('index'))

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))

        if file and file.filename.endswith('.xlsx'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            app.logger.debug(f'File saved to {filepath}')

            # Read the Excel file
            df = pd.read_excel(filepath)
            df.rename(columns={
                'Part Number': 'PartNumber',   # Rename 'Part Number' to 'PartNumber'
                'Part NameL1': 'partNameL1'    # Rename 'part NameL1' to 'partNameL1'
            }, inplace=True)

            data = df.to_dict(orient='records')
            app.logger.debug('Excel file read successfully')
            print("data",data)
            return render_template('display.html', data=data)
        else:
            flash('Invalid file format. Please upload an Excel file.')
            return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')
        return f'An error occurred while processing the file: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
