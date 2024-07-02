import psycopg2
import Cli.actions.utils.utils as ut
from Cli.actions.utils.utils import war, ok, detail
from termcolor import cprint

class Actions():
	REGISTER = 'register'
	REMOVE = 'remove'
	INCREASE_CREDIT = 'credit'
	ADD_FOOD = 'add'
	DELETE_FOOD = 'delete'
	RESERVE = 'reserve'
	CHANGE_RESERVE = 'change'
	DELETE_DB = 'deleteDB'
	SHOW_DB ='showDB'
	TABLE_NAMES = ['students', 'foods', 'reservations', 'transactions']
	SHOW_TODAY = 'showToday'
	SHOW_STUDENT_RESERVE_TODAY = 'showStuToday'
	SHOW_LAST_10_TRANSACTIONS = 'showLast10Transactions'
	SHOW_REMAIN_FOOD = 'showRemainFood'
	ASSET_TURNOVER = 'assetTurnover'
	STUDENT_FOOD = 'studentFood'
	STUDENT_TRANSACTION = 'studentTransaction'

	def __str__(self):
		return self.value.lower()
	
class Action():
	def __init__(self, cursor) -> None:
		self.cursor = cursor

	def register(self, ID, studentID, major, birth_date, first_name, last_name, balance):
		try:

			self.cursor.execute(f"INSERT INTO students(ID, studentID, major, birth_date, first_name, last_name, balance) VALUES('{ID}', '{studentID}', '{major}', '{birth_date}', '{first_name}', '{last_name}', '{balance}')")
			ok("Student Registrated Successfully")

		except psycopg2.errors.UniqueViolation as e:
			war("national ID or studentID is already exists")

		except psycopg2.errors.CheckViolation as e:
			if str(e).find("studentid") != -1:
				war("studentID should have 7 or 8 digits")
			elif str(e).find("id") != -1:
				war("ID should have 10 digits")
			elif str(e).find("balance") != -1:
				war("balance should be positive")

		except psycopg2.errors.StringDataRightTruncation:
			war("values length of id and first_name and last_name and major should be less than 20")

		except psycopg2.errors.DatetimeFieldOverflow:
			war("value of birth date should like this format yyyy-mm-dd")

		except Exception as e:
			war(e)

	def remove(self, ID):
		self.cursor.execute(f"SELECT * FROM students WHERE ID = '{ID}'")

		if self.cursor.rowcount == 0:
			war("No students with this national ID were found")
			return
		
		data = self.cursor.fetchall()[0]
		for i in range(7):
			detail(ut.studentDetails[i], data[i])
		print()

		war("Are you sure to remove student with this ditails? [Y/n]")
		x = input()
		if x == "Y":
			self.cursor.execute(f"DELETE FROM students WHERE ID = '{ID}'")
			if self.cursor.rowcount == 1:
				ok("removed successfully")
			else:
				war("error removing student")
		else:
			war("remove operation cancelled")

	def credit(self, studentID, money):
		if int(money) <= 0:
			war("value of money should be positive")
			return
		
		self.cursor.execute(f"UPDATE students SET balance = balance + {money} WHERE studentID = '{studentID}'")
		if self.cursor.rowcount == 0:
			war("Error: studentID not found")
		else:
			ok("credit charged successfully")

	def add(self, name, date, price, inventory):
		try:
			self.cursor.execute(f"INSERT INTO foods VALUES(DEFAULT, '{name}', '{date}', '{price}', '{inventory}') RETURNING ID")
			ID = self.cursor.fetchone()[0]
			ok("food added successfully with ID = " + str(ID))
		except Exception as e:
			war(e)

	def delete(self, ID):
		try:
			self.cursor.execute(f"DELETE FROM foods WHERE ID = '{ID}' AND inventory = 0")
			if self.cursor.rowcount == 0:
				war(f"there is no food with ID '{ID}' and inventory = 0")
			else:
				ok("food with ID = " + ID + " removed successfully")
		except Exception as e:
			war(e)
	
	def checkReservePossibelity(self, studentID, foodID):
		self.cursor.execute(f"SELECT price, inventory FROM foods WHERE ID = '{foodID}'")
		if self.cursor.rowcount == 0:
			raise Exception("There is no food with ID = " + foodID)
		
		price, inventory = map(int, self.cursor.fetchone())

		self.cursor.execute(f"SELECT balance FROM students WHERE studentID = '{studentID}'")
		if self.cursor.rowcount == 0:
			raise Exception("There is no student with StudentID = " + studentID)
		
		balance = self.cursor.fetchone()[0]

		if balance < price:
			raise Exception("Your money is low")
		if inventory == 0:
			raise Exception("This food has been finished")
		
	def reserve(self, studentID, foodID):
		try:
			self.checkReservePossibelity(studentID, foodID)
			self.cursor.execute(f"INSERT INTO reservations(studentID, foodID) VALUES('{studentID}', '{foodID}') RETURNING ID")
			ID = self.cursor.fetchone()[0]
			ok("food reserved with ID = " + str(ID))
			self.reserveOpt(studentID, foodID, '-')
			self.cursor.execute(f"INSERT INTO transactions(SRCreservationID, DSTreservationID) VALUES(NULL, {ID})")
		except Exception as e:
			war(e)

	def reserveOpt(self, studentID, foodID, operand):
		self.cursor.execute(f"SELECT price FROM foods WHERE ID = '{foodID}'")
		price = self.cursor.fetchone()[0]
		self.cursor.execute(f"UPDATE students SET balance = balance {operand} {price} WHERE studentID = '{studentID}'")
		self.cursor.execute(f"UPDATE foods SET inventory = inventory {operand} 1 WHERE ID = '{foodID}'")

	def updateIsReserved(self, ID, operand):
		check = 't'
		if operand == '+':
			check = 'f'
		if ID != 'null':
			self.cursor.execute(f"UPDATE reservations SET isReserved = '{check}' WHERE ID = '{ID}'")
			self.cursor.execute(f"SELECT studentID, foodID FROM reservations WHERE ID = '{ID}'")
			studentID, foodID = self.cursor.fetchone()
			self.reserveOpt(studentID, foodID, operand)

	def checkReserveID(self, ID, name):
		x = ''
		if name == 'SRC':
			x = 'not'

		if ID != 'null':
			self.cursor.execute(f"SELECT isReserved FROM reservations WHERE ID = '{ID}'")
			if self.cursor.rowcount == 0:
				raise Exception ("Error: Cannot change reserved food (" + name + " is not found)")
			if self.cursor.fetchone()[0] == (name == 'DST'):
				raise Exception ("Error: Cannot change reserved food (" + name + " is " + x + "already reserved)")

	def setNull(self, ID):
		if ID is None or ID.casefold() == 'null':
			return 'null'
		return ID

	def change(self, SRC, DST, TIME):
		if TIME is None:
			TIME = 'DEFAULT'
		else:
			TIME = f"'{TIME}'"
		SRC = self.setNull(SRC)
		DST = self.setNull(DST)

		try:
			self.checkReserveID(SRC, 'SRC')
			self.checkReserveID(DST, 'DST')
			self.cursor.execute(f"INSERT INTO transactions VALUES({SRC}, {DST}, {TIME})")
			self.updateIsReserved(SRC, '+')
			self.updateIsReserved(DST, '-')

		except Exception as e:
			war(e)

	def deleteDB(self):
		for table in Actions.TABLE_NAMES:
			self.cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")

	def showDB(self):
		print()
		for table in Actions.TABLE_NAMES:
			cprint(table, "magenta", attrs=["bold"])
			cprint("=" * len(table), "yellow")
			self.cursor.execute(f"SELECT * FROM {table}")
			rows = self.cursor.fetchall()
			for row in rows:
				cprint(row, "cyan")
			print()
			
	def showToday(self):
		self.cursor.execute(f"CALL name_inv()")
		self.cursor.execute(f"SELECT * FROM today")
		cprint("today", "magenta", attrs=["bold"])
		cprint("=====", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row, "cyan")
		print()

	def showStudentReserveToday(self):
		self.cursor.execute(f"CALL stu_today()")
		self.cursor.execute(f"SELECT * FROM stuToday")
		cprint("stuToday", "magenta", attrs=["bold"])
		cprint("========", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row[0], "cyan")
		print()

	def showLast10Transactions(self):
		self.cursor.execute(f"CALL last10()")
		self.cursor.execute(f"SELECT * FROM last10Transactions")
		cprint("last10Transactions", "magenta", attrs=["bold"])
		cprint("==================", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row, "cyan")
		print()
	
	def showRemainfood(self):
		self.cursor.execute(f"CALL foods_remain()")
		self.cursor.execute(f"SELECT * FROM foodsRemain")
		cprint("foodsRemain", "magenta", attrs=["bold"])
		cprint("==========", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row, "cyan")
		print()

	def assetTurnover(self):
		self.cursor.execute(f"CALL asset_turnover()")
		self.cursor.execute(f"SELECT * FROM assetTurnover")
		cprint("assetTurnover", "magenta", attrs=["bold"])
		cprint("=============", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row, "cyan")
		print()

	def studentFood(self):
		self.cursor.execute(f"SELECT * FROM student_food")
		cprint("student_food", "magenta", attrs=["bold"])
		cprint("============", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row, "cyan")
		print()

	def studentTransaction(self):
		self.cursor.execute(f"SELECT * FROM student_transaction")
		cprint("student_transaction", "magenta", attrs=["bold"])
		cprint("===================", "yellow")
		rows = self.cursor.fetchall()
		for row in rows:
			cprint(row, "cyan")
		print()