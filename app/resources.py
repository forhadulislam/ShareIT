'''
    # Borrowed codes:
        HALJsonObject ( Some codes are copied from PWP Exercise )
        ShareITObject ( Some codes are copied PWP Exercise )

'''

import json
from flask import Flask, request, Response, g, _request_ctx_stack, redirect, send_from_directory
from flask.ext.restful import Resource, Api, abort
from werkzeug.exceptions import HTTPException, NotFound

from utils import RegexConverter
import db

#Constants for hypermedia formats and profiles
HalJSON = "application/hal+json"
JSON = "application/json"

SHAREIT_USER_PROFILE = "/profiles/user-profile"
SHAREIT_USER_PROFILES_PROFILE = "/profiles/user-profiles-profile"
SHAREIT_MESSAGE_PROFILE = "/profiles/message-profile"
SHAREIT_CATEGORY_PROFILE = "/profiles/category-profile"
SHAREIT_POST_PROFILE = "/profiles/post-profile"
SHAREIT_REPORT_PROFILE = "/profiles/report-profile"
SHAREIT_SEARCH_PROFILE = "/profiles/search-profile"
ERROR_PROFILE = "/profiles/error-profile"


# Fill these in
APIARY_PROFILES_URL = "http://docs.shareitpwp21.apiary.io/reference/"
APIARY_RELS_URL = "STUDENT_APIARY_PROJECT/reference/link-relations/"

USER_SCHEMA_URL = "/shareit/schema/user/"
USER_PROFILE_SCHEMA_URL = "/shareit/schema/user-profile/"
MESSAGE_SCHEMA_URL = "/shareit/schema/message/"
CATEGORY_SCHEMA_URL = "/shareit/schema/category/"
POST_SCHEMA_URL = "/shareit/schema/post/"
REPORT_SCHEMA_URL = "/shareit/schema/report/"
LINK_RELATIONS_URL = "/shareit/link-relations/"

# Gender List
genderList = ['M','F']

#Define the application and the api
app = Flask(__name__, static_folder="static", static_url_path="/.")
app.debug = True

app.config.update({"Engine": db.Engine()})
#Start the RESTful API.
api = Api(app)

'''
    Some codes are copied from PWP Exercises
'''

