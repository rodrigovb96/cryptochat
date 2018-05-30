create table chat_user(
		user_id serial not null,
		nickname varchar(64) not null,
		pass_hash text not null,
		salt char(16)  not null,
		public_key text not null,
		is_active char(1) not null,
		CONSTRAINT USER_PK PRIMARY KEY(user_id),
		CONSTRAINT UNIQUE_NICK UNIQUE(nickname));

create table message(
		message_id serial not null,
		receiving_user integer not null,
		sending_user integer not null,
		message_data text not null,
		date_sent date not null,
		exp_date date not null,
		was_read char(1) not null,
		was_received char(1) not null,
		CONSTRAINT MESSAGE_PK primary key(message_id),
		CONSTRAINT RECEIVING_FK foreign key(receiving_user) REFERENCES chat_user(user_id) ON DELETE CASCADE,
		CONSTRAINT SENDING_FK foreign key(sending_user) REFERENCES chat_user(user_id) ON DELETE CASCADE,
		CONSTRAINT EXP_DATE_CHECK CHECK(exp_date > date_sent));

create table user_relation(
		first_user integer not null,
		second_user integer not null,
		relation_type varchar(7) not null,
		CONSTRAINT PRECEDENCE_CHECK CHECK(first_user < second_user),
		CONSTRAINT USER_RELATION_PK primary key(first_user,second_user),
		CONSTRAINT FIRST_FK foreign key(first_user) references chat_user(user_id) ON DELETE CASCADE,
		CONSTRAINT SECOND_FK foreign key(second_user) references chat_user(user_id) ON DELETE CASCADE,
		CONSTRAINT CHECK_RELATION CHECK (relation_type in ('pendent_first_second','pendent_second_first','friends','blocked_first_second','blocked_second_first','both_blocked')));