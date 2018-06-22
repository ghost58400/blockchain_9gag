
from web import app


class Post(Resource):
	

class Chain(Resource):


app.config['API_MODELS'] = {'post': Post}
app.config['CRUD_URL_MODELS'] = {'post': Post}
