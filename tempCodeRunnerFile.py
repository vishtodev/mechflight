    ob_x = screen_width
    ob_y = random.randint(200, g_limit - 40)

    # Load image properly
    img = pygame.image.load("obstacles.png").convert_alpha()

    # Get original size
    orig_w = img.get_width()
    orig_h = img.get_height()

    # Set desired width (adjust if needed)
    ob_w = 120

    # Maintain aspect ratio (IMPORTANT)
    scale_factor = ob_w / orig_w
    ob_h = int(orig_h * scale_factor)

    # Scale image correctly (no distortion)
    ob_img = pygame.transform.scale(img, (ob_w, ob_h))