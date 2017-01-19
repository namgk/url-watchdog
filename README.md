# url-watchdog
A url watchdog on Google App Engine

[![URL Watchdog](https://snag.gy/QBMiGp.jpg)](#features)

## Why?
You want to ping your web server periodically to recognize any downtime as soon as possible.

--> probably a "toy" version of <https://newrelic.com>

## How?
Google App Engine has a cron service that help you run a cron job with high availability if you don't own an expensive server.

This app setup a cron job in a GAE project, the job periodically calls upon an endpoint.

The endpoint executes some http requests to check up on provided urls.

The urls are stored in Google Datastore.

## More how?
Create a GAE project, setup GAE Python SDK on your local machine.

Clone the code and do "gcloud app deploy"
