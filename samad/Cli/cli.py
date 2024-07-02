from termcolor import cprint

from Cli.actions.utils.argParser import ArgParser
from Cli.actions.Actions import Action, Actions
from config import load_config
from connect import connect
from Cli import CreatTableCommand

class CLI():
	def __init__(self):
		self._argParser = ArgParser()
		self._args = self._argParser.get_args()
		self._parser = self._argParser.parser
		config = load_config()
		self.conn = connect(config)
		self.cursor = self.conn.cursor()
		for table in CreatTableCommand.commands:
			self.cursor.execute(table)
		self.conn.commit()
		self._action = Action(self.cursor)
	
	def execute(self):

		cprint(self._args, "yellow", attrs=["dark"])

		if self._args.command == str(Actions.REGISTER):
			self._action.register(self._args.ID ,self._args.studentID, self._args.major, self._args.birth_date, self._args.first_name, self._args.last_name, self._args.balance)
		
		elif self._args.command == str(Actions.REMOVE):
			for id in self._args.ID:
				self._action.remove(id)

		elif self._args.command == str(Actions.INCREASE_CREDIT):
			self._action.credit(self._args.studentID, self._args.money)

		elif self._args.command == str(Actions.ADD_FOOD):
			self._action.add(self._args.name, self._args.date, self._args.price, self._args.inventory)

		elif self._args.command == str(Actions.DELETE_FOOD):
			for id in self._args.ID:
				self._action.delete(id)

		elif self._args.command == str(Actions.RESERVE):
			self._action.reserve(self._args.studentID, self._args.foodID)

		elif self._args.command == str(Actions.CHANGE_RESERVE):
			self._action.change(self._args.SRCreserveID, self._args.DSTreserveID, self._args.Time)
			
		elif self._args.command == str(Actions.DELETE_DB):
			self._action.deleteDB()

		elif self._args.command == str(Actions.SHOW_DB):
			self._action.showDB()
		
		elif self._args.command == str(Actions.SHOW_TODAY):
			self._action.showToday()
		
		elif self._args.command == str(Actions.SHOW_STUDENT_RESERVE_TODAY):
			self._action.showStudentReserveToday()
		
		elif self._args.command == str(Actions.SHOW_LAST_10_TRANSACTIONS):
			self._action.showLast10Transactions()

		elif self._args.command == str(Actions.SHOW_REMAIN_FOOD):
			self._action.showRemainfood()

		elif self._args.command == str(Actions.ASSET_TURNOVER):
			self._action.assetTurnover()

		elif self._args.command == str(Actions.STUDENT_FOOD):
			self._action.studentFood()
		
		elif self._args.command == str(Actions.STUDENT_TRANSACTION):
			self._action.studentTransaction()
		
		else:
			self._parser.print_help()

		self.conn.commit()
