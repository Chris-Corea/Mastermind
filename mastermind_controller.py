
import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import sessions
import mastermind
from mastermind import Scores
class LoginHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
	self.redirect('/maingame')######
    login_url=users.create_login_url(self.request.uri)
    template_values={'loginurl': login_url}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'login1.html')
    self.response.out.write(template.render(path,template_values))


# main page appears on load
class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    sess = sessions.Session()
    # generate the secret code and store it in the session hash table
    sess['secret']=mastermind.generateSecret()
    guessFeedBackList=[]
    sess['guessFeedBackList']=guessFeedBackList
    #assign values for the welcome to get into HTML
    logout_url=users.create_logout_url('/')
    template_values={"logout": logout_url}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index1.html')
    self.response.out.write(template.render(path,template_values))

#controller for the new game button
class NewGameController(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    sess = sessions.Session()
    # generate the secret code and store it in the session hash table
    sess['secret']=mastermind.generateSecret()
    guessFeedBackList=[]
    sess['guessFeedBackList']=guessFeedBackList
    #assign values for the welcome to get into HTML
    logout_url=users.create_logout_url('/')
    template_values={"logout": logout_url}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index1.html')
    self.response.out.write(template.render(path,template_values))

class MMController(webapp.RequestHandler):
  def get(self):
    user=users.get_current_user()
    #remember to print instructions...create a template variable
    
    Welcome=str('Choose between red, green, blue, purple, orange, or yellow. Good Luck!')
    # get the secret code from the session hash table
    sess=sessions.Session()
    secret=sess['secret']
    guessFeedBackList=sess['guessFeedBackList']
    # get the guess from the user
    guess = []
    guess.append(self.request.get('color1'))
    guess.append(self.request.get('color2'))
    guess.append(self.request.get('color3'))
    guess.append(self.request.get('color4'))
    guessCopy=guess[:]
    secretCopy=secret[:]
    if mastermind.computeExacts(guessCopy, secretCopy) == 4:
        message = "Congratulations! Give yourself a pat on the back."
    else:
        message = ''
    # make sure there is a secret code
    if secret == None:
      secret = mastermind.generateSecret()
    sess['secret'] = secret
    secretCopy = secret[:]
    guessCopy = guess[:]
    sess['guessFeedBackList'] = guess
    sess['guess'] = guessFeedBackList

   # secret and guess
    exacts = mastermind.computeExacts(guessCopy,secretCopy)
    partials = mastermind.computePartials(guessCopy, secretCopy)
    guessStrList = "Your guess: " + str(guess) + ' ' + 'exacts: ' + str(exacts) + ' ' + 'partials: ' + str(partials)
    guessFeedBackList.append(guessStrList)
    sess['guessFeedBackList'] = guessFeedBackList
    logout_url = users.create_logout_url('/')
   # set up the template_values with guess and secret...eventually you'll want to show exact matches
    template_values = {'Welcome':str(Welcome), 'guess':str(guess), 'exacts':str(exacts), 'partials':str(partials),
                       'guessFeedBackList':guessFeedBackList, 'message': message, 'logout': logout_url}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__) , 'index1.html')
    self.response.out.write(template.render(path,template_values))

class ScoreHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    logout_url = users.create_logout_url('/')
    pquery=db.GqlQuery("Select * from Scores where user= :1" , user)
    score = pquery.fetch(10)
    if len(score) > 0:
      i = 0
      total = 0
      while i < len(scores):
        total = total + scores[i].numberGuesses
        i += 1
      x = total/len(scores)
    else:
      x = 0
    template_values={'x':x, 'user':user, 'score':score,'logout_url':logout_url}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'scorepage.html')
    self.response.out.write(template.render(path,template_values))

# create this global variable that represents the application and specifies which class
# should handle each page in the site
application = webapp.WSGIApplication(
					# MainPage handles the home load
          [('/', LoginHandler),
					('/maingame', MainPage),
					('/scoreIt', ScoreHandler),
					('/newgame', NewGameController),
					('/on_guess', MMController)],
          debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

