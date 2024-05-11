import connexion
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
from swagger_server import encoder

app = connexion.FlaskApp(__name__, specification_dir='./swagger/')
app.app.json = encoder.JSONEncoder(app=app.app)

app.add_middleware(
    CORSMiddleware,
    position=MiddlewarePosition.BEFORE_EXCEPTION,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=['X-Requested-With', 'Accept', 'Content-Type', 'Authorization'],
)

app.add_api('swagger.yaml', arguments={'title': 'OMC'}, pythonic_params=True)