'''
    # Borrowed codes:
        ResourcesAPITestCase ( PWP Exercise )

'''


import unittest, copy
import json
import flask

import app.resources as resources
import app.db as database

DB_PATH = "db/shareit_test.db"
ENGINE = database.Engine(DB_PATH)

JSON = "application/json"
HAL = "application/hal+json"
SHAREIT_USER_PROFILE = "/profiles/user-profile"
SHAREIT_USER_PROFILES_PROFILE = "/profiles/user-profiles-profile"
SHAREIT_MESSAGE_PROFILE = "/profiles/message-profile"
SHAREIT_CATEGORY_PROFILE = "/profiles/category-profile"
SHAREIT_POST_PROFILE = "/profiles/post-profile"
SHAREIT_REPORT_PROFILE = "/profiles/report-profile"
SHAREIT_SEARCH_PROFILE = "/profiles/search-profile"
ERROR_PROFILE = "/profiles/error-profile"


resources.app.config["TESTING"] = True
resources.app.config["SERVER_NAME"] = "localhost:3000"


resources.app.config.update({"Engine": ENGINE})

initial_messages = 5
initial_users = 5

class ResourcesAPITestCase(unittest.TestCase):
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Activate app_context for using url_for
        self.app_context = resources.app.app_context()
        self.app_context.push()
        #Create a test client
        self.client = resources.app.test_client()

    def tearDown(self):
        ENGINE.clear()
        self.app_context.pop()
        

'''
    Some codes are copied from PWP Exercises
'''        
class MessagesTestCase (ResourcesAPITestCase):

    # Valid contents
    message_1_request = {
          "message_details":"I want that product",
          "sender":1,
          "receiver":2
    }
    
    # Valid contents
    message_2_request = {
          "message_details":"Hello, can i come to see the product",
          "sender":2,
          "receiver":4
    }

    #Non-existing sender
    message_1_wrong = {
        "message_details":"I want that product",
        "sender":100,
        "receiver":2
    }

    #Non exsiting receiver
    message_2_wrong = {
        "message_details":"I want that product",
        "sender":1,
        "receiver":200
    }

    #Missing the sender
    message_3_wrong = {
        "message_details":"I want that product",
        "receiver":2
    }

    #Missing the receiver
    message_4_wrong = {
        "message_details":"I want that product",
        "sender":1
    }
    
    #Missing the message_details
    message_5_wrong = {
        "sender":1,
        "receiver":2
    }

    url = "/shareit/api/messages/"
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Messages)
    
    def test_get_messages(self):
        """
        Checks that GET Messages return correct status code and data format
        """
        print "("+self.test_get_messages.__name__+")", self.test_get_messages.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("messages"))
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = unicode(resp.data, 'latin-1')
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        self.assertIn("add", _links)
        
        _message1 = data["items"][0]
        __mlinks = _message1["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_get_messages_mimetype(self):
        """
        Checks that GET Messages return correct status code and mimetype
        """
        print "("+self.test_get_messages_mimetype.__name__+")", self.test_get_messages_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("messages"))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_MESSAGE_PROFILE))
                          
    def test_add_message(self):
        """
        Test adding a message to the database.
        """
        print "("+self.test_add_message.__name__+")", self.test_add_message.__doc__
        
        # First message
        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.message_1_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
        # First message
        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.message_2_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
    def test_add_message_wrong_media(self):
        """
        Test adding messages with a media different than JSON
        """
        print "("+self.test_add_message_wrong_media.__name__+")", self.test_add_message_wrong_media.__doc__
        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": "text"},
                                data=self.message_1_request.__str__()
                               )
        self.assertTrue(resp.status_code == 415)
    
    def test_add_message_incorrect_format(self):
        """
        Test that add message response correctly when sending erroneous message format.
        """
        print "("+self.test_add_message_incorrect_format.__name__+")", self.test_add_message_incorrect_format.__doc__
        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.message_4_wrong)
                               )
        self.assertTrue(resp.status_code == 400)

        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.message_5_wrong)
                               )
        self.assertTrue(resp.status_code == 400)
        
        
