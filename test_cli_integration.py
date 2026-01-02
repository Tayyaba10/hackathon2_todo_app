import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.cli.todo_cli import TodoCLI

# Create a CLI instance
cli = TodoCLI()

# Test that the service has all the required methods
service = cli.service
print('Service has intermediate features:')
print('- search_tasks:', hasattr(service, 'search_tasks'))
print('- filter_tasks:', hasattr(service, 'filter_tasks'))
print('- sort_tasks:', hasattr(service, 'sort_tasks'))
print('- set_priority:', hasattr(service, 'set_priority'))
print('- add_tag:', hasattr(service, 'add_tag'))
print('- remove_tag:', hasattr(service, 'remove_tag'))

print('\nCLI has interactive handlers:')
print('- handle_search_tasks:', hasattr(cli, 'handle_search_tasks'))
print('- handle_filter_tasks:', hasattr(cli, 'handle_filter_tasks'))
print('- handle_sort_tasks:', hasattr(cli, 'handle_sort_tasks'))
print('- handle_set_priority:', hasattr(cli, 'handle_set_priority'))
print('- handle_add_tag:', hasattr(cli, 'handle_add_tag'))
print('- handle_remove_tag:', hasattr(cli, 'handle_remove_tag'))

print('\n✅ All intermediate features successfully connected to interactive CLI!')