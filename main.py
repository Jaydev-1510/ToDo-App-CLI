import random
import json
import time
import csv
import os
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

task_file = 'ToDo-tasks.json'

#------------------------------------------------------------------------------

def load_tasks() -> list:
  '''
  Loads tasks from the ToDo-tasks.json file if exists.
  Returns an empty list if the file doesn't exist.
  '''
  
  if os.path.exists(task_file):
    with open(task_file, 'r') as f:
      return json.load(f)
    return []
  
#------------------------------------------------------------------------------

def view_tasks(tasks) -> None:
  '''
  Displays the list of tasks form the tasks list.
  Each task is shown with its own title and status complete/incomplete.
  '''
  clear_screen()
  
  if not tasks:
    print('No tasks found.')
    return
      
  print(Fore.RESET + Style.BRIGHT +'Here\'s the list of your tasks:\n')
    
  for i, task in enumerate(tasks, start=1):
    
    
    if task['done']:
      status = '✅'
      print(Fore.GREEN + f'{i}. {task['title']} [{status}]')
      
    else:
      status = '❌'
      print(Fore.RED + f'{i}. {task['title']} [{status}]')
      
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
  tasks.append({'title': title, 'done': False})
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
      removed = tasks.pop(index)
      save_tasks(tasks)
      print(f'Deleted task: {removed['title']}')
      
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
    filename = input("Enter tasks filename (default = tasks.json): ").replace(' ', '_')
    
    if filename.strip() == '':
      filename = 'tasks.json'
      
    with open(filename, "w") as f:
      json.dump(tasks, f, indent=4)
      
    print(Fore.GREEN + f'Tasks exported to {filename}')
    time.sleep(1)
    
  elif choice == 'c':   
    filename = input("Enter tasks filename (default = tasks.csv): ").replace(' ', '_')
    
    if filename.strip() == '':
      filename = 'tasks.csv'
      
    with open(filename, "w", newline='') as f:
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