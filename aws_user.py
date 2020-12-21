import random
import string
import boto3

print("Enter user's email address")
entered_username = input()
print("Enter Group to which you want to add created user")
entered_group = input()
splitted_username = entered_username.split('@')[0]

print("User's login to the portal: " + splitted_username)


iam = boto3.resource('iam') #using resource representing IAM
iam_client = boto3.client('iam')

def create_user(user_name):
    iam.create_user(
        UserName=user_name
    )
    
def set_user_password(user_name):
    generate_pw = ''.join([random.choice(string.ascii_letters + string.digits + string.digits) for n in range(16)])
    generated_password = ''.join(random.choice(generate_pw) for i in range(16))
    iam_client.create_login_profile(
        UserName=user_name,
        Password=generated_password,
        PasswordResetRequired=True
        )
    print("User's password to the portal: " + generated_password)   

def add_to_group(user_name,group):
    group = iam.Group(group) # Name of group
    group.add_user(
    UserName=user_name #name of user
    )

create_user(splitted_username)
add_to_group(splitted_username,entered_group)
set_user_password(splitted_username)