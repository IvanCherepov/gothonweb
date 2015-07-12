import web
import map

urls = (
  '/game', 'GameEngine',
  '/','index'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

if web.config.get('_session') is None:
	store = web.session.DiskStore('sessions')
	session = web.session.Session(app, store,
									initializer = {'room': None})
	web.config._session = session
else:
	session = web.config._session

render = web.template.render('templates/', base ='layout')


class index(object):
    # def GET(self):
    # 	form = web.input(name="Nobody", greet = None)

    # 	if form.greet:
    #     	greeting = "%s, %s" % (form.greet, form.name)
    #     	return render.index(greeting = greeting)
    #     else:
    #     	return "ERROR: greet is required."
    def GET(self):
      session.room = map.START
      web.seeother("/game")

class GameEngine(object):

  def GET(self):
    if session.room:
      return render.show_room(room=session.room)
    else:
      return render.you_died()

  def POST(self):
    form = web.input(action=None)
    if session.room and session.room.go(form.action):
        session.room = session.room.go(form.action)
    web.seeother("/game")

if __name__ == "__main__":
    app.run()