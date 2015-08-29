from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## Import sql functions needed for the database_helper
from sqlalchemy import create_engine, and_, asc, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

## Create session for DB connection.
from database_helper import *

class generalStyling():
    """
    generalStyling takes the page specific stylings
    and the global page styling and puts them together
    cleanly.
    """
    def __init__(self):
        self.output = (
        """
        <head>
            <link href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
            <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
            <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
            <title>Catalogue Project</title>
        </head>
        <body>
            %s
        </body>        
        """ )
        
    def styler(self, pageSpecific):
        output = self.output % pageSpecific
        return output
        
        
class webServerHandler(BaseHTTPRequestHandler):
    """
    webServerHandler inherits from the python BaseHTTPRequestHandler library
    in order to do http requests.
    """
    def do_GET(self):
    
        try:
        
            ## EDIT
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = generalStyling().styler(
                    """
                       <form action='/edit' method='POST'
                       enctype='multipart/form-data'>
                       Rename restaurant: <input type='text'
                       name='newRestaurantName'>
                       <input type='submit' value='Submit'>
                       </form>
                    """)
                self.wfile.write(output)
                return
                
            ## NEW
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = generalStyling().styler(
                    """
                        <form action='/restaurants/new' method ='POST'
                        enctype='multipart/form-data'>
                        Restaurant name: <input type='text'
                        name='newRestaurantName'>
                        <input type='submit' value='Submit'>
                        </form>
                    """)
                self.wfile.write(output)
                return
                
            ## LIST RESTAURANTS
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html') 
                self.end_headers()
                pageSpecific = ""
                for e in session.query(Restaurant.name, Restaurant.id).group_by\
                    (Restaurant.name).order_by(asc(Restaurant.name)):
                    editName = str(e[0])
                    editID = str(e[1])
                    pageSpecific += (
                        """
                            <ul><h3>%s</h3>
                            <li><a href="%s/edit">Edit</a>
                            <li><a href="delete">Delete</a>
                            </ul>
                        """) % (str(e[0]), str(e[1]))
                output = generalStyling().styler(pageSpecific)
                self.wfile.write(output)
                print output
                return
                
            ## HELLO
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = generalStyling().styler(
                """ <h3>Hello!</h3>
                    <form method='POST' enctype='multipart/form-data'
                    action='/hello'><h2>What would you like me to say?</h2><input name="message"
                    type="text" ><input type="submit" value="Submit"> </form>
                """)
                self.wfile.write(output)
                print output
                return
                
            ## HOLA
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = generalStyling().styler(
                    """
                    <body>&#161Hola <a href = '/hello' >
                    Back to Hello</a></body></html>"
                    <form method='POST' enctype='multipart/form-data'
                    action='/hello'><h2>What would you like me to say?</h2>
                    <input name="message" type="text" ><input type="submit"
                    value="Submit"> </form>
                    """)
                self.wfile.write(output)
                print output
                return
                

                       
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
           
    def do_POST(self):
        try:
            # Create post in database
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('Content-type', 'text/html')) # Get contents of header name
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
            
            if self.path.endswith('/edit'): 
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('Content-type', 'text/html')) # Get contents of header name
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    currentName = session.query(Restaurant.name, Restaurant.id).filter_by(id=editID).one()
                    print currentName 
                    currentName.name = messagecontent
                    session.add(currentName) # Rename not working
                    session.commit()
                
                
                    
            if self.path.endswith('/hello'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data': # If content type is form data
                    # parse it. Return a dict of fieldnames and values
                    fields = cgi.parse_multipart(self.rfile, pdict) 
                    messagecontent = fields.get('message') # stores the content of message.

                output = ""
                output += "<html>"
                output += "<body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data'\
                    action='/hello'><h2>What would you like me to say?</h2>\
                    <input name="message" type="text" >
                    <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
            
        except:
            pass
        

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webServerHandler)
        print "Web server is running on port %s" % port
        server.serve_forever()
    
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()