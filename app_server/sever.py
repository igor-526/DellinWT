from flask import Flask
from view_contacts import view_contacts_rules
from view_timejournal import view_timejournal_rules
from view_fueljournal import view_fueljournal_rules
from view_turnoverjournal import view_turnoverjournal_rules
from view_users import view_users_rules
from auth import view_auth_rules

app = Flask(__name__)
view_contacts_rules(app)
view_timejournal_rules(app)
view_fueljournal_rules(app)
view_turnoverjournal_rules(app)
view_users_rules(app)
view_auth_rules(app)
