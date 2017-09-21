'''
    Code structure followed from Exercises
'''

import unittest, sqlite3
from app import db

#Path to the database file, different from the deployment db
DB_PATH = 'db/shateit_test.db'
ENGINE = db.Engine(DB_PATH)

INITIAL_SIZE = 5

MESSAGE1_ID = 1
MESSAGE2_ID = 4
INVALID_MESSAGE_ID = 10

MESSAGE_INSERT = {'send_time': 1488413298, 'receiver': 3, 'message_details': 'Hi there .. I am interested in this product', 'sender': 2}
MESSAGE_INSERT_ID = 6

MESSAGE_INSERT_INVALID_SENDER = {'send_time': 1488413298, 'receiver': 3, 'message_details': 'Hi there .. I am interested in this product', 'sender': 40}
MESSAGE_INSERT_INVALID_RECEIVER = {'send_time': 1488413298, 'receiver': 40, 'message_details': 'Hi there .. I am interested in this product', 'sender': 2}

MESSAGE1 = {'message_id': 1,'send_time': 1488413278, 'receiver': 1, 'message_details': 'Hi sadi .. I am interested in this product', 'sender': 2}
MESSAGE2 = {'message_id': 4,'send_time': 1488413278, 'receiver': 3, 'message_details': 'will contact you soon', 'sender': 1}


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

USER = {'primary_profile': {'username': 'sadi', 'reg_date': 1488404307, 'user_id': '1', 'email': 'sadi@gmail.com'}, 'profile_details': {'website': 'http://99reviews.com', 'gender': 'M', 'address': 'Yliopistokatu 24 C', 'phone': '0469555307', 'skype': 'shifat2sadi', 'fullname': 'Sadi Aliss'}}
    
user_1 = {        
        "username":"nahidan",
        "email":"nahidan@gmail.com"
    }
    
user_2 = {        
    "username":"anotheruser",
    "email":"anotheruser@gmail.com"
}


USER_ID2 = 2
User_Profile2 = {'website': 'http://egyptian.com', 'user_id': 2, 'gender': 'M', 'address': 'Yliopistokatu 38', 'phone': '048998980', 'skype': 'khaled.mohamed', 'fullname': 'Mohamed Khaled '}

USERNAME = 'sadi'
USER_ID = 1
INVALID_USERNAME = 'johndoe'

CATEGORY_ID = 2
CATEGORY = {'add_date': 1488404307, 'last_update': 1488404307, 'category_id': 2, 'description': 'Books and study materials', 'title': 'Book'}

INVALID_CATEGORY = 10

POST_ID = 1
POST = {'post_id': 1,'user_id': 1, 'tags': 'chair, sale', 'add_date': 1488413278, 'title': 'New chair for sale', 'last_update': 1488413278, 'details': 'I want to sell my chair', 'category_id': 2}
POST_INVALID_ID = 20

POST_WITH_INVALID_USER = {'user_id': 20, 'tags': 'chair, sale', 'add_date': 1488413278, 'title': 'New chair for sale', 'last_update': 1488413278, 'details': 'I want to sell my chair', 'category_id': 2}

POST_WITH_INVALID_CATEGORY = {'user_id': 1, 'tags': 'chair, sale', 'add_date': 1488413278, 'title': 'New chair for sale', 'last_update': 1488413278, 'details': 'I want to sell my chair', 'category_id': 99}

POST_INSERT = {'user_id': 2, 'tags': 'tv, electronics', 'add_date': 1488413278, 'title': 'A TV for sale', 'last_update': 1488413278, 'details': 'I want to sell my TV. Almost new', 'category_id': 2}
POST_INSERT_ID = 6

POST_UPDATE_ID = 3
POST_UPDATE = {'user_id': 2, 'tags': 'tv, electronics', 'add_date': 1488413278, 'title': 'TV for sale', 'last_update': 1488413278, 'details': 'I want to sell my TV. Almost new', 'category_id': 3}

GET_REPORT_ID = 2
GET_REPORT = {'post_id': 1, 'user_id': 1, 'details': 'Bad post', 'report_id': 2}

REPORT_ID = 1
EDIT_REPORT = { 'details': 'Bad post' }

INVALID_REPORT_ID = 60

DELETE_REPORT_ID = 3
DELETE_INVALID_REPORT_ID = 30


NEW_USER = {
            'username': 'mario',
            'email': 'mario@gmail.com',
            'reg_date': 1488404307
           }                               
