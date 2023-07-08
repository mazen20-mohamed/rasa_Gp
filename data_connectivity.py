import mysql.connector
import time
from datetime import datetime
mydatabase = mysql.connector.connect(
  host="containers-us-west-77.railway.app",
  user="root",
  password="fLd8Nd0xTojBeCndX16r",
  database="railway",
  port = 8033,
  auth_plugin='mysql_native_password'
)
mycrursor = mydatabase.cursor()

###### return weight of a user ######
def get_weight(id):
    a = mycrursor.execute("SELECT weight from user where Id = '"+str(id)+"'")
    p = mycrursor.fetchall()[0][0]
    return p

###### return goal weight of a user ######
def get_goal_weight(id):
    a = mycrursor.execute("SELECT goal_weight from user where Id = '"+str(id)+"'")
    p = mycrursor.fetchall()[0][0]
    return p

###### return calories of a user ######
def get_calories(id):
    print(id)
    a = mycrursor.execute("SELECT calories from user where Id = '"+str(id)+"'")
    p = mycrursor.fetchall()[0][0]
    return p

#### return food by its id #######
def get_food(id):
   mycrursor.execute("SELECT * FROM food_table where id = '"+str(id)+"'")
   return mycrursor.fetchall()


##### return a breakfast meal randomly #####
def get_breakfast_meal():
  mycrursor.execute("SELECT * FROM Breakfast_Meals2 ORDER BY RAND() LIMIT 1")
  return mycrursor.fetchall()

##### return food id and percent by breakfast_id #####
def get_food_breakast_id(id):
  mycrursor.execute("SELECT food_id,percentage FROM breakfast_food where breakfast_id = '"+str(id)+"'")
  return mycrursor.fetchall()

##### return a dinner meal randomly #####
def get_dinner_meal():
  mycrursor.execute("SELECT * FROM dinner_Meals ORDER BY RAND() LIMIT 1")
  return mycrursor.fetchall()

##### return food id and percent by dinner_id #####
def get_food_dinner_id(id):
  mycrursor.execute("SELECT food_id,percentage FROM dinner_food where dinner_id = '"+str(id)+"'")
  return mycrursor.fetchall()

##### return a lunch meal randomly #####
def get_lunch_meal():
  mycrursor.execute("SELECT * FROM lunch_Meals ORDER BY RAND() LIMIT 1")
  return mycrursor.fetchall()

##### return food id and percent by lunch_id #####
def get_food_lunch_id(id):
  mycrursor.execute("SELECT food_id,percentage FROM lunch_food where lunch_id = '"+str(id)+"'")
  return mycrursor.fetchall()

##### return last time for login for specific user ######
def get_last_time_taken(id):
  mycrursor.execute("SELECT time_taken FROM login_update where user_id = '"+str(id)+"'")
  p = mycrursor.fetchall()
  m = len (p)
  return p[m-1][0]

##### update weight for specific user ######
def update_weightt(id,weight):
  sql = 'INSERT INTO weight_table (user_id,time_taken,weight) VALUES ( "{0}", "{1}", "{2}")'.format(id,datetime.now(),str(weight))
  mycrursor.execute(sql)
  mycrursor.execute("UPDATE user SET weight= '"+str(weight)+"' WHERE Id = '"+str(id)+"'")
  mydatabase.commit()
##### update goal weight for specific user ######
def update_goal_weightt(id,weight):
  mycrursor.execute("UPDATE user SET goal_weight= '"+str(weight)+"' WHERE Id = '"+str(id)+"'")
  mydatabase.commit()

##### add breakfast_meal to specific user in certain time ######
def add_breakfast_time(id,time,break_id):
  mycrursor.execute("INSERT breakfast_time(user_id,time,break_id) VALUES ('"+str(id)+"','"+str(time)+"','"+str(break_id)+"')")
  mydatabase.commit()

