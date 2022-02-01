import boto3
import json, string, random
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Creating an boto3 client representing IAM service.
    iam_client = boto3.client('iam')

    # Recieve group and user name as input

    group_name = event['GroupName']
    user_name = event['UserName']
    sender_email = event['SenderEmail']
    receiver_email = event['ReceiverEmail']

    try:
        group_response = iam_client.create_group(
            GroupName=group_name)
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Group already exists... Use the same group')
        else:
            print('Unexpected error occured while creating group... exiting from here', error)
            return 'User could not be create', error

    try:
        user = iam_client.create_user(
            UserName=user_name,
            Tags=[
                {
                    'Key': 'Owner',
                    'Value': 'Vilius'
                }
            ]
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('User already exists')
            return 'User already exists'
        else:
            print('Unexpected error occured while creating user.... exiting from here', error)
            return 'User could not be create', error

    password = random_string()
    try:
        login_profile = iam_client.create_login_profile(
            UserName=user_name,
            Password=password,
            PasswordResetRequired=True
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('login profile already exists')
        else:
            print('Unexpected error occured while creating login profile... hence cleaning up', error)
            return 'User could not be create', error
    print('User with UserName:{0} got created successfully'.format(user_name))

    # Add user to group
    add_user_to_group_res = iam_client.add_user_to_group(
        GroupName=group_name,
        UserName=user_name
    )

    # Now user got created... Sending its details via email
    ses_client = boto3.client('ses')
    sender_email = event['SenderEmail']
    receiver_email = event['ReceiverEmail']
    ses_res = ses_client.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [
                receiver_email
            ]
        },
        Message={
            'Subject': {
                'Data': 'You IAM user deatils'
            },
            'Body': {
                'Text': {
                    'Data': 'User name is : "{0}" \nOne time password is : "{1}"'.format(user_name, password) + '\nLogin link https://myawsacc.signin.aws.amazon.com/console'
                }
            }
        }
    )

    return 'User with UserName:{0} got created successfully'.format(user_name)


# This function generates random string
def random_string():
    generate_pw = ''.join([random.choice(string.ascii_letters + string.digits + string.digits) for n in range(16)])
    generated_password = ''.join(random.choice(generate_pw) for i in range(16))
    return generated_password
