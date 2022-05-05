import psycopg2
from fake_web_events import Simulation
import uuid

dsn = (
    "dbname={dbname} "
    "user={user} "
    "password={password} "
    "port={port} "
    "host={host} ".format(
        dbname="myDb",
        user="admin",
        password="admin1234",
        port=5433,
        host="localhost",
    )
)

conn = psycopg2.connect(dsn)
print("connected")
conn.set_session(autocommit=True)
cur = conn.cursor()

cur.execute(
    """
    create table if not exists web_events(
      event_id varchar(200),
      event_timestamp timestamp,
      event_type varchar(200),
      page_url varchar(200),
      page_url_path varchar(200),
      referer_url varchar(200),
      referer_url_scheme  varchar(200),
      referer_url_port integer,
      referer_medium varchar(200),
      utm_medium varchar(200),
      utm_source varchar(200),
      utm_content varchar(200),
      utm_campaign varchar(200),
      click_id varchar(200),
      geo_latitude varchar(200),
      geo_longitude varchar(200),
      geo_country varchar(200),
      geo_timezone varchar(200),
      geo_region_name varchar(200),
      ip_address varchar(200),
      browser_name varchar(200),
      browser_user_agent varchar(200),
      browser_language varchar(200),
      os varchar(200),
      os_name varchar(200),
      os_timezone varchar(200),
      device_type varchar(200),
      device_is_mobile boolean,
      user_custom_id varchar(200),
      user_domain_id varchar(200));
    """
)

simulation = Simulation(user_pool_size=100, sessions_per_day=1000)
events = simulation.run(duration_seconds=20)

for e in events:
    e["event_id"] = uuid.uuid1().hex
    cur.execute(
      f"""
      INSERT INTO web_events VALUES (
        '{e["event_id"]}',
        '{e["event_timestamp"]}',
        '{e["event_type"]}',
        '{e["page_url"]}',
        '{e["page_url_path"]}',
        '{e["referer_url"]}',
        '{e["referer_url_scheme"]}',
        '{e["referer_url_port"]}',
        '{e["referer_medium"]}',
        '{e["utm_medium"]}',
        '{e["utm_source"]}',
        '{e["utm_content"]}',
        '{e["utm_campaign"]}',
        '{e["click_id"]}',
        '{e["geo_latitude"]}',
        '{e["geo_longitude"]}',
        '{e["geo_country"]}',
        '{e["geo_timezone"]}',
        '{e["geo_region_name"]}',
        '{e["ip_address"]}',
        '{e["browser_name"]}',
        '{e["browser_user_agent"]}',
        '{e["browser_language"]}',
        '{e["os"]}',
        '{e["os_name"]}',
        '{e["os_timezone"]}',
        '{e["device_type"]}',
        '{e["device_is_mobile"]}',
        '{e["user_custom_id"]}',
        '{e["user_domain_id"]}'
      )
      """
    )
