"""
TechDegree: Python Web Developer
Project 3: work log
Date: Oct 2018
"""


import re
import csv
from datetime import datetime


def add_entry(task, minutes, notes, filename = 'work_log.csv'):
	"""
	A help function to write task assoicated info into a csv log
	arg: task, string, the name of a task 
	     minutes, int or decimal, minutes taken to complete a task 
	     notes, string, optional notes for the task
	     filename, a string for csv log file name
	return: nothing, just open the file and add an entry
	"""
	with open(filename, 'a', newline = '') as csvfile:
		fieldnames = ['Created_Date', 'Task_Name', 'Time_Taken', 'Notes']
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

		writer.writerow({'Created_Date': datetime.now().strftime('%Y-%m-%d'),
						 'Task_Name': task_name,
						 'Time_Taken': minute_used,
						 'Notes': notes})


def print_entry(row, idx):
	"""
	a help function to print log entry 
	arg: row, a csv row object
	     idx, an integer
	return: does not return anything, just print
	"""
	print('\nfound matched entry {}'.format(idx))
	print('  Date: {}'.format(row['Created_Date']))
	print('  Task name: {}'.format(row['Task_Name']))
	print('  Time spent: {}'.format(row['Time_Taken']))
	print('  Notes: {}'.format(row['Notes']))



if __name__ == '__main__':

	# check if the log file is existed
	try:
		csvfile = open('work_log.csv', 'r')

	except FileNotFoundError:
		with open('work_log.csv', 'w', newline = '') as csvfile:
			fieldnames = ['Created_Date', 'Task_Name', 'Time_Taken', 'Notes']
			writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
			writer.writeheader()  

			print('This is a brand new log file, please start to add entries\n')

			task_name = input('Task name: ')
			minute_used = input('How many minutes did you take to complete the task? ')
			notes = input('Any additional notes you would like to provide? ')

			if task_name:
				add_entry(task_name, minute_used, notes)
			else:
				print('\nThe log file is still empty. You are able to add new entries but nothing to lookup\n')


	else: 
		csvfile.close()


	# start to add or search
	while True:
		print('Are you going to add new entry or lookup previous entries?\n Enter "1" to add\n Enter "2" to search\n')

		choice1 = input('Please select [1 or 2]: ')

		if choice1 == str(1):

			# this while loop helps control multiple entry addition by user's choice
			while True:
				print('\nGreat! let us add a new entry:\n')

				while True:
					task_name = input('Task name: ')
					if len(task_name) == 0:
						print('\nTask name cannot be empty, please try again and enter a valid name\n')
						continue
					else: 
						break
				
				while True:
					try:
						minute_used = float(input('How many minutes did you take to complete the task? '))
						break
					except ValueError:
						print('\nminutes should be integers or decimals, please try again')
						continue

				notes = input('Any additional notes you would like to provide? ')

				add_entry(task_name, minute_used, notes)

				# check for additional entry or not 
				add_more = input('A new task is created. Would you like to do add more [Y / N]?: ')
				if add_more.lower() == 'y':
					continue
				else:
					print('\nGood-Bye\n')
					break


			break

		elif choice1 == str(2):

			# this while loop gives a control on valid vs invalid input
			while True:
				print('\nAll right, what are you looking for?\n')
				print('\n Enter "1" to find by date')
				print('\n Enter "2" to find by time (minutes) spent')
				print('\n Enter "3" to find by exact search from task name or notes')
				print('\n Enter "4" to find by pattern from task name or notes\n')

				choice2 = input('How would you like to search? [1, 2, 3, or 4]: ')

				if choice2 == str(1):
					# open the csv log file and find all dates
					set_dates = set()
					with open('work_log.csv', newline = '') as csvfile:
						reader = csv.DictReader(csvfile)
						for row in reader:
							set_dates.add(row['Created_Date'])

					if len(set_dates) != 0:

						# this while loop gives a control on valid vs invalid input
						while True:

							print('Here is the list of dates to choose from: {}'.format(list(set_dates)))
							select_date = input('Please enter task created date from the list above: ')

							if select_date in set_dates:
								with open('work_log.csv', newline = '') as csvfile:
									reader = csv.DictReader(csvfile)
									
									idx = 1   # create a pointer
									# iterate each row to find the entries with matching date
									for row in reader:
										if row['Created_Date'] == select_date:
											print_entry(row, idx)
											idx += 1
								break
						    	
							else:
								print('Invalid selection, please choose again!')
								break

					else:
						print('\nThe log file is empty and it is not ready for lookup by date. Please restart the program and add entries first\n')
						break
						


				elif choice2 == str(2):
					try:
						minute_select = float(input('Please enter minutes used approximately to complete the task: '))
					except ValueError:
						print('\nWrong type of value, has to be integers or decimals. Back to main menueand try again\n')
						continue

					with open('work_log.csv', newline = '') as csvfile:
						reader = csv.DictReader(csvfile)

						idx = 1  # create a pointer
						for row in reader: 
							if minute_select == float(row['Time_Taken']):
								print_entry(row, idx)
								idx += 1

						# if pointer is not updated, meaning there is no match
						if idx == 1:
							print('\nUnfortunately, there is no match in task name or notes of any entry\n')
					

				elif choice2 == str(3):
					exact_search = input('Please enter the exact word or phrase for task name or notes: ')

					with open('work_log.csv', newline = '') as csvfile:
						reader = csv.DictReader(csvfile)

						idx = 1  # create a pointer
						for row in reader: 
							if exact_search in row['Task_Name'] or exact_search in row['Notes']:
								print_entry(row, idx)
								idx += 1  # update the pointer

						# if pointer is not updated, meaning there is no match
						if idx == 1:
							print('\nUnfortunately, there is no match in task name or notes of any entry\n')
					

				elif choice2 == str(4):
					regex = input('Please enter the regex pattern for search: ')

					with open('work_log.csv', newline = '') as csvfile:
						reader = csv.DictReader(csvfile)

						idx = 1  # create a pointer
						for row in reader:
							if re.search(regex, row['Task_Name']) or re.search(regex, row['Notes']):
								print_entry(row, idx)
								idx += 1  # update the pointer

						# if pointer is not updated, meaning there is no match
						if idx == 1:
							print('\nUnfortunately, there is no match in task name or notes of any entry\n')
			

				else:
					print('\nInvalid selection, please select again')

					continue

				# check if more lookup is desired
				search_more = input('Would you like to do more lookup [Y / N]?: ')
				if search_more.lower() == 'y':
					continue

				else:
					print('\nGood-Bye\n')
					break

			break

		else:
			print('\nInvalid selection, please select "1" or "2"\n')

			continue




