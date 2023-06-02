from flask import jsonify, Flask, make_response
from flask_restful import Resource, Api, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import uuid
import jwt
import datetime
from functools import wraps
import os
from datetime import date

import logging as logger

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#        token = None
#        if 'x-access-tokens' in request.headers:
#            token = request.headers['x-access-tokens']

#        if not token:
#            return jsonify({'message': 'a valid token is missing'})
#        try:
#            data = jwt.decode(token, JWT_SECRET_KEY)
from BitCoinDb import BitCoinFile

errorMessage = [
    {
        "Get Top N data": "http://<ip>:<port>/api/v1/bitcoin?limit=20",
        "Get Data Between Start & End Date": "http://<ip>:<port>/api/v1/bitcoin?start='2012-01-02'&end='2012-01-02'",
        "Get Data From Start Date": "http://<ip>:<port>/api/v1/bitcoin?start='2012-01-02'",
        "Get Data till End Date": "http://<ip>:<port>/api/v1/bitcoin?end='2012-01-02'",
        "Get Data for single Date": "http://<ip>:<port>/api/v1/bitcoin?dt='2012-01-02'"
    }
]


class HomePage(Resource):

    def get(self):
        return make_response(jsonify({"View all entry": "<ip>:<port>/api/v1/bitcoin/all"}), 200)


class ProjectAPI(Resource):
    def get(self):
        bit = BitCoinFile()
        limit = 10
        return_data = bit.getTopN(limit)
        code = return_data[-1]
        data = return_data[:-1]
        return make_response(jsonify(data), code)


class ProjectAPIFilter(Resource):
    def get(self):
        start = request.args.get('start')
        end = request.args.get('end')
        limit = request.args.get('limit')
        dt = request.args.get('dt')
        bit = BitCoinFile()

        if start or end or dt:
            return_data = bit.getStartAndEnd(start, end, dt)
            code = return_data[-1]
            data = return_data[:-1]
            return make_response(jsonify(data), code)

        if limit:
            returndata = bit.getTopN(limit)
            code = returndata[-1]
            data = returndata[:-1]
            return make_response(jsonify(data), code)


        if not (limit or start or end or dt):
            return make_response(jsonify({"Invalid Parameter": errorMessage}), 400)
