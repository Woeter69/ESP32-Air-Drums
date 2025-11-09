python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

python run.py --host 0.0.0.0 --port 6000
