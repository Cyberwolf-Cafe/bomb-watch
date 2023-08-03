import requests
from datetime import datetime, timedelta


def get_faction_members(faction_id):
    api_key = 'TOILETS API'
    base_url = 'https://api.torn.com/faction/'

    # Prepare the API request URL
    url = f'{base_url}{faction_id}?selections=basic&key={api_key}'

    try:
        # Send the API request
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if data.get('error'):
            raise Exception(f"Error: {data['error']['error']}")

        # Create a dictionary of member IDs
        members_dict = {}
        for member_id, member_data in data['members'].items():
            members_dict[member_id] = member_data['name']

        return members_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_user_info(api_key, base_url, user_id):
    # Prepare the API request URL
    url = f'{base_url}{user_id}?selections=profile,timestamp,networth&key={api_key}'

    try:
        # Send the API request
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if data.get('error'):
            raise Exception(f"Error: {data['error']['error']}")

        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def check_networth_decrease(user_id, networth_data, threshold):
    networth_values = networth_data[user_id]['networth']['total']

    if len(networth_values) < 2:
        return False

    # Get nw values from the last 48 hours
    now = datetime.now()
    two_days_ago = now - timedelta(hours=48)
    relevant_networth_values = [value for timestamp, value in networth_values.items() if
                                datetime.fromtimestamp(int(timestamp)) >= two_days_ago]

    if len(relevant_networth_values) < 2:
        return False

    # Convert nw values to int
    relevant_networth_values = [int(value) for value in relevant_networth_values.values()]

    # Calculate nw difference over the last 48 hours
    networth_diff = relevant_networth_values[-1] - relevant_networth_values[0]

    return networth_diff <= -threshold

if __name__ == "__main__":
    api_key = 'TOILETS API'
    base_url = 'https://api.torn.com/faction/'

    faction_id = '20303'
    members_dict = get_faction_members(faction_id)

    if members_dict:
        print(f"Members of Faction {faction_id}:")
        for member_id, member_name in members_dict.items():
            user_info = get_user_info(api_key, base_url, member_id)

            if user_info:
                networth_decreased = check_networth_decrease(member_id, user_info, 200_000_000)
                if networth_decreased:
                    print(f"{member_name}'s net worth decreased by $200 million or more in the last 48 hours.")

    else:
        print("Failed to retrieve faction members.")
