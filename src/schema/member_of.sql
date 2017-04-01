CREATE TABLE IF NOT EXISTS member_of
(
	username TEXT NOT NULL PRIMARY KEY,
	o_id TEXT NOT NULL,
	FOREIGN KEY (username) REFERENCES person (username) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (o_id) REFERENCES organisation (o_id) ON DELETE CASCADE ON UPDATE CASCADE
 );