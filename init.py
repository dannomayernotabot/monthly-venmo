from dotenv import load_dotenv
from datetime import datetime

from utils import get_env, env_vars, get_month, Venmo, Telegram

def send_batch(members, service, amount, venmo, telegram):
  month = get_month(now)
  successfulRequests = []  
  expectedRequests = len(members)

  for friend in members:    
    id = venmo.get_user_id_by_username(friend)
    description = service + " for the month of " + month + ""    
    message = f"""Good news old sport!

I have successfully requested money from {friend}.

— Efron 🤵🏻‍♂️
    """
    success = venmo.request_money(id, amount, description, telegram.send_message(message))
    if success:
      successfulRequests.append(success)

  if len(successfulRequests) == expectedRequests:
    print("✅ Ran script successfully and sent " + str(expectedRequests) + " Venmo requests.")
  else:
    print("❌ Something went wrong. Only sent " + str(len(successfulRequests)) + "/" + str(expectedRequests) + " venmo requests.")



def main(now):
  """
  The main function which initiates the script.
  """

  load_dotenv()  # take environment variables from .env.
  actualVars = []
  for var in env_vars:
    actualVars.append(get_env(var))

  access_token, chat_id, bot_token, bay_club_members, spotify_members = actualVars

  venmo = Venmo(access_token)
  telegram = Telegram(bot_token, chat_id)

  send_batch(bay_club_members.split(','), 'Bay Club Membership', 103, venmo, telegram)
  send_batch(spotify_members.split(','), 'Spotify', 5.34, venmo, telegram)
  

now = datetime.now()
main(now)