class MessageTestCase (ResourcesAPITestCase):

    # Valid contents
    message_1_edit = {
          "message_details":"Edited: I want that product"
    }
    
    # Valid contents
    message_2_edit = {
          "message_details":"Edited: Hello, can i come to see the product"
    }

    # Wrong Message
    message_1_wrong_edit = {
        "data":"I want that product"
    }
    
    message_2_wrong_edit = {
        "nothing": "nothing"
    }

    def setUp(self):
        super(MessageTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Message, messageid="1", _external=False)
        self.url_wrong = resources.api.url_for(resources.Message, messageid="90", _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        _url = "/shareit/api/messages/1/"
        print "("+self.test_url.__name__+")", self.test_url.__doc__
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Message)
            
    def test_wrong_url(self):
        """
        Checks that GET Message return correct status code if given a wrong message
        """
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

    def test_get_message(self):
        """
        Checks that GET Message return correct status code and data format
        """
        print "("+self.test_get_message.__name__+")", self.test_get_message.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code, 200)
            data = json.loads(resp.data)


            _links = data["_links"]
            self.assertIn("self", _links)
            self.assertIn("profile", _links)
            #self.assertIn("edit", _links)
            #self.assertIn("delete", _links)
            
    def test_get_message_mimetype(self):
        """
        Checks that GET Messages return correct status code and data format
        """
        print "("+self.test_get_message_mimetype.__name__+")", self.test_get_message_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_MESSAGE_PROFILE))
                          

    def test_modify_message(self):
        """
        Modify an exsiting message and check that the message has been modified correctly in the server
        """
        print "("+self.test_modify_message.__name__+")", self.test_modify_message.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.message_1_edit),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 204)
        #Check that the message has been modified
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        #Check that the title and the body of the message has been modified with the new data
        self.assertEquals(data["message_details"], self.message_1_edit["message_details"])
        

    def test_modify_unexisting_message(self):
        """
        Try to modify a message that does not exist
        """
        print "("+self.test_modify_unexisting_message.__name__+")", self.test_modify_unexisting_message.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.message_2_edit),
                                headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 404)

    def test_modify_wrong_message(self):
        """
        Try to modify a message sending wrong data
        """
        print "("+self.test_modify_wrong_message.__name__+")", self.test_modify_wrong_message.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.message_1_wrong_edit),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)
        resp = self.client.put(self.url,
                               data=json.dumps(self.message_2_wrong_edit),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)

    def test_delete_message(self):
        """
        Checks that Delete Message return correct status code if corrected delete
        """
        print "("+self.test_delete_message.__name__+")", self.test_delete_message.__doc__
        resp = self.client.delete(self.url)
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_message(self):
        """
        Checks that Delete Message return correct status code if given a wrong address
        """
        print "("+self.test_delete_unexisting_message.__name__+")", self.test_delete_unexisting_message.__doc__
        resp = self.client.delete(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

class UsersTestCase (ResourcesAPITestCase):

    user_1 = {        
        "username":"nahidan",
        "email":"nahidan@gmail.com"
    }
    
    user_2 = {        
        "username":"anotheruser",
        "email":"anotheruser@gmail.com"
    }
    
    user_1_edit = {
        "username":"agrani",
        "email":"agrani@gmail.com"
    }

    user_wrong_1 = {
        "email":"agrani@gmail.com"
    }

    user_wrong_2 = {
        "username":"agrani",
    }
    
    url = "/shareit/api/users/"    
    url_wrong = "/shareit/api/users-wrong/"

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Users)            
        
    def test_get_users(self):
        """
        Checks that GET Users return correct status code and data format
        """
        print "("+self.test_get_users.__name__+")", self.test_get_users.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("users"))
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        self.assertIn("add", _links)
        
        _message1 = data["items"][0]
        __mlinks = _message1["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_get_users_mimetype(self):
        """
        Checks that GET Messages return correct status code and mimetype
        """
        print "("+self.test_get_users_mimetype.__name__+")", self.test_get_users_mimetype.__doc__

        #Check status code 200
        resp = self.client.get(flask.url_for("users"))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_USER_PROFILE))
                          
    def test_add_user(self):
        """
        Test adding a user to the database.
        """
        print "("+self.test_add_user.__name__+")", self.test_add_user.__doc__
        
        # First user
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_1)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
        # Second message
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_2)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
    def test_add_user_wrong_media(self):
        """
        Test adding user with a media different than JSON
        """
        print "("+self.test_add_user_wrong_media.__name__+")", self.test_add_user_wrong_media.__doc__
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": "text"},
                                data=self.user_1.__str__()
                               )
        self.assertTrue(resp.status_code == 415)
    
    def test_add_user_incorrect_format(self):
        """
        Test that add user response correctly when sending erroneous data format.
        """
        print "("+self.test_add_user_incorrect_format.__name__+")", self.test_add_user_incorrect_format.__doc__
        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_1)
                               )
        self.assertTrue(resp.status_code == 400)

        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_wrong_2)
                               )
        self.assertTrue(resp.status_code == 400)
    
    
    
