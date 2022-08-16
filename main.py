from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
'''
we're gonna wrap our app in a api
'''
app = Flask(__name__)
api = Api(app)
#config is = name of DB
# 'sqlite://database.db' is a relative path, file is in same directory as script we are on
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#define field we want in model
#I'm guessing Model is a table
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #nullable=False because this field has to have something, can't be null
    likes = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False) 
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        #gives string representation of video
        return f"Video (name = {self.name}, views = {self.views}, likes = {self.likes})"

#creates all tables
db.create_all() 

#automatically parses request being sent & make sure it has correct info so we can easily grab info
#help= is kinda like an error 
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required.", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required.", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required.", required=True)

#Used for serialization purposes
#for how an object should be serialized
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

#Resouce lets us handle get, put, del requests
class Video(Resource):
    #when we return, take return values & serialize it using resource_fields dict, its returned in json format
    @marshal_with(resource_fields)
    def get(self, video_id): 
        #when returning info from api, that info has to be serializable
        #json format is serializable -> in the format of dictionary
        #we're gonna look for some row in the model where id = video_id
        return VideoModel.query.filter_by(id=video_id).first()
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        #we get an error if we put an item that already exists
        #filter all videos in VideoModel by id & return first entry filtered by
        if VideoModel.query.filter_by(id=video_id).first():
            abort(409, message="Video id taken.")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201


    def delete(self, video_id):
        return '', 204
        
        
#1st is class name added to api, 2nd is URL where class is accessible (endpoint)
#"/" is the default URL
#use angle brackets to pass in params
api.add_resource(Video, "/video/<int:video_id>")

#this starts our server & flask app
#debug=True for develop purposes. Not to be set to True when in production 

if __name__ == "__main__":
    app.run(debug=True)

#run on terminal by using python3 main.py
 