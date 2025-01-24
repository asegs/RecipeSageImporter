import requests


def get_recipes_with_login():
    print("The following are absolutely not saved and are just sent to RecipeBox for authentication.")
    username = input("Enter your RecipeBox username: ")
    password = input("Enter your RecipeBox password: ")

    cookies = {
        'downloadBannerExpiry': '1824134194022',
        '_ga_Y3ESL5WS4J': 'GS1.1.1737733956.5.1.1737734481.0.0.0',
        '_ga': 'GA1.2.1829418912.1713408176',
        'downloadBannerExpiry': '1824133956411',
        '_gid': 'GA1.2.295332551.1737733957',
    }

    login_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.recipebox.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.recipebox.com/users/login',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = {
        'username': username,
        'password': password,
    }

    response = requests.post('https://www.recipebox.com/users/login', cookies=cookies, headers=login_headers, data=data,
                             allow_redirects=False)

    auth_token = response.cookies.get("authToken")

    if not auth_token:
        print("Failed to authenticate.")
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Authorization': 'Bearer ' + auth_token,
        'Origin': 'https://www.recipebox.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.recipebox.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = requests.get('https://api.recipebox.com/v1/users/recipes', headers=headers)
    return response.json()
