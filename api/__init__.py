from flask_restful import Api
from app import flaskAppInstance
from .ProjectAPI import ProjectAPI,ProjectAPIFilter,HomePage

restServerInstance = Api(flaskAppInstance)

restServerInstance.add_resource(ProjectAPI, "/api/v1/bitcoin/all")
restServerInstance.add_resource(ProjectAPIFilter, "/api/v1/bitcoin")
restServerInstance.add_resource(HomePage, "/")

