# %%
import os
import glob

from collections import OrderedDict
import csv
# from datetime import datetime, date, timedelta
import datetime
from typing import Dict
from dagster_pandas import DataFrame
import pandas as pd
from faker import Faker
import random
from faker.providers import DynamicProvider
from faker_music import MusicProvider


EMPLOYEES = random.randint(2,4)
ACTIVATIONS = random.randint(45,175)
DEACTIVATIONS = random.randint(5,20)
CONTENT = 30

BACKFILL_DAYS = 2 # number of days to backfill_DAYS

PATH_TO_FAKE_DATA = '/home/dave/data-engineering/dbt-template-project/fake-data-generation/fake-data'


skill_provider = DynamicProvider(
     provider_name="skills",
     elements=["Big Ears", "Sining", "Song Writing", "Being Cool", "Big a Brain"],
)

subscription_type_provider = DynamicProvider(
     provider_name="subscription_type",
     elements=["Standard", "Big banana", "Speed"],
)

subscription_termination_reason_provider = DynamicProvider(
     provider_name="subscription_termination_reason",
     elements=["To expensive", "Big banana not big enough", "To Slow", "Poor Quality Content"],
)

web_event_type_provider = DynamicProvider(
     provider_name="web_event_type",
     elements=OrderedDict([("content_viewed",0.80), ("pricing_viewed", 0.05), ("content_shared", 0.05), ("comment_posted",0.1)]),
)

def fake_data_generation_content(current_timestamp, records, fake_data_employees):
    fake = Faker('en_AU')

    fake.add_provider(MusicProvider)
    
    content = []

    len_emp = len(fake_data_employees)
    
    
    fake.add_provider(skill_provider)

    for i in range(records):
        rnd_emp = random.randint(0, len_emp-1)

        content.append({
                "Content Name": fake.word(),
                "Content ID": fake.uuid4(),
                "Genre": fake.music_genre(),
                "Sub Genre": fake.music_subgenre(),
                "Instrument": fake.music_instrument(),
                "Instrument Category": fake.music_instrument_category(),
                "Email": fake_data_employees[rnd_emp]['Email'],
                "effective_from_ts": current_timestamp
                })
        
    return content

def fake_data_generation_employees(current_timestamp, records):
    fake = Faker('en_AU')
    
    employee = []
    
    fake.add_provider(skill_provider)

    for i in range(records):
        first_name = fake.first_name()
        last_name = fake.last_name()



        employee.append({
                "First Name": first_name,
                "Last Name": last_name,
                "Birth Date" : fake.date(pattern="%Y-%m-%d", end_datetime=datetime.date(1995, 1,1)),
                "Email": str.lower(f"{first_name}.{last_name}@fake_domain-2.com"),
                "Hobby": fake.word(),
                "Experience" : random.randint(0,15),
                "Start Date": current_timestamp,
                "Salary": random.randrange(75000,150000, 5000),
                "City" : fake.city(),
                "Nationality" : fake.country(),
                "Skill": fake.skills(),
                "effective_from_ts": current_timestamp
                })
        
    return employee

def fake_data_generation_subscription_events(current_timestamp, records):
    fake = Faker('en_AU')
    
    subscription_events = []
    
    fake.add_provider(subscription_type_provider)

    for i in range(records):
        first_name = fake.first_name()
        last_name = fake.last_name()

        # hours since activating
        n = random.randint(0,3)

        subscription_events.append({
                "Event ID": fake.uuid4(),
                "First Name": first_name,
                "Last Name": last_name,
                "Birth Date" : fake.date(pattern="%Y-%m-%d", end_datetime=datetime.date(1995, 1,1)),
                "Email": str.lower(f"{first_name}.{last_name}@fake_domain-2.com"),
                "Start Date": current_timestamp - + datetime.timedelta(hours=n),
                "City" : fake.city(),
                "Nationality" : fake.country(),
                "Subscription Type": fake.subscription_type(),
                "effective_from_ts": current_timestamp
                })
        
    return subscription_events

