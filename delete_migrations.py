import os

apps = ['users', 'webapp']

sql_file = './db.sqlite3'

for app in apps:
    migration_path = f'./apps/{app}/migrations/'
    for filename in os.listdir(migration_path):
        if filename.endswith('.py') and filename != '__init__.py' and sql_file:
            migration_file = os.path.join(migration_path, filename)
            os.remove(migration_file)
            os.remove(sql_file)

# Profile.objects.all().delete()
# CustomUser.objects.all().delete()