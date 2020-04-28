import mysql.connector

mydb = mysql.connector.connect(host='localhost',user='root',passwd='')
mycursor = mydb.cursor()

mycursor.execute('Create database Fathom')

mycursor.close()
mydb.close()

mydb = mysql.connector.connect(host='localhost',user='root',passwd='',database='Fathom')
mycursor = mydb.cursor()

mycursor.execute('Create table accounts(username varchar(50) primary key, user_password varchar(50) not null)')
mycursor.execute('''Create table user_profile(username varchar(50) primary key,
      img varchar(100) ,
      sex char not null,
      interest varchar(20) not null,
      bio varchar(300) not null,
      foreign key (username) 
      references accounts(username)
      on delete cascade
      on update cascade)''')
mycursor.execute('''Create table request(
	username varchar(50) ,
    target varchar(50), 
    sent_request int ,
    accept int ,
    foreign key (username) 
    references accounts(username)
    on delete cascade
    on update cascade,
    primary key(username,target)
)''')
mycursor.execute('''Create table chatbox(
	msg_id int not null AUTO_INCREMENT primary key,
	sender varchar(50) not null , 
    receiver varchar(50) not null,
    message varchar(100) not null
)''')

mycursor.close()
mydb.close()

