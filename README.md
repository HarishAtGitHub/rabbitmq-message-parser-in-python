# rabbitmq-message-parser-in-python
This project is to give a solution to message consumption from rabbitmq in python

In this solution we have 

1) requests-queue - which receives data from external environment

2) rejects-queue - which receives data that failed while being received from requests-queue and processed

# How is it processed ?

we have a set of consumer jobs to process items in requests-queue.

If the message processing is successful it sends an acknowledgement to rabbitmq.In case, after it processes if the processing fails, then it reposts the message to the rejects-queue.

Then we have set of consumer jobs to process items in rejects-queue. 

Here when these items in rejects-queue is processed successfully, then it sends an acknowledgement to rabbitmq.
In case, after it processes if the processing fails, then you can do some custom activity like logging to slack.


# How to start this entire system ?

Just do 


    python main.py


this configures the rabbitmq with all the queues and then runs all the consumer jobs. The number of consumer jobs is configurable. It is found in config/configuration.py. Even the POOL_SIZE is configurable.


# How to test this system ?


    python publisher.py <msg>


Just for testing the system's working

if the msg starts with 's' then it is a successfull message and it will be processed by one of the 'requests' consumer and the ack is sent to rabbitmq.

if the msg starts with 'fp' then it is a message that fails processing in the 'requests' consumer and so it reaches the 'rejects' queue.
Then a consumer picks it up from there processes it. But this time it passes and
so  an ack is sent to the rabbitmq.

if the msg starts with 'fo' then it is a message that fails processing in the 'r
equests' consumer and so it reaches the 'rejects' queue.
Then a consumer picks it up from there processes it. But this time it fails again here, so it is sent to a place decided by the user.


Try with the following commands

    python publisher.py s123
    python publisher.py fp123
    python publisher.py fo123


Tail the logs and see the output.


# FUTURE PLANS:

1) Authentication with RabbitMQ

2) Now it just has a place from where we can call other modules to do tasks we want to be done on receving message from queue. We want to make this part modular and pluggable in such a way that, people will have to just write a plugin file and drop it inside and it will be fecthed by the system as a 'TO DO TASK' when message is received in queue. So that people need not touch the main core code in order to add integrations.


