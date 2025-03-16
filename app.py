import configparser
import os

from src.factory import create_app
app = create_app()

@app.route("/")
def sustains_server():
    return "<p>Welcome to sustains server!</p>"

# if __name__ == "__main__":
#     app = create_app()
#     app.run()
