select * from chat_user;
insert into chat_user(nickname,pass_hash,salt,public_key,is_active) values('nick1','usdhaisudhaiush','asuaushsauauash','asuuahuhuashdu','0');
insert into chat_user(nickname,pass_hash,salt,public_key,is_active) values('nick2','usdhaisudhaiush','asuaushsauauash','asuuahuhuashdu','0');
--nick1 manda msg
select * from conversation;
select user_id from chat_user where nickname = 'nick1';
select user_id from chat_user where nickname = 'nick2';
insert into conversation(user_one,user_two) values (1,2);

select * from key_set;
insert into key_set (private_owner,key,conversation_id) values (2,'asdsadsdasd',1);
insert into key_set (private_owner,key,conversation_id) values (1,'assdadsdasd',1);

select * from message;

insert into message(message_data,date_sent,exp_date,receiving_user,was_received,conversation_id)
values ('aiudasiu','12-12-2012','21-12-2012','nick2','0',1);

select m.message_data,k.key from message m, key_set k 
where m.receiving_user = 'nick2' and m.was_received = '0' 
and k.conversation_id = m.conversation_id and k.private_owner = (select user_id from chat_user where nickname = 'nick2');



select key from key_set where conversation_id = 1 and private_owner = 2;

