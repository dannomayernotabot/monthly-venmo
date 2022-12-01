import os
from time import sleep
from venmo_api import Client, PaymentPrivacy
from notifiers import get_notifier

def get_env(env):
  """
  Verfies that an environment variable exists
  and returns it.

  Exits script if not found.
  """
  if os.getenv(env):
      print(f"✅ {env} is available in the environment.")
      return os.getenv(env)
  else:
      print(f"❌ Can't find {env} in environment.")
      print("  Exiting script. Please add and run again!")
      quit()

env_vars = ["VENMO_ACCESS_TOKEN", "TELEGRAM_CHAT_ID", "TELEGRAM_BOT_TOKEN", "BAY_CLUB_MEMBERS", "SPOTIFY_MEMBERS"]

def verify_env_vars(vars, numOfExpected):
  """
  Verifies the list of vars are defined in the environment.
  """

  availableEnvVars = []

  for var in vars:
    # If it returns the env, which would be True
    # then we know it's available
    if get_env(var):
        availableEnvVars.append(var)

  if len(availableEnvVars) == numOfExpected:
    return True
  else:
    # This will technically never run
    # because if one doesn't exist, then get_env quits
    # but adding here for posterity
    return False

def get_env_vars(vars):
    """
    Returns an array of the vars after getting them
    """

    allVars = []
    for var in vars:
        allVars.append(os.getenv(var))

    return allVars

def get_month(now):
    """
    Returns the current month.
    Example: April
    """

    month = now.strftime("%B")
    return month

def exponential_backoff_retry(timeout, attempt, attempts_remaining, request, args):    
    if attempts_remaining == 0:
        print('zero attempts remaining, aborting request')
        return False
    try:
        result = request(*args)
        return result
    except Exception as e:
        print('Request failed due to error. This request has failed ' + str(attempt) + ' times.')
        print(e)
        print('Retrying request in ' + str(timeout) + " seconds")
        sleep(timeout)
        return exponential_backoff_retry(attempt*attempt, attempt+1, attempts_remaining-1, request, args)

class Venmo:
    def __init__(self, access_token):
        self.client = Client(access_token=access_token)

    def get_user_id_by_username(self, username):                
        user = exponential_backoff_retry(            
            1,
            1,
            5,
            self.client.user.get_user_by_username,
            [username],
        )
        if (user):
            return user.id
        else:
            print("ERROR: user did not comeback. Check username.")
            return None

    def request_money(self, id, amount, description):
        # Returns a boolean: true if successfully requested
        return exponential_backoff_retry(            
            1,
            1,
            5,
            self.client.payment.request_money,
            [amount, description, id, PaymentPrivacy.PRIVATE, None])

class Telegram:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.client = get_notifier('telegram')

    def send_message(self, message):
        self.client.notify(message=message, token=self.bot_token, chat_id=self.chat_id)
