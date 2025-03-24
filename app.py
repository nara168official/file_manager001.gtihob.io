from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            files.append({
                'name': filename,
                'size': os.path.getsize(path),
                'upload_date': os.path.getctime(path)
            })
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Prevent overwriting existing files
        counter = 1
        while os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        file.save(filepath)
        flash(f'File "{filename}" uploaded successfully')
    else:
        flash('File type not allowed')
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    # Security check to prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        abort(400)
    
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    # Security check
    if '..' in filename or filename.startswith('/'):
        abort(400)
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'File "{filename}" deleted successfully')
    else:
        flash('File not found')
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="404 - Page not found"), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', error="400 - Bad request"), 400

if __name__ == '__main__':
    app.run(debug=True)