class HALJsonObject(dict):

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["error"] = {
            "message": title,
            "messages": [details],
        }

    def add_link(self, ns, **kwargs):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "_links" not in self:
            self["_links"] = {}

        self["_links"][ns] = kwargs

    def add_template(self, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        : param str ctrl_name: name of the control (including namespace if any)        
        """

        if "template" not in self:
            self["template"] = {}
        
        if "data" not in self["template"]:
            self["template"]["data"] = []
        
        self["template"]["data"].push( kwargs )
        
    
'''
    Some codes are copied from PWP Exercise 3, 4
'''
class ShareITObject(HALJsonObject):    
    """
    Our main ShareITObject which can be 
    """

    def __init__(self, **kwargs):
        """
        Calls dictionary init method with any received keyword arguments. Adds
        the controls key afterwards because hypermedia without controls is not 
        hypermedia. 
        """

        super(ShareITObject, self).__init__(**kwargs)
        self["_links"] = {}
        
    def add_link_add_user(self):
        """
        This adds the add-user control to an object. Intended ffor the 
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["_links"]["add"] = {
            "href": api.url_for(Users),
            "method": "POST"
        }
    
    def add_link_add_item(self, item):
        """
        This adds the add-user control to an object. Intended ffor the 
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["_links"]["add"] = {
            "href": api.url_for(item),
            "method": "POST"
        }
    
    def add_link_messages_all(self):
        """
        Adds the message-all link to an object. Intended for the document object.
        """

        self["_links"]["message"] = {
            "href": api.url_for(Messages),
            "method": "GET"
        }

    def add_template_data(self, required=False, prompt="", name="", value=""):
        """
        Add the template data of the ShareITObject
        """
        if "template" not in self:
            self["template"] = {}
        
        if "data" not in self["template"]:
            self["template"]["data"] = []
            
        dataTem = {
            "required": required,
            "prompt": prompt,
            "name": name,
            "value": value
          }
        
        self["template"]["data"].append( dataTem )

#ERROR Functionalities

def create_error_response(status_code, title, message=None):
    """ 
    Creates a: py: class:`flask.Response` instance when sending back an
    HTTP error response

    : param integer status_code: The HTTP status code of the response
    : param str title: A short description of the problem
    : param message: A long description of the problem
    : rtype:: py: class:`flask.Response`
    """

    resource_url = None
    #We need to access the context in order to access the request.path
    ctx = _request_ctx_stack.top
    if ctx is not None:
        resource_url = request.path
    envelope = HALJsonObject(resource_url=resource_url)
    envelope.add_error(title, message)

    return Response(json.dumps(envelope), status_code, mimetype=HalJSON+";"+ERROR_PROFILE)

@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found", "This resource url does not exit")

@app.errorhandler(400)
def resource_not_found(error):
    return create_error_response(400, "Malformed input format", "The format of the input is incorrect")

@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error", "The system has failed. Please, contact the administrator")

@app.before_request
def connect_db():
    """
    Creates a database connection before the request is proccessed
    """

    g.con = app.config["Engine"].connect()

#HOOKS
@app.teardown_request
def close_connection(exc):
    """ 
    Closes the database connection
    """

    if hasattr(g, "con"):
        g.con.close()

 
# RESOURCES


class Users(Resource):

    def get(self):
        """
        Gets a list of all the users in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/hal+json
            * Profile: User
                /profiles/user-profile


        Semantic descriptions used in items: username, email

        Link relations used in links: messages, 

        Semantic descriptors used in template: username, email
        
        """
        #Create the users list
        users_db = g.con.get_all_users()

        #FILTER AND GENERATE THE RESPONSE
       #Create the envelope
        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(Users))
        envelope.add_link_add_user()
        envelope.add_link_messages_all()
        envelope.add_template_data(True, prompt="Enter username", name="username", value="")
        envelope.add_template_data(True, prompt="Enter email", name="email", value="")

        items = envelope["items"] = []

        for user in users_db:
            item = HALJsonObject(
                username=user["username"],
                email=user["email"],
                reg_date=user["reg_date"]
            )
            #item.add_control_messages_history(user["nickname"])
            item.add_link("self", href=api.url_for(User, username=user["username"]))
            item.add_link("profile", href=SHAREIT_USER_PROFILE)
            
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_USER_PROFILE)

    def post(self):
        """
        Adds a new user in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: User

        Semantic descriptors used in template:
        username(mandatory), email(mandatory).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another user with the same username
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json
         
        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
        #Get the request body and serialize it to object
        #We should check that the format of the request body is correct. Check
        #That mandatory attributes are there.

        # pick up username so we can check for conflicts
        try:
            username = request_body["username"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "User username was missing from the request")

        #Conflict if user already exist
        if g.con.contains_user(username):
            return create_error_response(409, "Wrong nickname", "There is already a user with same username: %s." % username)       

        # pick up rest of the mandatory fields
        try:
            username = request_body["username"]
            email = request_body["email"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")        
        
        #Conflict if email already exist
        if g.con.check_user_by_email(email):
            return create_error_response(409, "Wrong email", "There is already a user with same email: %s." % email)
            
        user = {
            "username": username,
            "email": email
           }

        try:
            username = g.con.create_user(user)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )

        #CREATE RESPONSE AND RENDER
        return Response(status=201,
            headers={"Location": api.url_for(User, username=user['username'])})

class User(Resource):
    """
    User Resource.
    """

    def get(self, username):
        """
        Get basic information of a user:

        INPUT PARAMETER:
       : param str username: Username of the required user.

        OUTPUT:
         * Return 200 if the username exists.
         * Return 404 if the username is not stored in the system.

        RESPONSE ENTITY BODY:

        * Media type: application/hal+json
        * Profile : application/hal+json

        Link relations used: self, collection, public-data, private-data,
        messages.

        Semantic descriptors used: username, email and reg_date

        """

        #PERFORM OPERATIONS
        user_db = g.con.get_user_by_username(username)
        if not user_db:
            return create_error_response(404, "Unknown user",
                                         "There is no a user with nickname %s"
                                         % username)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = ShareITObject(
            username=user_db["username"],
            email=user_db["email"],
            reg_date= user_db["reg_date"]        
        )
        
        envelope.add_link("shareit", href=LINK_RELATIONS_URL)
        envelope.add_link("self", href=api.url_for(User, username=username))
        envelope.add_link("edit", href=api.url_for(User, username=username))
        envelope.add_link("delete", href=api.url_for(User, username=username))
        envelope.add_link("profile", href=SHAREIT_USER_PROFILE)
        '''
        envelope.add_control_messages_all()
        envelope.add_control("collection", href=api.url_for(Users))
        envelope.add_control_delete_user(nickname)
        '''
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_USER_PROFILE)
    
    def put(self, username):
        """
        Modify the public profile of a user. 
        
        REQUEST ENTITY BODY:
        * Media type: JSON
        
        """
        
        if not g.con.contains_user(username):
            return create_error_response(404, "Unknown user", "There is no user with username {}".format(username))
            
        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")            
        
        try:
            email = request_body["email"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")
        
        user = {
                "email": email,
            }
        
            
        if not g.con.modify_user_by_username(username, user['email']):
            return create_error_response(404, "Unknown user", "There is no user with username {}".format(username))
        
        return "", 204

    def delete(self, username):
        """
        Delete a user in the system.

       : param str username: username of the required user.

        RESPONSE STATUS CODE:
         * If the user is deleted returns 204.
         * If the username does not exist return 404
        """

        #PEROFRM OPERATIONS
        #Try to delete the user. If it could not be deleted, the database
        #returns None.
        if g.con.delete_user(username):
            #RENDER RESPONSE
            return '', 204
        else:
            #GENERATE ERROR RESPONSE
            return create_error_response(404, "Unknown user",
                                         "There is no a user with username %s"
                                         % username)
                                         
                                         
# Message Resource
class Messages(Resource):
    def get(self):
        """
        Gets a list of all the messages in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/hal+json
            * Profile: Messages
                /profiles/message-profile

        Link relations used in items: user

        Semantic descriptions used in items: sender, receiver, details

        Link relations used in links: messages-all

        Semantic descriptors used in template: sender, receiver, details
        
        """
        #PERFORM OPERATIONS
        #Create the messages list
        messages_db = g.con.get_messages()

        #FILTER AND GENERATE THE RESPONSE
       #Create the envelope
        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(Messages))
        envelope.add_link_add_item(Messages)
        envelope.add_link_messages_all()
        
        envelope.add_template_data(True, prompt="", name="sender", value="")
        envelope.add_template_data(True, prompt="", name="receiver", value="")
        envelope.add_template_data(True, prompt="", name="message_details", value="")
        envelope.add_template_data(False, prompt="", name="send_time", value="")

        items = envelope["items"] = []

        for message in messages_db:
            item = HALJsonObject(
                message
            )
            item.add_link("profile", href=SHAREIT_MESSAGE_PROFILE)
            item.add_link("self", href=api.url_for(Message, messageid=message["message_id"]))
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_MESSAGE_PROFILE)

    def post(self):
        """
        Adds a new message in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: ShareIt_Message

        Semantic descriptors used in template:
        message_details(mandatory), sender(mandatory), receiver(mandatory), send_time(optional).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another user with the same username
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json
         
        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
        #Get the request body and serialize it to object
        #We should check that the format of the request body is correct. Check
        #That mandatory attributes are there.

        # pick up rest of the mandatory fields
        try:
            message_details = request_body["message_details"]
            sender = request_body["sender"]
            receiver = request_body["receiver"]
                        
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")        
        
        send_time = request_body.get('send_time', None)
        
        message = {
            "message_details": message_details,
            "sender": sender,
            "receiver": receiver,
            "send_time": send_time
           }
        
        if not g.con.check_user_by_id(sender):
            return create_error_response(404, "Unknown sender", "There is no user with id {}".format(sender))
            
        if not g.con.check_user_by_id(receiver):
            return create_error_response(404, "Unknown receiver", "There is no user with id {}".format(receiver))
        
        try:
            messageid = g.con.create_message(message)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )
        if not messageid:
            return create_error_response(422 , "Unprocessable Entity",
                                         "Be sure you include all mandatory properties"
                                        )
        
        
        #CREATE RESPONSE AND RENDER
        return Response(status=201,
            headers={"Location": api.url_for(Message, messageid=messageid)})

  
class Message(Resource):
    """
    Message Resource.
    """

    def get(self, messageid):
        """
        Get basic information of a user:

        INPUT PARAMETER:
       : param int messageid: id of the message.

        OUTPUT:
         * Return 200 if the message exists.
         * Return 404 if the message is not found in the system.

        RESPONSE ENTITY BODY:

        * Media type recommended: application/hal+json
        * Profile : application/hal+json

        Link relations used: user.

        Semantic descriptors used: message_details, sender, and receiver

        """

        #PERFORM OPERATIONS
        msg_db = g.con.get_message(messageid)
        if not msg_db:
            return create_error_response(404, "Unknown message",
                                         "There is no a message with id %s"
                                         % messageid)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = ShareITObject(
            message_details= msg_db['message_details'],
            sender= msg_db['sender'],
            receiver= msg_db['receiver'],
            send_time= msg_db['send_time'],
            message_id= msg_db['message_id']        
        )
        
        envelope.add_link("shareit", href=LINK_RELATIONS_URL)
        envelope.add_link("self", href=api.url_for(Message, messageid=messageid))
        envelope.add_link("edit", href=api.url_for(Message, messageid=messageid))
        envelope.add_link("delete", href=api.url_for(Message, messageid=messageid))
        envelope.add_link("profile", href=SHAREIT_MESSAGE_PROFILE)
        '''
        # Previous code
        
        
        envelope.add_control_messages_history(nickname)
        envelope.add_control_messages_all()
        envelope.add_control("collection", href=api.url_for(Users))
        envelope.add_control_delete_user(nickname)
        '''
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_MESSAGE_PROFILE)
    
    def put(self, messageid):
        """
        Modify the a message. 
        
        REQUEST ENTITY BODY:
        * Media type: JSON
        
        """
        
        if not g.con.get_message(messageid):
            return create_error_response(404, "Unknown message", "There is no message with id {}".format(messageid))
            
        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")            
        
        try:
            message_details = request_body["message_details"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")
        
        
            
        if not g.con.modify_message(messageid, message_details):
            return create_error_response(404, "Unknown message", "There is no message with id {}".format(messageid))
        
        return "", 204

    def delete(self, messageid):
        """
        Delete a message in the system.

       : param int messageid:  id of the message.

        RESPONSE STATUS CODE:
         * If the message is deleted returns 204.
         * If the messageid does not exist return 404
        """

        #PEROFRM OPERATIONS
        #Try to delete the message. If it could not be deleted, the database returns None.
        if g.con.delete_message(messageid):
            #RENDER RESPONSE
            return '', 204
        else:
            #GENERATE ERROR RESPONSE
            return create_error_response(404, "Unknown message",
                                         "There is no a message with id %s"
                                         % messageid)
    


class UserProfiles(Resource):
    """
    UserProfiles Resource.
    """
    def get(self):
        """
        Gets a list of all the users-profile in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/hal+json
            * Profile:  /profiles/user-profile

        Link relations used in items: user

        Semantic descriptions used in items: nickname, registrationdate

        Link relations used in links: messages-all

        Semantic descriptors used in template: fullname, address, website, skype, gender
        
        """
        #Create the users-profile list
        users_db = g.con.get_users()

        #FILTER AND GENERATE THE RESPONSE
        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(UserProfiles))
        envelope.add_link_add_item(UserProfiles)
        envelope.add_link_messages_all()
        
        envelope.add_template_data(True, prompt="", name="user_id", value="")
        envelope.add_template_data(False, prompt="", name="fullname", value="")
        envelope.add_template_data(False, prompt="", name="phone", value="")
        envelope.add_template_data(False, prompt="", name="website", value="")
        envelope.add_template_data(False, prompt="", name="address", value="")
        envelope.add_template_data(False, prompt="", name="skype", value="")
        envelope.add_template_data(False, prompt="", name="gender", value="")

        items = envelope["items"] = []

        for user in users_db:
            item = HALJsonObject(
                user_id=user["primary_profile"]["user_id"],  
                fullname=user["profile_details"]["fullname"],  
                phone=user["profile_details"]["phone"],
                website=user["profile_details"]["website"],
                address=user["profile_details"]["address"],
                skype=user["profile_details"]["skype"],
                gender=user["profile_details"]["gender"]
                
            )
            
            item.add_link("self", href=api.url_for(UserProfile, userid=user["primary_profile"]["user_id"]))
            item.add_link("profile", href=SHAREIT_USER_PROFILE)
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_USER_PROFILES_PROFILE)

    def post(self):
        """
        Adds a new users-profile in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: User

        Semantic descriptors used in template:
        user_id(mandatory), fullname, address, website, skype, gender

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another users-profile with the same user_id
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json
         
        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
        
        
        try:
            user_id = request_body["user_id"]                        
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties") 

        #Conflict if user already exist
        if g.con._check_if_profile_exists(user_id):
            return create_error_response(409, "User profile already exists", "There is already a user profile with same id: %s." % user_id)       
        
        fullname = request_body.get('fullname', None)
        phone = request_body.get('phone', None)
        website = request_body.get('website', None)
        address = request_body.get('address', None)
        skype = request_body.get('skype', None)
        gender = request_body.get('gender', None)
        
        userProfile = {
                "user_id": user_id,
                "fullname": fullname,
                "phone": phone,
                "website": website,
                "address": address,
                "skype": skype,
                "gender": gender
            }        
       
        if gender and (gender not in genderList):
            return create_error_response(400, "Invalid gender provided", "There is no such gender")        
        
        try:
            user_id = g.con.create_user_profile(userProfile)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )
        
        if not user_id:
            return create_error_response(422 , "Unprocessable Entity",
                                         "Be sure you include all mandatory properties"
                                        )
            
        #CREATE RESPONSE AND RENDER
        return Response(status=201,
            headers={"Location": api.url_for(UserProfile, userid=user_id)})
    
