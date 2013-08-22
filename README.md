Livia
=====

Livia aims to make data collection and storage easy and fun. Livia aims to be as data agnostic as possible, allowing you to store anything from simple numerical data to complex structures, even images. This project defines the *Livia Server*, that accepts, stores, and retrieves data.

How it works
------------

The Livia server communicates most of its data using *JSON*. A logging computer, once registered to the server, posts logger metadata and a JSON string to the server. The datum is then stored in a *sqlite* database. Requests can then be made to the Livia server using a REST API to retrieve the data, or a subset of the data. On request, the data are compiled into a JSON string, in order to facititate further processing in a wide range of settings.

The livia server proudly uses
*Python 3.3
*Flask
*AngularJS
*Bootstrap
