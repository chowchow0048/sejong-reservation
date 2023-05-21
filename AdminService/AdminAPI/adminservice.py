from flask import request
from flask_restx import Resource, namespace
from sqlalchemy import select, insert, update, delete
from service import Service
from config import model_config, api_config
from utils import serialization, check_jwt_exists, check_if_room_identical
from validators import room_name_validator, room_address1_validator, room_address2_validator, is_usable_validator, max_users_validator


# namespace for handy routing
admin = namespace.Namespace(
    name="admin",
    description="유저, 회의실, 예약 관리를 위한 API"
)

# keys to be excluded when serializing data to GET all rooms
exclude = ['created_at', 'updated_at']

@admin.route('')
class ConferenceRoom(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    # CREATE room 
    def post(self):
        # request body data, need to be validated
        req = request.json  

        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        print("!!!!!!!!!TYPE: ", user_status['User']['type'], "!!!!!!!!!!!!", flush=True)
        if(check_jwt_exists(user_status) 
           and (user_status['User']['type'] != 2)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                valid_data, invalid_data = Room.validate(req)

                if len(invalid_data) > 0:
                    return {
                        "status": False,
                        "msg": "invalid data",
                        "invalid": invalid_data
                    }, 200
                
                res = conn.execute(select(Room)).mappings().all()
                print(valid_data, res)
                
                # if validated data is already in table, 
                # send message 'data already exists'
                if check_if_room_identical(conn, Room, valid_data):
                    return { 
                        "status": False,
                        "msg": "Room already exists"
                    }, 200
                
                # insert verified body data to Room table
                conn.execute(
                    insert(Room), {
                        **valid_data
                    }
                )

                # CREATE room
                return{
                    "status": True,
                    "msg": "Room Created"
                }, 200
        
        # error
        except OSError as e:
            print(e)
            return {
                "status": False,
                "msg": "Room Create Failed"
            }, 500
        
    # GET all rooms
    def get(self):     
        # check if user is logged in.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        # print("!!!!!!!!!TYPE: ", user_status['User']['type'], "!!!!!!!!!!!!", flush=True)
        if not check_jwt_exists(user_status):
            return {
                "status": False,
                "msg": "Not logged in",
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # get all json data from Room table as list with dicts
                rooms = conn.execute(select(Room)).mappings().all()
            
                # serialize each room data in Room table
                serialized_rooms = [
                    serialization(room, exclude=exclude)
                    for room in rooms
                ]

                # if there's no such room
                if len(serialized_rooms) == 0:
                    return {
                        "status": False,
                        "msg": "Room Not Found"
                    }, 200

                # GET all rooms
                return {
                    "status": True,
                    "allRooms": serialized_rooms,
                    "msg": "Room found"
                }, 200

        # error
        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "Failed to get room data"
            }, 500
        
# GET, DELETE, UPDATE by room id
@admin.route('/<int:id>')
class ConferenceRoomById(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)
    
    # GET room by id    
    def get(self, id):
        # check if user is logged in.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        print("!!!!!!!!!TYPE: ", user_status['User']['type'], "!!!!!!!!!!!!", flush=True)
        if not check_jwt_exists(user_status):
            return {
                "status": False,
                "msg": "Not logged in"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res == None:
                    return {
                        "status": False,
                        "msg": f"Room id:{id} not found"
                    }, 200
                
                serialized_room = serialization(res, exclude=exclude)
                
                # GET room with given id
                return {
                    # "id": res.id,
                    # "room_name": res.room_name,
                    # "roomAdderss1": res.room_address1,
                    # "room_address2": res.room_address2,
                    # "max_users": res.max_users,
                    "status": True,
                    "room": serialized_room,
                    "msg": f"Room id:{id} found",
                }, 200

        # error      
        except OSError as e:
            print(e)
            return {
                "msg": "Room GET failed"
            }, 500
        
    # DELETE room by id
    def delete(self, id):
        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        # print("!!!!!!!!!TYPE: ", user_status['User']['type'], "!!!!!!!!!!!!", flush=True)
        if(check_jwt_exists(user_status) 
           and (user_status['User']['type'] != 2)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "status": True,
                        "msg": f"Room id:{id} not found"
                    }, 200
                
                # DELETE room
                conn.execute(
                    delete(Room).where(Room.id == id)
                )

                # DELETE room done
                return {
                    "status": True,
                    "msg": "Room Deleted"
                }, 200

        # error
        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "Room Delete Failed"
            }, 500
        
    # UPDATE Room by id
    def patch(self, id):
        # request body data, needs to be validated
        req = request.json
        
        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        # print("!!!!!!!!!TYPE: ", user_status['User']['type'], "!!!!!!!!!!!!", flush=True)
        if(check_jwt_exists(user_status) 
           and (user_status['User']['type'] != 2)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # validate data from request body
                valid_data, invalid_data = Room.validate(req)
                
                if len(invalid_data) > 0:
                    return {
                        "status": False,
                        "msg": "invalid data",
                        "invalid": invalid_data
                    }, 200

                roomById = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()
                # if there's no such room by given id
                if roomById is None:
                    return {
                        "status": False,
                        "msg": f"Room id:{id} not found"
                    }, 200
                
                # if updated room data already exists in the table
                for room in valid_data:
                    if check_if_room_identical(conn, Room, valid_data):
                        return{
                            "statsus": False,
                            "msg": f"Room {room['room_name']} already exists." 
                        }, 200

                
                # UPDATE room
                conn.execute(
                    update(Room).where(Room.id == id),{
                        **valid_data
                    }
                )

                # UPDATE room done
                return {
                    "status": True,
                    "msg": "Room Updated"
                }, 200

        # error
        except OSError as e:
            print(e)
            return {
                "status": False,
                "msg": "Room Update Failed"
            }, 500

@admin.route('/upload/<int:id>')
class PreviewImageUpload(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg'}

        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    # insert preview_image into a room found by id
    def post(self, id):
        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        # print("!!!!!!!!!TYPE: ", user_status['User']['type'], "!!!!!!!!!!!!", flush=True)
        if(check_jwt_exists(user_status) 
           and (user_status['User']['type'] != 2)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200
        
        uploaded_image = request.files['image']
        # print(uploaded_image.filename, flush=True)

        # validate uploaded image
        # check extension
        # Not working... upload_image.filename
        # if (not uploaded_image 
        #     or not self.allowed_file(uploaded_image.filename)):
        #     return {
        #         "status": False,
        #         "msg": "image invalid",
        #         "invalid": uploaded_image
        #     }, 200

        try:
            with self.query_model("Room") as (conn, Room):
                # The above code is reading the contents of an uploaded image file and storing it in
                # the variable `preview_image`.
                preview_image = uploaded_image.read()

                # insert image into the room                
                conn.execute(
                    update(Room).where(Room.id == id), {
                        "preview_image": preview_image
                    }
                )

                # insert image done
                return {
                    "status": True,
                    "msg": "Image uploaded",
                    "uploadedImage": uploaded_image.filename,
                }
        except OSError as e:
            print(e)
            return {
                "status": False,
                "msg": "Uploading image failed"
            }, 500
