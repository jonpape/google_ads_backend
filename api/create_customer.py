import os
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# These will come from the frontend
# refresh_token = '1//06p0agHdIYOviCgYIARAAGAYSNwF-L9Ir39B3AqLvuVUU4p1oUhDqiM_ikxYW0tCVBsqih7xew8DVmSgBtu_WfzItBaPyl5tNDjI'
# account_name = 'testing2'
# currency = 'USD'
# time_zone = 'America/New_York'
# email_address = 'fblascogarma@gmail.com'

# """
# Possible access role of a user. We are going to give users ADMIN access for the account created for them.
#         UNSPECIFIED = 0
#         UNKNOWN = 1
#         ADMIN = 2
#         STANDARD = 3
#         READ_ONLY = 4
#         EMAIL_ONLY = 5
# """
# access_role = 'ADMIN'

def create_client_customer (
    refresh_token, 
    account_name, 
    currency, 
    time_zone, 
    email_address):
    
    try:

        # Configurations
        GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
        GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
        GOOGLE_DEVELOPER_TOKEN = os.environ.get("GOOGLE_DEVELOPER_TOKEN", None)
        GOOGLE_LOGIN_CUSTOMER_ID = os.environ.get("GOOGLE_LOGIN_CUSTOMER_ID", None)

        # Configure using dict (the refresh token will be a dynamic value)
        credentials = {
        "developer_token": GOOGLE_DEVELOPER_TOKEN,
        "refresh_token": refresh_token,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "login_customer_id": GOOGLE_LOGIN_CUSTOMER_ID}

        client = GoogleAdsClient.load_from_dict(credentials)

        '''
        Step 1. Create a Google Ads account
        '''

        customer_service = client.get_service("CustomerService")

        customer = client.get_type("Customer")

        # now = datetime.today().strftime("%Y%m%d %H:%M:%S")

        customer.descriptive_name = account_name
        # customer.descriptive_name = f"Account created with CustomerService on {now}"
        # For a list of valid currency codes and time zones see this documentation:
        # https://developers.google.com/google-ads/api/reference/data/codes-formats
        customer.currency_code = currency
        # customer.currency_code = "USD"
        customer.time_zone = time_zone
        # customer.time_zone = "America/New_York"
        # The below values are optional. For more information about URL
        # options see: https://support.google.com/google-ads/answer/6305348
        customer.tracking_url_template = "{lpurl}?device={device}"
        customer.final_url_suffix = (
            "keyword={keyword}&matchtype={matchtype}" "&adgroupid={adgroupid}"
        )

        response = customer_service.create_customer_client(
            customer_id=GOOGLE_LOGIN_CUSTOMER_ID, customer_client=customer
        )
        print(
            f'Customer created with resource name "{response.resource_name}" '
            f'under manager account with ID "{GOOGLE_LOGIN_CUSTOMER_ID}".'
        )

        resource_name = response.resource_name
        customer_id = resource_name.split('/')[1]
        print('customer_id of newly created account is '+customer_id)

        '''
        Step 2. Send email to user's email with invitation they need to accept manually.

        There is a possibility of handling this process differently by 
        creating a link (field name invitation_link of the CustomerService response) for 
        inviting user to access the created customer, but you need to
        contact Google and ask to be added to the corresponding allowlist.
        '''
        service = client.get_service("CustomerUserAccessInvitationService")
        # [START invite_user_with_access_role]
        invitation_operation = client.get_type(
            "CustomerUserAccessInvitationOperation"
        )
        invitation = invitation_operation.create
        invitation.email_address = email_address
        invitation.access_role = client.enums.AccessRoleEnum['ADMIN'].value

        response = service.mutate_customer_user_access_invitation(
            customer_id=customer_id, operation=invitation_operation
        )
        print(
            "Customer user access invitation was sent for "
            f"customer ID: '{customer_id}', "
            f"email address {email_address}, and "
            f"access role ADMIN. The invitation resource name is: "
            f"{response.result.resource_name}"
        )

        # created_account_info = {
        #     'customer_id': customer_id,
        #     'email_address': email_address,
        #     'account_name': account_name,
        #     'refresh_token': refresh_token

        # }

        return customer_id

    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)