import datetime
import logging
import azure.functions as func
import asyncio, requests, json, datetime
from azure.eventhub.aio import EventHubProducerClient
from dateutil.relativedelta import relativedelta
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')

async def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info("Iniciando envio dos dados")


    producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://padaria-eventhubs.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=OW1DDFjQvnKNb81LzhcQxF9BRwotHPC73y09ffl+6BI=", eventhub_name="customer-topic")
    async with producer:
    # Create a batch.
        event_data_batch = await producer.create_batch()
        logging.info('Iniciando loop e criando batch...')
    # Add events to the batch.
        for x in range(5):
            if fake.simple_profile()["sex"] == 'F':
                firstname = fake.first_name_female()
                sex = 'F'
                url = 'https://fakeface.rest/face/json?gender=female&minimum_age=999&maximum_age=999'
            else:
                firstname = fake.first_name_male()
                sex = 'M'
                url = 'https://fakeface.rest/face/json?gender=male&minimum_age=999&maximum_age=999'

            lastname = fake.last_name()
            middlename = fake.last_name()
            domainemail = fake.free_email_domain()
            username = firstname[0].lower().replace(' ', '') + lastname.lower().replace(' ', '')
            email = firstname.lower().replace(' ', '') + lastname.lower().replace(' ', '') + '@' + domainemail
            birthdate = fake.date_between(start_date='-90y', end_date='-10y')
            age = relativedelta(datetime.datetime.now(), birthdate)
            url = url.replace('999', str(age.years))
            response = requests.get(url)
            if response.status_code == 200:
                imagelink = response.json()['image_url']
            else:
                imagelink = ""

            if age.years >= 18:
                job = fake.job()
            else:
                job = 'Estudante'

            Customer = {
                "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                "cpf": fake.cpf(),
                "originBranchId": fake.random_number(3),
                "name": firstname + ' ' + middlename + ' ' + lastname,
                "loginname": username,
                "email": email,
                "birthdate": birthdate.strftime('%d/%m/%Y'),
                "age": age.years,
                "job": fake.job(),
                "phone": fake.phone_number(),
                "sex": sex,
                "photo": imagelink,
                "addresses": [{
                    "addressStreet": fake.street_name(),
                    "addressNumber": fake.building_number(),
                    "addressCity": fake.city(),
                    "addressState": fake.state_abbr(),
                    "addressCountry": fake.current_country(),
                    "addressPostalCode": fake.postcode(),
                    "addressComplement": fake.neighborhood(),
                    "isMain": True
                }],
                "socialMidia": {
                    "facebook": "",
                    "instagram": "",
                    "linkeDin": "",
                    "twiter": ""
                },
                "createdDate": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "lastRecentsOrders": [{
                    "orderNumber": ""
                }],
                "summary": [{
                    "totalOrders": 0,
                    "totalVisits": 0,
                    "averageTicket": 0,
                    "lastOrderDate": 'null',
                    "lastFeedbackStatus": 'null',
                    "lastFeedbackMessage": 'null'
                }],
                "possiblePromotions": [{
                    "productId": "",
                    "disacountPercent": 0
                }]
            }

            event_data_batch.add(EventData(json.dumps(Customer, indent=4)))
            #print(json.dumps(Customer, indent=4))
            logging.info('enviado registro %s', datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

