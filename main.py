from src.server.server import server
from src.db_models.macapa.database import database_macapa
from src.db_models.varejao.database import database_varejao

import src.controllers.contacts_macapa
import src.controllers.contacts_varejao

app = server.app
@app.teardown_appcontext
def shutdown_session(exception=None):
    database_varejao.db_session.remove()
    database_macapa.db_session.remove()

server.run()