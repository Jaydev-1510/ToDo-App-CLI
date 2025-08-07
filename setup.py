import os
import json
import subprocess
import sys


required_packages = [
    'colorama',
    'tabulate',
    'tqdm',
    'pyfiglet'
]

def install_packages():
  print('🔧 Installing required packages...')
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', *required_packages])
  print('✅ All required packages installed.')

def create_task_file():
  
  filename = 'ToDo_tasks.json'
  
  if not os.path.exists(filename):
    print(f'📄 Creating {filename}...')
    
    with open(filename, 'w') as f:
      json.dump([], f, indent=4)
      
    print(f'✅ {filename} created successfully.')
  
  else:
    print(f'ℹ️  {filename} already exists. Skipping creation.')

def main():
  
    install_packages()
    create_task_file()
    print('\n🚀 Setup complete! You can now run your To-Do App.\n')

if __name__ == '__main__':
    main()
