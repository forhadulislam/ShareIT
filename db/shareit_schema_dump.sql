BEGIN TRANSACTION;
CREATE TABLE users_profile(user_id INTEGER PRIMARY KEY,                     fullname TEXT,                     phone TEXT, website TEXT,                     address TEXT,                     skype TEXT, gender TEXT,                     FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,                      username TEXT UNIQUE, email TEXT UNIQUE,                      reg_date INTEGER,                      UNIQUE(username, email));
CREATE TABLE reports ( report_id INTEGER PRIMARY KEY,                      post_id INTEGER, user_id INTEGER,                      details TEXT,                      FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE,                      FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE posts (post_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,                      title TEXT, details TEXT,                      category_id INTEGER, tags TEXT,                      add_date INTEGER, last_update INTEGER,                      FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,                      FOREIGN KEY(category_id) REFERENCES categories(category_id) ON DELETE CASCADE);
CREATE TABLE messages(message_id INTEGER PRIMARY KEY AUTOINCREMENT,                     message_details TEXT,                     sender INTEGER, receiver INTEGER,                     send_time INTEGER,                     FOREIGN KEY(sender) REFERENCES users(user_id) ON DELETE CASCADE,                     FOREIGN KEY(receiver) REFERENCES users(user_id) ON DELETE CASCADE);
CREATE TABLE "categories" (
	`title`	TEXT UNIQUE,
	`description`	TEXT,
	`add_date`	INTEGER,
	`last_update`	INTEGER,
	`category_id`	INTEGER PRIMARY KEY AUTOINCREMENT
);
COMMIT;
