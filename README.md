# Fathom
A dating app in tkinter python

# getting started :
this app consist of pages like signup, login, profile, homepage, request page, chatbox.
you must create a male and female account both to start its working.
some changes need to be done in profile page code - 
    for a newly created account a default image is added . value of that variable has to be changed accordingly in line 118 and 119.
    database password has to be changed in line 8

# prerequisites:
python, tkinter , mysql-connetor-python, PIL

create a database named <b>fathom<b>
create table as follows
1) accounts(username varchar(50) primary key ,password varchar(50) not null)

2) user_profile(username varchar(50) primary key,
      img varchar(100) ,
      sex char not null,
      interest varchar(20) not null,
      bio varchar(300) not null,
      foreign key (username) 
      references accounts(username)
      on delete cascade
      on update cascade
      
3) request(
	username varchar(50) ,
    target varchar(50), 
    sent_request int ,
    accept int ,
    foreign key (username) 
    references accounts(username)
    on delete cascade
    on update cascade,
    primary key(username,target)
);

4) chatbox(
	msg_id int not null AUTO_INCREMENT primary key,
	sender varchar(50) not null , 
    reciever varchar(50) not null,
    message varchar(100) not null
);

# built with:
tkinter - gui
python - backend
mysql - database
