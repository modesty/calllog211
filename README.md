# CallLog211

## A RESTful Web Service Python Starter Project on Google App Engine

This project is an application skeleton and working example for a typical RESTful Web Service project on 
[Google Cloud Platform](https://cloud.google.com/). You can use it to quickly bootstrap the server side of 
[Service Oriented HTML Application (SOHA)](http://www.codeproject.com/Articles/118683/SOHA-Service-Oriented-HTML-Application-Concepts-an) 
applications and dev environment for these projects.

The seed contains dependency Python libraries, one API endpoint and a bunch of scripts all pre-configured 
for instant data persistence development gratification. Just clone the repo (or download the zip/tarball), 
[get a project id from Google](https://developers.google.com/cloud/),
[activate Google Cloud Datastore](https://developers.google.com/datastore/docs/activate),
start up [Google App Engine App Launcher](https://developers.google.com/appengine/downloads),
and you are ready to develop and test your RESTful API.

The seed app doesn't do much, it implements one endpoint that takes and validates a HTTP POST request, 
then save the data to [Google Cloud Datastore - Google's version of NoSQL cloud data storage](https://developers.google.com/datastore/).
This project shows how to set up 3rd party Python libraries for [Google App Engine](https://developers.google.com/appengine/),
how to structure your source code, how to validate data from request, how to handle exceptions and 
how to response with a customized response JSON object.

_Note: This project is intended to serve as a seed project to develop RESTful Web Service with specific 
Python frameworks and libraries (more on this later), it does not has a full fledged CRUD sample code 
with NDB, although it can be added later on._

## Up and running

To run this project in your local development environment, clone the repository first, then edit app.yaml by replacing `<Your Google Cloud Poject ID>` with your own Google App Engine project ID, in terminal, run:
 
 
    `cd <your-project-clone-directory>`
    
    `dev_appserver.py .`

## What it is built with

There are many options to built RESTful web service in Python on Google App Engine, I've evaluated 
[Django](https://www.djangoproject.com/), [Django REST framework](http://www.django-rest-framework.org/),
[Google Cloud Endpoints](https://developers.google.com/appengine/docs/java/endpoints/), since all I need
is a lightweight, easy to use and plug-able RESTful-only framework, I eventually landed on the following
stack:

### Flask-RESTful

[Flask-RESTful](https://github.com/twilio/flask-restful) provides a lightweight abstraction for building
RESTful service, it's an extension for [Flask](http://flask.pocoo.org/) and has all the bells and whistles
to quickly get a RESTful service up and running on Google App Engine. 

All dependencies of Flask-RESTful and dependencies of dependencies are packaged up in `lib` directory,
including:

* aniso8601
* flask
* pytz
* werkzeug
* itsdangerous

### RESTful building blocks

Although [Flask-RESTful](https://github.com/twilio/flask-restful) has provided an excellent starting point
for all sorts of RESTful service building blocks, like useful decorators, Resource base class, easy API routes,
request parsing and validation, error handing, etc., there always are opportunities to add more utilities and
helper functions to make it more suitable to your specific project. To be as much as generic as possible, I
also include the following building blocks in the `api/common` directory:

* response.py: two base classes to structure all response in a unified form
* session.py: utilize Google App Engine's memcache to validate a session
* util.py: lots of utilities methods mainly around data types and ndb model processes
* validators: validator types that works with [ReqParse](http://flask-restful.readthedocs.org/en/latest/api.html#module-reqparse)
* [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS): I was trying to use Flask-RESTful
 built-in support for [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS), but when I tested
 it with HTTP OPTIONS, it returns HTTP 200 without access control headers. So I commented out decorators code,
 and implemented OPTIONS in CallLogAPI.py. I should revisit this issue later...

And lots more! Clone it and start to hack!


### Configurations for Google App Engine

Since Flask-RESTful is not included in Google App Engine by default, we need to configure our project to make
it 'Cloud Ready'. All the necessary libraries, source trees and scripts/yaml are included:

* lib: this directory includes all the 3rd party Python libraries that Flask-RESTful requires, no special
installation commandline to run, just clone or copy the entire directory, it's ready to go
* app.yaml: Google App Engine requires app.yaml to run your project, since this project is a backend
 example of [SOHA](http://www.codeproject.com/Articles/118683/SOHA-Service-Oriented-HTML-Application-Concepts-an),
 architecture, this file is essentially empty: it only includes two other yaml files to ensure the front-end
 is separated from back-end, these two other yaml files are:
    - web_app.yaml: this is a fork of yaml that enables hosting a static site on Google App Engine. This seed
 project does not have UI front-end, this yaml is provided for future reference
    - web_api.yaml: this yaml tells Google App Engine which Python class to load to run RESTful service if
 the request path matches `/api/*`
* appengine_config.py: this config file is the key to use Python modules underneath `lib` directory
* data.datastore: optional data file for local testing, it requires `--datastore_path=<Your Clone Path>/data.datastore`
commandline arguments when run the project on localhost.
* api/config.py: some API level configuration constants and variables are defined here, including:
    - session time span
    - datastore version string
    - api base url for version management
    - application version, etc.

### Run and deploy the project

Google has excellent documentation on [how to run on local development server](https://developers.google.com/appengine/docs/python/tools/devserver),
and also [how to deploy and manage your app on App Engine](https://developers.google.com/appengine/docs/python/tools/uploadinganapp).
You can also reference [Python tutorial](https://developers.google.com/appengine/docs/python/gettingstartedpython27/introduction) for more details.

### Test the API

Here are some sample `curl` command to test the API in terminal. When testing after deployment, simply replace
`http://127.0.0.1:8080` with `http://<your_google_project_id>.appspot.com`:

    curl -isv -H "Content-Type: application/json" -X POST -d '{"name":"modesty zhang", "zip":"92129"}' http://127.0.0.1:8080/api/v1.0/calllog/

It should return HTTP 400 Bad Request with:

    {"message": "Missing required parameter callReason in json or the post body or the query string"}    

The above `curl` command line shows how the service responds when required fields not found in request body.

The following `curl` command should return a HTTP 200 OK:

    curl -isv -H "Content-Type: application/json" -X POST -d '{"name":"modesty zhang", "zip":"92129", "callReason": "GAE RESTful sample", "location": "Google Cloud Platform", "phone": "8588889999"}' http://127.0.0.1:8080/api/v1.0/calllog/
    
The response body is structured by `common/response.py` and returns with datastore newly created entity id:

    {
        "result": {
            "created": "2014-07-20 01:32:43", 
            "id": 5655612935372800
        }, 
        "status": {
            "code": 200, 
            "message": "OK"
        }
    }

### Receiving updates from upstream

When we upgrade this repo with newer python code or testing library code, you can just
fetch the changes and merge them into your project with git.


## Contact

For more information on more advanced RESTful services with [Python NDB API](https://developers.google.com/appengine/docs/python/ndb/), 
please check out https://cloud.google.com/, or leave me a message in [GitHub](https://github.com/modesty).
