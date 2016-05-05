Thought Exercise
================

Overview
--------
The goal of this project is to process large JSON files so that their contents (records) are persisted to a database in a way that minimizes processing time and is fault tolerant.

Components
----------

This topology will include the following components:

- celery server(s)
- distributed message queue (rabbitmq or redis would work fine)
- mongodb


Because the records needing to be processed vary in both schema and size a noSQL database will be used for persistence.

In order to reduce the time needed to process the file, celery will be used to process the records in parallel.  Multiple celery servers can be used if more processing power is required.

Celery requires a message queue and in this case rabbitmq or redis would be a good choice.

The client can be a command line, a web application or any process that can call a celery task.

Implementation Details
----------------------

Client
~~~~~~
The client will call a celery task passing in the URL for the JSON file to be read.
Example python call from shell or web app:

.. code:: python

   from inmar.tasks import process_json_file

   process_json_file.delay('path_to_json_file')


Celery Tasks
~~~~~~~~~~~~
There will be a primary celery task that will read the JSON file, call sub-tasks for chunks of records and log the completion of the task.  Because it is not certain that the file can be loaded into memory it will need to be read as a stream.  The ijson_ library can be used to read the records in from the stream.  The master task can use a celery chord to run subtasks and be aware of when all the subtasks are completed.  Once all the tasks have concluded the task can log that the task has been completed.  Example code:

.. code:: python

   from celery import chord, shared_task
   import ijson.backends.yajl2_cffi as ijson
   import urllib2

   @shared_task
   def process_json_file(url):
       callback = log_succes.s()
       header = []
       for records_chunk in get_records(url):
           header.append(persist_records(records_chunk))

        # will run as many of these in parallel as we have cores
        # allocated for celery
        result = chord(header)(callback)


    @shared_task
    def persist_records(records):
        # write each record to the database

    def get_records(url):
        fd = urllib2.urlopen(url)
        chunk_size = 500
        records = []
        processed = 0
        for record in ijson.items(fd, 'item'):
            records.append(record)
            if not processed % chunk_size:
                yield records
                records = []


Each subtask will write its set of records to the database in a try block and place any failed attempts in a retry list. Because the database may be intermitently unavailable, the subtask will retry the records in the retry list until all records succeeded.

Message Queue
~~~~~~~~~~~~~
No special configuration is needed for the message queue other than the usual steps to integrate with celery (adding user and credentials, setting up a vhost and permissions for the user on the vhost).

.. _ijson: https://pypi.python.org/pypi/ijson/
