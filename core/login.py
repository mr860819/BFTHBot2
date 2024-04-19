import requests
from bs4 import BeautifulSoup
from core.loadcarkeys import load_car_keys

def login_with_csrf():
    """Login to a service, handling CSRF token, cookies, and redirects.

    Args:
        url (str): The base URL of the service to login to.

    Returns:
        requests.Response: The response from the login request.

    Raises:
        ValueError: If required environment variables are not set.
        Exception: If unable to retrieve CSRF token or login fails.
    """
    session = requests.Session()
    url = "https://battleforthehill.com/login"
    # Retrieve credentials from environment variables
    data = load_car_keys()
    email = data['user']
    password = data['pass']
    if not email or not password:
        raise ValueError("LOGIN_EMAIL or LOGIN_PASSWORD environment variables are not set.")

    # Fetch the login page to get the CSRF token and cookies
     # Define initial headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    # Update the referer if one is provided
   

    login_page_response = session.get(url, headers=headers)
    if login_page_response.ok:
        soup = BeautifulSoup(login_page_response.text, 'html.parser')
        csrf_token = soup.find('input', attrs={'name': '_token'})
        if not csrf_token or 'value' not in csrf_token.attrs:
            raise Exception("CSRF token not found in login page.")
        csrf_token_value = csrf_token['value']
    else:
        raise Exception(f"Failed to fetch the login page, status code: {login_page_response.status_code}")

    # Prepare login data including the CSRF token
    login_data = {
        'email': email,
        'password': password,
        '_token': csrf_token_value,
        'remember':'on'
    }

    # Perform the login request
    login_url = url  # This might need to be updated to the specific URL for submitting the login form if different from the base URL
    response = session.post(login_url, data=login_data, headers=headers, allow_redirects=False)
    response.headers
    if response.status_code == 200 or response.status_code == 302:
        # Assuming 200 OK or 302 Found indicate a successful login
        print("Login successful.")
    elif response.status_code == 303:
        # Handle redirect after login
        redirect_url = response.headers['Location']
        redirect_response = session.get(redirect_url, headers=headers)
        if redirect_response.ok:
            print("Login successful after redirect.")
        else:
            raise Exception(f"Failed to fetch the redirect page, status code: {redirect_response.status_code}")
    else:
        # Handle unsuccessful login attempts or other errors
        raise Exception(f"Login failed, status code: {response.status_code}")

    # Handle cookies
    cookies = response.cookies
    session.cookies.update(cookies)
    print(session.cookies)

    return response, session
