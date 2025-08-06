from datetime import datetime
from tabulate import tabulate
import random
import json
import time
import csv
import os
import re

with open('todo-tasks.json', 'r') as f:
    todo_list = json.load(f)

# Function to colorize rows
def colorize(task): 
  ...

#-------------------------------------------------------------------------------

def clear_screen():
  '''
  Clears the output screen.
  Uses 'cls' for Windows and 'clear' for Unix-like systems.
  '''
  
  os.system('cls' if os.name == 'nt' else 'clear')

#------------------------------------------------------------------------------

try:
  
  from colorama import Fore, Style
  from tqdm import tqdm
  import pyfiglet
  ascii_banner = pyfiglet.figlet_format('ToDo App')
  
except ImportError:
  acci_banner = 'Welcome to the ToDo App'

#------------------------------------------------------------------------------

re_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
task_file = './ToDo-tasks.json'

#------------------------------------------------------------------------------

def load_tasks() -> list:
  '''
  Loads tasks from the ToDo-tasks.json file if exists.
  Returns an empty list if the file doesn't exist.
  '''
  
  if os.path.exists(task_file):
    with open(task_file, 'r') as f:
      loaded_tasks = json.load(f)
      return loaded_tasks
  
  else:
    return []
  
#------------------------------------------------------------------------------
def view_tasks(tasks) -> None:
  '''
  Displays the list of tasks in a colored table with serial numbers.
  Tasks are color-coded based on completion and priority.
  '''
  clear_screen()

  if not tasks:
    print(Fore.YELLOW + 'No tasks found.')
    return

  print(Fore.CYAN + Style.BRIGHT + "Here's the list of your tasks:\n")

  table_data = []
  for i, task in enumerate(tasks, start=1):

    status_text = "Completed" if task.get("done") else "Pending"
    status_color = Fore.GREEN if task.get("done") else Fore.RED

    priority = task.get("priority", "Low").lower()
    title = task.get("title", "")

    if priority == "high":
      title_colored = Fore.RED + title
    elif priority == "medium":
      title_colored = Fore.YELLOW + title
    elif priority == "low":
      title_colored = Fore.BLUE + title
    else:
      title_colored = Fore.WHITE + title

    due = task.get("due") if task.get("due") else "-"

    table_data.append([
      i,
      title_colored,
      status_color + status_text,
      due,
      task.get("priority", "Low")
    ])

  headers = ["Sr. No", "Task", "Status", "Due Date", "Priority"]
  print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
  print(Style.RESET_ALL)
        
#------------------------------------------------------------------------------

def save_tasks(tasks) -> None:
  '''
  Saves the modified tasks list to the ToDo-tasks.json file.
  '''
  
  with open(task_file, 'w') as file:
    json.dump(tasks, file, indent=4)
  
#------------------------------------------------------------------------------

def add_task(tasks) -> None:
  '''
  Adds a new task to the tasks list.
  Asks the user for the task and appends it to the list.
  Also, saves the updated tasks list to the ToDo-tasks.json file.
  '''
  clear_screen()
  
  title = input(Fore.LIGHTWHITE_EX + 'Enter task you wanna add: ')
  due_date = input(Fore.LIGHTWHITE_EX + '(OPTIONAL) Enter task due date (DD.MM.YYYY) or enter number of days to add to current date: ')
  priority = input(Fore.LIGHTWHITE_EX + '(OPTIONAL) Enter task priority - low[l], medium[m], high[h] (default = low): ').lower()   
      
  if not re.match(re_pattern, due_date):
    
    if due_date.isdigit():
      due_date = datetime.now().date().split('-')[2].int() + int(due_date)
      
    else:
      due_date = None
    
  if priority == 'm':
    priority = 'Medium' 
    
  elif priority == 'h':
    priority = 'High' 
    
  else: 
    priority = 'Low'
    
  tasks.append({'title': title, 'done': False, 'due': due_date, 'priority': priority})
  save_tasks(tasks)
  print(Fore.YELLOW + 'Task added.')
  
