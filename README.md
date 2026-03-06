# Surakshit Marg - Safety Advisor

A Python + Flask web app for student road-safety learning.

Students can:
- Describe a road scenario in text.
- Toggle hazards using checkboxes.
- Optionally attach an image for local preview.
- Predict a safety score and risk level.
- See the top risk factor, key control focus, and precautions.
- Save scenarios to local device history (browser localStorage).

## Tech stack
- Python (Flask)
- HTML, CSS, JavaScript

## Run locally (PowerShell)

From:
`C:\Users\drshi\OneDrive\Documents\Surakshit marg for school`

```powershell
# Existing local venv with bin layout:
.\.venv\bin\python.exe -m pip install -r requirements.txt
.\.venv\bin\python.exe app.py
```

If you want a Windows-style venv (`Scripts` folder):

```powershell
py -m venv .venv_win
.\.venv_win\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open:
- `http://127.0.0.1:5000`

## Deployment-ready setup

This repo is now ready for cloud deployment:
- `wsgi.py` provides the WSGI app entrypoint.
- `requirements.txt` includes `gunicorn`.
- `Procfile` start command: `gunicorn wsgi:app`.
- `render.yaml` for Render blueprint deployment.
- `runtime.txt` pins Python version.

## Deploy on Render

1. Push this project to GitHub.
2. Go to Render dashboard and choose **New +** -> **Blueprint**.
3. Connect your GitHub repo.
4. Render reads `render.yaml` and deploys automatically.
5. Open your live URL after build completes.

## Deploy on Railway

1. Push this project to GitHub.
2. In Railway, create **New Project** -> **Deploy from GitHub repo**.
3. Select your repository.
4. Railway will install dependencies and use `Procfile` (`gunicorn wsgi:app`).
5. Open the generated public domain.

## Upload to GitHub

1. Create a new repository on GitHub (empty repository).
2. In VS Code terminal, run:

```powershell
git init
git add .
git commit -m "Initial Surakshit Marg Safety Advisor"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

3. For next updates:

```powershell
git add .
git commit -m "Describe your change"
git push
```

## Project structure
- `app.py` - Flask backend and scoring engine
- `wsgi.py` - WSGI entrypoint for deployment
- `templates/index.html` - Main UI layout
- `static/styles.css` - UI styling
- `static/app.js` - Client interactions
- `render.yaml` - Render service definition
- `Procfile` - Process start command