NEW_USER_ID = 6
MODIFY_USER_EMAIL = 'anotheremail@gmail.com'

NEW_USER_DUP_USERNAME = {
            'username': 'khaled',
            'email': 'mario@gmail.com',
            'reg_date': 1488404307
           }
           
NEW_USER_DUP_EMAIL = {
            'username': 'mario',
            'email': 'asare@gmail.com',
            'reg_date': 1488404307
           }
INVALID_USER_ID = 50
EDIT_USER_PROFILE = {
                     'firstname': 'John Doe', 
                     'phone': 'sully@rda.com',                     
                     'website': 'http: //www.pandora.com/',
                     'address': 'USA', 
                     'gender': 'Male',
                     'skype': 'mario.1925',
                     'mobile': "83232323",
                     'age': 24,
                     'skype': 'jakesully'
                   }
            
USER_WRONG_USERNAME= 'johndoe'

'''
    Some codes are copied from PWP Exercise 3, 4
'''

class DBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
        
    def test_table_created(self):
        '''
        Checks that if the tables initially contains 5 rows for each of them
        '''
        print '('+self.test_table_created.__name__+')', \
              self.test_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM users'
        query2 = 'SELECT * FROM users_profile'
        query3 = 'SELECT * FROM messages'
        query4 = 'SELECT * FROM categories'
        query5 = 'SELECT * FROM posts'
        query6 = 'SELECT * FROM reports'
        #Connects to the database.
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query1)
            users = cur.fetchall()
            #Assert
            self.assertEquals(len(users), INITIAL_SIZE)
            
            #Check the users_profile:
            cur.execute(query2)
            users_profile = cur.fetchall()
            #Assert
            self.assertEquals(len(users_profile), INITIAL_SIZE)
            
            #Check the messages:
            cur.execute(query3)
            messages = cur.fetchall()
            #Assert
            self.assertEquals(len(messages), INITIAL_SIZE)
            
            #Check the categories:
            cur.execute(query4)
            categories = cur.fetchall()
            #Assert
            self.assertEquals(len(categories), INITIAL_SIZE)
            
            #Check the posts:
            cur.execute(query5)
            posts = cur.fetchall()
            #Assert
            self.assertEquals(len(posts), INITIAL_SIZE)
            
            #Check the reports:
            cur.execute(query6)
            reports = cur.fetchall()
            #Assert
            self.assertEquals(len(reports), INITIAL_SIZE)

# Message API Testing Starts
class MessageAPITestCase(unittest.TestCase):
    
    

    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
    '''
        Test functions
    '''
    def test_create_message(self):
        '''
        Test delete_message with id 3 
        '''
        print '('+self.test_create_message.__name__+')', \
              self.test_create_message.__doc__
        #Test with an existing message
        message = self.connection.create_message(MESSAGE_INSERT)
        self.assertEquals(message, MESSAGE_INSERT_ID)
       
    def test_create_message_with_invalid_sender(self):
        '''
        Test delete_message with an invalid sender id 40
        '''
        print '('+self.test_create_message_with_invalid_sender.__name__+')', \
              self.test_create_message_with_invalid_sender.__doc__
        #Test with an existing message
        message = self.connection.create_message(MESSAGE_INSERT_INVALID_SENDER)
        self.assertIsNone(message)

    def test_create_message_with_invalid_receiver(self):
        '''
        Test delete_message with an invalid receiver id 40
        '''
        print '('+self.test_create_message_with_invalid_receiver.__name__+')', \
              self.test_create_message_with_invalid_receiver.__doc__
        #Test with an existing message
        message = self.connection.create_message(MESSAGE_INSERT_INVALID_RECEIVER)
        self.assertIsNone(message)
            
    def test_get_message(self):
        '''
        Test get_message with id 1 and 4
        '''
        print '('+self.test_get_message.__name__+')', \
              self.test_get_message.__doc__
        #Test with an existing message
        message = self.connection.get_message(MESSAGE1_ID)
        self.assertDictContainsSubset(message, MESSAGE1)
        message = self.connection.get_message(MESSAGE2_ID)
        self.assertDictContainsSubset(message, MESSAGE2)

    def test_get_message_with_invalidid(self):
        '''
        Test get_message with id 10 which is not a valid id because it does not exist
        '''
        print '('+self.test_get_message_with_invalidid.__name__+')', \
              self.test_get_message_with_invalidid.__doc__
        #Test with an existing message
        message = self.connection.get_message(INVALID_MESSAGE_ID)
        self.assertIsNone(message)
    
        
    def test_modify_message(self):
        '''
        Test edit_message with an valid message id
        '''
        print '('+self.test_modify_message.__name__+')', \
              self.test_modify_message.__doc__
        #Test with an existing message
        message = self.connection.modify_message(MESSAGE1_ID, message_1_edit["message_details"])
        self.assertIs(message, MESSAGE1_ID)
    
    def test_delete_message(self):
        '''
        Test delete_message with id 3 
        '''
        print '('+self.test_delete_message.__name__+')', \
              self.test_delete_message.__doc__
        #Test with an existing message
        message = self.connection.delete_message(MESSAGE2_ID)
        self.assertTrue(message)
        
    def test_delete_message_with_invalidid(self):
        '''
        Test delete_message with id 30 which is not a valid id because it does not exist
        '''
        print '('+self.test_delete_message_with_invalidid.__name__+')', \
              self.test_delete_message_with_invalidid.__doc__
        #Test with an existing message
        message = self.connection.delete_message(INVALID_MESSAGE_ID)
        self.assertIs(message, False)
    
