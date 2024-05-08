from connexion import FlaskApp

app = FlaskApp(__name__, specification_dir='./swagger')
app.add_api('swagger.yaml', arguments={'title': 'Weather Watch'}, pythonic_params=True)