class UserTestCase (ResourcesAPITestCase):

    user_1 = {        
        "username":"nahida",
        "email":"nahida@gmail.com"
    }

    mod_user_1 = {
        "username":"nahidan",
        "email":"nahida19@yahoo.com"    
    }

    user_wrong_req_1 = {
        "username":"nahida"
    }

    user_wrong_req_2 = {
        "emailss":"nahida19@yahoo.com"
    }

    def setUp(self):
        super(UserTestCase, self).setUp()
        self.url = resources.api.url_for(resources.User, username="khaled", _external=False)
        self.url_wrong = resources.api.url_for(resources.User, username="noone", _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        _url = "/shareit/api/users/1/"
        print "("+self.test_url.__name__+")", self.test_url.__doc__
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.User)
            
    def test_wrong_url(self):
        """
        Checks that GET Message return correct status code if given a wrong message
        """
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)
        
    def test_get_user(self):
        """
        Checks that GET User return correct status code and data format
        """
        print "("+self.test_get_user.__name__+")", self.test_get_user.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code, 200)
            data = json.loads(resp.data)


            _links = data["_links"]
            self.assertIn("self", _links)
            self.assertIn("profile", _links)
            #self.assertIn("edit", _links)
            #self.assertIn("delete", _links)
            
    def test_get_user_mimetype(self):
        """
        Checks that GET user return correct status code and data format
        """
        print "("+self.test_get_user_mimetype.__name__+")", self.test_get_user_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_USER_PROFILE))
                          

    def test_modify_user(self):
        """
        Modify an exsiting user and check that the user has been modified correctly in the server
        """
        print "("+self.test_modify_user.__name__+")", self.test_modify_user.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.mod_user_1),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 204)
        #Check that the user has been modified
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        #Check that the title and the body of the user has been modified with the new data
        self.assertEquals(data["email"], self.mod_user_1["email"])
        

    def test_modify_unexisting_user(self):
        """
        Try to modify a user that does not exist
        """
        print "("+self.test_modify_unexisting_user.__name__+")", self.test_modify_unexisting_user.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.user_1),
                                headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 404)

    def test_modify_wrong_user(self):
        """
        Try to modify a user sending wrong data
        """
        print "("+self.test_modify_wrong_user.__name__+")", self.test_modify_wrong_user.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.user_wrong_req_1),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)
        resp = self.client.put(self.url,
                               data=json.dumps(self.user_wrong_req_2),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)

    def test_delete_user(self):
        """
        Checks that Delete user return correct status code if corrected delete
        """
        print "("+self.test_delete_user.__name__+")", self.test_delete_user.__doc__
        resp = self.client.delete(self.url)
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_user(self):
        """
        Checks that Delete user return correct status code if given a wrong user
        """
        print "("+self.test_delete_unexisting_user.__name__+")", self.test_delete_unexisting_user.__doc__
        resp = self.client.delete(self.url_wrong)
        self.assertEquals(resp.status_code, 404)


class CategoriesTestCase (ResourcesAPITestCase):

    # Valid contents
    category_1_req = {
            "title": "My category",
            "description": "category description"
    }
    
    # Valid contents
    category_2_req = {
          "title": "Another category",
          "description": "Another category description"
    }

    #Non-existing sender
    category_1_wrong = {
        "cat_details":"I want that product",
    }

    #Non exsiting receiver
    category_2_wrong = {
        "description": "Another category description wrong"
    }

    url = "/shareit/api/categories/"
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Categories)
    
    def test_get_categories(self):
        """
        Checks that GET Categories return correct status code and data format
        """
        print "("+self.test_get_categories.__name__+")", self.test_get_categories.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("categories"))
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        self.assertIn("add", _links)
        
        _category1 = data["items"][0]
        __mlinks = _category1["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_get_categories_mimetype(self):
        """
        Checks that GET Categories return correct status code and mimetype
        """
        print "("+self.test_get_categories_mimetype.__name__+")", self.test_get_categories_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("categories"))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_CATEGORY_PROFILE))
                          
    def test_add_category(self):
        """
        Test adding a category to the database.
        """
        print "("+self.test_add_category.__name__+")", self.test_add_category.__doc__
        
        # First message
        resp = self.client.post(resources.api.url_for(resources.Categories),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.category_1_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
        # First message
        resp = self.client.post(resources.api.url_for(resources.Categories),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.category_2_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
    def test_add_category_wrong_media(self):
        """
        Test adding messages with a media different than JSON
        """
        print "("+self.test_add_category_wrong_media.__name__+")", self.test_add_category_wrong_media.__doc__
        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": "text"},
                                data=self.category_1_req.__str__()
                               )
        self.assertTrue(resp.status_code == 415)
    
    def test_add_category_incorrect_format(self):
        """
        Test that add message response correctly when sending erroneous message format.
        """
        print "("+self.test_add_category_incorrect_format.__name__+")", self.test_add_category_incorrect_format.__doc__
        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.category_1_wrong)
                               )
        self.assertTrue(resp.status_code == 400)

        resp = self.client.post(resources.api.url_for(resources.Messages),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.category_2_wrong)
                               )
        self.assertTrue(resp.status_code == 400)
        
        
