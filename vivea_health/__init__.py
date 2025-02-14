# vivea_health/__init__.py
from flask import Flask
from flask_cors import CORS
from pyngrok import ngrok
from graphql_server.flask import GraphQLView


# Import components from your package
from .routes import api
from .schema import schema


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register the REST blueprint
    app.register_blueprint(api)
    
    # Add GraphQL endpoint with GraphiQL for testing
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )
    
    # Attempt to set up an ngrok tunnel
    try:
        public_url = ngrok.connect(5000)
        print(" * ngrok tunnel available at:", public_url)
    except Exception as e:
        print(" * ngrok tunnel could not be established:", e)
    
    return app

   
