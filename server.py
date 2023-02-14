from flask_app import app
from flask_app.controllers import main_con
from flask_app.controllers import item_con
from flask_app.controllers import weapon_con
from flask_app.controllers import armor_con
from flask_app.controllers import character_con
from flask_app.controllers import char_class_con
from flask_app.controllers import user_con
from flask_app.controllers import char_race_con
from flask_app.controllers import char_background_con



if __name__ == "__main__":
    app.run(debug=True, port=8000)