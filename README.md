# Famous Twin #

This is a Web application where users can enter the day, month, _and year_ to see a list of famous people born on that exact same date. The data is collected from the Births sections on Wikipedia's day pages, [like this](https://en.wikipedia.org/wiki/October_29#Births).

But this is really just a way for me to learn and play around with some cool technologies.

## Technology Stack ##

* Python script scrapes Wikipedia using [mwclient](http://sourceforge.net/projects/mwclient/).
* Birthday data stored in MongoDB. (Although right now it's just a JSON file and resides in memory when app server is running.)
* Node.js service for serving birthday requests via JSONP calls.
* jQuery and Knockout JavaScript libraries in the front end.

## Instructions ##

### Prerequisites ###

* Python 2.7
* Node 0.6.19+


### Set Up ###

1. pip install mwclient

**more TBD**