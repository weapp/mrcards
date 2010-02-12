from library import core
from library.stdmodules import scenemanager
from library.stdmodules.apps import basicapp
import factory

from library.stdmodules.apps import extendedapp

core.core.ticks = 40

app = extendedapp.ExtendedApp(factory)

sm = app.find('#SceneManager')

core.core.set_app(app)

sm.charge_and_change_scene("menu", "menu.xml")
sm.charge_scene("menu2", "menu2.xml")
sm.charge_scene("menu3", "menu3.xml")

core.core.start()