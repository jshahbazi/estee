import sqlite3
from typing import List, Optional
from pydantic import BaseModel
import csv
from contextlib import contextmanager

# Most of these fields are probably useless, but data is data
class FoodTruck(BaseModel):
    location_id: Optional[int]
    applicant: str
    facility_type: str
    cnn: int
    location_description: str
    address: str
    blocklot: str
    block: str
    lot: str
    permit: str
    status: str
    food_items: str
    x: float
    y: float
    latitude: float
    longitude: float
    schedule: Optional[str]
    dayshours: Optional[str]
    NOISent: Optional[str]
    approved: Optional[str]
    received: Optional[str]
    prior_permit: Optional[str]
    expiration_date: Optional[str]
    location: Optional[str]
    fire_prevention_districts: Optional[int]
    police_districts: Optional[int]
    supervisor_districts: Optional[int]
    zip_codes: Optional[int]
    neighborhoods_old: Optional[int]


@contextmanager
def database_connection(db_name: str):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def create_database(self, csv_file):
        with database_connection(self.db_name) as conn:
            self.create_table()
            with open(csv_file, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Some of the columns are empty, so we need to handle that
                    def to_float(value):
                        return float(value) if value.strip() else 0.0

                    def to_int(value):
                        return int(value) if value.strip() else 0

                    food_truck = FoodTruck(
                        location_id=to_int(row.get("location_id", "")),
                        applicant=row.get("Applicant", ""),
                        facility_type=row.get("FacilityType", ""),
                        cnn=to_int(row.get("cnn", "")),
                        location_description=row.get("LocationDescription", ""),
                        address=row.get("Address", ""),
                        blocklot=row.get("blocklot", ""),
                        block=row.get("block", ""),
                        lot=row.get("lot", ""),
                        permit=row.get("permit", ""),
                        status=row.get("Status", ""),
                        food_items=row.get("FoodItems", ""),
                        x=to_float(row.get("X", "")),
                        y=to_float(row.get("Y", "")),
                        latitude=to_float(row.get("Latitude", "")),
                        longitude=to_float(row.get("Longitude", "")),
                        schedule=row.get("Schedule", ""),
                        dayshours=row.get("dayshours", ""),
                        NOISent=row.get("NOISent", ""),
                        approved=row.get("Approved", ""),
                        received=row.get("Received", ""),
                        prior_permit=row.get("PriorPermit", ""),
                        expiration_date=row.get("ExpirationDate", ""),
                        location=row.get("Location", ""),
                        fire_prevention_districts=to_int(row.get("Fire Prevention Districts", "")),
                        police_districts=to_int(row.get("Police Districts", "")),
                        supervisor_districts=to_int(row.get("Supervisor Districts", "")),
                        zip_codes=to_int(row.get("Zip Codes", "")),
                        neighborhoods_old=to_int(row.get("Neighborhoods (old)", "")),
                    )
                    self.insert_food_truck(food_truck)

    def create_table(self):
        with database_connection(self.db_name) as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS food_trucks (
                            location_id INTEGER PRIMARY KEY,
                            applicant TEXT,
                            facility_type TEXT,
                            cnn INTEGER,
                            location_description TEXT,
                            address TEXT,
                            blocklot TEXT,
                            block TEXT,
                            lot TEXT,
                            permit TEXT,
                            status TEXT,
                            food_items TEXT,
                            x REAL,
                            y REAL,
                            latitude REAL,
                            longitude REAL,
                            schedule TEXT,
                            dayshours TEXT,
                            NOISent TEXT,
                            approved TEXT,
                            received TEXT,
                            prior_permit TEXT,
                            expiration_date TEXT,
                            location TEXT,
                            fire_prevention_districts INTEGER,
                            police_districts INTEGER,
                            supervisor_districts INTEGER,
                            zip_codes INTEGER,
                            neighborhoods_old INTEGER
                            )"""
            )

    def insert_food_truck(self, food_truck: FoodTruck):
        sql = """INSERT INTO food_trucks (location_id, applicant, facility_type, cnn, location_description, address, blocklot, block, lot,
                 permit, status, food_items, x, y, latitude, longitude, schedule, dayshours, NOISent, approved, received,
                 prior_permit, expiration_date, location, fire_prevention_districts, police_districts, supervisor_districts,
                 zip_codes, neighborhoods_old)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            food_truck.location_id,
            food_truck.applicant,
            food_truck.facility_type,
            food_truck.cnn,
            food_truck.location_description,
            food_truck.address,
            food_truck.blocklot,
            food_truck.block,
            food_truck.lot,
            food_truck.permit,
            food_truck.status,
            food_truck.food_items,
            food_truck.x,
            food_truck.y,
            food_truck.latitude,
            food_truck.longitude,
            food_truck.schedule,
            food_truck.dayshours,
            food_truck.NOISent,
            food_truck.approved,
            food_truck.received,
            food_truck.prior_permit,
            food_truck.expiration_date,
            food_truck.location,
            food_truck.fire_prevention_districts,
            food_truck.police_districts,
            food_truck.supervisor_districts,
            food_truck.zip_codes,
            food_truck.neighborhoods_old,
        )
        with database_connection(self.db_name) as conn:
            conn.execute(sql, values)
            conn.commit()
        return True

    def get_all_food_trucks(self) -> List[FoodTruck]:
        with database_connection(self.db_name) as conn:
            cursor = conn.execute("SELECT * FROM food_trucks")
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [FoodTruck(**dict(zip(map(str, columns), row))) for row in data]

    def get_food_truck_by_id(self, location_id: int) -> Optional[FoodTruck]:
        with database_connection(self.db_name) as conn:
            cursor = conn.execute(
                "SELECT * FROM food_trucks WHERE location_id = ?", (location_id,)
            )
            data = cursor.fetchone()
            if data:
                columns = [column[0] for column in cursor.description]
                return FoodTruck(**dict(zip(columns, data)))
            return None

    def get_food_truck_by_name(self, name: str) -> List[FoodTruck]:
        with database_connection(self.db_name) as conn:
            cursor = conn.execute(
                "SELECT * FROM food_trucks WHERE applicant LIKE ?", ("%" + name + "%",)
            )
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [FoodTruck(**dict(zip(map(str, columns), row))) for row in data]

    def update_food_truck(self, location_id: int, food_truck: FoodTruck):
        with database_connection(self.db_name) as conn:
            existing_truck = self.get_food_truck_by_id(location_id)
            if existing_truck is None:
                return None
            sql = """UPDATE food_trucks SET location_id = ?, applicant = ?, facility_type = ?, cnn = ?, location_description = ?, address = ?,
                     blocklot = ?, block = ?, lot = ?, permit = ?, status = ?, food_items = ?, x = ?, y = ?, latitude = ?,
                     longitude = ?, schedule = ?, dayshours = ?, NOISent = ?, approved = ?, received = ?, prior_permit = ?,
                     expiration_date = ?, location = ?, fire_prevention_districts = ?, police_districts = ?, supervisor_districts = ?,
                     zip_codes = ?, neighborhoods_old = ? WHERE location_id = ?"""
            values = (
                food_truck.location_id,
                food_truck.applicant,
                food_truck.facility_type,
                food_truck.cnn,
                food_truck.location_description,
                food_truck.address,
                food_truck.blocklot,
                food_truck.block,
                food_truck.lot,
                food_truck.permit,
                food_truck.status,
                food_truck.food_items,
                food_truck.x,
                food_truck.y,
                food_truck.latitude,
                food_truck.longitude,
                food_truck.schedule,
                food_truck.dayshours,
                food_truck.NOISent,
                food_truck.approved,
                food_truck.received,
                food_truck.prior_permit,
                food_truck.expiration_date,
                food_truck.location,
                food_truck.fire_prevention_districts,
                food_truck.police_districts,
                food_truck.supervisor_districts,
                food_truck.zip_codes,
                food_truck.neighborhoods_old,
                location_id,
            )
            conn.execute(sql, values)
            conn.commit()
        return food_truck

    def delete_food_truck(self, location_id: int):
        with database_connection(self.db_name) as conn:
            existing_truck = self.get_food_truck_by_id(location_id)
            if existing_truck is None:
                return None
            conn.execute(
                "DELETE FROM food_trucks WHERE location_id = ?", (location_id,)
            )
            conn.commit()
        return True
