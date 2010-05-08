from library import core
from library.stdmodules import scenemanager
from library.stdmodules.apps import basicapp
from library.stdmodules.apps import extendedapp
import objects

screen=core.core.video.get_screen()

class factory:
	def list(self,*arg): return arg
	def __getattr__(self, name):
		return getattr(getattr(objects, name), name)

factory = factory()

core.core.ticks = 40

app = extendedapp.ExtendedApp(factory)

sm = app.find('#SceneManager')

core.core.set_app(app)

sm.charge_and_change_scene("menu", "data/menu.xml")
sm.charge_and_change_scene("spot", "data/spot.xml")

core.core.start()