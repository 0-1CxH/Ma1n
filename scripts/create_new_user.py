import argparse
from src.backend.user import UserManager
# PYTHONPATH=$(pwd) python  scripts/create_new_user.py test-common-user test-common-password 
# PYTHONPATH=$(pwd) python  scripts/create_new_user.py test-high-user test-high-password --perm_type 1 --resrc_type 1
# PYTHONPATH=$(pwd) python  scripts/create_new_user.py test-lv2-user test-lv2-password --perm_type 2 --resrc_type 1
# 

parser = argparse.ArgumentParser(description='Create a new user.')
parser.add_argument('username', type=str, help='Username for the new user.')
parser.add_argument('password', type=str, help='Password for the new user.')
parser.add_argument('--user_db_path', type=str, default="db/user_info.db", help='Path to the user database.')
parser.add_argument('--perm_type', type=int, default=0, help='Permission type for the new user.')
parser.add_argument('--resrc_type', type=int, default=0, help='Resource type for the new user.')

args = parser.parse_args()


um = UserManager(args.user_db_path)
um.add_user(
    {
        "username": args.username,
        "perm_type": args.perm_type,
        "resrc_type": args.resrc_type,
        "password": args.password
    }
)
print(um.load_user(args.username))
