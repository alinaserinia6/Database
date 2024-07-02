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
	""",
	"""
	CREATE TABLE IF NOT EXISTS today (
		name VARCHAR (20) PRIMARY KEY,
		inventory SMALLINT NOT NULL
	);
	""",
	"""
	CREATE OR REPLACE PROCEDURE name_inv ()
	LANGUAGE SQL
	AS $$
		DELETE FROM today;
		INSERT INTO today(name, inventory)
			SELECT f.name, count(*)
			FROM foods f INNER JOIN reservations r ON f.ID = r.foodID
			WHERE f.date = CURRENT_DATE and r.isReserved
			GROUP BY f.name
	$$;
 	""",
	"""
	CREATE TABLE IF NOT EXISTS stuToday (
		id SERIAL PRIMARY KEY
	);
	""",
	"""
	CREATE OR REPLACE PROCEDURE stu_today ()
	LANGUAGE SQL
	AS $$
		DELETE FROM stuToday;
		INSERT INTO stuToday(id)
			SELECT DISTINCT s.studentID
			FROM (students s INNER JOIN reservations r ON s.studentID = r.studentID) INNER JOIN foods f ON r.foodID = f.ID
			WHERE r.isReserved and f.date = CURRENT_DATE;
	$$;
	""",
	"""
	CREATE TABLE IF NOT EXISTS last10Transactions (
		srcreservationID INT,
		dstreservationID INT,
		dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	""", 
	"""
	CREATE OR REPLACE PROCEDURE last10 ()
	LANGUAGE SQL
	AS $$
		DELETE FROM last10Transactions;
		INSERT INTO last10Transactions
			SELECT *
			FROM TRANSACTIONS
			ORDER BY dt DESC
			LIMIT 10;
	$$;
	""", 
	"""
	CREATE TABLE IF NOT EXISTS foodsRemain (
		name VARCHAR (20) PRIMARY KEY,
		num SMALLINT NOT NULL
	);
	""",
	"""
		CREATE OR REPLACE PROCEDURE foods_remain ()
		LANGUAGE SQL
		AS $$
			DELETE FROM foodsRemain;
			INSERT INTO foodsRemain
				SELECT DISTINCT f.name, f.inventory
				FROM reservations r LEFT JOIN foods f ON f.ID = r.foodID
				WHERE f.date = CURRENT_DATE and r.isReserved;
		$$;
	""",
	"""
		CREATE TABLE IF NOT EXISTS assetTurnover (
			date DATE PRIMARY KEY,
			totalSales INT NOT NULL
		);
	""",
	"""
		CREATE OR REPLACE PROCEDURE asset_turnover ()
		LANGUAGE SQL
		AS $$
			DELETE FROM assetTurnover;
			INSERT INTO assetTurnover
			SELECT f.date, sum(f.price)
			FROM reservations r INNER JOIN foods f ON r.foodID = f.ID
			WHERE r.isReserved
			GROUP BY f.date
			ORDER BY f.date ASC;
		$$;
	""",
    """
		CREATE OR REPLACE FUNCTION duplicateStuId ()
        RETURNS TRIGGER AS 
		$$
		BEGIN
			IF EXISTS (SELECT * FROM students s WHERE s.ID = NEW.ID OR s.studentID = NEW.studentID) THEN
				RAISE EXCEPTION 'duplicate id';
				RETURN NULL;
            END IF;
			RETURN NEW;
		END;
		$$
        LANGUAGE plpgsql;
	""",
    """
		CREATE OR REPLACE TRIGGER duplicateTrigger
		BEFORE INSERT ON students
		FOR EACH ROW 
		EXECUTE PROCEDURE duplicateStuId();
	""",
    """
		CREATE OR REPLACE FUNCTION lessFood ()
        RETURNS TRIGGER AS 
		$$
		BEGIN
			IF (NEW.inventory < 500) THEN
				RAISE EXCEPTION 'inventory of food is less than 500';
				RETURN NULL;
            END IF;
			RETURN NEW;
		END;
		$$
        LANGUAGE plpgsql;
	""",
    """
		CREATE OR REPLACE TRIGGER lessFoodTrigger
		BEFORE INSERT ON foods
		FOR EACH ROW 
		EXECUTE PROCEDURE lessFood();
	""",
    """
		CREATE OR REPLACE FUNCTION sameTime ()
        RETURNS TRIGGER AS 
		$$
		DECLARE
			newfoodId INT;
		BEGIN
			SELECT r.foodID INTO newfoodId FROM reservations r WHERE r.ID = NEW.DSTreservationID;
			IF EXISTS (SELECT * FROM transactions t INNER JOIN reservations r ON t.DSTreservationID = r.ID 
						WHERE t.dt = NEW.dt AND newfoodId <> r.foodID) THEN 
				RAISE EXCEPTION 'same time transactions, do your transaction another time';
				RETURN NULL;
            END IF;
			RETURN NEW;
		END;
		$$
        LANGUAGE plpgsql;
	""",
    """
		CREATE OR REPLACE TRIGGER sameTimeTrigger
		BEFORE INSERT ON transactions
		FOR EACH ROW 
		EXECUTE PROCEDURE sameTime();
	""",
    """
		CREATE OR REPLACE FUNCTION sameTimeStudent ()
        RETURNS TRIGGER AS 
		$$
		DECLARE
			userId INT;
		BEGIN
			SELECT r.studentID INTO userID FROM reservations r WHERE r.ID = NEW.DSTreservationID; 
			IF EXISTS (SELECT * FROM transactions t INNER JOIN reservations r ON t.DSTreservationID = r.ID
				WHERE t.dt = NEW.dt AND r.studentID = userId) THEN
				RAISE EXCEPTION 'same time transactions for this user';
				RETURN NULL;
            END IF;
			RETURN NEW;
		END;
		$$
        LANGUAGE plpgsql;
	""",
    """
		CREATE OR REPLACE TRIGGER sameTimeStudentTrigger
		BEFORE INSERT ON transactions
		FOR EACH ROW 
		EXECUTE PROCEDURE sameTimeStudent();
	""",
    """
		CREATE OR REPLACE VIEW student_food AS
        SELECT s.last_name, f.name
        FROM reservations r INNER JOIN students s ON r.studentID = s.studentID
			INNER JOIN foods f ON f.ID = r.foodID
		WHERE r.isReserved
		ORDER BY s.last_name;
	""",
    """
		CREATE OR REPLACE VIEW student_transaction AS
        SELECT s.studentID, s.first_name, s.last_name, f1.name f1name, f2.name f2name
        FROM transactions t 
			LEFT JOIN reservations r1 ON r1.ID = t.SRCreservationID
			LEFT JOIN reservations r2 ON r2.ID = t.DSTreservationID
			LEFT JOIN foods f1 ON f1.ID = r1.foodID
			LEFT JOIN foods f2 ON f2.ID = r2.foodID,
			students s WHERE s.studentID = r1.studentID OR s.studentID = r2.studentID;		
	"""
)