import json
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from faker import Faker
fake = Faker('pt_BR')


async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str="Endpoint=sb://padaria-eventhubs.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=OW1DDFjQvnKNb81LzhcQxF9BRwotHPC73y09ffl+6BI=", eventhub_name="customer-topic")
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        for x in range(10):
            Customer = {
                "id": fake.hexify(text='^^^^-^^^^-^^^^-^^^^'),
                "cpf": fake.cpf(),
                "originBranchId": fake.random_number(3),
                "name": fake.name(),
                "loginname": "",
                "email": "",
                "birthdate": "",
                "age": fake.random_number(2),
                "career": "",
                "phone": "",
                "photo": "azure blob link",
                "addresses": [{
                    "addressStreet": "",
                    "addressNumber": "",
                    "addressCity": "",
                    "addressState": "",
                    "addressCountry": "",
                    "addressPostalCode": "",
                    "addressComplement": "",
                    "isMain": True
                }],
                "socialMidia": {
                    "facebook": "",
                    "instagram": "",
                    "linkeDin": "",
                    "twiter": ""
                },
                "createdDate": "",
                "lastRecentsOrders": [{
                    "orderNumber": ""
                }],
                "summary": [{
                    "totalOrders": 10,
                    "totalVisits": 9,
                    "averageTicket": 85.00,
                    "lastOrderDate": "20210731",
                    "lastFeedbackStatus": "Positive",
                    "lastFeedbackMessage": "Pão estava ótimo e bem quentinho, atendimento super rápido"
                }],
                "possiblePromotions": [{
                    "productId": "",
                    "disacountPercent": 10
                }]
            }
            event_data_batch.add(EventData(json.dumps(Customer,indent=4)))
            print(json.dumps(Customer,indent=4))
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