def check_take_breakfast(id):
  mycrursor.execute("SELECT time from breakfast_time WHERE user_id = '"+str(id)+"' ORDER BY id DESC LIMIT 1")
  p = mycrursor.fetchall()
  if not mycrursor.rowcount:
    return -1
  return p[0][0]


##### add lunch_meal to specific user in certain time ######
def add_lunch_time(id,time,lunch_id):
  mycrursor.execute("INSERT lunch_time(user_id,time,lunch_id) VALUES ('"+str(id)+"' , '"+str(time)+"' , '"+str(lunch_id)+"')")
  mydatabase.commit()

def check_take_lunch(id):
  mycrursor.execute("SELECT time from lunch_time WHERE user_id = '"+str(id)+"' ORDER BY id DESC LIMIT 1")
  p = mycrursor.fetchall()
  if not mycrursor.rowcount:
    return -1
  return p[0][0]


##### add dinner_meal to specific user in certain time ######
def add_dinner_time(id,time,dinner_id):
  mycrursor.execute("INSERT dinner_time(user_id,time,dinner_id) VALUES ('"+str(id)+"' , '"+str(time)+"' , '"+str(dinner_id)+"')")
  mydatabase.commit()

def check_take_dinner(id):
  mycrursor.execute("SELECT time from dinner_time WHERE user_id = '"+str(id)+"' ORDER BY id DESC LIMIT 1")
  p = mycrursor.fetchall()
  if not mycrursor.rowcount:
    return -1
  return p[0][0]

def add_snack_time(id,time,snack_id):
  mycrursor.execute("INSERT snack_time(user_id,time,snack_id) VALUES ('"+str(id)+"' , '"+str(time)+"' , '"+str(snack_id)+"')")
  mydatabase.commit()

def check_take_snack(id):
  mycrursor.execute("SELECT time from snack_time WHERE user_id = '"+str(id)+"' ORDER BY id DESC LIMIT 2")
  p = mycrursor.fetchall()
  if mycrursor.rowcount == 1 or mycrursor.rowcount == 0 :
    return -1,-1
  return p[0][0],p[1][0]

def print_execrsices():
  mycrursor.execute("SELECT name from exce ")
  c = mycrursor.fetchall()
  return_menu = ""
  item = 0 
  for i in c :
     item+=1
     return_menu += "({}) ".format(item) + i[0] + "\n"
  return return_menu
################### return exce link #####################
def get_exce_link(id):
  st = "SELECT link FROM exce WHERE Id = "+str(id)
  mycrursor.execute(st)
  return mycrursor.fetchall()[0][0]
##### return a snack meal randomly #####
def get_snack_meal():
  mycrursor.execute("SELECT * FROM snack_food ORDER BY RAND() LIMIT 1")
  return mycrursor.fetchall()

##### update colries for user after update weight #####
def update_colries(id):
  mycrursor.execute("SELECT gender,weight,height,age,activation_rate from user where Id = '"+str(id)+"'")
  a = mycrursor.fetchall()
  if a[0][0] == 'men':
    bmr = 10*float(a[0][1]) # weight
    bmr+= (6.25*float(a[0][2])) # height
    bmr-= (5*float(a[0][3])) # age
    bmr+=5
    bmr = (bmr * float(a[0][4])) # activationRate
    bmr = int(bmr)
    mycrursor.execute("UPDATE user SET calories= '"+str(bmr)+"' WHERE Id = '"+str(id)+"'")
  else:
    bmr = (10*float(a[0][1])) # weight
    bmr+= (6.25*float(a[0][2])) # height
    bmr-= (5*float(a[0][3])) # age
    bmr-=161
    bmr = (bmr * float(a[0][4])) # activationRate
    bmr = int(bmr)
    mycrursor.execute("UPDATE user SET calories= '"+str(bmr)+"' WHERE Id = '"+str(id)+"'")
  mydatabase.commit()

mydatabase.commit()

