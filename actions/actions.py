# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import psycopg2


class ActionLogin(Action):

    def name(self) -> Text:
          return "action_login"
      
    def get_db_connection():
        try:
            connection = psycopg2.connect(
                host="localhost",
                database="onyxdatabase",
                user="postgres",
                password="root"
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")
            return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            connection=get_db_connection()
            
            if connection:
             user_id = tracker.get_slot("AgencyId")
             user_pwd = tracker.get_slot("Password")
             cursor = connection.cursor()
             
            cursor.execute("SELECT password FROM agency_user_table WHERE agency_id = %s", (user_id,))
            stored_password = cursor.fetchone()
            if (user_pwd==stored_password):
                return [SlotSet("user_authenticated", True)]
            else:
                dispatcher.utter_message("Login failed. Please check your credentials.")
                return [SlotSet("user_authenticated", False)]
          
            cursor.close()
            connection.close()
            

    


