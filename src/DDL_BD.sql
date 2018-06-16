create table chat_user(
		user_id serial not null,
		nickname varchar(64) not null,
		pass_hash text not null,
		salt char(16)  not null,
		public_key text not null,
		is_active char(1) not null,
		CONSTRAINT USER_PK PRIMARY KEY(user_id),
		CONSTRAINT UNIQUE_NICK UNIQUE(nickname));

create table user_relation(
		first_user integer not null,
		second_user integer not null,
		relation_type varchar(20) not null,
		CONSTRAINT PRECEDENCE_CHECK CHECK(first_user < second_user),
		CONSTRAINT USER_RELATION_PK primary key(first_user,second_user),
		CONSTRAINT FIRST_FK foreign key(first_user) references chat_user(user_id) ON DELETE CASCADE,
		CONSTRAINT SECOND_FK foreign key(second_user) references chat_user(user_id) ON DELETE CASCADE,
		CONSTRAINT CHECK_RELATION CHECK (relation_type in ('pendent_first_second','pendent_second_first','friends','blocked_first_second','blocked_second_first','both_blocked')));

create table conversation(
		conversation_id serial not null,
		user_one integer not null,
		user_two integer not null,
		CONSTRAINT CONVERSATION_PK PRIMARY KEY(conversation_id),
		CONSTRAINT USER_ONE_FK FOREIGN KEY(user_one) REFERENCES chat_user (user_id) ON DELETE CASCADE,
		CONSTRAINT USER_TWO_FK FOREIGN KEY(user_two) REFERENCES chat_user (user_id) ON DELETE CASCADE,
		CONSTRAINT PRECEDENCE_CHECK CHECK(user_one < user_two),
		CONSTRAINT UNIQUE_CONV UNIQUE(user_one,user_two));

create table message(
		message_id serial not null,
		message_data text not null,
		date_sent date not null,
		exp_date date not null,
		receiving_user integer not null,
		was_received char(1) not null,
		conversation_id integer not null,
		CONSTRAINT CONVERSATION_FK FOREIGN KEY(conversation_id) REFERENCES conversation(conversation_id),
		CONSTRAINT MESSAGE_PK primary key(message_id),
		CONSTRAINT USER_FK FOREIGN KEY(receiving_user) REFERENCES char_user(user_id),
		CONSTRAINT EXP_DATE_CHECK CHECK(exp_date > date_sent));

create table key_set(
		key_set_id serial not null,
		private_owner integer not null,
		key char(16) not null,
		conversation_id integer not null,
		CONSTRAINT KEY_SET_PK PRIMARY KEY(key_set_id),
		CONSTRAINT CONVERSATION_FK FOREIGN KEY(conversation_id) REFERENCES conversation (conversation_id) ON DELETE CASCADE);
		CONSTRAINT UNIQUE_USER_CONV UNIQUE(private_owner,conversation_id)
