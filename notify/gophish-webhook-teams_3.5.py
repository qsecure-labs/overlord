import pymsteams
import sys
from flask import Flask,request,json

app = Flask(__name__)
teamsHook = '' 


def send_new_message_teams(event_type, client_name):
    """Send a Microsoft Teams Activity Card HTTP POST message to a web hook"""
    global teamsHook
    myTeamsMessage = pymsteams.connectorcard(teamsHook)
    myTeamsMessage.title("GoPhish")
    myTeamsMessage.text('[+] New Event from {}'.format(client_name))

    # create the section
    myMessageSection = pymsteams.cardsection() 
    myMessageSection.activityTitle("Event Type")
    myMessageSection.activitySubtitle(event_type)
    myTeamsMessage.addSection(myMessageSection)
    
    #send notification to Microsoft Teams
    if (myTeamsMessage.send()):
        print("New message successfully posted to Microsoft Teams")
    else:
        print("Message was not posted to Microsoft Teams.")


@app.route('/webhook',methods=['POST'])
def receive_event():
    data = request.json
    try:
        client_name = data['email'].split('@')[1]
        event_type = data["message"]
        if event_type in ["Email Opened","Clicked Link", "Submitted Data"]:
            send_new_message_teams(event_type, client_name)
    except KeyError:
        print('Debug message {}'.format(data))
    except:
        print('Unknown error - see below')
        print(sys.exc_info())

    return data
 

if __name__ == '__main__':
    app.run(debug=True, port=9999)



