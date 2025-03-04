# Necessary imports
from flask import Flask
from app import create_app

# Web application initialization
app = create_app()

# Main logic entry point
if __name__ == "__main__":
    app.run()
