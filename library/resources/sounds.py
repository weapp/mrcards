def load_sound(name):
    """Carga un sonido a partir de un archivo.

    Si existe algun problema al cargar el sonido intenta crear
    un objeto Sound virtual."""

    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join("datos", name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'No se pudo cargar el sonido: ', fullname
        raise SystemExit, message

    return sound
