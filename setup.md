# Installing Manual Process: Powershell VS Code

To get started you will need to install all the dependencies using the Python package manager, pip.

Please ensure you have Python and pip installed on your system. If you haven't installed them yet, you can find Python installation instructions [here](https://www.python.org/downloads/) and pip installation instructions [here](https://pip.pypa.io/en/stable/installation/).

Once Python and pip are installed, you can create virtual environment in which zango will be installed.

Now you are ready to create and activate the virtual environment by running the following command in your terminal or command prompt

```shell
python3 -m venv <virtual_environment_name>
<virtual_environment_name>\Scripts\activate
```

install the Zango Open Source Platform by running the following command in your terminal or command prompt

```shell
git clone https://github.com/griffin-pitts/Overreliance-Testing-Platform.git
pip install -r requirements.txt
```

This command will download and install the latest required dependencies.

##### Project Structure

```plaintext
project_name/                  # Project root directory
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates/
│   │   ├── layout.html
│   │   ├── index.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── encryption_utils.py
│   └── config.py
│
├── migrations/
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_models.py
│
├── .env
├── requirements.txt
├── config.py
├── run.py
└── README.md
```
