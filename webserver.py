from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## Import sql functions needed for the database_helper
from sqlalchemy import create_engine, and_, asc, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

## Create session for DB connection.
from database_helper import *


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
    
        try:
        
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<form action='/restaurants/new' method='POST'\
                           enctype='multipart/form-data'>"
                output += "Restaurant name: <input type='text'\
                           name='newRestaurantName'>"
                output += "<input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
                
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html') 
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create new restaurant</a>"
                for e in session.query(Restaurant.name).group_by\
                    (Restaurant.name).order_by(asc(Restaurant.name)):
                    output += """<ul>%s""" % str(e[0])
                    output += """<li><a href="edit">Edit</a>"""
                    output += """<li><a href="delete">Delete</a>"""
                    output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
                
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>Hello!</body></html>"
                output += '''<form method='POST' enctype='multipart/form-data'\
                    action='/hello'><h2>What would you like me to say?</h2><input name="message"\
                    type="text" ><input type="submit" value="Submit"> </form>'''
                self.wfile.write(output)
                print output
                return
                
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>&#161Hola <a href = '/hello' >\
                    Back to Hello</a></body></html>"
                output += '''<form method='POST' enctype='multipart/form-data'\
                    action='/hello'><h2>What would you like me to say?</h2>\
                    <input name="message" type="text" ><input type="submit" \
                    value="Submit"> </form>'''
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
                output += "<html><body>"
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