class UserProfile(Resource):
    """
    User profile Resource.
    """

    def get(self, userid):
        """
        Get basic information of a user:

        INPUT PARAMETER:
       : param str userid: id of the required user.

        OUTPUT:
         * Return 200 if the id exists.
         * Return 404 if the id is not stored in the system.

        RESPONSE ENTITY BODY:

        * Media type recommended: application/hal+json
        * Profile : application/hal+json

        Link relations used: self, user.

        Semantic descriptors used: fullname, website, phone, website, skype and gender

        """

        #PERFORM OPERATIONS
        user_db = g.con.get_user_profile(userid)
        if not user_db:
            return create_error_response(404, "Unknown user",
                                         "There is no a user with id %s"
                                         % userid)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = ShareITObject(
            fullname=user_db["fullname"],
            phone=user_db["phone"],
            website=user_db["website"],
            address=user_db["address"],
            skype=user_db["skype"],
            gender= user_db["gender"]        
        )
        
        envelope.add_link("shareit", href=LINK_RELATIONS_URL)
        envelope.add_link("self", href=api.url_for(UserProfile, userid=userid))
        envelope.add_link("edit", href=api.url_for(UserProfile, userid=userid))
        envelope.add_link("profile", href=SHAREIT_USER_PROFILE)
        
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_USER_PROFILES_PROFILE)
    
    def put(self, userid):
        """
        Modify the public profile of a user. 
        
        REQUEST ENTITY BODY:
        * Media type: JSON
        
        """
        
        if not g.con._check_if_profile_exists(userid):
            return create_error_response(404, "Unknown user profile", "There is no user profile with id {}".format(userid))
            
        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")            
        
        fullname = request_body.get('fullname', None)
        phone = request_body.get('phone', None)
        website = request_body.get('website', None)
        address = request_body.get('address', None)
        skype = request_body.get('skype', None)
        gender = request_body.get('gender', None)
        
        userProfile = {
                "fullname": fullname,
                "phone": phone,
                "website": website,
                "address": address,
                "skype": skype,
                "gender": gender
            }
        
        if gender and (gender not in genderList):
            return create_error_response(400, "Invalid gender provided", "There is no such gender")
            
        if not g.con.edit_user_profile(userid, userProfile):
            return create_error_response(404, "Unknown user profile", "There is no user profile with id {}".format(userid))
        
        return "", 204
    
