import sqlite3,csv,getpass 
def main():
  print("""\t**********************************************************************
        **                Welcome to Quiz Compition                         ** 
        **        Please select the below option                            **
        **        1) Login                                                  **  
        **        2) Register                                               **
        **        3) Quit                                                   **
        **********************************************************************""")
  choice=int(input("enter the option 1 and 2 \n"))
  if choice==1:
    username=input("enter username \t")
    password=getpass.getpass()
    login(username,password)
  elif choice==2: 
    username=input("enter username \t")
    password=input("enter password \t")
    register(username,password)
  else:
    pass
def startquiz():
  username=input("Your Name: ")
  count=0
  con=sqlite3.connect("Quizdb")
  cur = con.cursor()
  ques=cur.execute('SELECT * FROM question ') 
  for que in ques:
    print(que)
    print("*************************************************************************")
    print("Question:""\n",que[2],end="\n\n")
    print("A) ",que[3],end="\n\n")
    print("B) ",que[4],end="\n\n")
    print("C) ",que[5],end="\n\n")
    print("D) ",que[6],end="\n\n")
    answer=que[7]
    output=input("Select the correct answer ")
    if(output=='A' or output=='B' or output=='C' or output=='D'):
      if(answer==output):
        print("Your answer is correct",end="\n\n")  
        count=count+1
      else:
        print("Correct answer is ",answer,end="\n\n")
    else:
      print("Sorry, Please select A/B/C/D or use Capital Letter")
  conn=sqlite3.connect("result.db")
  result=conn.cursor()
  result.execute("""CREATE TABLE IF NOT EXISTS RESULT(Username TEXT,Score INT,Result TEXT)""")
  print("Your Total Score is ",count)
  if (count>6):
    print(" Congratulation You Passed the test")
    result.execute("INSERT INTO RESULT(Username,Score,Result) VALUES(?,?,?)",(username,count,"Pass"))
  else:
    result.execute("INSERT INTO RESULT(Username,Score,Result) VALUES(?,?,?)",(username,count,"Fail"))
    retry=(input("Will you re-try the test "))
    if(retry=='Yes' or retry=='YES' or retry=='yes'):
      startquiz()
    else:
      pass
def login(username,password):
  if username=="MASTER" and password=="MASTER123":
    print("successfully logdin as super user")
    addquestion()
  elif username and password:
    conn=sqlite3.connect("userdetail.db")
    database=conn.cursor()
    database.execute("SELECT * FROM USERDETAIL ")   
    for row in database:
      if username==row[0] and password==row[1]:
        startquiz()
      else: print("Please register yourself")
def register(username,password):
   if username and password:
      conn=sqlite3.connect("userdetail.db")
      database=conn.cursor()
      database.execute("""CREATE TABLE IF NOT EXISTS USERDETAIL(Username TEXT,Password TEXT)""")
      database.execute("INSERT INTO USERDETAIL(Username,Password) VALUES(?,?)",(username,password))
      conn.commit()
      print("registered")
      main()
def quesadd():
  Level=input("enter the diffuclty level")
  Question=input("enter the questions")
  Topic=input("enter the topic name")
  optiona=input("enter option a")
  optionb=input("enter option b")
  optionc=input("enter option c")
  optiond=input("enter option d")
  answer=input("enter correct answer")
  userinput=input("Want to add new question?")
  if userinput=="yes" or userinput=="YES":
  	quesadd()
  else: addquestion()
  con=sqlite3.connect("Quizdb")
  cur = con.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS question (Level,Topic,Question,optiona,optionb,optionc,optiond,answer)")
  cur.execute("INSERT INTO question VALUES (?,?,?,?,?,?,?,?);", (Level,Topic,Question,optiona,optionb,optionc,optiond,answer))
  con.commit()
  
def addquestion():
  print("""  \t****************************************************************************
        **                  SUPER USER TO ADD QUESTION                            **
        **            Please select the below option                              **
        **            1) Add Question from CSV                                    **
        **            2) Add Question manually                                    **
        **            3) Quit                                                     **
        ****************************************************************************""")
  option=int(input("Please select the option \n"))
  if option==1:
    con = sqlite3.connect("Quizdb")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS question (Level,Topic,Question,optiona,optionb,optionc,optiond,answer)")
    with open('C:\\Users\\win 10\\Desktop\\New folder\\quizquestion.csv','r') as fin:
      dr = csv.DictReader(fin)
      for values in dr:
        todo=dict(values)
        cur.execute("INSERT INTO question  VALUES (?,?,?,?,?,?,?,?);", (todo.get("Level"),todo.get("Topic"),todo.get("Question"),todo.get("optiona"),todo.get("optionb"),todo.get("optionc"),todo.get("optiond"),todo.get("answer")))
        con.commit()
    addquestion()
  elif option==2:
  	quesadd()
  else:
    main()
main()