class CategoryTestCase (ResourcesAPITestCase):

    # Valid contents
    category_1_req = {
            "title": "My category",
            "description": "category description"
    }
    
    # Valid contents
    category_2_req = {
          "title": "Another category",
          "description": "Another category description"
    }

    # Wrong Message
    category_1_wrong_edit = {
        "data":"I want that product"
    }
    
    category_2_wrong_edit = {
        "nothing": "nothing"
    }

    def setUp(self):
        super(CategoryTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Category, categoryid="1", _external=False)
        self.url_wrong = resources.api.url_for(resources.Category, categoryid="90", _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        _url = "/shareit/api/categories/1/"
        print "("+self.test_url.__name__+")", self.test_url.__doc__
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Category)
            
    def test_wrong_url(self):
        """
        Checks that GET Category return correct status code if given a wrong data
        """
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

    def test_get_category(self):
        """
        Checks that GET Category return correct status code and data format
        """
        print "("+self.test_get_category.__name__+")", self.test_get_category.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code, 200)
            data = json.loads(resp.data)


            _links = data["_links"]
            self.assertIn("self", _links)
            self.assertIn("profile", _links)
            #self.assertIn("edit", _links)
            #self.assertIn("delete", _links)
            
    def test_get_category_mimetype(self):
        """
        Checks that GET Messages return correct status code and data format
        """
        print "("+self.test_get_category_mimetype.__name__+")", self.test_get_category_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_CATEGORY_PROFILE))
                          

    def test_modify_category(self):
        """
        Modify an exsiting category and check that the category has been modified correctly in the server
        """
        print "("+self.test_modify_category.__name__+")", self.test_modify_category.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.category_1_req),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 204)
        #Check that the category has been modified
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        #Check that the category has been modified with the new data
        self.assertEquals(data["title"], self.category_1_req["title"])
        

    def test_modify_unexisting_category(self):
        """
        Try to modify a category that does not exist
        """
        print "("+self.test_modify_unexisting_category.__name__+")", self.test_modify_unexisting_category.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.category_1_req),
                                headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 404)

    def test_modify_wrong_category(self):
        """
        Try to modify a category sending wrong data
        """
        print "("+self.test_modify_wrong_category.__name__+")", self.test_modify_wrong_category.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.category_1_wrong_edit),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)
        resp = self.client.put(self.url,
                               data=json.dumps(self.category_2_wrong_edit),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)

    def test_delete_category(self):
        """
        Checks that Delete category return correct status code if corrected delete
        """
        print "("+self.test_delete_category.__name__+")", self.test_delete_category.__doc__
        resp = self.client.delete(self.url)
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_category(self):
        """
        Checks that Delete category return correct status code if given a wrong data
        """
        print "("+self.test_delete_unexisting_category.__name__+")", self.test_delete_unexisting_category.__doc__
        resp = self.client.delete(self.url_wrong)
        self.assertEquals(resp.status_code, 404)


