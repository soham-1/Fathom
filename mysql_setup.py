import mysql.connector

mydb = mysql.connector.connect(host='localhost',user='root',passwd='')
mc = mydb.cursor()

mc.execute('Create database Fathom')

mc.close()
mydb.close()

mydb = mysql.connector.connect(host='localhost',user='root',passwd='',database='Fathom')
mc = mydb.cursor()

mc.execute('Create table accounts(username varchar(50) primary key ,password varchar(50) not null)')
mc.execute('''Create table user_profile(username varchar(50) primary key,
      img varchar(100) ,
      sex char not null,
      interest varchar(20) not null,
      bio varchar(300) not null,
      foreign key (username) 
      references accounts(username)
      on delete cascade
      on update cascade)''')
mc.execute('''Create table request(
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
mc.execute('''Create table chatbox(
	msg_id int not null AUTO_INCREMENT primary key,
	sender varchar(50) not null , 
    reciever varchar(50) not null,
    message varchar(100) not null
)''')

mc.close()
mydb.close()

