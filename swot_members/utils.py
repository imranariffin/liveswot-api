import mailjet_rest
from backend.deploy_scripts import read_from_file

username = read_from_file('mailjet_username')
password = read_from_file('mailjet_password')
client = mailjet_rest.Client(auth=(username, password), version='v3')


def send_invite_email(invitor, email):
    data = {
        'FromName': 'LiveSWOT',
        'FromEmail': 'contact@liveswot.com',
        'Subject': 'Test Email',
        'HTML-Part': ''.join([
            '<html><body>',
            '<p>Hey there!<p>',
            '<p>Your college {} has invited to contribute to a swot.</p>'.format(invitor),
            '<p>Signup <a href=\'http://localhost:3000/login/\'>here</a> to join the swot</p>',
            '<p>Cheers,</p>',
            '<p>liveSWOT team</p>',
            '</body></html>'
        ]),
        'Recipients': [{'Email': email}]
    }
    client.send.create(data)
