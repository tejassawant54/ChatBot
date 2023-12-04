# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
# import psycopg2
# import sqlite3
from sqlalchemy import select, create_engine, Table, Column, Integer, String, MetaData
import sqlalchemy as db

# conn = sqlite3.connect('/mnt/nvme1n1p2/vamsik1211/Data/FreeLancing-Projects/KaranProjects/ChatBot/debug_data/database_sqlite/sqlite.db')

# engine = create_engine('sqlite:////mnt/nvme1n1p2/vamsik1211/Data/FreeLancing-Projects/KaranProjects/ChatBot/debug_data/database_sqlite/sqlite.db', echo=True)
# conn = engine.connect()

engine = db.create_engine('sqlite:////mnt/nvme1n1p2/vamsik1211/Data/FreeLancing-Projects/KaranProjects/ChatBot/debug_data/database_sqlite/uid.db')
conn = engine.connect()

metadata = db.MetaData()



class ValidateLoginForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_login_form"
    
    def validate_AgencyID(self, value, dispatcher, tracker, domain):

        table = db.Table('uid', metadata, autoload=True, autoload_with=engine)
        stmt = db.select([table.columns.agency_id]).where(table.columns.agency_id == value)

        results = conn.execute(stmt).fetchall()

        if results:
            print("Valid Agency ID")
            return {"AgencyID": value}
        else:
            print("Invalid Agency ID")
            dispatcher.utter_message("Invalid Agency ID. Please try again.")
            return {"AgencyID": None}

        # if value == "5689975":
        #     print("Valid Agency ID")
        #     return {"AgencyID": value}
        # else:
        #     print("Invalid Agency ID")
        #     dispatcher.utter_message("Invalid Agency ID. Please try again.")
        #     return {"AgencyID": None}

    def validate_Password(self, value, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict):

        value = str(value)
        agency_id = tracker.get_slot("AgencyID")

        table = db.Table('uid', metadata, autoload=True, autoload_with=engine)
        stmt = db.select([table.columns.agency_id]).where(table.columns.agency_id == agency_id, table.columns.password == value)

        results = conn.execute(stmt).fetchall()

        if results:
            print("Valid Password")
            dispatcher.utter_message("Login Successful")

            return {"Password": value, "login_status": True}
        else:
            print("Invalid Password")
            dispatcher.utter_message("Invalid Password. Please try again.")
            return {"Password": None}

        # if value == "123456":
        #     print("Valid Password")
        #     return {"Password": value}
        # else:
        #     print("Invalid Password")
        #     dispatcher.utter_message("Invalid Password. Please try again.")
        #     return {"Password": None}

class ConversartionReset(Action):
    
        def name(self) -> Text:
            return "action_conversation_reset"
        
        def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict):
            return [AllSlotsReset()]

class PopulateAgencyNameAction(Action):
    def name(self) -> Text:
        return "action_populate_agency_name"
    
    def run(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict):

        agency_id = tracker.get_slot("AgencyID")

        table = db.Table('user', metadata, autoload=True, autoload_with=engine)

        stmt = db.select([table.columns.agency_name]).where(table.columns.agency_id == agency_id)

        results = conn.execute(stmt).fetchone()

        if results:
            print("Setting Agency Name")
            # dispatcher.utter_message("Your booking confirmation number is " + str(results[0]))
            return [SlotSet("AgencyName", results[0])]

class BookingConfirmationNumberAction(Action):

    def name(self) -> Text:
        return "action_booking_confirmation_number"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict):

        agency_id = tracker.get_slot("AgencyID")
        login_status = tracker.get_slot("login_status")

        if login_status == False:
            dispatcher.utter_message("Please type 'login' to enter credentials")
            return []

        table = db.Table('user', metadata, autoload=True, autoload_with=engine)

        stmt = db.select([table.columns.booking_confirmation_number]).where(table.columns.agency_id == agency_id)

        results = conn.execute(stmt).fetchone()

        if results:
            print("Valid Confirmation Number")
            dispatcher.utter_message("Your booking confirmation number is " + str(results[0]))
            return []
        else:
            dispatcher.utter_message("No Booking Confirmation found. Please try again.")
            return []

class PaymentStatusAction(Action):

    def name(self) -> Text:
        return "action_payment_status"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict ):

        agency_id = tracker.get_slot("AgencyID")
        login_status = tracker.get_slot("login_status")

        if login_status == False:
            dispatcher.utter_message("Please type 'login' to enter credentials")
            return []

        table = db.Table('user', metadata, autoload=True, autoload_with=engine)

        stmt = db.select([table.columns.payment_status]).where(table.columns.agency_id == agency_id)

        results = conn.execute(stmt).fetchone()

        if results:
            # print("Valid Confirmation Number")
            dispatcher.utter_message("Your Payment status is " + str(results[0]))
            return []
        else:
            dispatcher.utter_message("No Payment status found. Please try again.")
            return []

# class ActionLogin(Action):

#     def name(self) -> Text:
#           return "action_login"
      
#     def get_db_connection():
#         try:
#             connection = psycopg2.connect(
#                 host="localhost",
#                 database="onyxdatabase",
#                 user="postgres",
#                 password="root"
#             )
#             return connection
#         except Exception as e:
#             print(f"Error connecting to the database: {str(e)}")
#             return None

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#             connection=self.get_db_connection()
            
#             if connection:
#              user_id = tracker.get_slot("AgencyId")
#              user_pwd = tracker.get_slot("Password")
#              cursor = connection.cursor()
             
#             cursor.execute("SELECT password FROM agency_user_table WHERE agency_id = %s", (user_id,))
#             stored_password = cursor.fetchone()
#             try:
#                 if (user_pwd==stored_password):
#                     return [SlotSet("user_authenticated", True)]
#                 else:
#                     dispatcher.utter_message("Login failed. Please check your credentials.")
#                     return [SlotSet("user_authenticated", False)]
#             finally:
#                 cursor.close()
#                 connection.close()
            

    