class Categories(Resource):
    def get(self):
        """
        Gets a list of all the categories in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/hal+json
            * Profile: Messages
                /profiles/message-profile

        Link relations used in items: post,

        Semantic descriptions used in items: title, description

        Link relations used in links: categories-all
        
        """
        #PERFORM OPERATIONS
        #Create the categories list
        categories_db = g.con.get_categories()

        #FILTER AND GENERATE THE RESPONSE
        #Create the envelope
        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(Categories))
        envelope.add_link_add_item(Categories)
        envelope.add_link_messages_all()
        
        envelope.add_template_data(True, prompt="", name="title", value="")
        envelope.add_template_data(True, prompt="", name="description", value="")
        envelope.add_template_data(False, prompt="", name="add_date", value="")
        envelope.add_template_data(False, prompt="", name="last_update", value="")

        items = envelope["items"] = []

        for category in categories_db:
            item = HALJsonObject(
                category
            )
            
            #item.add_link("self", href=api.url_for(User, username=user["primary_profile"]["username"]))
            item.add_link("profile", href=SHAREIT_CATEGORY_PROFILE)
            item.add_link("self", href=api.url_for(Category, categoryid=category["category_id"]))
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_CATEGORY_PROFILE)

    def post(self):
        """
        Adds a new message in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: ShareIt_Message

        Semantic descriptors used in template:
        title(mandatory), description(mandatory).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another user with the same username
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json
         
        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
        #Get the request body and serialize it to object
        #We should check that the format of the request body is correct. Check
        #That mandatory attributes are there.

        # pick up rest of the mandatory fields
        try:
            title = request_body["title"]
            description = request_body["description"]
                        
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")        
        
        
        
        category = {
            "title": title,
            "description": description
           }
        
        if g.con._check_category_by_title(title):
            return create_error_response(409, "Wrong title", "The title already exists {}".format(title))
                    
        try:
            categoryid = g.con.create_category(category)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )
        if not categoryid:
            return create_error_response(422 , "Unprocessable Entity",
                                         "Be sure you include all mandatory properties"
                                        )
        
        
        #CREATE RESPONSE AND RENDER
        return Response(status=201,
            headers={"Location": api.url_for(Category, categoryid=categoryid)})
    
class Category(Resource):
    """
    Category Resource.
    """

    def get(self, categoryid):
        """
        Get basic information of a category:

        INPUT PARAMETER:
       : param int categoryid: id of the category.

        OUTPUT:
         * Return 200 if the category exists.
         * Return 404 if the category is not found in the system.

        RESPONSE ENTITY BODY:

        * Media type : application/hal+json
        * Profile : application/hal+json

        Link relations used: self, postmessages.

        Semantic descriptors used: title and description

        """

        #PERFORM OPERATIONS
        cat_db = g.con.get_category(categoryid)
        if not cat_db:
            return create_error_response(404, "Unknown category",
                                         "There is no a category with id %s"
                                         % categoryid)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
            
        envelope = ShareITObject(
            category_id= cat_db['category_id'],
            title= cat_db['title'],
            description= cat_db['description'],
            add_date= cat_db['add_date'],
            last_update= cat_db['last_update']        
        )
        
        envelope.add_link("shareit", href=LINK_RELATIONS_URL)
        envelope.add_link("self", href=api.url_for(Category, categoryid=categoryid))
        envelope.add_link("edit", href=api.url_for(Category, categoryid=categoryid))
        envelope.add_link("delete", href=api.url_for(Category, categoryid=categoryid))
        envelope.add_link("profile", href=SHAREIT_CATEGORY_PROFILE)
        '''
        # Previous code
        
        
        envelope.add_control_messages_history(nickname)
        envelope.add_control_messages_all()
        envelope.add_control("collection", href=api.url_for(Users))
        envelope.add_control_delete_user(nickname)
        '''
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_CATEGORY_PROFILE)
    
    def put(self, categoryid):
        """
        Modify the a category. 
        
        REQUEST ENTITY BODY:
        * Media type: JSON
        
        """
        
        if not g.con.get_category(categoryid):
            return create_error_response(404, "Unknown category", "There is no category with id {}".format(categoryid))
            
        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")            
        
        try:
            title = request_body["title"]
            description = request_body["description"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")
        
        
            
        if not g.con.edit_category(categoryid, title, description):
            return create_error_response(404, "Unknown category", "There is no category with id {}".format(categoryid))
        
        return "", 204

    def delete(self, categoryid):
        """
        Delete a category in the system.

       : param int categoryid:  id of the category.

        RESPONSE STATUS CODE:
         * If the category is deleted returns 204.
         * If the category does not exist return 404
        """

        #PEROFRM OPERATIONS
        #Try to delete the category. If it could not be deleted, the database returns None.
        if g.con.delete_category(categoryid):
            #RENDER RESPONSE
            return '', 204
        else:
            #GENERATE ERROR RESPONSE
            return create_error_response(404, "Unknown category",
                                         "There is no a category with id %s"
                                         % categoryid)

class Posts(Resource):
    def get(self):
        """
        Gets a list of all the posts in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/hal+json
            * Profile: Posts
                /profiles/post-profile

        Link relations used in items: user, category

        Semantic descriptions used in items: title, description

        Link relations used in links: user, category

        Semantic descriptors used in template: title, description, tags, category
        
        """
        #Create the posts list
        posts_db = g.con.get_posts()

        #FILTER AND GENERATE THE RESPONSE
       #Create the envelope
        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(Posts))
        envelope.add_link_add_item(Posts)
        envelope.add_link_messages_all()
        
        envelope.add_template_data(True, prompt="", name="title", value="")
        envelope.add_template_data(True, prompt="", name="details", value="")
        envelope.add_template_data(True, prompt="", name="user_id", value="")
        envelope.add_template_data(False, prompt="", name="category_id", value="")
        envelope.add_template_data(False, prompt="", name="tags", value="")
        envelope.add_template_data(False, prompt="", name="add_date", value="")
        envelope.add_template_data(False, prompt="", name="last_update", value="")
        
        items = envelope["items"] = []

        for post in posts_db:
            item = HALJsonObject(
                post
            )
            #item.add_control_messages_history(user["nickname"])
            #item.add_link("self", href=api.url_for(User, username=user["primary_profile"]["username"]))
            item.add_link("profile", href=SHAREIT_MESSAGE_PROFILE)
            item.add_link("self", href=api.url_for(Post, postid=post["post_id"]))
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_POST_PROFILE)

    def post(self):
        """
        Adds a new post in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: Post

        Semantic descriptors used in template:
        message_details(mandatory), sender(mandatory), receiver(mandatory), send_time(optional).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another user with the same username
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json
         
        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSING THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )

        # pick up rest of the mandatory fields
        try:
            user_id = request_body["user_id"]
            title = request_body["title"]
            details = request_body["details"]                  
                        
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")        
        
        category_id = request_body.get('category_id', None)
        tags = request_body.get('tags', None)
        
        if not g.con.check_user_by_id(user_id):
            return create_error_response(404, "Unknown user", "There is no user with id {}".format(user_id))
        
        if category_id:
            if not g.con._check_category_by_id(category_id):
                return create_error_response(404, "Unknown category", "There is no category with id {}".format(category_id))
        
        post = {
            "user_id": user_id,
            "title": title,
            "details": details,
            "category_id": category_id,
            "tags": tags
           }
        
        
        
        try:
            postid = g.con.create_post(post)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )
        if not postid:
            return create_error_response(422 , "Unprocessable Entity",
                                         "Be sure you include all mandatory properties"
                                        )
        
        
        #CREATE RESPONSE AND RENDER
        return Response(status=201,
            headers={"Location": api.url_for(Post, postid=postid)})
    
