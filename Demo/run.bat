REM Check if venv folder exists
if not exist venv (
    echo Virtual environment not found. Creating one...
    call python -m venv venv
)

call venv/Scripts/activate
python src/main.py