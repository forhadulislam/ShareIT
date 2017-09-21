## ShareIT API

Dependencies
- Python 2.7
- Standard Python libraries for implementing and testing
	
Database
- SQLite Database used for implementation
- All Database files are in the `db` directory
- Database can be executed with
   -> sqlite3 db/shareit.db

## Running the API
Running our API is simple. In the root directory of the app, we need to run this command:
	`python main.py`
	
## Testing
Run all test cases in file with `python -m unittest test.<testfilename>`.

In our case-
	`python -m unittest test.test_database`
	or
	`python -m test.test_database`
	
Run a specific test case using `python -m unittest test.<testFileName>.<testCaseName>`

In our case-
	`python -m unittest test.test_database.DBAPITestCase`
	 Here, `DBAPITestCase` is the test case name.

We have two different test file for two different criteria.

	For -	
	`test_database` -> We have all test cases written for database testing
	
	`test_api` -> We have all test cases written for API testing

In `test_database`, we have different test cases. Here is the complete list:

	* DB Test (DBAPITestCase) - `python -m unittest test.test_database.DBAPITestCase`
	* Messages - `python -m unittest test.test_database.MessageAPITestCase`
	* Users - `python -m unittest test.test_database.UsersAPITestCase`
	* UserProfiles - `python -m unittest test.test_database.UserProfileAPITestCase`
	* Categories - `python -m unittest test.test_database.CategoriesAPITestCase`
	* Posts - `python -m unittest test.test_database.PostAPITestCase`
	* Reports - `python -m unittest test.test_database.ReportAPITestCase`
	
In `test_api`, we have written 13 test cases. Here is the complete list:

	* MessagesTestCase - `python -m unittest test.test_api.MessagesTestCase`
	* MessageTestCase - `python -m unittest test.test_api.MessageTestCase`
	* UsersTestCase - `python -m unittest test.test_api.UsersTestCase`
	* UserTestCase - `python -m unittest test.test_api.UserTestCase`
	* CategoriesTestCase - `python -m unittest test.test_api.CategoriesTestCase`
	* CategoryTestCase - `python -m unittest test.test_api.CategoryTestCase`
	* PostsTestCase - `python -m unittest test.test_api.PostsTestCase`
	* PostTestCase - `python -m unittest test.test_api.PostTestCase`
	* ReportsTestCase - `python -m unittest test.test_api.ReportsTestCase`
	* ReportTestCase - `python -m unittest test.test_api.ReportTestCase`
	* UserProfilesTestCase - `python -m unittest test.test_api.UserProfilesTestCase`
	* UserProfileTestCase - `python -m unittest test.test_api.UserProfileTestCase`
	* SearchTestCase - `python -m unittest test.test_api.SearchTestCase`


## Client
Dependencies -

	* jQuery
	* Materializecss
	
### Setting Up Client
At first you need to run the Flask server. Running our the server is simple. In the root directory of the app, you need to run this command:
	`python main.py`
	
This command will run the API server and Client both. So we do not need to run 2 servers for these two functionalities. To access the client we need to visit the URL:
	<a href="http://localhost:5000/shareit/client/index.html#home">Client Home</a>