class Post(Resource):
    """
    Post Resource.
    """

    def get(self, postid):
        """
        Get basic information of a post:

        INPUT PARAMETER:
       : param int postid: id of the post.

        OUTPUT:
         * Return 200 if the post exists.
         * Return 404 if the post is not found in the system.

        RESPONSE ENTITY BODY:

        * Media type recommended: application/hal+json
        * Profile recommended: application/hal+json

        Link relations used: collection, public-data, private-data,
        messages.

        Semantic descriptors used: nickname and registrationdate

        """

        #PERFORM OPERATIONS
        post_db = g.con.get_post(postid)
        if not post_db:
            return create_error_response(404, "Unknown post",
                                         "There is no a post with id %s"
                                         % postid)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = ShareITObject(
            user_id= post_db['user_id'],
            title= post_db['title'],
            details= post_db['details'],
            category_id= post_db['category_id'],
            tags= post_db['tags'],
            add_date= post_db['add_date'],
            last_update= post_db['last_update']
        )
        
        envelope.add_link("shareit", href=LINK_RELATIONS_URL)
        envelope.add_link("self", href=api.url_for(Post, postid=postid))
        envelope.add_link("delete", href=api.url_for(Post, postid=postid))
        envelope.add_link("edit", href=api.url_for(Post, postid=postid))
        envelope.add_link("profile", href=SHAREIT_POST_PROFILE)
                
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_POST_PROFILE)
    
    def put(self, postid):
        """
        Modify the a post. 
        
        REQUEST ENTITY BODY:
        * Media type: JSON
        
        """
        
        if not g.con._check_post_by_id(postid):
            return create_error_response(404, "Unknown post", "There is no post with id {}".format(postid))
            
        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")            
        
        try:
            user_id = request_body["user_id"]
            title = request_body["title"]
            details = request_body["details"] 
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")

        category_id = request_body.get('category_id', None)
        tags = request_body.get('tags', None)
        
        if not g.con.check_user_by_id(user_id):
            return create_error_response(404, "Unknown user", "There is no user with id {}".format(user_id))
        
        if category_id:
            if not g.con._check_category_by_id(category_id):
                return create_error_response(404, "Unknown category", "There is no category with id {}".format(category_id))
        
        post = {
            "user_id": user_id,
            "title": title,
            "details": details,
            "category_id": category_id,
            "tags": tags
           }
            
        if not g.con.edit_post(postid, post):
            return create_error_response(404, "Unknown post", "There is no post with id {}".format(postid))
        
        return "", 204

    def delete(self, postid):
        """
        Delete a post in the system.

       : param int postid:  id of the post.

        RESPONSE STATUS CODE:
         * If the post is deleted returns 204.
         * If the postid does not exist return 404
        """

        #PEROFRM OPERATIONS
        #Try to delete the message. If it could not be deleted, the database returns None.
        if g.con.delete_post(postid):
            #RENDER RESPONSE
            return '', 204
        else:
            #GENERATE ERROR RESPONSE
            return create_error_response(404, "Unknown post",
                                         "There is no a post with id %s"
                                         % postid)


