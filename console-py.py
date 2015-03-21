"""Creates a custom Python Interpreter
Note: I can get this to work on google app engine by commenting out sh.interact()
and uncommenting sh.push and code = message.body"""
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from code import InteractiveConsole
import sys

class FileCacher:
    """Cache stdout text so we can analyze it before returning it."""
    def __init__(self):self.out = []
    def reset(self):self.out = []
    def write (self,line):self.out.append(line)
    def flush(self):
        output = ''.join(self.out)
        self.reset()
        return output

class Jonathan(InteractiveConsole):
    """Wrapper around Python that can filter output to the shell."""
    def __init__(self):
        self.stdout = sys.stdout
        self.stderr= sys.stderr
        self.cache = FileCacher()
        self.errcache = FileCacher()
        InteractiveConsole.__init__(self)
        self.output = ''
        return
    def get_output(self):
        sys.stdout = self.cache
        sys.stderr = self.errcache
    def return_output(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
    def push(self, line):
        self.get_output()
        InteractiveConsole.push(self, line)
        self.return_output()
        self.output = self.cache.flush()
        return self.output
        
sh = Jonathan()

class XMPPHandler(webapp.RequestHandler):
    def post(self):
            message = xmpp.Message(self.request.POST)
            output = sh.push(message.body)
            message.reply(output)
 

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("Working Awesomely Fine")

app = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler),('/',MainPage)],
                                     debug=True)
 
def main():
    run_wsgi_app(app)

   
    