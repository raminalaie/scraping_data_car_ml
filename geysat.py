from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import mysql.connector

vorodi = input("data beroz shavad?y/n = ")

if vorodi == "y":
      driver = webdriver.Firefox()
      url = "https://bama.ir/car/all/isfahan-isfahan?year=1397,1401&price=0,950000000&image=1&country=iranian"
      driver.get(url)
      #scorol web
      SCROLL_PAUSE_TIME = 2
      last_height = driver.execute_script("return document.body.scrollHeight")
      while True:
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight-400));")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                  break
            last_height = new_height
      #sett data    
      name = driver.find_elements(By.TAG_NAME, 'p')
      price = driver.find_elements(By.CLASS_NAME, "bama-ad__price-holder")
      kilometer = driver.find_elements(By.CLASS_NAME, "bama-ad__detail-row")
      kilometers = []
      list_name = []
      list_price = []
      list_kilometr = []
      list_sal = []
      for i in kilometer:
            kilometers.append(i.text.replace("\n",",").split(","))
      for i in kilometers:
            list_kilometr.append(i[1])
      for i in kilometers:
            list_sal.append(int(i[0]))
      for i in name:
            list_name.append(i.text.replace("،",""))
      for i in price:
            list_price.append(int(i.text.replace(",","")))
      #sql clean  table and add new data    
      def clean():
            mydb = mysql.connector.connect( 
            user="root",
            password="",
            host="127.0.0.1",
            database = "learn"
            )      
            mycursor = mydb.cursor()      
            mycursor.execute("TRUNCATE TABLE listname")
            mydb.close()
      #add new data in table sql 
      def create(list_name,list_price,list_kilometr,list_sal):
            clean()
            mydb = mysql.connector.connect(
            user="root",
            password="",
            host="127.0.0.1",
            database = "learn"
            )
            mycursor = mydb.cursor()
            for i in range(len(list_name)):
                  Name = list_name[i]
                  price = list_price[i]
                  kilome = list_kilometr[i]
                  sale = list_sal[i]
                  mycursor.execute("INSERt INTO listnameml VALUES (\"%s\", \"%s\" , %i , \"%i\")" % (Name,kilome,sale,price))
                  mydb.commit()
            mydb.close()
      create(list_name,list_price,list_kilometr,list_sal)
elif vorodi == "n":
      def data_ml():
            mydb = mysql.connector.connect(    
            user="root",
            password="",
            host="127.0.0.1",
            database = "learn"
            )
            mycursor = mydb.cursor()
            query = 'SELECT * FROM listnameml;'
            mycursor.execute(query)
            x = []
            y = []
            for (Name,kilome,sale,price) in mycursor:
                  p=[Name,kilome,sale]
                  x.append(p)         
                  y.append(price)
            
            for  i in range(len(x)):
                  print(x[i],"   ",y[i])      

            mydb.close()

      data_ml()






