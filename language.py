import os.path
import gettext


TRANSLATION_DOMAIN = "mrcards"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "mo")

#gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)
#en windows no encuentra el lenguaje
gettext.translation(TRANSLATION_DOMAIN, localedir=LOCALE_DIR ,languages=['es']).install()
