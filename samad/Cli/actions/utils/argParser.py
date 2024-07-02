import argparse
from Cli.actions.Actions import Actions
class ArgParser():
	def __init__(self):
		self._parser = argparse.ArgumentParser(description="SAMAD")
		subparsers = self._parser.add_subparsers(dest="command")

		# REGISTER
		reg_parser = subparsers.add_parser(Actions.REGISTER, help="Register new student")
		reg_parser.add_argument("-n", "--ID" , type=str, required=True, help="10 digit StudentID")
		reg_parser.add_argument("-i", "--studentID" , type=str, required=True, help="7-8 digit StudentID")
		reg_parser.add_argument("-m", "--major"     , type=str, required=True, help="Field of Study")
		reg_parser.add_argument("-b", "--birth-date", type=str, required=True, help="Birth date eg. 1402/01/08")
		reg_parser.add_argument("-f", "--first-name", type=str, required=True, help="First name")
		reg_parser.add_argument("-l", "--last-name" , type=str, required=True, help="Last name")
		reg_parser.add_argument("-c", "--balance"   , type=str, required=True, help="cash balance")

		# REMOVE
		rm_parser = subparsers.add_parser(Actions.REMOVE, help="Remove student")
		rm_parser.add_argument("ID", type=str, nargs='+', help="ID of students that you want remove")

		# INCREASE CREDIT
		ic_parser = subparsers.add_parser(Actions.INCREASE_CREDIT, help="Increase credit")
		ic_parser.add_argument("-i", "--studentID", type=str, required=True, help="StudentID")
		ic_parser.add_argument("-m", "--money", type=str, required=True, help="Money")

		# ADD FOOD
		add_parser = subparsers.add_parser(Actions.ADD_FOOD, help="Add new food")
		add_parser.add_argument("-n", "--name", 	type=str, required=True, help="Name of food")
		add_parser.add_argument("-d", "--date", 	type=str, required=True, help="lunch or dinner")
		add_parser.add_argument("-p", "--price", 	type=str, required=True, help="food's price")
		add_parser.add_argument("-i", "--inventory",type=str, required=True, help="Number of food")
		
		# DELETE FOOD
		delete_parser = subparsers.add_parser(Actions.DELETE_FOOD, help="Delete food")
		delete_parser.add_argument("ID", type=str, nargs='+', help="Ids of food that you want to delete")
		
		# RESERVE
		reserve_parser = subparsers.add_parser(Actions.RESERVE, help="Reserve Food")
		reserve_parser.add_argument("-s", "--studentID", type=str, required=True, help="StudentID of who is want to reserve food")
		reserve_parser.add_argument("-f", "--foodID", 	type=str, required=True, help="foodID that you want to reserve")

		# CHANGE
		change_parser = subparsers.add_parser(Actions.CHANGE_RESERVE, help="Change reserve")
		change_parser.add_argument("-s", "--SRCreserveID", type=str, help="source reseve ID")
		change_parser.add_argument("-d", "--DSTreserveID", type=str, help="destinaion reserve ID")
		change_parser.add_argument("-t", "--Time", type=str, nargs='?', help="time of change reserve (optional)")
		
		# DELETE DB
		delete_db_parser = subparsers.add_parser(Actions.DELETE_DB, help="Delete database")
  
		# SHOW DB
		show_db_parser = subparsers.add_parser(Actions.SHOW_DB, help="Show database")

		# SHOW TODAY
		show_today_parser = subparsers.add_parser(Actions.SHOW_TODAY, help="Show today's reserve")

		# SHOW STUDENT RESERVE TODAY
		show_today_reserve_parser = subparsers.add_parser(Actions.SHOW_STUDENT_RESERVE_TODAY, help="Show today's reserve of student")

		# SHOW LAST 10 TRANSACTIONS
		show_last_10_transactions_parser = subparsers.add_parser(Actions.SHOW_LAST_10_TRANSACTIONS, help="Show last 10 transactions")

		# SHOW REMAIN FOOD
		show_remain_food_parser = subparsers.add_parser(Actions.SHOW_REMAIN_FOOD, help="Show remain food")

		# ASSET TURNOVER
		asset_parser = subparsers.add_parser(Actions.ASSET_TURNOVER, help="Show asset turnover")

		# STUDENT FOOD
		student_food_parser = subparsers.add_parser(Actions.STUDENT_FOOD, help="show foods that student reserved")

		# STUDENT TRANSACTION
		student_transaction_parser = subparsers.add_parser(Actions.STUDENT_TRANSACTION, help="show transaction by user")

	def get_args(self):
		args =  self._parser.parse_args()
		return args
	
	@property
	def parser(self):
		return self._parser
