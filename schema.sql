drop table if exists driver;
create table driver (
  id integer primary key autoincrement,
  name text not null,
  phone text not null,
  vehicleno text not null
);

drop table if exists bookings;
create table booking(
	id integer primary key autoincrement,
	name text not null,
	phone text ,
	startlocation text ,
	endlocation text ,
	driver int 

);