class PostsTestCase (ResourcesAPITestCase):

    # Valid contents
    post_1_req = {
          "details":"i wanna sell my monitor",
          "title":"selling my monitor",
          "user_id":1,
          "category_id":2
        }
    
    # Valid contents
    post_2_req = {
          "details":"i wanna sell a Car",
          "title":"selling a car",
          "user_id":1
        }


    #Non-existing sender
    post_1_wrong = {
        "details":"i wanna sell my monitor",
        "title":"sell my monitor",
        "category_id":20
    }

    #Non exsiting receiver
    post_2_wrong = {
        "details":"i wanna sell my monitor",
        "title":"sell my monitor"
    }

    url = "/shareit/api/posts/"
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Posts)
    
    def test_get_posts(self):
        """
        Checks that GET Posts return correct status code and data format
        """
        print "("+self.test_get_posts.__name__+")", self.test_get_posts.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("posts"))
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        self.assertIn("add", _links)
        
        _category1 = data["items"][0]
        __mlinks = _category1["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_get_posts_mimetype(self):
        """
        Checks that GET Posts return correct status code and mimetype
        """
        print "("+self.test_get_posts_mimetype.__name__+")", self.test_get_posts_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("posts"))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_POST_PROFILE))
                          
    def test_add_post(self):
        """
        Test adding a Post to the database.
        """
        print "("+self.test_add_post.__name__+")", self.test_add_post.__doc__
        
        # First message
        resp = self.client.post(resources.api.url_for(resources.Posts),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.post_1_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
        # First post
        resp = self.client.post(resources.api.url_for(resources.Posts),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.post_2_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
    def test_add_post_wrong_media(self):
        """
        Test adding post with a media different than JSON
        """
        print "("+self.test_add_post_wrong_media.__name__+")", self.test_add_post_wrong_media.__doc__
        resp = self.client.post(resources.api.url_for(resources.Posts),
                                headers={"Content-Type": "text"},
                                data=self.post_1_req.__str__()
                               )
        self.assertTrue(resp.status_code == 415)
    
    def test_add_post_incorrect_format(self):
        """
        Test that add post response correctly when sending erroneous message format.
        """
        print "("+self.test_add_post_incorrect_format.__name__+")", self.test_add_post_incorrect_format.__doc__
        resp = self.client.post(resources.api.url_for(resources.Posts),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.post_1_wrong)
                               )
        self.assertTrue(resp.status_code == 400)

        resp = self.client.post(resources.api.url_for(resources.Posts),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.post_2_wrong)
                               )
        self.assertTrue(resp.status_code == 400)
        
        
class PostTestCase (ResourcesAPITestCase):

    # Valid contents
    post_1_req = {
          "details":"edit: i wanna sell my monitor",
          "title":"selling my monitor",
          "user_id":1,
          "category_id":2
        }
    
    # Valid contents
    post_2_req = {
          "details":"edit: i wanna sell a Car",
          "title":"selling a car",
          "user_id":1
        }


    #Non-existing sender
    post_1_wrong = {
        "details":"i wanna sell my monitor",
        "title":"sell my monitor",
        "category_id":20
    }

    #Non exsiting receiver
    post_2_wrong = {
        "details":"i wanna sell my monitor",
        "title":"sell my monitor"
    }

    def setUp(self):
        super(PostTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Post, postid="1", _external=False)
        self.url_wrong = resources.api.url_for(resources.Post, postid="90", _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        _url = "/shareit/api/posts/1/"
        print "("+self.test_url.__name__+")", self.test_url.__doc__
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Post)
            
    def test_wrong_url(self):
        """
        Checks that GET post return correct status code if given a wrong data
        """
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

    def test_get_post(self):
        """
        Checks that GET post return correct status code and data format
        """
        print "("+self.test_get_post.__name__+")", self.test_get_post.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code, 200)
            data = json.loads(resp.data)


            _links = data["_links"]
            self.assertIn("self", _links)
            self.assertIn("profile", _links)
            #self.assertIn("edit", _links)
            #self.assertIn("delete", _links)
            
    def test_get_post_mimetype(self):
        """
        Checks that GET post return correct status code and data format
        """
        print "("+self.test_get_post_mimetype.__name__+")", self.test_get_post_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_POST_PROFILE))
                          

    def test_modify_post(self):
        """
        Modify an exsiting post and check that the post has been modified correctly in the server
        """
        print "("+self.test_modify_post.__name__+")", self.test_modify_post.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.post_1_req),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 204)
        #Check that the post has been modified
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        #Check that the post has been modified with the new data
        self.assertEquals(data["title"], self.post_1_req["title"])
        

    def test_post_unexisting_post(self):
        """
        Try to modify a post that does not exist
        """
        print "("+self.test_post_unexisting_post.__name__+")", self.test_post_unexisting_post.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.post_1_req),
                                headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 404)

    def test_post_wrong_post(self):
        """
        Try to modify a post sending wrong data
        """
        print "("+self.test_post_wrong_post.__name__+")", self.test_post_wrong_post.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.post_1_wrong),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)
        resp = self.client.put(self.url,
                               data=json.dumps(self.post_2_wrong),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)

    def test_delete_post(self):
        """
        Checks that Delete post return correct status code if corrected delete
        """
        print "("+self.test_delete_post.__name__+")", self.test_delete_post.__doc__
        resp = self.client.delete(self.url)
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_post(self):
        """
        Checks that Delete post return correct status code if given a wrong data
        """
        print "("+self.test_delete_unexisting_post.__name__+")", self.test_delete_unexisting_post.__doc__
        resp = self.client.delete(self.url_wrong)
        self.assertEquals(resp.status_code, 404)
        