class Reports(Resource):
    def get(self):
        """
        Gets a list of all the reports` in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/hal+json
            * Profile: application/hal+json

        Link relations used in items: user, post

        Semantic descriptions used in items: title, description

        Link relations used in links: messages-all

        Semantic descriptors used in template: address, avatar, birthday
        
        """
        #PERFORM OPERATIONS
        #Create the report list
        reports_db = g.con.get_reports()

        #FILTER AND GENERATE THE RESPONSE
       #Create the envelope
        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(Reports))
        envelope.add_link_add_item(Reports)
        envelope.add_link_messages_all()
        
        envelope.add_template_data(True, prompt="", name="post_id", value="")
        envelope.add_template_data(True, prompt="", name="details", value="")
        envelope.add_template_data(True, prompt="", name="user_id", value="")

        items = envelope["items"] = []

        for report in reports_db:
            item = HALJsonObject(
                report
            )
            #item.add_link("self", href=api.url_for(User, username=user["primary_profile"]["username"]))
            item.add_link("profile", href=SHAREIT_MESSAGE_PROFILE)
            item.add_link("self", href=api.url_for(Report, reportid=report["report_id"]))
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_REPORT_PROFILE)

    def post(self):
        """
        Adds a new report in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: Report

        Semantic descriptors used in template:
        message_details(mandatory), sender(mandatory), receiver(mandatory), send_time(optional).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another user with the same username
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json
         
        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
        #Get the request body and serialize it to object
        #We should check that the format of the request body is correct. Check
        #That mandatory attributes are there.

        # pick up rest of the mandatory fields
        try:
            post_id = request_body["post_id"]
            user_id = request_body["user_id"]                 
            details = request_body["details"]                 
                        
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")        
        
        
        if not g.con.check_user_by_id(user_id):
            return create_error_response(404, "Unknown user", "There is no user with id {}".format(user_id))
        
        if not g.con._check_post_by_id(post_id):
            return create_error_response(404, "Unknown post", "There is no post with id {}".format(post_id))
        '''
        report = {
            "post_id": post_id,
            "user_id": user_id,
            "details": details
           }        
        '''
        try:
            reportid = g.con.create_report(post_id, user_id, details)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )
        if not reportid:
            return create_error_response(422 , "Unprocessable Entity",
                                         "Be sure you include all mandatory properties"
                                        )
        
        
        #CREATE RESPONSE AND RENDER
        return Response(status=201,
            headers={"Location": api.url_for(Report, reportid=reportid)})
    
class Report(Resource):
    """
    Report Resource.
    """

    def get(self, reportid):
        """
        Get basic information of a report:

        INPUT PARAMETER:
       : param int reportid: id of the report.

        OUTPUT:
         * Return 200 if the report exists.
         * Return 404 if the report is not found in the system.

        RESPONSE ENTITY BODY:

        * Media type recommended: application/vnd.mason+json
        * Profile recommended: application/vnd.mason+json

        Link relations used: collection, public-data, private-data,
        messages.

        Semantic descriptors used: nickname and registrationdate

        """

        #PERFORM OPERATIONS
        report_db = g.con.get_report(reportid)
        if not report_db:
            return create_error_response(404, "Unknown report",
                                         "There is no a report with id %s"
                                         % reportid)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = ShareITObject(
            user_id= report_db['user_id'],
            details= report_db['details'],
            post_id= report_db['post_id']
        )
        
        envelope.add_link("shareit", href=LINK_RELATIONS_URL)
        envelope.add_link("self", href=api.url_for(Report, reportid=reportid))
        envelope.add_link("edit", href=api.url_for(Report, reportid=reportid))
        envelope.add_link("delete", href=api.url_for(Report, reportid=reportid))
        envelope.add_link("profile", href=SHAREIT_REPORT_PROFILE)
                
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_REPORT_PROFILE)
    
    def put(self, reportid):
        """
        Modify the a report. 
        
        REQUEST ENTITY BODY:
        * Media type: JSON
        
        """
        
        if not g.con._check_report_by_id(reportid):
            return create_error_response(404, "Unknown report", "There is no report with id {}".format(reportid))
            
        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")            
        
        try:
            user_id = request_body["user_id"]
            details = request_body["details"]
            post_id = request_body["post_id"] 
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")

        
        if not g.con.check_user_by_id(user_id):
            return create_error_response(404, "Unknown user", "There is no user with id {}".format(user_id))        
       
       
        if not g.con.edit_report(reportid, details):
            return create_error_response(404, "Unknown report", "There is no report with id {}".format(reportid))
        
        return "", 204

    def delete(self, reportid):
        """
        Delete a report in the system.

       : param int reportid:  id of the report.

        RESPONSE STATUS CODE:
         * If the report is deleted returns 204.
         * If the reportid does not exist return 404
        """

        #PEROFRM OPERATIONS
        #Try to delete the message. If it could not be deleted, the database returns None.
        if g.con.delete_report(reportid):
            #RENDER RESPONSE
            return '', 204
        else:
            #GENERATE ERROR RESPONSE
            return create_error_response(404, "Unknown report",
                                         "There is no a report with id %s"
                                         % reportid)
    
class Search(Resource):
    """
    Search Resource.
    """

    def get(self):
        """
        Get basic search of posts:

        """
        
        #PERFORM OPERATIONS
        try:
            queryWord = request.args.get('q')
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")
        
        
        #PERFORM OPERATIONS
        #Create the posts list
        post_db = g.con.search_posts(queryWord)
        
        if not post_db:
            return create_error_response(404, "No item found", "There is no post with keyword {}".format(queryWord))

        envelope = ShareITObject()

        envelope.add_link("shareit", href=LINK_RELATIONS_URL)        
        envelope.add_link("self", href=api.url_for(Search))
        envelope.add_link_add_user()
        envelope.add_link_messages_all()
        

        items = envelope["items"] = []

        for post in post_db:
            item = HALJsonObject(
                post
            )
            item.add_link("profile", href=SHAREIT_SEARCH_PROFILE)
            item.add_link("self", href=api.url_for(Post, postid=post["post_id"]))
            items.append(item)
            
        
        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=HalJSON+";" + SHAREIT_SEARCH_PROFILE)
    
#Add the Regex Converter so we can use regex expressions when we define the
#routes
app.url_map.converters["regex"] = RegexConverter

# Routes

api.add_resource(Users, "/shareit/api/users/", endpoint="users")
api.add_resource(User, "/shareit/api/users/<username>/", endpoint="user")
api.add_resource(Messages, "/shareit/api/messages/", endpoint="messages")
api.add_resource(Message, "/shareit/api/messages/<messageid>/", endpoint="message")
api.add_resource(Categories, "/shareit/api/categories/", endpoint="categories")
api.add_resource(Category, "/shareit/api/categories/<categoryid>/", endpoint="category")
api.add_resource(Posts, "/shareit/api/posts/", endpoint="posts")
api.add_resource(Post, "/shareit/api/posts/<postid>/", endpoint="post")
api.add_resource(Reports, "/shareit/api/reports/", endpoint="reports")
api.add_resource(Report, "/shareit/api/reports/<reportid>/", endpoint="report")

api.add_resource(UserProfiles, "/shareit/api/user-profiles/", endpoint="user-profiles")
api.add_resource(UserProfile, "/shareit/api/user-profiles/<userid>/", endpoint="user-profile")

api.add_resource(Search, "/shareit/api/search/posts/", endpoint="search")


#Redirect profile
@app.route("/profiles/<profile_name>")
def redirect_to_profile(profile_name):
    return redirect(APIARY_PROFILES_URL + "profiles/"  + profile_name)

@app.route("/shareit/link-relations/<rel_name>/")
def redirect_to_rels(rel_name):
    return redirect(APIARY_RELS_URL + rel_name)

#Send our schema file(s)
@app.route("/shareit/schema/<schema_name>/")
def send_json_schema(schema_name):
    return send_from_directory("static/schema", "{}.json".format(schema_name))

#Start the application
if __name__ == "__main__":
    app.run(debug=True, port=3000)