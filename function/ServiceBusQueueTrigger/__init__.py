import logging
from multiprocessing import connection

from colorama import Cursor
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    connection = psycopg2.connect(host="uadproject3dbserver.postgres.database.azure.com",dbname="techconfdb",user="udaadmin@uadproject3dbserver",password="Matkhaulan#1")
    cur = connection.cursor()    

    try:
        # TODO: Get notification message and subject from database using the notification_id
        message_subject =  cur.execute
        (
            "select message, subject from notification where id = {};".format(notification_id) 
        )

        # TODO: Get attendees email and name
        cur.execute("select first_name, last_name, email from attendee")

        # TODO: Loop through each attendee and send an email with a personalized subject
        attendees = cur.fetchall()
        for attendee in attendees: 
            Mail('{},{},{}'.format({'admin@techconf.com'},{attendee[2]},{message_subject}))
        
        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        notification_sent_date = datetime.utcnow()
        notification_status = "Notified to {} attendees".format(len(attendees))
        cur.execute("update notification set status = '{}', completed_date = '{}' where id = {};".format(notification_status, notification_sent_date, notification_id))
        
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        connection.rollback()
    finally:
        # TODO: Close connection
        cur.close()
        connection.close()