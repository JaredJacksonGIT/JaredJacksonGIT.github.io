import time
from subscribe import message_queue, start_mqtt

start_mqtt()

print("Waiting for messages...")
while True:
    if not message_queue.empty():
        msg = message_queue.get()
        print("Received message dict:", msg)
    time.sleep(5)