# Message API Testing Ends
    
    
# Users API Testing Starts
class UsersAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
        
    '''
        Test functions
    '''
    
    def test_get_user(self):
        '''
        Test get_user with username `sadi` 
        '''
        print '('+self.test_get_user.__name__+')', \
              self.test_get_user.__doc__
        #Test with an existing message
        user = self.connection.get_user(USERNAME)
        #print(user)
        self.assertEquals(user, USER) 

    def test_create_user(self):
        '''
        Test create_user with NEW_USER parameters
        '''
        print '('+self.test_create_user.__name__+')', \
              self.test_create_user.__doc__
        #Test with creating user
        user = self.connection.create_user(NEW_USER)
        self.assertEquals(user, NEW_USER_ID)
        
    def test_create_user_with_duplicate_username(self):
        '''
        Test create_user with NEW_USER_DUP_USERNAME parameters where the username already exists in the database
        '''
        print '('+self.test_create_user_with_duplicate_username.__name__+')', \
              self.test_create_user_with_duplicate_username.__doc__
        #Test with creating user
        user = self.connection.create_user(NEW_USER_DUP_USERNAME)
        self.assertIsNone(user)
        
    def test_create_user_with_duplicate_email(self):
        '''
        Test create_user with NEW_USER_DUP_EMAIL parameters where the email already exists in the database
        '''
        print '('+self.test_create_user_with_duplicate_email.__name__+')', \
              self.test_create_user_with_duplicate_email.__doc__
        #Test with creating user 
        user = self.connection.create_user(NEW_USER_DUP_EMAIL)
        self.assertIsNone(user)        
    
    def test_get_user_id(self):
        '''
        Test get_user_id with username `sadi` 
        '''
        print '('+self.test_get_user_id.__name__+')', \
              self.test_get_user_id.__doc__
        #Test with an existing message
        user = self.connection.get_user_id(USERNAME)
        self.assertEquals(user, USER_ID)
        
    def test_get_user_id_with_invalid_username(self):
        '''
        Test get_user_id with username `johndoe` 
        '''
        print '('+self.test_get_user_id_with_invalid_username.__name__+')', \
              self.test_get_user_id_with_invalid_username.__doc__
        #Test with an existing message
        user = self.connection.get_user_id(INVALID_USERNAME)
        self.assertIsNone(user)
        
    def test_modify_user(self):
        '''
        Test modify_user with an valid user id
        '''
        print '('+self.test_modify_user.__name__+')', \
              self.test_modify_user.__doc__
        #Test with an existing user
        user = self.connection.modify_user(USER_ID, user_1["email"])
        self.assertIs(user, USER_ID)
        
    def test_delete_user(self):
        '''
        Test delete_user with username `sadi` 
        '''
        print '('+self.test_delete_user.__name__+')', \
              self.test_delete_user.__doc__
        #Test with an existing message
        user = self.connection.delete_user(USERNAME)
        self.assertTrue(user)
        
    def test_delete_user_with_invalid_username(self):
        '''
        Test delete_user with username `johndoe` 
        '''
        print '('+self.test_delete_user_with_invalid_username.__name__+')', \
              self.test_delete_user_with_invalid_username.__doc__
        #Test with an existing message
        user = self.connection.delete_user(INVALID_USERNAME)
        self.assertIs(user, False)
    
