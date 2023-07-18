# Open-Table-Bot
Snipe hard to get reservations from OpenTable. The idea for this project from https://github.com/Alkaar/resy-booking-bot
# Onboarding Steps
1. Clone Repo
2. Find you're OpenTable Token by looking in the headers of the requests sent from the OpenTable client to the API
3. Add the following details at the bottom of the bot.py file: date, time, party_size, open_table_token (should be added via a .env file), resturant_id, firstName, lastName, email.
4. Install the dependencies
5. Run the project by running  ```python bot.py``` in the directory