def fake_data_generation_subscription_deactivate_events(current_timestamp, records):
    fake = Faker('en_AU')
    
    subscription_events = []
    
    fake.add_provider(subscription_termination_reason_provider)

    for i in records:

        # disconnection hours since activating
        n = random.randint(0,15)

        subscription_events.append({
                "Event ID": fake.uuid4(),
                "Email": i['Email'],
                "End Date": i["Start Date"] + datetime.timedelta(hours=n),
                "Subscription Termination Reason": fake.subscription_termination_reason(),
                "effective_from_ts": current_timestamp
                })
        
    return subscription_events


def fake_data_web_events(current_timestamp, records, content):
    fake = Faker('en_AU')
    
    web_events = []

    content_len = len(content)
    
    fake.add_provider(web_event_type_provider)

    for i in records:
        for j in range(random.randint(0,15)):
            # start event
            n = random.randint(0,15)
            # event length 
            l = random.randint(0,15)

            event_type = fake.web_event_type()

            event_start = i["Start Date"] + datetime.timedelta(hours=n)

            web_events.append({
                    "Event ID": fake.uuid4(),
                    "Email": i['Email'],
                    "Event Start": event_start,
                    "Event End": event_start + datetime.timedelta(seconds=n*60) if event_type == 'content_viewed' else None,
                    "Web Event Type": event_type,
                    "Content ID": content[random.randint(0,content_len-1)]['Content ID'] if 'content' in event_type else None,
                    "effective_from_ts": current_timestamp
                    })
        
    return web_events

def remove_fake_old_data():
    files = glob.glob(f'{PATH_TO_FAKE_DATA}/*.csv')

    for f in files:
        try:
            # f.unlink()
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

# %%
def generate_fake_data() -> Dict[str, pd.DataFrame]:
    remove_fake_old_data()
    for i in range(BACKFILL_DAYS):

        current_execution_timestamp = datetime.datetime.now() - datetime.timedelta(days=i)

        fake_data_employees = fake_data_generation_employees(current_execution_timestamp, EMPLOYEES)
        fake_content = fake_data_generation_content(current_execution_timestamp, CONTENT, fake_data_employees)
        fake_sub_activate = fake_data_generation_subscription_events(current_execution_timestamp, ACTIVATIONS)
        fake_sub_deactivate = fake_data_generation_subscription_deactivate_events(current_execution_timestamp, fake_sub_activate[0:DEACTIVATIONS])
        fake_web_events = fake_data_web_events(current_execution_timestamp, fake_sub_activate, fake_content)

        file_partition = current_execution_timestamp.strftime("%Y%m%dT%H%M%S")

        df_fake_content = pd.DataFrame(fake_content)
        df_fake_data_employees = pd.DataFrame(fake_data_employees)
        df_fake_sub_activate = pd.DataFrame(fake_sub_activate)
        df_fake_sub_deactivate= pd.DataFrame(fake_sub_deactivate)
        df_fake_web_events = pd.DataFrame(fake_web_events)

        # df_fake_web_events.head()


        df_fake_content.to_csv(f'{PATH_TO_FAKE_DATA}/fake_content_{file_partition}.csv', index=False)
        df_fake_data_employees.to_csv(f'{PATH_TO_FAKE_DATA}/fake_data_employees_{file_partition}.csv', index=False)
        df_fake_sub_activate.to_csv(f'{PATH_TO_FAKE_DATA}/fake_sub_activate_{file_partition}.csv', index=False)
        df_fake_sub_deactivate.to_csv(f'{PATH_TO_FAKE_DATA}/fake_sub_deactivate_{file_partition}.csv', index=False)
        df_fake_web_events.to_csv(f'{PATH_TO_FAKE_DATA}/fake_web_events_{file_partition}.csv', index=False)


# %%

if __name__ == '__main__':
    dict_of_df = generate_fake_data()