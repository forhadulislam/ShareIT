'''
    Some of the parts of the code were takes from Exercise codes of PWP 2017
'''

from datetime import datetime
import time, sqlite3, re, os
#Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/shareit.db'
DEFAULT_SCHEMA = "db/shareit_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/shareit_data_dump.sql"

'''
    Some codes are copied from PWP Exercises
'''
class Engine(object):

    def __init__(self, db_path=None):
        '''
        '''

        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH

    def connect(self):
        '''
        Creates a connection to the database.
        :return: A Connection instance

        '''
        return Connection(self.db_path)

    def remove_database(self):
        '''
        Removes the database file from the filesystem.

        '''
        if os.path.exists(self.db_path):
            #THIS REMOVES THE DATABASE STRUCTURE
            os.remove(self.db_path)

    def clear(self):
        '''
        Purge the database removing all records from the tables. It only keeps the database schema
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        #THIS KEEPS THE SCHEMA AND REMOVE VALUES
        con = sqlite3.connect(self.db_path)
        #Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM messages")
            cur.execute("DELETE FROM reports")
            cur.execute("DELETE FROM posts")
            cur.execute("DELETE FROM categories")
            cur.execute("DELETE FROM users_profile")
            cur.execute("DELETE FROM users")
            #NOTE since we have ON DELETE CASCADE BOTH IN users_profile AND
            #friends, WE DO NOT HAVE TO WORRY TO CLEAR THOSE TABLES.

    #METHODS TO CREATE AND POPULATE A DATABASE USING DIFFERENT SCRIPTS
    def create_tables(self, schema=None):
        '''
        Create programmatically the tables from a schema file.

        :param schema: path to the .sql schema file. If this parmeter is
            None, then *db/shareit_schema_dump.sql* is utilized.

        '''
        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = DEFAULT_SCHEMA
        try:
            with open(schema) as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def populate_tables(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.

        :param dump:  path to the .sql dump file. If this parmeter is
            None, then *db/shareit_data_dump.sql* is utilized.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        #Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        #Populate database from dump
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        with open (dump) as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)

    #METHODS TO CREATE THE TABLES PROGRAMMATICALLY WITHOUT USING SQL SCRIPT
    def create_messages_table(self):
        '''
        Create the table ``messages`` programmatically
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE messages(message_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    message_details TEXT, \
                    sender INTEGER, receiver INTEGER, \
                    send_time INTEGER, \
                    FOREIGN KEY(sender) REFERENCES users(user_id) ON DELETE CASCADE, \
                    FOREIGN KEY(receiver) REFERENCES users(user_id) ON DELETE CASCADE)'
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
                return False
        return True

    def create_categories_table(self):
        '''
        Create the table ``categories`` programmatically
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE categories(category_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                                    title TEXT UNIQUE, description TEXT,\
                                    add_date INTEGER, last_update INTEGER,\
                                    UNIQUE(title))'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
                return False
        return True

    def create_users_profile_table(self):
        '''
        Create the table ``users_profile`` programmatically,
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE users_profile(user_id INTEGER PRIMARY KEY, \
                    fullname TEXT, \
                    phone TEXT, website TEXT, \
                    address TEXT, \
                    skype TEXT, gender TEXT, \
                    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE)'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
                return False
        return True

    def create_users_table(self):
        '''
        Create the table ``users`` programmatically
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                     username TEXT UNIQUE, email TEXT UNIQUE, \
                     reg_date INTEGER, \
                     UNIQUE(username, email))'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None
        
    def create_reports_table(self):
        '''
        Create the table ``reports`` programmatically
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE reports ( report_id INTEGER PRIMARY KEY, \
                     post_id INTEGER, user_id INTEGER, \
                     details TEXT, \
                     FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE, \
                     FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE)'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None
            
    def create_posts_table(self):
        '''
        Create the table ``posts`` programmatically
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE posts (post_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, \
                     title TEXT, details TEXT, \
                     category_id INTEGER, tags TEXT, \
                     add_date INTEGER, last_update INTEGER, \
                     FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE, \
                     FOREIGN KEY(category_id) REFERENCES categories(category_id) ON DELETE CASCADE)'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None       

'''
    Some codes are copied from PWP Exercise 3, 4
