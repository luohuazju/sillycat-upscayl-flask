# sillycat-upscayl-flask

Sample .env file
```dotenv
UPSCAYL_PATH = '/opt/upscayl/bin/upscayl-bin'
MODEL_PATH = '/opt/upscayl/models'
UPLOAD_FOLDER = '/opt/upscayl/inputs'
OUTPUT_FOLDER = '/opt/upscayl/outputs'
```

### run the dev MODE
```commandline
pip install -r requirements.txt
python web_app.py
```

### deployment to Prod
```commandline
pip install -r requirements.txt
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:4000 web_app:app
```
