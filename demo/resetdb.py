"""
Reset the database with default test values
"""
import os, sys, argparse, contextlib, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netvd.settings')
django.setup()

from netvd.settings import DATABASES
from django.contrib.auth.models import User, Group

def resetDatabase():
	# Remove database file if exists
	with contextlib.suppress(FileNotFoundError):
		os.remove(DATABASES['default']['NAME'])

	# Remove migrations
	os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
	os.system('find . -path "*/migrations/*.pyc" -delete')


	# Rebuild database
	os.system('python3 manage.py makemigrations')
	os.system('python3 manage.py migrate')

def createFakeAdmin(fake):
	fakeadmin = Group.objects.get_or_create(name='FakeAdmin')
	fakeadmin = Group.objects.get(name="FakeAdmin")
	user=User.objects.create_user('admin', password=fake)
	user.groups.add(fakeadmin)
	user.save()

def createDjangoAdminUser(name, email, password):
	admin = User.objects.create_superuser(name, email, password)
	admin.save()


def main():

	parser = argparse.ArgumentParser(description="NVD demo reset script")
	parser.add_argument('-n', '--admin_name', action='store', dest='admin_name', help="Name of admin user", default='admin')
	parser.add_argument('-e', '--admin_email', action='store', dest='admin_email', help="Email of admin user", default='admin@admin.com')
	parser.add_argument('-p', '--admin_password', action='store', dest='admin_password', help="Password of admin user")
	parser.add_argument('-f', '--fakeadmin_password', action='store', dest='fakeadmin_password', help="Password of fakeadmin user")

	args = parser.parse_args()

	if not args.admin_password:
		print("[-] Error admin password is required!")
		sys.exit(1)

	if not args.fakeadmin_password:
		print("[-] Error fakeadmin password is required!")
		sys.exit(1)

	resetDatabase()
	createDjangoAdminUser(args.admin_name, args.admin_email, args.admin_password)
	createFakeAdmin(args.fakeadmin_password)


# Hook
if __name__ == "__main__":
	main()
