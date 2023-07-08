# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from data_connectivity import *
import math
from datetime import datetime, timedelta
from rasa_sdk.events import SlotSet
import re
class ActionAskForBreakfast(Action):
    def name(self) -> Text:
        return "action_ask_for_breakfast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.sender_id
        time = check_take_breakfast(id)
        if time != -1 and time + timedelta(hours=+23) > datetime.now():
            dispatcher.utter_message(text="لقد حصلت علي وجبة افطارك بالفعل ")
            return []
        
        calories = get_calories(id)
        
        breakfast_calory = (25.0*calories)/100.0
        meal = get_breakfast_meal()
        dispatcher.utter_message(text=meal[0][1])
        if meal[0][2] != 'nan':
            dispatcher.utter_message(text="بامكانك مشاهدة طريقة الطبخ من خلال ذلك اللينك")
            dispatcher.utter_message(text=str(meal[0][2]))

        dispatcher.utter_message(text="المكونات كالتالي")
        food_ids = get_food_breakast_id(meal[0][0])
        m = len(food_ids)
        for i in range (m):
            food_item = get_food(food_ids[i][0])

            food_calory = (food_ids[i][1]*breakfast_calory)/100.0
            
            grams = (food_calory*100) / food_item[0][2]
            grams = math.floor(grams)
            dispatcher.utter_message(text=food_item[0][1]+" بمقدار " + str(grams) +" جرام ")
        dispatcher.utter_message(text="هل اعجبتك هذه الوجبة ؟")
        return [SlotSet("break_id", meal[0][0])]
    
class ActionBreakDone(Action):
    def name(self) -> Text:
        return "action_break_done"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.sender_id
        print(tracker.get_slot("break_id"))
        add_breakfast_time(id,datetime.now(),int(tracker.get_slot("break_id")))

        return []
class ActionAskForSnack(Action):
    def name(self) -> Text:
        return "action_ask_for_snack"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        id = tracker.sender_id
        time1,time2 = check_take_snack(id)
        time = check_take_breakfast(id)
        if time==-1 or time.day != datetime.now().day:
            dispatcher.utter_message(text="لبد ان تفطر الاول قبل انا تاخذ وجبة خفيفة")
            return []
        if time1 != -1 and time2 !=-1 and time1 + timedelta(hours=+23) > datetime.now() and time2 + timedelta(hours=+23) > datetime.now():
            dispatcher.utter_message(text="لقد حصلت علي وجبتين الخفتين بالفعل ")
            return []
        

        calories = get_calories(id)
        snack_calory = (((20.0)/2)*calories)/100.0
        meal = get_snack_meal()
        
        food_item = get_food(meal[0][1])
        print(food_item[0][0])
        food_calory = (food_item[0][2]*snack_calory)/100.0
            
        grams = (food_calory*100) / food_item[0][2]
        grams = math.floor(grams)
        dispatcher.utter_message(text=food_item[0][1]+" بمقدار " + str(grams) +" جرام ")
        dispatcher.utter_message(text="هل اعجبتك هذه الوجبة ؟")
        
        return [SlotSet("snack_id", meal[0][0])]
class ActionSnackDone(Action):
    def name(self) -> Text:
        return "action_snack_done"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.sender_id
        print(tracker.get_slot("snack_id"))
        add_snack_time(id,datetime.now(),int(tracker.get_slot("snack_id")))

        return []
class ActionAskForLunch(Action):
    def name(self) -> Text:
        return "action_ask_for_lunch"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = tracker.sender_id

        time = check_take_lunch(id)
        if time != -1 and time + timedelta(hours=+23) > datetime.now():
            dispatcher.utter_message(text="لقد حصلت علي وجبة الغداء بالفعل ")
            return []

        calories = get_calories(id)
        lunch_calory = (35.0*calories)/100.0

        meal = get_lunch_meal()

        dispatcher.utter_message(text=meal[0][1])
        if meal[0][2] != 'nan':
            dispatcher.utter_message(text="بامكانك مشاهدة طريقة الطبخ من خلال ذلك اللينك")
            dispatcher.utter_message(text=str(meal[0][2]))

        dispatcher.utter_message(text="المكونات كالتالي")

        food_ids = get_food_lunch_id(meal[0][0])

        m = len(food_ids)
        for i in range (m):
            food_item = get_food(food_ids[i][0])

            food_calory = (food_ids[i][1]*lunch_calory)/100.0
            
            grams = (food_calory*100) / food_item[0][2]
            grams = math.floor(grams)
            dispatcher.utter_message(text=food_item[0][1]+" بمقدار " + str(grams) +" جرام ")
        dispatcher.utter_message(text="هل اعجبتك هذه الوجبة ؟")
        return [SlotSet("lunch_id", meal[0][0])]
    
class ActionLunchDone(Action):
    def name(self) -> Text:
        return "action_lunch_done"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.sender_id
        print(tracker.get_slot("lunch_id"))
        add_lunch_time(id,datetime.now(),int(tracker.get_slot("lunch_id")))

        return []
        
