import os
import shutil
import subprocess
import uuid
from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
import settings
import logging


app = Flask(__name__)

os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(settings.OUTPUT_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('images')

        if not files:
            return "No files uploaded", 400

        unique_id = str(uuid.uuid4())
        input_dir = os.path.join(settings.UPLOAD_FOLDER, unique_id)
        output_dir = os.path.join(settings.OUTPUT_FOLDER, unique_id)

        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        input_files = []
        for file in files:
            file_path = os.path.join(input_dir, file.filename)
            file.save(file_path)
            input_files.append(file_path)

        command = [
            settings.UPSCAYL_PATH,
            '-i', input_dir,
            '-o', output_dir,
            '-m', settings.MODEL_PATH
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return f"Failed to process images: {str(e)}", 500

        processed_images = [os.path.join(output_dir, f) for f in os.listdir(output_dir)]

        app.logger.info('processed image: {0}'.format(processed_images))

        if len(processed_images) == 1:
            app.logger.info('processed only 1 image: {0}'.format(processed_images[0]))
            return render_template('result.html', image=processed_images[0], is_multiple=False)
        else:
            zip_filename = f"{unique_id}.zip"
            zip_filepath = os.path.join(settings.OUTPUT_FOLDER, zip_filename)
            shutil.make_archive(zip_filepath[:-4], 'zip', output_dir)
            return render_template('result.html', zip_file=url_for('download_zip', filename=zip_filename), is_multiple=True)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_zip(filename):
    return send_file(os.path.join(settings.OUTPUT_FOLDER, filename), as_attachment=True)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_file(os.path.join("", filename))


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
