# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource            | Service Tier | Monthly Cost |
| *Azure Postgres Database* | Basic        |     35.32    |
| *Azure Service Bus*       | Basic        |     0.05     |
| *Azure Functions*         | Consumption  |      0       |
| *Azure App Service*       | Free         |      0       |
| *Storage Account*         | Basic V1     |     52.2     |

Refer to the image in screenshot folder for more details.

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

Azure App Service is a powerful web application hosting platform. Azure Functions, built on top of the App Service infrastructure, enables you to easily build serverless and event-driven compute workloads.

This app is ligthweight and doesn't need a lot of computing power as well as the deployment is not too complicated. It also support both microservices and service bus. Azure App Service in Free tier is enough to run this app.

PostgreSQL is an advanced, enterprise-class, and open-source relational database system. PostgreSQL supports both SQL (relational) and JSON (non-relational) querying. Small data size and not many transactions so Basic Tier is enough

Service Bus : Data is transferred between different applications and services using messages.Flow : create a client from Service Bus connection string, create a service bus message, open a single connection, send the supplied message and close connection

Azure Function : It is triggered by Service Bus message. Decrypt message body and use SendGrid to send email with that subject and message. In this case, Consumption Tier is enough.

--- Change Request ---

Drawbacks of Previous architecture : 
- Based on scenario there are 1000 attendees the user must wait on the notification page until all attendees are notified. Need tell request library to stop waiting for response after a given amount of time by passing a number to "timeout" parameter. If forget or not set timeout when call api so can make your program to hang indefinitely.If no "timeout" is specificed explicitly, requests do not time out. It make users like endless time. Hence to resolve the above-mentioned timeout issue, we use the Azure function.

Advantages of the current architecture: 
- Azure function is used for decoupling the web app for sending mail.The web app triggers the queue and the function fetches the notification id from the queue and processes the mail triggering function. After that it is triggered by Service Bus message.Decode message body to get message and then use Sengrid to send mail.

- Service Bus is used for decoupling the web app for sending mail. Create a client from Service Bus connection string, create a service bus message, open a single connection, send the supplied message and close connection

- This app is ligthweight and doesn't need a lot of computing power. so it make sense to deploy via App service. Function app support microservices as well as runs the bakcground job Service Bus very well

- PostgreSQL supports both SQL (relational) and JSON (non-relational) querying.