# streamalert is a reddit bot that alerts you when a Twitch streamer in
# your list is using undesirable words in their stream title.
# Made with Python 3.4.0 by /u/twistitup

import praw, oaux, requests, time, json

# List of targeted streamers by their twitch ids.
STREAMERS = ["nl_kripp", "popskyy"]
# List of words you want to look out for.
BAD_WORDS = ["fun", "terraria"]
# Twitch app client id, don't worry about it.
CLIENT_ID = 'k0omm8abqfbeqk073wqnkwhcg98z7ew'

# The below time values should not be changed without
# previous thought. Always keep in mind not to send too
# many requests to Twitch's servers. Otherwise the bot will
# get IP banned from using the API.

# Time in between each channel scan.
TIME_BETWEEN_SCANS = 10
# Time in between each iteration. That is, time waited
# after all streamers are scanned until repeating the process.
TIME_BETWEEN_ITERATIONS = 300

def searchAndAlert():
    for streamer in STREAMERS:
        url = "https://api.twitch.tv/kraken/channels/" + streamer
        client_id = {'client_id': CLIENT_ID}
        channel = requests.get(url, headers = client_id)
        json = channel.json()
        streamTitle = json["status"]
        for word in BAD_WORDS:
            if word in str.lower(streamTitle):
                # Recipient of alert message, without /u/. If recipient is
                # a subreddit, add /r/
                recipient = "/r/LighthouseSherpas"
                # Subject of alert message.
                subject = "Alert! Streamer using bad word!"
                # Content of alert message.
                message = (
                    streamer + " has included the word " + word + " in his/her"
                    " stream title.\n\nThe title is: \"" + streamTitle +
                    "\".\n\nHere is a link to the stream. "
                    "http://www.twitch.tv/" + streamer)
                r.send_message(recipient, subject, message)
                print(message)
                print("Modmail has been sent.\n")
                break
        time.sleep(TIME_BETWEEN_SCANS)
        
if __name__ == "__main__":
    r = oaux.login()
    while True:
        try:
            searchAndAlert()
            time.sleep(TIME_BETWEEN_ITERATIONS)
        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except Exception as e:
            print("Something bad happened!", e)
            traceback.print_exc()
            print("Waiting 60 seconds.")
            time.sleep(60)
