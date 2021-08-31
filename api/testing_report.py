import os

from google.ads.googleads.client import GoogleAdsClient

# Configurations
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DEVELOPER_TOKEN = os.environ.get("GOOGLE_DEVELOPER_TOKEN", None)
GOOGLE_LOGIN_CUSTOMER_ID = os.environ.get("GOOGLE_LOGIN_CUSTOMER_ID", None)
GOOGLE_REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", None)
refresh_token = GOOGLE_REFRESH_TOKEN
customer_id = '4037974191'

date_range = "ALL_TIME"

# Configure using dict (the refresh token will be a dynamic value)
credentials = {
"developer_token": GOOGLE_DEVELOPER_TOKEN,
"refresh_token": refresh_token,
"client_id": GOOGLE_CLIENT_ID,
"client_secret": GOOGLE_CLIENT_SECRET,
"login_customer_id": GOOGLE_LOGIN_CUSTOMER_ID}

googleads_client = GoogleAdsClient.load_from_dict(credentials)

ga_service = googleads_client.get_service("GoogleAdsService")

# date selected by user on UI
date_range = date_range

if date_range == "ALL_TIME":
    query = """
    SELECT 
        campaign.id, 
        campaign.name, 
        campaign_budget.amount_micros, 
        campaign.status, 
        campaign.start_date, 
        campaign.advertising_channel_sub_type, 
        metrics.average_cpc, 
        metrics.average_cpm, 
        metrics.clicks, 
        metrics.interactions, 
        metrics.interaction_rate, 
        metrics.impressions, 
        metrics.ctr, 
        metrics.all_conversions, 
        metrics.all_conversions_value, 
        metrics.cost_micros, 
        metrics.cost_per_all_conversions
    FROM campaign
    ORDER BY campaign.id"""
else: query = ('SELECT campaign.id, campaign.name, '
        'campaign_budget.amount_micros, '
        'campaign.status, '
        'campaign.start_date, '
        'campaign.advertising_channel_sub_type, '
        'metrics.average_cpc, '
        'metrics.average_cpm, '
        'metrics.clicks, '
        'metrics.interactions, '
        'metrics.interaction_rate, '
        'metrics.impressions, '
        'metrics.ctr, '
        'metrics.all_conversions, '
        'metrics.all_conversions_value, '
        'metrics.cost_micros, '
        'metrics.cost_per_all_conversions '
    'FROM campaign '
    'WHERE segments.date DURING '+ date_range + ' '
    'ORDER BY campaign.id')



# Issues a search request using streaming.
response = ga_service.search_stream(customer_id=customer_id, query=query)

campaign_data = []

for batch in response:
    for row in batch.results:

        # get campaign status name
        if row.campaign.status == 0:
            campaign_status = "Unspecified"
        else: 
            if row.campaign.status == 1:
                campaign_status = "Unknown"
            else:
                if row.campaign.status == 2:
                    campaign_status = "Active"
                else:
                    if row.campaign.status == 3:
                        campaign_status = "Paused"
                    else:
                        if row.campaign.status == 4:
                            campaign_status = "Removed"

        # get campaign type name
        if row.campaign.advertising_channel_sub_type == 0:
            campaign_type = "Unspecified"
        else:
            if row.campaign.advertising_channel_sub_type == 1:
                campaign_type = "Unknown"
            else:
                if row.campaign.advertising_channel_sub_type == 2:
                    campaign_type = "Mobile app for Search"
                else:
                    if row.campaign.advertising_channel_sub_type == 3:
                        campaign_type = "Mobile app for Display"
                    else:
                        if row.campaign.advertising_channel_sub_type == 4:
                            campaign_type = "AdWords Express for Search"
                        else:
                            if row.campaign.advertising_channel_sub_type == 5:
                                campaign_type = "AdWords Express for Display"
                            else:
                                if row.campaign.advertising_channel_sub_type == 6:
                                    campaign_type = "Smart Shopping"
                                else:
                                    if row.campaign.advertising_channel_sub_type == 7:
                                        campaign_type = "Gmail Ad"
                                    else:
                                        if row.campaign.advertising_channel_sub_type == 8:
                                            campaign_type = "Smart Display"
                                        else:
                                            if row.campaign.advertising_channel_sub_type == 9:
                                                campaign_type = "Video Outstream"
                                            else:
                                                if row.campaign.advertising_channel_sub_type == 10:
                                                    campaign_type = "Video TrueView for Action"
                                                else:
                                                    if row.campaign.advertising_channel_sub_type == 11:
                                                        campaign_type = "Non-skippable Video"
                                                    else:
                                                        if row.campaign.advertising_channel_sub_type == 12:
                                                            campaign_type = "App"
                                                        else:
                                                            if row.campaign.advertising_channel_sub_type == 13:
                                                                campaign_type = "App for Engagement"
                                                            else:
                                                                if row.campaign.advertising_channel_sub_type == 14:
                                                                    campaign_type = "Local"
                                                                else:
                                                                    if row.campaign.advertising_channel_sub_type == 15:
                                                                        campaign_type = "Shopping Comparison Listing"
                                                                    else:
                                                                        if row.campaign.advertising_channel_sub_type == 16:
                                                                            campaign_type = "Smart"
                                                                        else:
                                                                            if row.campaign.advertising_channel_sub_type == 17:
                                                                                campaign_type = "Sequence Video Ads"
            
        # to solve the error of conv rate if there are zero conversions
        if row.metrics.interactions == 0:
            conv_rate = 0
        else:
            conv_rate = round(((row.metrics.all_conversions/row.metrics.interactions))*100, 2)

        
        data = {}
        data["campaign_id"] = row.campaign.id
        data["campaign_name"] = row.campaign.name
        data["campaign_budget"] = round((row.campaign_budget.amount_micros/1000000), 2)
        data["start_date"] = row.campaign.start_date
        data["status"] = campaign_status
        data["campaign_type"] = campaign_type
        data["impressions"] = row.metrics.impressions
        data["cpc"] = round((row.metrics.average_cpc/1000000),2)
        data["cpm"] = round((row.metrics.average_cpm/1000000),2)
        data["clicks"] = row.metrics.clicks
        data["interactions"] = row.metrics.interactions
        data["interaction_rate"] = round((row.metrics.interaction_rate)*100, 2)
        data["ctr"] = round(row.metrics.ctr, 2)
        data["conv"] = round(row.metrics.all_conversions, 0)
        data["conv_value"] = round(row.metrics.all_conversions_value, 0)
        data["cost"] = round((row.metrics.cost_micros/1000000), 0)
        data["cost_per_conv"] = round((row.metrics.cost_per_all_conversions/1000000), 2)
        data["conv_rate"] = conv_rate
        campaign_data.append(data)

    

print(campaign_data)