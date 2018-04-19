# Web Protocols


## Instructions

Your goal for this week is to extend the simple web server that we created in class to serve files from the file system.
Once you're done, you should be able to start the web server inside the homework directory using python http_server.py and then point your web browser at locations like

http://localhost:10000/sample.txt.
http://localhost:10000/a_web_page.html , or 
http://localhost:10000/images/sample_1.png . 

and see the corresponding file located under /webroot. Take a moment to look into the /webroot and see these files. Then find and complete the TODO items in the homework.

Mapping Mime-types
When writing the resolve_uri function, there is a standard library that can help you guess the correct mimetype for any given file. We can guess the mime-type of a file based on the filename or map a file extension to a type:

>>> import mimetypes
>>> mimetypes.guess_type('file.txt')
('text/plain', None)
>>> mimetypes.types_map['.txt']
'text/plain'
This library might incorrectly guess the mimetype of the python file in the webroot. If you have a test which fails because of the mimetype of the python file, then you might make a special case for it in your resolve_uri function.

How to Know When You're Done
Try starting up your server, and visiting the following pages:

http://localhost:10000/sample.txt (Links to an external site.)Links to an external site.
You should see the contents of the sample.txt that's in the webroot directory

 (Links to an external site.)Links to an external site.http://localhost:10000/a_web_page.html
 (Links to an external site.)Links to an external site.You should see a web page.

http://localhost:10000/ (Links to an external site.)Links to an external site.
You should see a list of all of the files inside of the webroot directory

http://localhost:10000/some_page_that_doesnt_exist.html (Links to an external site.)Links to an external site.
You should get a 404 error

http://localhost:10000/images/sample_1.png (Links to an external site.)Links to an external site. 
You should see the sample_1.png image that's inside of the webroot/images directory

You can also run the included tests by opening two terminal windows: use Python to run the server in one window and the tests in the other.