class ReportsTestCase (ResourcesAPITestCase):

    # Valid contents
    report_1_req = {
          "details":"a bad post",
          "user_id":1,
          "post_id":2
        }
    
    # Valid contents
    report_2_req = {
          "details":"a bad post",
          "user_id":4,
          "post_id":3
        }


    #Non-existing sender
    report_1_wrong = {
          "details":"a bad post",
          "user_id":1
        }

    #Non exsiting receiver
    report_2_wrong = {
          "details":"a bad post"
        }

    url = "/shareit/api/reports/"
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Reports)
    
    def test_get_reports(self):
        """
        Checks that GET Reports return correct status code and data format
        """
        print "("+self.test_get_reports.__name__+")", self.test_get_reports.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("reports"))
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        self.assertIn("add", _links)
        
        _category1 = data["items"][0]
        __mlinks = _category1["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_get_reports_mimetype(self):
        """
        Checks that GET reports return correct status code and mimetype
        """
        print "("+self.test_get_reports_mimetype.__name__+")", self.test_get_reports_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("reports"))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_REPORT_PROFILE))
                          
    def test_add_report(self):
        """
        Test adding a Report to the database.
        """
        print "("+self.test_add_report.__name__+")", self.test_add_report.__doc__
        
        # First post
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.report_1_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
        # Second post
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.report_2_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
    def test_add_report_wrong_media(self):
        """
        Test adding report with a media different than JSON
        """
        print "("+self.test_add_report_wrong_media.__name__+")", self.test_add_report_wrong_media.__doc__
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": "text"},
                                data=self.report_1_req.__str__()
                               )
        self.assertTrue(resp.status_code == 415)
    
    def test_add_report_incorrect_format(self):
        """
        Test that add post response correctly when sending erroneous message format.
        """
        print "("+self.test_add_report_incorrect_format.__name__+")", self.test_add_report_incorrect_format.__doc__
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.report_1_wrong)
                               )
        self.assertTrue(resp.status_code == 400)

        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.report_2_wrong)
                               )
        self.assertTrue(resp.status_code == 400)
        
        
