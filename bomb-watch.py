import requests
import time

api_key = 'L40rkMstF9EBf6ot'

def get_faction_members(faction_id):
    base_url = 'https://api.torn.com/faction/'

    # Prepare the API request URL
    url = f'{base_url}{faction_id}?selections=basic&key={api_key}'

    # Send the API request
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if 'members' not in data:
        raise Exception(f'Expected members in response but got {data}')

    # Create a dictionary of member IDs
    members_dict = {key: val['name'] for (key,val) in data['members'].items()}

    return members_dict



def get_networth(user_id, timestamp):
    # Prepare the API request URL
    base_url = 'https://api.torn.com/user/'
    url = f'{base_url}{user_id}?selections=personalstats&timestamp={timestamp}&stat=networth&key={api_key}'
    print(url)

    try:
        # Send the API request
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if data.get('error'):
            raise Exception(f"Error: {data['error']['error']}")

        nw = data['personalstats']['networth']
        print(nw)
        return nw

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def check_networth_decrease(user_id, threshold):

    # Get nw values from the last week
    now = int(time.time())
    day = 60*60*24

    pnw = get_networth(user_id, now)
    for i in range(7):
        now -= day
        nw = get_networth(user_id, now)
        if False and (pnw - nw) <= threshold:
            return True
        pnw = nw
    return False

def main():
    faction_id = '20303'
    members_dict = get_faction_members(faction_id)

    if members_dict:
        print(f"Members of Faction {faction_id}:")
        for member_id, member_name in members_dict.items():
            if check_networth_decrease(member_id, 200e6):
                print(f"{member_name}'s net worth decreased by $200 million or more in the last week.")

    else:
        print("Failed to retrieve faction members.")

def test():
    bask = 2514476
    print(check_networth_decrease(bask, 1))

test()


