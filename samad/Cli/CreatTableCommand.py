commands = (
	"""
	CREATE TABLE IF NOT EXISTS foods (
		ID SERIAL PRIMARY KEY,
		name VARCHAR (20) NOT NULL,
		date DATE NOT NULL,
		price BIGINT NOT NULL,
		inventory SMALLINT NOT NULL,
        UNIQUE(name, date),
		CONSTRAINT inv CHECK (
			inventory >= 0
		),
        CONSTRAINT price CHECK (
			price >= 0
		)
	);
	""",
	"""
	CREATE TABLE IF NOT EXISTS students (
		ID VARCHAR (20) PRIMARY KEY,
		studentID SERIAL UNIQUE NOT NULL,
		major VARCHAR (20) NOT NULL,
		birth_date DATE NOT NULL, 
		first_name VARCHAR (20) NOT NULL,
		last_name VARCHAR (20) NOT NULL,
		balance BIGINT NOT NULL,
		CONSTRAINT id CHECK (
			LENGTH (ID::text) = 10
		),
		CONSTRAINT balance CHECK (
			balance >= 0
		),
		CONSTRAINT studentid CHECK (
			LENGTH (studentID::text) = 7 OR
			LENGTH (studentID::text) = 8
		)
	);
	""",
	"""
	CREATE TABLE IF NOT EXISTS reservations(
		ID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		studentID SERIAL NOT NULL,
		foodID SERIAL NOT NULL,
        isReserved BOOL DEFAULT TRUE,
        UNIQUE (studentID, foodID),
        
		CONSTRAINT student
			FOREIGN KEY (studentID)
			REFERENCES students (studentID)
            ON DELETE CASCADE,
            

		CONSTRAINT food
			FOREIGN KEY (foodID)
			REFERENCES foods (ID)
            ON DELETE CASCADE
	);
	""",
	"""
	CREATE TABLE IF NOT EXISTS transactions (
		SRCreservationID INT REFERENCES reservations(ID) ON DELETE CASCADE,
		DSTreservationID INT REFERENCES reservations(ID) ON DELETE CASCADE,
		dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	"""
)