'''
class Connection(object):
    '''
        API to access the Share IT database.
    '''
    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)

    def close(self):
        '''
        Closes the database connection, commiting all changes.

        '''
        if self.con:
            self.con.commit()
            self.con.close()

    #FOREIGN KEY STATUS
    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated.

        :return: ``True`` if  foreign_keys is activated and ``False`` otherwise.
        :raises sqlite3.Error: when a sqlite3 error happen. In this case the
            connection is closed.

        '''
        try:
            #Create a cursor to receive the database values
            cur = self.con.cursor()
            #Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            #We know we retrieve just one record: use fetchone()
            data = cur.fetchone()
            is_activated = data == (1,)
            print "Foreign Keys status: %s" % 'ON' if is_activated else 'OFF'
        except sqlite3.Error, excp:
            print "Error %s:" % excp.args[0]
            self.close()
            raise excp
        return is_activated

    def set_foreign_keys_support(self):
        '''
        Activate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        try:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            #execute the pragma command, ON
            cur.execute(keys_on)
            return True
        except sqlite3.Error, excp:
            print "Error %s:" % excp.args[0]
            return False

    def unset_foreign_keys_support(self):
        '''
        Deactivate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = OFF'
        try:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            #execute the pragma command, OFF
            cur.execute(keys_on)
            return True
        except sqlite3.Error, excp:
            print "Error %s:" % excp.args[0]
            return False
    
    #Messages API Starts
    def _format_message(self,message):
        '''
            :return: a formatted key value pairs of message object
        '''
        return{
            'message_details': str(message['message_details']),
            'sender': message['sender'],
            'receiver': message['receiver'],
            'send_time': message['send_time'],
            'message_id': message['message_id']
        }
    
    def get_messages(self):
        '''
            :return: Return a list of all the messages in the database
        '''
        #Create the SQL Statement for retrieving posts
        query = 'SELECT * FROM messages'  
        self.set_foreign_keys_support()        
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return post object
        messages = []
        for row in rows:
            message = self._format_message(row)
            messages.append(message)
        return messages
    
    def get_message(self, messageid):
        '''
        Extracts a message from the database.

        :param messageid: The id of the message. 
        :return: A dictionary of message

        '''
        #Extracts the int which is the id for a message in the database
        
        messageid = int(messageid)        
        self.set_foreign_keys_support()        
        query = 'SELECT * FROM messages WHERE message_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        pvalue = (messageid,)
        cur.execute(query, pvalue)
        
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._format_message(row)

    def get_messages_sent(self, user_id):
        '''
        Return a list of all the messages sent by the user in the database filtered by user_id

        :param user_id: search messages of a user with the given user_id. 

        :return: A list of messages. Each message is a dictionary containing the following keys:

            * ``message_id``: Id of the message.
            * ``sender``: nickname of the message's author.
            * ``receiver``: string containing the title of the message.
            * ``send_time``: UNIX timestamp (long int) that specifies when the message was sent.

        '''
        #Create the SQL Statement for searching messages by user_id
        query = "SELECT * FROM messages WHERE sender = '%s' ORDER BY send_time DESC"  % user_id
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        messages = []
        for row in rows:
            message = self._format_message(row)
            messages.append(message)
        return messages

    def delete_message(self, messageid):
        '''
            Delete the message with id given as parameter.

            :param str messageid: id of the message to remove
            
            :return: True if the message has been deleted, False otherwise
            :return: None: if the messageid is not valid

        '''
        
        messageid = int(messageid)        
        if not messageid:
            return False
            
        #Create the SQL statment
        stmnt = 'DELETE FROM messages WHERE message_id = ?'
        
        self.set_foreign_keys_support()        
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (messageid,)
        cur.execute(stmnt, pvalue)
        #Commit the message
        self.con.commit()
        #Check that the message has been deleted
        if cur.rowcount < 1:
            return False
        #Return true if message is deleted.
        return True

    def modify_message(self, messageid, message_details):
        '''
        Modify the ``message_details`` of the message with id ``messageid``

        :param str messageid: The id of the message to remove
        :param str message_details: the message's content
        
        :return: the id of the edited message or None if the message was not found or messageid is invalid

        '''
        
        messageid = int(messageid)
        if not messageid:
            return None     
            
        # Checking if the message exists 
        queryGetMessage = "SELECT * FROM messages WHERE message_id = '%s'"  % messageid
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(queryGetMessage)
        #Get results
        messageRow = cur.fetchall()
        if messageRow is None:
            return None
            
        #Create the SQL statment
        stmnt = 'UPDATE messages SET message_details=? WHERE message_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (message_details, messageid,)
        cur.execute(stmnt, pvalue)
        self.con.commit()
        if cur.rowcount < 1:
            return None
        return messageid

    def create_message(self, message):
        '''
        Create a new message with the data provided as arguments.

        :param str message: Is an object which containes several parameters  
            str message["message_details"]: The message's content or details
            str message["sender"]: the id of the person who is sending this message
            str message["receiver"]: the id of the person who will receive this message

        :return: the id of the created message or None if the message could not be created

        '''
        message_details = message.get('message_details', None)
        sender = message.get('sender', None)
        receiver = message.get('receiver', None)
        send_time = message.get('send_time', None)
        
        if not message_details or not sender or not receiver:
            return None
        
        sender = int(sender)        
        receiver = int(receiver)
        
        if not send_time:
            send_time = time.mktime(datetime.now().timetuple())
        
        #Create the SQL statment
        #SQL to test that the message which I am answering does exist
        findSender = self.check_user_by_id(sender)
          #SQL Statement for getting the user id given a nickname
        findReceiver = self.check_user_by_id(receiver)
        
        if not findSender or not findReceiver:
            return None
        
        #SQL Statement for inserting the data
        stmnt = 'INSERT INTO messages (message_details, sender, receiver, send_time) VALUES(?,?,?,?)'
        
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()        
        
        pvalue = (message_details, sender, receiver, send_time)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        messageid = cur.lastrowid
        #Return the id of message
        return messageid
    
    # Messages API Ends
    
    # Posts API Starts
    
    def _format_post(self, post):
        '''
            :return: a formatted key value pairs of post object
        '''
        return {
                   'post_id': post['post_id'],
                   'user_id': post['user_id'],
                   'title': str(post['title']),
                   'details': str(post['details']),
                   'category_id': post['category_id'],
                   'tags': str(post['tags']),
                   'add_date': post['add_date'],
                   'last_update': post['last_update']                                       
                }
    
    def get_posts(self):
        '''
            :return: Return a list of all the posts in the database and ordered by add_date
        '''
        #Create the SQL Statement for retrieving posts
        query = "SELECT * FROM posts ORDER BY add_date DESC"        
        self.set_foreign_keys_support()        
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return post object
        posts = []
        for row in rows:
            post = self._format_post(row)
            posts.append(post)
        return posts
        
    def search_posts(self, keyword):
        '''
            :return: Return a list of all the posts in the database which matches the keyword
        '''
        if not keyword:
            return False
        #Create the SQL Statement for retrieving posts
        query = "SELECT * FROM posts where title like ? or details like ? or tags like ? ORDER BY add_date DESC"        
        self.set_foreign_keys_support()        
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        pvalue = ('%'+keyword+'%','%'+keyword+'%','%'+keyword+'%',)
        cur.execute(query, pvalue)
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return post object
        posts = []
        for row in rows:
            post = self._format_post(row)
            posts.append(post)
        return posts
        
    def get_post(self, post_id):
        '''
            :param int post_id: id of the post to be collected from database
            
            :return: a formatted key value pairs of post object
        '''
        post_id = int(post_id)
        
        if post_id is None:            
            return None
            
        self.set_foreign_keys_support()        
        queryGetPost = 'SELECT * from posts WHERE post_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        pvalue = (post_id,)
        cur.execute(queryGetPost, pvalue)
        
        row = cur.fetchone()
        if row is None:
            return None
        return self._format_post(row)
        
    def _check_post_by_id(self, post_id):
        '''
            Checking if the Post exists by searching with post_id
            
            :return: the id of the post if it exists or None if the message could not be found or the id is invalid
        '''
        queryFindPost = "SELECT * FROM posts WHERE post_id = '%s'"  % post_id
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(queryFindPost)
        # Get post if it exists
        postRow = cur.fetchone()
        if postRow is None:
            return None
        return post_id
        
    def create_post(self, post):              
        '''
            Create a new post with the data provided as arguments.

            :param object post: Is an object which containes several parameters  
                int post["user_id"]: The posts's owner is the user_id or that owner user
                str post["details"]: the details of the post
                str post["title"]: the title of the post
                int post["category_id"]: the category_id of the post, it can be empty
                str post["tags"]: the tags of the post, it can be empty

            :return: the id of the created post or False if the message could not be created

        '''
        try:
            title = post['user_id']
            details = post['details']
            user_id = int(post['user_id'])
        except:
            return None            
            
        getUser = self.check_user_by_id(user_id)        
        if not getUser:
            return None
            
        category = post.get('category_id', None)    
        if category:
            check_category = self._check_category_by_id(category)
            if not check_category:
                return None
            
        tags = post.get('tags', None)
        add_date = time.mktime(datetime.now().timetuple())        
        last_update = time.mktime(datetime.now().timetuple())
        
        queryPost = 'INSERT INTO posts (title,details,user_id,category_id,tags,add_date,last_update) VALUES(?,?,?,?,?,?,?)'
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        
        cur = self.con.cursor()      
                
        pvalue = (title,details,user_id,category,tags,add_date,last_update,)
        cur.execute(queryPost, pvalue)
        
        self.con.commit()
        # Extract the id of the added post
        post_id = cur.lastrowid
        #Return the id of category
        if post_id:
            return post_id
        return False
        
    def edit_post(self, post_id, post):
        '''
             Edits a new post with the data provided as arguments along with post_id.

            :param object post: Is an object which containes several parameters  
                int post["user_id"]: The posts's owner is the user_id or that owner user
                str post["details"]: the details of the post
                str post["title"]: the title of the post
                int post["category_id"]: the category_id of the post, it can be empty
                str post["tags"]: the tags of the post, it can be empty

            :return: the id of the edited post or None if the post could not be edited      
        '''
        post_id = int(post_id)
        
        if not post_id:
            return None
            
        checkPost = self._check_post_by_id(post_id)
        if not checkPost:
            return None
        
        try:
            title = post['title']
            details = post['details']
            user_id = int(post['user_id'])
        except:
            return None            
            
        getUser = self.check_user_by_id(user_id)        
        if not getUser:
            return None
            
        category = post.get('category_id', None)
        tags = post.get('tags', None)     
        last_update = time.mktime(datetime.now().timetuple())        
        
        queryPost = 'UPDATE posts SET title=?,details=?,user_id=?,category_id=?,tags=?,last_update=? WHERE post_id = ?'
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row        
        cur = self.con.cursor()               
        pvalue = (title,details,user_id,category,tags,last_update,post_id,)
        cur.execute(queryPost, pvalue)        
        self.con.commit()
        if cur.rowcount < 1:
            return None
        return post_id
        
    def delete_post(self, post_id): 
        '''
            Delete the post with id given as parameter.

            :param int post_id: id of the post to remove
            
            :return: True if the post has been deleted, False otherwise
            :return: None: if the messageid is not valid

        '''
        post_id = int(post_id)
        if not post_id:
            return None
        
        #SQL Statement for deleting the user information
        query = 'DELETE FROM posts WHERE post_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (post_id,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True
        
    ## Posts API Ends
    
    
    
    ## Categories API Starts
    
    def _format_category(self,category):
        '''
            :return: a formatted key value pairs of category object
        '''
        return {
            'category_id': category['category_id'],        
            'title': str(category['title']),        
            'description': str(category['description']),        
            'add_date': category['add_date'],
            'last_update': category['last_update']       
        }
    
    def get_categories(self): 
        '''
            :return: Return a list of all the categories in the database and ordered by add_date
        '''
    
        #Create the SQL Statement for retrieving categories
        query = "SELECT * FROM categories ORDER BY add_date DESC"
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        categories = []
        for row in rows:
            category = self._format_category(row)
            categories.append(category)
        return categories
        
    def get_category(self, category_id):
        '''
            :param int category_id: id of the category to be collected from database
            
            :return: int category_id if the category exists
            :return: None: if the category_id is not valid or not found
        '''
        
        category_id = int(category_id)        
        if category_id is None:            
            return None
            
        self.set_foreign_keys_support()        
        queryGetCat = 'SELECT * from categories WHERE category_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        pvalue = (category_id,)
        cur.execute(queryGetCat, pvalue)
        
        row = cur.fetchone()
        if row is None:
            return None
        return self._format_category(row)
        
    def _check_category_by_id(self, category_id):
        '''
            Checking if the category exists by searching with category_id
            
            :param int category_id: id of the category to be checked
            
            :return: a formatted key value pairs of category object using ``_format_category`` function
        '''
        queryFindCategory = "SELECT * FROM categories WHERE category_id = '%s'"  % category_id
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(queryFindCategory)
        # Get post if it exists
        categoryRow = cur.fetchone()
        if categoryRow is None:
            return None
        return category_id
        
    def _check_category_by_title(self, title):
        '''
            Checking if the category exists by searching with title
            
            :param str title: title of the category to be checked
            
            :return: the title of the category if exists
        '''
        queryFindCategory = "SELECT * FROM categories WHERE title = '%s'"  % title
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(queryFindCategory)
        # Get post if it exists
        categoryRow = cur.fetchone()
        if categoryRow is None:
            return None
        return title
        
    def create_category(self, category):
        '''
            Create a new post with the data provided as arguments.

            :param object post: Is an object which containes several parameters  
                str category["title"]: The title of the category
                str category["description"]: the description of the category
                int category["add_date"]: the timestamp of the add date of the category
                int category["last_update"]: the timestamp of last update of the category

            :return: the id of the created category or False if the message could not be created

        '''
        
        title = category.get('title', None)
        description = category.get('description', None)
        add_date = category.get('add_date', None)
        last_update = category.get('last_update', None)
        
        if not title:
            return None
            
        if add_date is None:
            add_date = time.mktime(datetime.now().timetuple())
            
        if last_update is None:
            last_update = time.mktime(datetime.now().timetuple())
            
        queryCategory = 'INSERT INTO categories (title,description,add_date,last_update) VALUES(?,?,?,?)'
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        
        cur = self.con.cursor()        
                
        pvalue = (title,description,add_date,last_update,)
        cur.execute(queryCategory, pvalue)
        
        self.con.commit()
        #Extract the id of the added category
        category_id = cur.lastrowid
        #Return the id of category
        if category_id:
            return category_id
        return False
        
    def edit_category(self, category_id, title="", description=""):
        '''
            Create a new post with the data provided as arguments.

            :param object post: Is an object which containes several parameters  
                int category_id: The id of the category to be edited
                str title: the title of the category
                str description: the description of the category

            :return: the id of the created category or None if the category could not be edited

        '''
        category_id = int(category_id)
        if not category_id:
            return None           
            
        # Checking if the category exists 
        queryGetCategory = "SELECT * FROM categories WHERE category_id = '%s'"  % category_id
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(queryGetCategory)
        #Get results
        categoryRow = cur.fetchone()
        if categoryRow is None:
            return None
        else:
            if not title:
                title = categoryRow['title']
                
            if not description:
                description = categoryRow['description']
                
            last_update = time.mktime(datetime.now().timetuple())
            
        #Create the SQL statment
        stmnt = 'UPDATE categories SET title=?, description=?, last_update=? WHERE category_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (title, description, last_update, category_id,)
        cur.execute(stmnt, pvalue)
        self.con.commit()
        if cur.rowcount < 1:
            return None
        return category_id
        
    def delete_category(self, category_id):
        '''
            Delete the category with category_id given as parameter.

            :param int category_id: id of the category to remove
            
            :return: True if the category has been deleted, False otherwise
            :return: None if the category_id is not valid

        '''
        category_id = int(category_id)
        if not category_id:
            return None
            
        #Create the SQL Statements
        #SQL Statement for deleting the user information
        query = 'DELETE FROM categories WHERE category_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (category_id,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True
        
    ## Categories API Ends
    
    
    ## Reports API Starts
    
    def _format_report(self,report):
        '''
            :return: a formatted key value pairs of report object
        '''
        return {
            'report_id': report['report_id'],        
            'post_id': report['post_id'],        
            'user_id': report['user_id'],
            'details': str(report['details'])       
        }
    def _check_report_by_id(self, report_id):
        '''
            Checking if the report exists by searching with report_id
            
            :param int report_id: id of the report to be checked
            
            :return: id of the repott if exists otherwise None
        '''
        queryFindReport = "SELECT * FROM reports WHERE report_id = '%s'"  % report_id
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(queryFindReport)
        # Get report if it exists
        reportRow = cur.fetchone()
        if reportRow is None:
            return None
        return report_id
        
    def get_reports(self):
        '''
            :return: Return a list of all the reports in the database. None if no report exists
        '''
        #Create the SQL Statement for retrieving posts
        query = "SELECT * FROM reports"
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        reports = []
        for row in rows:
            report = self._format_report(row)
            reports.append(report)
        return reports
        
    def get_report(self, report_id):
        '''
            :param int report_id: id of the report to be collected from database
            
            :return: the report object which formatted with ``_format_report`` method
            :return: None: if the report_id is not valid or not found
        '''
        report_id = int(report_id)        
        if report_id is None:            
            return None
            
        self.set_foreign_keys_support()        
        queryGetReport = 'SELECT * from reports WHERE report_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        pvalue = (report_id,)
        cur.execute(queryGetReport, pvalue)
        
        row = cur.fetchone()
        if row is None:
            return None
        return self._format_report(row)
        
    def create_report(self, post_id, user_id, details):
        '''
            Create a new report with the parameters provided

            :param object post: Is an object which containes several parameters  
                int post_id: The post_id to be reported
                int user_id: The used with user_id who is reporting
                str details: the description of the report by the user

            :return: None if the post is not found or the user is not found
            :return: the id of the created report if successful or False if the message could not be created

        '''
        post_id = int(post_id)
        user_id = int(user_id)
        
        if not user_id or not user_id or not details:
            return None
        
        # Checking if the Post exists 
        queryFindPost = "SELECT * FROM posts WHERE post_id = '%s'"  % post_id
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(queryFindPost)
        # Get results
        postRow = cur.fetchone()
        if postRow is None:
            return None

        # Checking if the User exists 
        queryFindUser = "SELECT * FROM users WHERE user_id = '%s'"  % user_id
        
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(queryFindUser)
        # Get results
        userRow = cur.fetchone()
        if userRow is None:
            return None
        
        
        queryReportInsert = 'INSERT INTO reports (post_id,user_id,details) VALUES(?,?,?)'
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        
        cur = self.con.cursor()        
                
        pvalue = (post_id,user_id,details,)
        cur.execute(queryReportInsert, pvalue)
        
        self.con.commit()
        #Extract the id of the added report_id
        report_id = cur.lastrowid
        #Return the id of report_id
        if report_id:
            return report_id
        return False
        
    def edit_report(self, report_id, details): 
        '''
            Edit a report with the parameters provided

            :param object post: Is an object which containes several parameters  
                int report_id: The id of the report
                str details: the description of the report by the user

            :return: None if the report is not found
            :return: the id of the report if successful or False if the report could not be edited

        '''
        
        report_id = int(report_id)
        if not report_id:
            return None

        if not details:
            return None
            
        # Checking if the category exists 
        queryGetReports = "SELECT * FROM reports WHERE report_id = '%s'"  % report_id
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(queryGetReports)
        #Get results
        reportRow = cur.fetchone()
        if reportRow is None:
            return None
            
        #Create the SQL statment
        stmnt = 'UPDATE reports SET details=? WHERE report_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (details, report_id,)
        cur.execute(stmnt, pvalue)
        self.con.commit()
        if cur.rowcount < 1:
            return False
        return report_id
        
    def delete_report(self, report_id):
        '''
            Delete the report with report_id given as parameter.

            :param int report_id: id of the report to remove
            
            :return: True if the report has been deleted, False otherwise
            :return: None if the report_id is not valid

        '''
        report_id = int(report_id)
        if not report_id:
            return None
        #Create the SQL Statements
        #SQL Statement for deleting the user information
        query = 'DELETE FROM reports WHERE report_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (report_id,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True
        
    ## Reports API Ends
    
    ## Users API Starts
    def _create_user_object(self, row):
        return {'primary_profile': {
                                   'user_id': str(row['user_id']),
                                   'username': str(row['username']),
                                   'email': str(row['email']),
                                   'reg_date': row['reg_date']
                                   },
                'profile_details': {
                                    'fullname': str(row['fullname']),
                                    'phone': str(row['phone']),
                                    'website': str(row['website']),
                                    'address': str(row['address']),
                                    'skype': str(row['skype']),
                                    'gender': str(row['gender'])
                                   }
                }
    
    def _create_user_primary_object(self, row):
        return {
                   'username': str(row['username']),
                   'email': str(row['email']),
                   'reg_date': row['reg_date']
               }
               
    def _create_user_details_object(self, row):
        return {
                   'user_id': str(row['user_id']),
                   'username': str(row['username']),
                   'email': str(row['email']),
                   'reg_date': row['reg_date']
               }
               
    def get_all_users(self):
        '''
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary. None is returned if the database has no users.
        
        '''
        #Create the SQL Statements
          #SQL Statement for retrieving the users
        query = 'SELECT * FROM users'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Process the response.
        users = []
        for row in rows:
            user = self._create_user_primary_object(row)
            users.append(user)
        return users
               
    def get_users(self):
        '''
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary. None is returned if the database has no users.
        
        '''
        #Create the SQL Statements
          #SQL Statement for retrieving the users
        query = 'SELECT users.*, users_profile.* FROM users, users_profile \
                 WHERE users.user_id = users_profile.user_id'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Process the response.
        users = []
        for row in rows:
            user = self._create_user_object(row)
            users.append(user)
        return users
        
    def check_user_by_id(self, user_id):
        '''
            Checking if the user exists by searching with user_id
            
            :param int user_id: id of the user to be checked
            
            :return: int user_id if the user exists, None if the user not found
        '''
        # Checking if the User exists by searching with user_id
        queryFindUser = "SELECT * FROM users WHERE user_id = '%s'"  % user_id
        
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(queryFindUser)
        # Get results
        userRow = cur.fetchone()
        if userRow is None:
            return None
        return user_id
        
    def check_user_by_email(self, email):
        '''
            Checking if the user exists by searching with email
            
            :param str email: id of the user to be checked
            
            :return: str email if the user exists, None if the user not found
        '''
        # Checking if the email exists already
        queryFindUser = "SELECT * FROM users WHERE email = '%s'"  % email
        
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(queryFindUser)
        # Fetching results
        userRow = cur.fetchone()
        if userRow is None:
            return None
        return email

    def get_user(self, username):
        '''
            Extracts all the information of a user.

            :param str username: The username of the user to search
            :return: dictionary with the format using method ``_create_user_object``

        '''
        
        #SQL Statement for retrieving the user given a username
        query1 = 'SELECT user_id from users WHERE username = ?'
          #SQL Statement for retrieving the user information
        query2 = 'SELECT users.*, users_profile.* FROM users, users_profile \
                  WHERE users.user_id = ? \
                  AND users_profile.user_id = users.user_id'
          #Variable to be used in the second query.
        user_id = None
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute SQL Statement to retrieve the id given a nickname
        pvalue = (username,)
        cur.execute(query1, pvalue)
        #Extract the user id
        row = cur.fetchone()
        if row is None:
            return None
        user_id = row["user_id"]
        # Execute the SQL Statement to retrieve the user invformation.
        # Create first the valuse
        pvalue = (user_id, )
        #execute the statement
        cur.execute(query2, pvalue)
        #Process the response. Only one posible row is expected.
        row = cur.fetchone()
        if row:
            return self._create_user_object(row)
        return None
        
    
    def get_user_by_username(self, username):
        '''
            Extracts all the information of a user.

            :param str username: The username of the user to search
            :return: dictionary with the format using method ``_create_user_primary_object``

        '''
        
        #SQL Statement for retrieving the user given a username
        query = 'SELECT * from users WHERE username = ?'
        
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute SQL Statement to retrieve the id given a nickname
        pvalue = (username,)
        cur.execute(query, pvalue)
        #Extract the user id
        row = cur.fetchone()
        
        if row:
            print(row)
            return self._create_user_primary_object(row)
        return None
    
    def delete_user(self, username):
        '''
            Remove all information of the user with the username passed in as argument.

            :param str username: The username of the user to remove.

            :return: True if the user is deleted, False otherwise.

        '''
        #Create the SQL Statements
        #SQL Statement for deleting the user information
        query = 'DELETE FROM users WHERE username = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (username,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True
        
    def create_user(self, user):
        '''
            Create a new user_profile if it doesn't exist using the data provided as arguments

            :param object post: Is an object which containes several parameters  
                str user["username"]: The username of the user
                str user["email"]: the email of the user
                str user["reg_date"]: the timestamp of the registration date of the user

            :return: the user_id of the created user or False if the message could not be created, None if username or email already exists

        '''
        username = user.get('username', None)
        email = user.get('email', None)
        reg_date = user.get('reg_date', None)
        
        if not username or not email:
            return None
            
        checkUserEmail = self.check_user_by_email(email)
        # If user already exists then it will return None
        if checkUserEmail:
            return None
        
        checkUsername = self.get_user(username)
        # If user already exists then it will return None
        if checkUsername:
            return None

        if not reg_date:
            reg_date = time.mktime(datetime.now().timetuple())
        
        stmnt = 'INSERT INTO users (username,email, reg_date) VALUES(?,?,?)'
        
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()        
        
        pvalue = (username,email, reg_date)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        user_id = cur.lastrowid
        #Return the id of message
        if user_id:
            return user_id
        return False

    def modify_user(self, user_id, email):
        '''
        Modify the information of a user.

        :param int user_id: The id of the user to modify
        :param str email: the email of the user. Email is the only parameter which can be modified for the user's primary_profile,
                            for secondary_profile we can use user_profile functionalities

        :return: the user_id of the user,  None if the update was not completed or the user not found

        '''
        user_id = int(user_id)
        checkEmail = None
        
        if not user_id:
            return False
        
        checkUser = self.check_user_by_id(user_id)    
        if not checkUser:
            return "NOTEXIST"
            
        if email:
            checkEmail = self.check_user_by_email(email)
            
            if checkEmail:
                return None
        else:
            return False
        
        #Create the SQL Statements
        #SQL Statement for extracting the userid given a username
        
        #SQL Statement to update the user_profile table
        query = 'UPDATE users SET email = ? WHERE user_id = ?'
        
        
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        #Execute the statement to extract the id associated to a nickname
        pvalue = (email,user_id)
        cur.execute(query, pvalue)
        #Only one value expected
        row = cur.fetchone()
        #if does not exist, return
        self.con.commit()
        #Check that I have modified the user
        if cur.rowcount < 1:
            return None
        return user_id
        
    def modify_user_by_username(self, username, email):
        '''
        Modify the information of a user.

        :param int user_id: The id of the user to modify
        :param str email: the email of the user. Email is the only parameter which can be modified for the user's primary_profile,
                            for secondary_profile we can use user_profile functionalities

        :return: the user_id of the user,  None if the update was not completed or the user not found

        '''
        username = str(username)
        checkEmail = None
        
        if not username:
            return False
                    
        if email:
            checkEmail = self.check_user_by_email(email)            
            if checkEmail:
                return None
        else:
            return False
                
        #SQL Statement to update the users table
        query = 'UPDATE users SET email = ? WHERE username = ?'
        
        
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        #Execute the statement to extract the id associated to a nickname
        pvalue = (email,username)
        cur.execute(query, pvalue)
        #Only one value expected
        row = cur.fetchone()
        #if does not exist, return
        self.con.commit()
        #Check that I have modified the user
        if cur.rowcount < 1:
            return None
        return username

    def get_user_id(self, username):
        '''
            Get the id of the user with the given username.

            :param str username: The username of the user to search.
            :return: int user_id of the user or None if ``username`` does not exist.

        '''
        
        query = 'SELECT user_id from users WHERE username = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the  main statement
        pvalue = (username,)
        cur.execute(query, pvalue)
        #Extract the results. Just one row expected.
        row = cur.fetchone()
        if row is None:
            return None
        else:
            return row["user_id"]

    def contains_user(self, username):
        '''
        :return: True if the user is in the database. False otherwise
        '''
        return self.get_user_id(username) is not None
    
    
    #Users API Ends
    
    ## User Profile API Starts
    
    def _format_user_profile(self, profile):
        return {
                   'user_id': profile['user_id'],
                   'fullname': str(profile['fullname']),
                   'phone': str(profile['phone']),
                   'website': str(profile['website']),
                   'address': str(profile['address']),
                   'skype': str(profile['skype']),
                   'gender': str(profile['gender'])                                   
                }
                
    def _check_if_profile_exists(self, user_id):
        '''
            Checking if the user_profile exists by searching with user_id
            
            :param int user_id: id of the user to be checked
            
            :return: int user_id if the user exists, None if the user not found
        '''
        query = 'SELECT user_id from users_profile WHERE user_id = ?'
        
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the  main statement
        pvalue = (user_id,)
        cur.execute(query, pvalue)
        #Extract the results. Just one row expected.
        row = cur.fetchone()
        if row is None:
            return None
        else:
            return row["user_id"]
    
    def get_user_profile(self, user_id):
        '''
            :param int user_id: id of the user to be collected from database
            
            :return: the user_profile object which formatted with ``_format_user_profile`` method
            :return: None: if the user_id is not valid or not found
        '''
        user_id = int(user_id)
        
        if user_id is None:            
            return None
            
        self.set_foreign_keys_support()        
        queryGetPost = 'SELECT * from users_profile WHERE user_id = ?'
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        
        pvalue = (user_id,)
        cur.execute(queryGetPost, pvalue)
        
        row = cur.fetchone()
        if row is None:
            return None
        return self._format_user_profile(row)
        
    def create_user_profile(self, user):
        '''
            Create a new user_profile if it doesn't exist using the data provided as arguments

            :param object post: Is an object which containes several parameters  
                str user["fullname"]: The fullname of the user
                str user["phone"]: the phone of the user
                str user["website"]: the website of the user
                str user["address"]: the address of the user
                str user["skype"]: the skype address of user
                str user["gender"]: the gender of the user. M or F

            :return: the user_id of the created user or False if the message could not be created, None if profile already exists

        '''
        user_id = user.get('user_id', None)
        if not user_id:
            return None
            
        checkProfile = self._check_if_profile_exists(user['user_id'])
        # If user profile already exists then it will return False
        if checkProfile:
            return None
        
        #
        fullname = user.get('fullname', None)
        phone = user.get('phone', None)
        website = user.get('website', None)
        address = user.get('address', None)
        skype = user.get('skype', None)
        gender = user.get('gender', None)
        
        stmnt = 'INSERT INTO users_profile (user_id,fullname, phone, website, address, skype, gender) VALUES(?,?,?,?,?,?,?)'
        
        self.set_foreign_keys_support()
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()        
        
        pvalue = (user_id,fullname, phone, website, address, skype, gender)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        user_id = cur.lastrowid
        #Return the id of message
        if user_id:
            return user_id
        return False
        
    def edit_user_profile(self, user_id, user):
        '''
            Edit an existing user_profile using the data provided as arguments

            :param object post: Is an object which containes several parameters  
                str user["fullname"]: The fullname of the user
                str user["phone"]: the phone of the user
                str user["website"]: the website of the user
                str user["address"]: the address of the user
                str user["skype"]: the skype address of user
                str user["gender"]: the gender of the user. M or F

            :return: the user_id of the edited user_profile or False if the message could not be edited, 
                     None if profile not found or user_id not valid

        '''
        user_id = int(user_id)
        if not user_id:
            return False
            
        checkProfile = self._check_if_profile_exists(user_id)
        # If user profile already exists then it will return False
        if not checkProfile:
            return None
            
        fullname = user.get('fullname', None)
        phone = user.get('phone', None)
        website = user.get('website', None)
        address = user.get('address', None)
        skype = user.get('skype', None)
        gender = user.get('gender', None)
    
        stmnt = 'UPDATE users_profile SET fullname=?, phone=?, website=?, address=?, skype=?, gender=? WHERE user_id = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (fullname, phone, website, address, skype, gender,user_id,)
        cur.execute(stmnt, pvalue)
        self.con.commit()
        if cur.rowcount < 1:
            return False
        return user_id
        
    ## User Profile API Ends