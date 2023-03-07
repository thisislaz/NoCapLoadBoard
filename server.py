from flask_app import app
from flask_app.controllers import loads_controller,users_controller, carriers_controller,trucks_controller,shippers_controller,brokers_controller

if __name__ == "__main__":
  app.run(debug=True)