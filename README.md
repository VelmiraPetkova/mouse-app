# Step-by-Step Guide to Set Up and Run the Application on Ubuntu

1. Clone the app locally and change into its directory

```bash
git clone https://github.com/VelmiraPetkova/mouse-app.git
cd mouse-app
```

2. Create a venv and install the requirements

```bash
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip install -r requirement.txt
```

3. Run the app

```bash
python3 app.py
```
