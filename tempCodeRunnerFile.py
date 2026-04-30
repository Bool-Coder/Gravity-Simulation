    if len(planets) > 80:
            show_trails = False

        for i in range(len(planets) - 1):
            for j in range(i + 1, len(planets)):
                apply_gravity(planets[i], planets[j])

        for p in planets:
            update_position(p, show_trails)
        
        update_collisions(planets)
        if show_trails:
            for p in planets:
                p.draw_trail(screen)
        for p in planets:
            p.draw(screen)

        # 🔹 UI BOXES
        mass_box.draw(screen)
        radius_box.draw(screen)

        # 🔹 LABELS (restored)
        screen.blit(font.render("Mass kg", True, WHITE), (10, 45))
        screen.blit(font.render("Radius px", True, WHITE), (100, 45))
        screen.blit(font.render(f"FPS: {int(fps)}", True, WHITE), (WIDTH - 100, 10))
        screen.blit(font.render(f"Zoom: {camera.zoom:.2f}", True, WHITE), (WIDTH - 100, 30))
        screen.blit(font.render("R reset", True, WHITE), (10, 85))
        screen.blit(font.render("Q orbits on/off", True, WHITE), (10, 105))
        screen.blit(font.render(f"Planets: {len(planets)}", True, WHITE), (10, 125))

        mouse_world_x, mouse_world_y = camera.screen_to_world(*pygame.mouse.get_pos())
        pos_text = font.render(f"X: {mouse_world_x:.1f} Y: {mouse_world_y:.1f}", True, WHITE)
        screen.blit(pos_text, (10, HEIGHT - 30))

        
        if dragging:
            sx1, sy1 = camera.world_to_screen(*drag_start)
            sx2, sy2 = camera.world_to_screen(*drag_end)

            pygame.draw.circle(screen, WHITE, (sx1, sy1), 5)
            pygame.draw.line(screen, WHITE, (sx1, sy1), (sx2, sy2), 2)

            dx = drag_start[0] - drag_end[0]
            dy = drag_start[1] - drag_end[1]
            speed = math.sqrt(dx * dx + dy * dy) * 0.5

            screen.blit(font.render(f"v = {speed:.5f} px/s", True, WHITE), (sx1 + 10, sy1 + 10))