class ReportTestCase (ResourcesAPITestCase):

    # Valid contents
    report_1_req = {
          "details":"a bad post",
          "user_id":1,
          "post_id":2
        }
    
    # Valid contents
    report_2_req = {
          "details":"edited: a bad post",
          "user_id":1,
          "post_id":2
        }


    #Non-existing sender
    report_1_wrong = {
        "nothing":"a bad post"
        }

    #Non exsiting receiver
    report_2_wrong = {
          "nothing":"a bad post"
        }

    def setUp(self):
        super(ReportTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Report, reportid="1", _external=False)
        self.url_wrong = resources.api.url_for(resources.Report, reportid="90", _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        _url = "/shareit/api/reports/1/"
        print "("+self.test_url.__name__+")", self.test_url.__doc__
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Report)
            
    def test_wrong_url(self):
        """
        Checks that GET Report return correct status code if given a wrong data
        """
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

    def test_get_report(self):
        """
        Checks that GET Report return correct status code and data format
        """
        print "("+self.test_get_report.__name__+")", self.test_get_report.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code, 200)
            data = json.loads(resp.data)


            _links = data["_links"]
            self.assertIn("self", _links)
            self.assertIn("profile", _links)
            #self.assertIn("edit", _links)
            #self.assertIn("delete", _links)
            
    def test_get_report_mimetype(self):
        """
        Checks that GET report return correct status code and data format
        """
        print "("+self.test_get_report_mimetype.__name__+")", self.test_get_report_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_REPORT_PROFILE))
                          

    def test_modify_report(self):
        """
        Modify an exsiting report and check that the report has been modified correctly in the server
        """
        print "("+self.test_modify_report.__name__+")", self.test_modify_report.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.report_1_req),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 204)
        #Check that the report has been modified
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        #Check that the report has been modified with the new data
        self.assertEquals(data["details"], self.report_1_req["details"])
        

    def test_report_unexisting_report(self):
        """
        Try to modify a report that does not exist
        """
        print "("+self.test_report_unexisting_report.__name__+")", self.test_report_unexisting_report.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.report_1_req),
                                headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 404)

    def test_report_wrong_report(self):
        """
        Try to modify a report sending wrong data
        """
        print "("+self.test_report_wrong_report.__name__+")", self.test_report_wrong_report.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.report_1_wrong),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)
        resp = self.client.put(self.url,
                               data=json.dumps(self.report_2_wrong),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)

    def test_delete_report(self):
        """
        Checks that Delete post return correct status code if corrected delete
        """
        print "("+self.test_delete_report.__name__+")", self.test_delete_report.__doc__
        resp = self.client.delete(self.url)
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_report(self):
        """
        Checks that Delete post return correct status code if given a wrong data
        """
        print "("+self.test_delete_unexisting_report.__name__+")", self.test_delete_unexisting_report.__doc__
        resp = self.client.delete(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

class UserProfilesTestCase (ResourcesAPITestCase):

    # Valid contents
    profile_1_req = {
          "details":"a bad post",
          "user_id":1,
          "post_id":2
        }
    
    # Valid contents
    profile_2_req = {
          "details":"a bad post",
          "user_id":4,
          "post_id":3
        }


    #Non-existing sender
    profile_1_wrong = {
          "details":"a bad post",
          "user_id":1
        }

    #Non exsiting receiver
    profile_2_wrong = {
          "details":"a bad post"
        }

    url = "/shareit/api/user-profiles/"
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.UserProfiles)
    
    def test_get_user_profiles(self):
        """
        Checks that GET User profiles return correct status code and data format
        """
        print "("+self.test_get_user_profiles.__name__+")", self.test_get_user_profiles.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("user-profiles"))
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        self.assertIn("add", _links)
        
        _category1 = data["items"][0]
        __mlinks = _category1["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_get_user_profiles_mimetype(self):
        """
        Checks that GET user profiles return correct status code and mimetype
        """
        print "("+self.test_get_user_profiles_mimetype.__name__+")", self.test_get_user_profiles_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("user-profiles"))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_USER_PROFILES_PROFILE))
                          
    def test_add_user_profile(self):
        """
        Test adding a Report to the database.
        """
        print "("+self.test_add_user_profile.__name__+")", self.test_add_user_profile.__doc__
        
        # First post
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.profile_1_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
        # Second post
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.profile_1_req)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)
        
    def test_add_user_profile_wrong_media(self):
        """
        Test adding report with a media different than JSON
        """
        print "("+self.test_add_user_profile_wrong_media.__name__+")", self.test_add_user_profile_wrong_media.__doc__
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": "text"},
                                data=self.profile_1_req.__str__()
                               )
        self.assertTrue(resp.status_code == 415)
    
    def test_add_user_profile_incorrect_format(self):
        """
        Test that add post response correctly when sending erroneous message format.
        """
        print "("+self.test_add_user_profile_incorrect_format.__name__+")", self.test_add_user_profile_incorrect_format.__doc__
        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.profile_1_wrong)
                               )
        self.assertTrue(resp.status_code == 400)

        resp = self.client.post(resources.api.url_for(resources.Reports),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.profile_2_wrong)
                               )
        self.assertTrue(resp.status_code == 400)
        
        
