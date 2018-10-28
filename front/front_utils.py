import conf

def path_to_image(type, image_folder=conf.images_folder):
    """
    :return: The image path corresponding to the given type.
    """
    if type == 'o':
        return image_folder + 'transporter.png'
    elif type == '\\':
        return image_folder + 'back_slash_mirror.png'
    elif type == '/':
        return image_folder + 'forward_slash_mirror.png'
    elif type == '#':
        return image_folder + 'square_mirror.png'
    elif type == '|':
        return image_folder + 'vertical_mirror.png'
    elif type == '-':
        return image_folder + 'horizontal_mirror.png'
    elif type == ' ':
        return image_folder + 'aether.png'
    print("Erreur : type d'objet inconnu.")
    return None