# Users API Testing Ends
    
    
    
# Users_Profile API Testing Starts
class UserProfileAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
    '''
        Test functions
    '''
    def test_get_user_profile(self):
        '''
        Test get_user_profile with id 2 
        '''
        print '('+self.test_get_user_profile.__name__+')', \
              self.test_get_user_profile.__doc__
        #Test with an existing message
        user_profile = self.connection.get_user_profile(USER_ID2)
        self.assertEquals(user_profile, User_Profile2)
        
    def test_get_user_profile_with_invalidid(self):
        '''
        Test get_user_profile with INVALID_USER_ID
        '''
        print '('+self.test_get_user_profile_with_invalidid.__name__+')', \
              self.test_get_user_profile_with_invalidid.__doc__
        #Test with an existing message
        user_profile = self.connection.get_user_profile(INVALID_USER_ID)
        self.assertIsNone(user_profile)
        
    def test_edit_user_profile(self):
        '''
        Test get_user_profile with USER_ID2
        '''
        print '('+self.test_edit_user_profile.__name__+')', \
              self.test_edit_user_profile.__doc__
        #Test with an existing message
        user_profile = self.connection.edit_user_profile(USER_ID2, EDIT_USER_PROFILE)
        self.assertEquals(user_profile, USER_ID2)

    def test_edit_user_profile_with_invalidid(self):
        '''
        Test get_user_profile with INVALID_USER_ID
        '''
        print '('+self.test_edit_user_profile_with_invalidid.__name__+')', \
              self.test_edit_user_profile_with_invalidid.__doc__
        #Test with an existing message
        user_profile = self.connection.edit_user_profile(INVALID_USER_ID, EDIT_USER_PROFILE)
        self.assertIsNone(user_profile)
        
        
# Users_Profile API Testing Ends
    
    
# Categories API Testing Starts
class CategoriesAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
    '''
        Test functions
    '''
    def test_get_category(self):
        '''
        Test get_category with id 2 
        '''
        print '('+self.test_get_category.__name__+')', \
              self.test_get_category.__doc__
        #Test with an existing message
        category = self.connection.get_category(CATEGORY_ID)
        self.assertEquals(category, CATEGORY)
        
    def test_get_category_with_invalidid(self):
        '''
        Test get_category with invalid id 20
        '''
        print '('+self.test_get_category_with_invalidid.__name__+')', \
              self.test_get_category_with_invalidid.__doc__
        #Test with an existing message
        category = self.connection.get_category(INVALID_CATEGORY)
        self.assertIsNone(category)
    

    def test_edit_category(self):
        '''
        Test edit_category with valid category id
        '''
        print '('+self.test_edit_category.__name__+')', \
              self.test_edit_category.__doc__
        #Test with an existing category
        category = self.connection.edit_category(CATEGORY_ID, CATEGORY["title"], CATEGORY["description"])
        self.assertEquals(category, CATEGORY_ID)
    
    def test_delete_category(self):
        '''
        Test delete_category with id 2 
        '''
        print '('+self.test_delete_category.__name__+')', \
              self.test_delete_category.__doc__
        #Test with an existing message
        category = self.connection.delete_category(CATEGORY_ID)
        self.assertTrue(category)
        
    def test_delete_category_with_invalidid(self):
        '''
        Test delete_category with invalid id 20
        '''
        print '('+self.test_delete_category_with_invalidid.__name__+')', \
              self.test_delete_category_with_invalidid.__doc__
        #Test with an existing message
        category = self.connection.delete_category(INVALID_CATEGORY)
        self.assertIs(category, False)
    
# Categories API Testing Ends    
    
    
# Posts API Testing Starts
    
class PostAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
    '''
        Test functions
    '''
    def test_get_post(self):        
        '''
        Test get_post with id 1
        '''
        print '('+self.test_get_post.__name__+')', \
              self.test_get_post.__doc__
        #Test with an existing message
        post = self.connection.get_post(POST_ID)
        self.assertEquals(post, POST)
        
    def test_create_post(self):        
        '''
        Test create_post with POST_INSERT parameters 
        '''
        print '('+self.test_create_post.__name__+')', \
              self.test_create_post.__doc__
        #Test with an existing message
        post = self.connection.create_post(POST_INSERT)
        self.assertEquals(post, POST_INSERT_ID)
        
    def test_create_post_with_invalid_userid(self):        
        '''
        Test create_post with POST_WITH_INVALID_USER parameters 
        '''
        print '('+self.test_create_post_with_invalid_userid.__name__+')', \
              self.test_create_post_with_invalid_userid.__doc__
        #Test with an invalid user_id
        post = self.connection.create_post(POST_WITH_INVALID_USER)
        self.assertIsNone(post)
        
    def test_create_post_with_invalid_category(self):        
        '''
        Test create_post with POST_WITH_INVALID_CATEGORY parameters 
        '''
        print '('+self.test_create_post_with_invalid_category.__name__+')', \
              self.test_create_post_with_invalid_category.__doc__
        #Test with an invalid category
        post = self.connection.create_post(POST_WITH_INVALID_CATEGORY)
        self.assertIsNone(post)
        
    def test_edit_post(self):        
        '''
        Test edit_post with POST_UPDATE AND POST_UPDATE_ID parameters 
        '''
        print '('+self.test_edit_post.__name__+')', \
              self.test_edit_post.__doc__
        #Test with an existing message
        post = self.connection.edit_post(POST_UPDATE_ID,POST_INSERT)
        self.assertEquals(post, POST_UPDATE_ID)
        
    def test_edit_post_with_invalidid(self):        
        '''
        Test edit_post with POST_UPDATE AND POST_INVALID_ID parameters 
        '''
        print '('+self.test_edit_post_with_invalidid.__name__+')', \
              self.test_edit_post_with_invalidid.__doc__
        #Test with an existing message
        post = self.connection.edit_post(POST_INVALID_ID,POST_INSERT)
        self.assertIsNone(post)
    
    def test_delete_post(self):
        '''
        Test delete_post with id 1
        '''
        print '('+self.test_delete_post.__name__+')', \
              self.test_delete_post.__doc__
        #Test with an existing message
        post = self.connection.delete_post(POST_ID)
        self.assertTrue(post)
        
    def test_delete_post_with_invalidid(self):
        '''
        Test delete_post with invalid id 20
        '''
        print '('+self.test_delete_post_with_invalidid.__name__+')', \
              self.test_delete_post_with_invalidid.__doc__
        #Test with an existing message
        post = self.connection.delete_post(POST_INVALID_ID)
        self.assertIs(post, False)
    
# Posts API Testing Ends
    
    
# Reports API Testing Starts
class ReportAPITestCase(unittest.TestCase):
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print "Testing ", cls.__name__
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print "Testing ENDED for ", cls.__name__
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()
    '''
        Test functions
    '''
    def test_get_report(self):
        '''
        Test get_report with id GET_REPORT_ID which is 2
        '''
        print '('+self.test_get_report.__name__+')', \
              self.test_get_report.__doc__
        
        report = self.connection.get_report(GET_REPORT_ID)
        self.assertEquals(report, GET_REPORT)
        
    def test_get_report_with_invalidid(self):
        '''
        Test get_report with id INVALID_REPORT_ID which is 60
        '''
        print '('+self.test_get_report_with_invalidid.__name__+')', \
              self.test_get_report_with_invalidid.__doc__
        
        report = self.connection.get_report(INVALID_REPORT_ID)
        self.assertIsNone(report)
        
        
    def test_edit_report(self):
        '''
        Test edit_report with an valid report id
        '''
        print '('+self.test_edit_report.__name__+')', \
              self.test_edit_report.__doc__
        #Test with an existing report
        report = self.connection.edit_report(REPORT_ID, EDIT_REPORT["details"])
        self.assertIs(report, REPORT_ID)
        
    def test_delete_report(self):
        '''
        Test delete_report with id DELETE_REPORT_ID which is 3
        '''
        print '('+self.test_delete_report.__name__+')', \
              self.test_delete_report.__doc__
        
        report = self.connection.delete_report(DELETE_REPORT_ID)
        self.assertTrue(report)
        
    def test_delete_report_with_invalidid(self):
        '''
        Test delete_report with id DELETE_INVALID_REPORT_ID which is 30
        '''
        print '('+self.test_delete_report_with_invalidid.__name__+')', \
              self.test_delete_report_with_invalidid.__doc__
        
        report = self.connection.delete_report(DELETE_INVALID_REPORT_ID)
        self.assertIs(report, False)
        
# Reports API Testing Ends
   
if __name__ == '__main__':
    print 'Start running user tests'
    unittest.main()