#------------------------------------------------------------------------------

def complete_task(tasks):
  '''
  Marks a selected task as completed.
  '''
  
  view_tasks(tasks)
  
  try:
    
    index = int(input(Fore.LIGHTWHITE_EX + 'Enter task number to complete: ')) - 1
    
    if 0 <= index < len(tasks):
      tasks[index]['done'] = True
      save_tasks(tasks)
      print(Fore.GREEN + 'Task marked as completed ✅.')
      time.sleep(1)
      view_tasks(tasks)
      input('\nPress enter to continue...')

    else:
      print(Fore.RED + 'Invalid task number.')
      
  except ValueError:
    print(Fore.RED + 'Please enter a valid number.')
      
#------------------------------------------------------------------------------

def delete_task(tasks):
  
  view_tasks(tasks)
  
  try:
    index = int(input('Enter task number to delete: ')) - 1
    
    if 0 <= index < len(tasks):
      sure = input(f'Are you sure you want to delete task {index + 1} \'{tasks[index]['title']}\'? (y/n): ').lower()
      if sure == 'y':
        remove = tasks.pop(index)
        save_tasks(tasks)
        print(f'Deleted task: {remove['title']}')
      else:
        print('Task deletion cancelled.')
      
    else:
      print('Invalid task number.')
  
  except ValueError:
    print('Please enter a valid number.')  
    
#------------------------------------------------------------------------------

def export_tasks(tasks):
  
  if not tasks:
    print('No tasks to export.')
    return
  
  choice = input('Export to CSV (c) or JSON (j)? ').lower()
  
  if choice == 'j':
    filename = input('Enter tasks filename (default = tasks.json): ').replace(' ', '_')
    
    if filename.strip() == '':
      filename = 'tasks.json'
      
    with open(filename+'.json', 'w') as f:
      json.dump(tasks, f, indent=4)
      
    print(Fore.GREEN + f'Tasks exported to {filename}')
    time.sleep(1)
    
  elif choice == 'c':   
    filename = input('Enter tasks filename (default = tasks.csv): ').replace(' ', '_')
    
    if filename.strip() == '':
      filename = 'tasks.csv'
      
    with open(filename+'.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['Title', 'Done'])
      
      for task in tasks:
        writer.writerow([task['title'], task['done']])
      
    print(Fore.GREEN + f'Tasks exported to {filename}')
    time.sleep(1)
    
#------------------------------------------------------------------------------

def main() -> None:
  
  tasks = load_tasks()
    
  try:
    print(Fore.CYAN + ascii_banner)
    
    for i in tqdm(range(100)):
      time.sleep(random.uniform(0.001, 0.01))
  except:
    print(acci_banner)
    
  while True:
    
    clear_screen()
    colorize(tasks)
    print(Style.RESET_ALL + '''  
--- To-Do App Modes ---

1. View Tasks
2. Add Task
3. Complete Task
4. Delete Task
5. Export Tasks
0. Exit

------------------------         
         ''')
    
    choice = input(Style.BRIGHT + 'Please enter the number for your selected mode: ')
    
    if choice == '1':
      view_tasks(tasks)
      input('Press enter to continue...')
      
    elif choice == '2':
      add_task(tasks)
      
    elif choice == '3':
      complete_task(tasks)
      
    elif choice == '4':
      delete_task(tasks)
    
    elif choice == '5':
      export_tasks(tasks)
      
    elif choice == '0':
      print(Fore.GREEN + 'Thank you for using the ToDo app. Have a nice day!')
      print(Style.RESET_ALL)
      break
    
    else:
      print(Fore.LIGHTRED_EX + 'Please enter a number between 0 and 4.')
    
#------------------------------------------------------------------------------

if __name__ == '__main__':
  main()
  
#==============================================================================