class UserProfileTestCase (ResourcesAPITestCase):

    # Valid contents
    profile_1_req = {
            "fullname": "Forhadul Islam",
            "phone": "",
            "website": "",
            "address": "Yliopistokatu",
            "skype": "sadi.987",
            "gender": "M"
        }
    
    # Valid contents
    profile_2_req = {
            "fullname": "Khaled",
            "address": "Yliopistokatu",
            "skype": "sadi.987",
            "gender": "M"
        }


    #Non-existing sender
    profile_1_wrong = {
            "fullname": "Forhadul Islam",
            "address": "Yliopistokatu",
            "gender": "JK"
        }

    #Non exsiting receiver
    profile_2_wrong = {
            "fullname": "Forhadul Islam",
            "address": "Yliopistokatu",
            "gender": "P"
        }

    def setUp(self):
        super(UserProfileTestCase, self).setUp()
        self.url = resources.api.url_for(resources.UserProfile, userid="1", _external=False)
        self.url_wrong = resources.api.url_for(resources.UserProfile, userid="90", _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        _url = "/shareit/api/user-profiles/1/"
        print "("+self.test_url.__name__+")", self.test_url.__doc__
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.UserProfile)
            
    def test_wrong_url(self):
        """
        Checks that GET UserProfile return correct status code if given a wrong data
        """
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

    def test_get_user_profile(self):
        """
        Checks that GET Report return correct status code and data format
        """
        print "("+self.test_get_user_profile.__name__+")", self.test_get_user_profile.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code, 200)
            data = json.loads(resp.data)


            _links = data["_links"]
            self.assertIn("self", _links)
            self.assertIn("profile", _links)
            #self.assertIn("edit", _links)
            #self.assertIn("delete", _links)
            
    def test_get_user_profile_mimetype(self):
        """
        Checks that GET report return correct status code and data format
        """
        print "("+self.test_get_user_profile_mimetype.__name__+")", self.test_get_user_profile_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_USER_PROFILES_PROFILE))
                          

    def test_modify_user_profile(self):
        """
        Modify an exsiting report and check that the report has been modified correctly in the server
        """
        print "("+self.test_modify_user_profile.__name__+")", self.test_modify_user_profile.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.profile_1_req),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 204)
        #Check that the report has been modified
        resp2 = self.client.get(self.url)
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        #Check that the report has been modified with the new data
        self.assertEquals(data["fullname"], self.profile_1_req["fullname"])
        self.assertEquals(data["address"], self.profile_1_req["address"])
        self.assertEquals(data["gender"], self.profile_1_req["gender"])
        

    def test_report_unexisting_user_profile(self):
        """
        Try to modify a report that does not exist
        """
        print "("+self.test_report_unexisting_user_profile.__name__+")", self.test_report_unexisting_user_profile.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.profile_1_req),
                                headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 404)

    def test_report_wrong_user_profile(self):
        """
        Try to modify a report sending wrong data
        """
        print "("+self.test_report_wrong_user_profile.__name__+")", self.test_report_wrong_user_profile.__doc__
        resp = self.client.put(self.url,
                               data=json.dumps(self.profile_1_wrong),
                               headers={"Content-Type": JSON})
        self.assertEquals(resp.status_code, 400)

class SearchTestCase (ResourcesAPITestCase):

    # Valid contents
    keyword_1_right = "sale"

    #Non-existing sender
    keyword_1_wrong = "nowheretobefound"


    url = "/shareit/api/search/posts/"
    url_right_key = url + "?q=" + keyword_1_right
    url_wrong_key = url + "?q=" + keyword_1_wrong
    
    
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        
        print "("+self.test_url.__name__+")", self.test_url.__doc__,
        with resources.app.test_request_context(self.url_right_key):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Search)
    
    def test_search(self):
        """
        Checks that Searching by keywords return correct status code and data format
        """
        print "("+self.test_search.__name__+")", self.test_search.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url_right_key)
        self.assertEquals(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data)
        
        #Check links
        _links = data["_links"]
        self.assertIn("self", _links)
        
        _post = data["items"][0]
        __mlinks = _post["_links"]
        self.assertIn("profile", __mlinks)
        self.assertIn("self", __mlinks)
        
    def test_search_mimetype(self):
        """
        Checks that GET user profiles return correct status code and mimetype
        """
        print "("+self.test_search_mimetype.__name__+")", self.test_search_mimetype.__doc__

        #Check that I receive status code 200
        resp = self.client.get(self.url_right_key)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.headers.get("Content-Type",None),
                          "{};{}".format(HAL, SHAREIT_SEARCH_PROFILE))
                          
    
    
    def test_search_incorrect_keyword(self):
        """
        Test that add post response correctly when sending erroneous message format.
        """
        print "("+self.test_search_incorrect_keyword.__name__+")", self.test_search_incorrect_keyword.__doc__
        resp = self.client.get(self.url_wrong_key,
                                headers={"Content-Type": JSON},
                                data=(self.keyword_1_wrong)
                               )
        self.assertTrue(resp.status_code == 404)

        
        
if __name__ == "__main__":
    print "Start running tests"
    unittest.main()