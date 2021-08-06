import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


async def on_event(partition_context, event):
    # Print the event data.
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string("DefaultEndpointsProtocol=https;AccountName=padarialabcase;AccountKey=zl0VYcvcJIoy3ENSHhnmhv2JDOT0vBbnMyDFj8uhnA5r6HCHgYPwtGCw+eEXCf/uYN1dJPuNcJnZhDnHhyY60g==;EndpointSuffix=core.windows.net", "eventhubs-offset")

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(conn_str="Endpoint=sb://padaria-eventhubs.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=OW1DDFjQvnKNb81LzhcQxF9BRwotHPC73y09ffl+6BI=", consumer_group="$Default", eventhub_name="customer-topic", checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="-1")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())