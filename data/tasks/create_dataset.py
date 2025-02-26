from django.db import connections
from data.models import DuplicateDistanceConfig


def create_dataset():
    with connections['default'].cursor() as cursor:
        cursor.execute("insert into auth_group (id,name) values (1,'Superadmin'),(2,'Public');")

        cursor.execute("UPDATE auth_user SET email='superadmin@driver.com', first_name='driver', last_name='driver' "
                       "WHERE username=(SELECT username FROM auth_user ORDER BY date_joined ASC LIMIT 1);")

        cursor.execute("insert into driver_advanced_auth_groupdetail (name,description,group_id,is_admin) values "
                       "('Superadmin', 'superadmin', 1, True),('Public','public',2, False);")

        cursor.execute("insert into driver_advanced_auth_userdetail(password, username, first_name, last_name, email, "
                       "is_active, date_joined," "updated_on, user_id, is_staff,is_superuser, is_analyst, "
                       "is_tech_analyst, google_user, is_role_requested)" "select password, username, first_name, "
                       "last_name, email, is_active, date_joined, last_login, id, is_staff, " "is_superuser, False, "
                       "False, False, 'Not Requested' from auth_user where id = (select auth_user.id from auth_user);")

        cursor.execute("insert into authtoken_token (key,created,user_id) values "
                       "('36df3ade778ca4fcf66ba998506bdefa54fdff1c',now(),(select auth_user.id from auth_user));")

        cursor.execute("insert into auth_user_groups (user_id , group_id) values "
                       "((select auth_user.id from auth_user),1);")

        cursor.execute("insert into driver_advanced_auth_userdetail_groups (userdetail_id , group_id) values "
                       "((select driver_advanced_auth_userdetail.id from driver_advanced_auth_userdetail),1);")

        cursor.execute("insert into driver_advanced_auth_countryinfo (country_code, country_name, archived, latitude, "
                       "longitude) values ('ws', 'Samoa', True, -13.752724664397, -171.826171875);")

        cursor.execute("insert into data_duplicatedistanceconfig(dedupe_distance_threshold,unit,created,modified) "
                       "values (0.0009,'degree', '2020-07-30T08:11:42.706240Z', '2020-07-30T08:11:42.706240Z');")

        cursor.execute("insert into data_irapdetail (irap_treatment_id,irap_treatment_name,path) "
                       "values (3,'Additional Lane','http://toolkit.irap.org/api/?content=treatments&id=3'),"
                       "(37,'Addressing Alcohol and Other Drugs','http://toolkit.irap.org/api/?content=treatments&id=37'),"
                       "(1,'Bicycle Facilities','http://toolkit.irap.org/api/?content=treatments&id=1'),"
                       "(2,'Central Hatching','http://toolkit.irap.org/api/?content=treatments&id=2'),"
                       "(4,'Central Turning Lane Full Length','http://toolkit.irap.org/api/?content=treatments&id=4'),"
                       "(39,'Child Safety Initiatives','http://toolkit.irap.org/api/?content=treatments&id=39'),"
                       "(5,'Delineation','http://toolkit.irap.org/api/?content=treatments&id=5'),"
                       "(35,'Duplication','http://toolkit.irap.org/api/?content=treatments&id=35'),"
                       "(38,'Education','http://toolkit.irap.org/api/?content=treatments&id=38'),"
                       "(54,'Emergency Response','http://toolkit.irap.org/api/?content=treatments&id=54'),"
                       "(36,'Enforcement','http://toolkit.irap.org/api/?content=treatments&id=36'),"
                       "(40,'Fatigue Management','http://toolkit.irap.org/api/?content=treatments&id=40'),"
                       "(41,'Helmets and Protective Clothing','http://toolkit.irap.org/api/?content=treatments&id=41'),"
                       "(6,'Intersection - Delineation','http://toolkit.irap.org/api/?content=treatments&id=6'),"
                       "(7,'Intersection - Grade Separation','http://toolkit.irap.org/api/?content=treatments&id=7'),"
                       "(10,'Intersection - Roundabout','http://toolkit.irap.org/api/?content=treatments&id=10'),"
                       "(11,'Intersection - Signalise','http://toolkit.irap.org/api/?content=treatments&id=11'),"
                       "(8,'Intersection - Turn Lanes (Signalised)','http://toolkit.irap.org/api/?content=treatments&id=8'),"
                       "(9,'Intersection - Turn Lanes (Unsignalised)','http://toolkit.irap.org/api/?content=treatments&id=9'),"
                       "(12,'Lane Widening','http://toolkit.irap.org/api/?content=treatments&id=12'),"
                       "(45,'Licensing','http://toolkit.irap.org/api/?content=treatments&id=45'),"
                       "(13,'Median Barrier','http://toolkit.irap.org/api/?content=treatments&id=13'),"
                       "(55,'Median Crossing Upgrade','http://toolkit.irap.org/api/?content=treatments&id=55'),"
                       "(50,'Motor Vehicle Standards','http://toolkit.irap.org/api/?content=treatments&id=50'),"
                       "(14,'Motorcycle Lanes','http://toolkit.irap.org/api/?content=treatments&id=14'),"
                       "(42,'New Car Assessment Program (NCAP)','http://toolkit.irap.org/api/?content=treatments&id=42'),"
                       "(15,'One Way Network','http://toolkit.irap.org/api/?content=treatments&id=15'),"
                       "(16,'Parking Improvements','http://toolkit.irap.org/api/?content=treatments&id=16'),"
                       "(17,'Pedestrian Crossing - Grade Separation','http://toolkit.irap.org/api/?content=treatments&id=17'),"
                       "(18,'Pedestrian Crossing - Signalised','http://toolkit.irap.org/api/?content=treatments&id=18'),"
                       "(19,'Pedestrian Crossing - Unsignalised','http://toolkit.irap.org/api/?content=treatments&id=19'),"
                       "(56,'Pedestrian Fencing','http://toolkit.irap.org/api/?content=treatments&id=56'),"
                       "(20,'Pedestrian Footpath','http://toolkit.irap.org/api/?content=treatments&id=20'),"
                       "(21,'Pedestrian Refuge Island','http://toolkit.irap.org/api/?content=treatments&id=21'),"
                       "(51,'Publicity','http://toolkit.irap.org/api/?content=treatments&id=51'),"
                       "(22,'Railway Crossing','http://toolkit.irap.org/api/?content=treatments&id=22'),"
                       "(23,'Realignment - Horizontal','http://toolkit.irap.org/api/?content=treatments&id=23'),"
                       "(24,'Realignment - Vertical','http://toolkit.irap.org/api/?content=treatments&id=24'),"
                       "(25,'Regulate Roadside Commercial Activity','http://toolkit.irap.org/api/?content=treatments&id=25'),"
                       "(26,'Restrict/Combine Direct Access Points','http://toolkit.irap.org/api/?content=treatments&id=26'),"
                       "(60,'Road Surface Rehabilitation','http://toolkit.irap.org/api/?content=treatments&id=60'),"
                       "(28,'Roadside Safety - Barriers','http://toolkit.irap.org/api/?content=treatments&id=28'),"
                       "(29,'Roadside Safety - Hazard Removal','http://toolkit.irap.org/api/?content=treatments&id=29'),"
                       "(30,'Rumble Strips','http://toolkit.irap.org/api/?content=treatments&id=30'),"
                       "(48,'Safe Speed','http://toolkit.irap.org/api/?content=treatments&id=48'),"
                       "(59,'School Zones','http://toolkit.irap.org/api/?content=treatments&id=59'),"
                       "(44,'Seatbelts','http://toolkit.irap.org/api/?content=treatments&id=44'),"
                       "(31,'Service Road','http://toolkit.irap.org/api/?content=treatments&id=31'),"
                       "(32,'Shoulder Sealing','http://toolkit.irap.org/api/?content=treatments&id=32'),"
                       "(57,'Sideslope Improvement','http://toolkit.irap.org/api/?content=treatments&id=57'),"
                       "(61,'Sight Distance (obstruction removal)','http://toolkit.irap.org/api/?content=treatments&id=61'),"
                       "(27,'Skid Resistance','http://toolkit.irap.org/api/?content=treatments&id=27'),"
                       "(33,'Speed Management','http://toolkit.irap.org/api/?content=treatments&id=33'),"
                       "(58,'Street Lighting','http://toolkit.irap.org/api/?content=treatments&id=58'),"
                       "(34,'Traffic Calming','http://toolkit.irap.org/api/?content=treatments&id=34'),"
                       "(52,'Used Car Safety Ratings','http://toolkit.irap.org/api/?content=treatments&id=52'),"
                       "(43,'Vehicle Features and Devices','http://toolkit.irap.org/api/?content=treatments&id=43'),"
                       "(53,'Vehicle Roadworthiness','http://toolkit.irap.org/api/?content=treatments&id=53');")

        cursor.execute("insert into data_weatherdatalist (label, value, active) "
                       "values ('Clear day','clear-day', True),"
                       "('Clear Night','clear-night', True),"
                       "('Cloudy','cloudy', True),"
                       "('Hail','hail', True),"
                       "('Partly Cloudy Day','partly-cloudy-day', True),"
                       "('Partly Cloudy Night','partly-cloudy-night', True),"
                       "('Rain','rain', True),"
                       "('Sleet','sleet', True),"
                       "('Thunderstorm','thunderstorm', True),"
                       "('Tornado','tornado', True),"
                       "('Wind','wind', True),"
                       "('Thunderstorm with light rain','thunderstorm with light rain', True),"
                       "('Thunderstorm with rain','thunderstorm with rain', True),"
                       "('Thunderstorm with heavy rain','thunderstorm with heavy rain', True),"
                       "('Light thunderstorm','light thunderstorm', True),"
                       "('Thunderstorm','thunderstorm', True),"
                       "('Heavy thunderstorm','heavy thunderstorm', True),"
                       "('Ragged thunderstorm','ragged thunderstorm', True),"
                       "('Thunderstorm with light drizzle','thunderstorm with light drizzle', True),"
                       "('Thunderstorm with drizzle','thunderstorm with drizzle', True),"
                       "('Thunderstorm with heavy drizzle','thunderstorm with heavy drizzle', True),"
                       "('Light intensity drizzle','light intensity drizzle', True),"
                       "('Drizzle','drizzle', True),"
                       "('Heavy intensity drizzle','heavy intensity drizzle', True),"
                       "('Light intensity drizzle rain','light intensity drizzle rain', True),"
                       "('Drizzle rain','drizzle rain', True),"
                       "('Shower rain and drizzle','shower rain and drizzle', True),"
                       "('Heavy intensity drizzle rain','heavy intensity drizzle rain', True),"
                       "('Heavy shower rain and drizzle','heavy shower rain and drizzle', True),"
                       "('Shower drizzle','shower drizzle', True),('Light rain','light rain', True),"
                       "('Moderate rain','moderate rain', True),"
                       "('Heavy intensity rain','heavy intensity rain', True),"
                       "('Very heavy rain','very heavy rain', True),"
                       "('Extreme rain','extreme rain', True),"
                       "('Freezing rain','freezing rain', True),"
                       "('Light intensity shower rain','light intensity shower rain', True),"
                       "('Shower rain','shower rain', True),"
                       "('Heavy intensity shower rain','heavy intensity shower rain', True),"
                       "('Ragged shower rain','ragged shower rain', True),"
                       "('Light shower sleet','Light shower sleet', True),"
                       "('Shower sleet','Shower sleet', True),"
                       "('Mist','mist', True),('Smoke','Smoke', True),"
                       "('Haze','Haze', True),"
                       "('Sand/ dust whirls','sand/ dust whirls', True),"
                       "('Fog','Fog', True),"
                       "('Sand','sand', True),"
                       "('Dust','dust', True),"
                       "('Volcanic ash','volcanic ash', True),"
                       "('Squalls','squalls', True),"
                       "('Tornado','tornado', True),"
                       "('Clear sky','clear sky', True),"
                       "('Few clouds: 11-25%','few clouds: 11-25%', True),"
                       "('Scattered clouds: 25-50%','scattered clouds: 25-50%', True),"
                       "('Broken clouds: 51-84%','broken clouds: 51-84%', True),"
                       "('Overcast clouds: 85-100%','overcast clouds: 85-100%', True);")

        count = DuplicateDistanceConfig.objects.all().count()
        if count > 0:
            print("Initial dataset created successfully")