### get dinner meal #######    
class ActionAskForDinner(Action):
    def name(self) -> Text:
        return "action_ask_for_dinner"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = tracker.sender_id

        time = check_take_dinner(id)
        if time != -1 and time + timedelta(hours=+23) > datetime.now():
            dispatcher.utter_message(text="لقد حصلت علي وجبة العشاء بالفعل ")
            return []
        
        calories = get_calories(id)
        dinner_calory = (20.0*calories)/100.0
        meal = get_dinner_meal()
        dispatcher.utter_message(text=meal[0][1])
        if meal[0][2] != 'nan':
            dispatcher.utter_message(text="بامكانك مشاهدة طريقة الطبخ من خلال ذلك اللينك")
            dispatcher.utter_message(text=str(meal[0][2]))

        dispatcher.utter_message(text="المكونات كالتالي")
        food_ids = get_food_dinner_id(meal[0][0])
        m = len(food_ids)
        for i in range (m):
            food_item = get_food(food_ids[i][0])

            food_calory = (food_ids[i][1]*dinner_calory)/100.0
            
            grams = (food_calory*100) / food_item[0][2]
            grams = math.floor(grams)
            dispatcher.utter_message(text=food_item[0][1]+" بمقدار " + str(grams) +" جرام ")
        dispatcher.utter_message(text="هل اعجبتك هذه الوجبة ؟")
        return [SlotSet("dinner_id", meal[0][0])]
class ActionDinnerDone(Action):
    def name(self) -> Text:
        return "action_dinner_done"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = tracker.sender_id
        print(tracker.get_slot("dinner_id"))
        add_dinner_time(id,datetime.now(),int(tracker.get_slot("dinner_id")))

        return []
### Update weight for user #######    
class ActionAskForUpdateWeight(Action):
    def name(self) -> Text:
        return "action_ask_for_update_weight"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = tracker.sender_id
        weight = tracker.get_slot("weight")
        if(weight is None):
            dispatcher.utter_message(text="يرجي ادخال وزنك مرة اخرى")
        else:
            weightBefore = get_weight(id)
            update_weightt(id,float(weight))
            update_colries(id)
            if float(weight) < float(weightBefore):
                dispatcher.utter_message(text="جيد جدا احسنت استمر يا بطل")
            elif float(weight) > float(weightBefore):
                dispatcher.utter_message(text="يبدو انك لم تتبع النظام الغذائي جيدا ولكن انا معك سنصل لحلمك قريبا باذن الله ")
            
            goal_weight = get_goal_weight(id)
            if(float(weight) <= float(goal_weight)):
                dispatcher.utter_message(text="رائع جدا يا بطل لقد وصلت لهدفك اليوم")
                dispatcher.utter_message(text="من فضلك اعد ادخال وزنك الذي تطمح ان توصل اليه")
        return [SlotSet("weight", None)]

class FindMatchingFoodAction(Action):
    def name(self) -> Text:
        return "action_for_find_matching_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        food_word = tracker.get_slot("foodName")
        
        if food_word is None:
            dispatcher.utter_message(text="يبدو لي ان جملة غير صحيحة او انا لا اعرف هذا النوع من الطعام")
        else:
            print(food_word)
            df = pd.read_excel('food_table.xlsx')
            def find_matching_food(food_word):
                best_match = None
                best_ratio = 0

                for food_name in df['name']:
                    ratio = fuzz.ratio(food_word, food_name)

                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = food_name

                return best_match
            matched_food = find_matching_food(food_word)

            if matched_food is not None:
                food_info = df[df['name'] == matched_food]

                food_name = food_info['name'].values[0]
                calories = food_info['calories'].values[0]
                protein = food_info['protein'].values[0]
                fat = food_info['fat'].values[0]
                size = food_info['size'].values[0]
                type_size = food_info['type_size'].values[0]
                string = str(food_name) + " يوجد فيه " +str(calories)+" كالوري " +  str(protein)+ " بروتين "+ str(fat) + " دهون لكل 100 جرام "
                if str(type_size)!='nan':
                    string += " ما يعادل " + str(size) + " "+ str(type_size)
                dispatcher.utter_message(text=string )
            else:
                dispatcher.utter_message(text="لم اجد الطعام الذي تريده")
        return [SlotSet("foodName", None)]

class FindMatchingUpdateGoalWeight(Action):
    def name(self) -> Text:
        return "action_for_update_goal_weight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = tracker.sender_id
        weight = tracker.get_slot("goal_weight")

        if weight is None:
            dispatcher.utter_message(text="من فضلك اعد ادخال وزنك الذي تطمح ان توصل اليه بشكل صحيح")
        else:
            print(float(weight))
            update_goal_weightt(id,float(weight))
            dispatcher.utter_message(text="شكرا لك")
        return [SlotSet("goal_weight", None)]
class ActionShowExce(Action):
    def name(self) -> Text:
        return "action_show_exce"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain : Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        menu = print_execrsices()
        dispatcher.utter_message(text= menu)
        return []

class ActionExce(Action):
    def name(self) -> Text:
        return "action_exce"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
         domain : Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
    
        st = tracker.get_slot("ex")
        newst = re.sub(r'[^0-9]', '', st)
        out = get_exce_link(int(newst))
        dispatcher.utter_message(text=f"اليك رابط تمرينك")
        dispatcher.utter_message(text=f"{out}")

        return []