def main(req: func.HttpRequest) -> func.HttpResponse:
	message = ServiceBusMessage(req.get_json())
	service_bus_client = ServiceBusClient.from_connection_string(conn_str="your_connection_string")
	with service_bus_client:
    	sender = service_bus_client.get_topic_sender(topic_name="your_topic_name")
    	with sender:
        	sender.send_messages(message)
	return func.HttpResponse("Message sent to Service Bus", status_code=200)