pip install poetry==1.1.12
poetry export --without-hashes -o requirements.txt
pip install --no-cache-dir -r requirements.txt