import math
import random
import sys
import pygame

# AUTONOMOUS DRONE LANDING with a PID controller.
# the drone falls under gravity and gets pushed around by random wind. a PID
# controller works out how much thrust each side needs to keep it level and
# bring it down gently onto the landing pad. you can drag the pad with the
# mouse and the drone will chase it and land.

W, H = 900, 600
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("autonomous drone landing - PID control")
font = pygame.font.SysFont("consolas", 18)
clock = pygame.time.Clock()

GRAV = 0.18


class PID:
    # standard PID: reacts to the error, its buildup, and how fast its changing
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.prev = 0
        self.integral = 0

    def step(self, error):
        self.integral = max(-200, min(200, self.integral + error))  # clamp windup
        deriv = error - self.prev
        self.prev = error
        return self.kp * error + self.ki * self.integral + self.kd * deriv


# drone state
x, y = W / 2, 80
vx, vy = 0, 0
tilt = 0.0

pad_x = W / 2
pad_y = H - 40

# one PID for horizontal position, one for vertical descent, one to keep level
pid_x = PID(0.02, 0.0, 0.6)
pid_y = PID(0.05, 0.0, 0.8)
pid_level = PID(0.4, 0.0, 1.2)

landed = False
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
            pad_x = max(60, min(W - 60, e.pos[0]))  # drag the pad

    if not landed:
        # ---- the controller decides what to do ----
        ex = pad_x - x                      # how far off horizontally
        ey = (pad_y - 30) - y               # how far above the pad we want to be
        want_tilt = -pid_x.step(ex) * 0.04  # lean toward the pad
        want_tilt = max(-0.5, min(0.5, want_tilt))

        # vertical thrust to control the descent (aim for a slow drop)
        thrust = GRAV + pid_y.step(ey) * 0.02
        thrust = max(0, min(0.5, thrust))

        # level-out correction so it doesnt flip
        tilt += (pid_level.step(want_tilt - tilt)) * 0.02
        tilt = max(-0.6, min(0.6, tilt))

        # apply physics: thrust pushes opposite the tilt, gravity pulls down
        vx += thrust * tilt * 6
        vy += GRAV - thrust
        # random wind gusts
        vx += random.uniform(-0.04, 0.04)

        x += vx
        y += vy

        # touchdown check
        if y >= pad_y - 30 and abs(x - pad_x) < 50:
            landed = abs(vy) < 2.5  # only "landed" if it was a soft touchdown
            vy = 0
            vx *= 0.5

    screen.fill((15, 18, 28))

    # landing pad
    pygame.draw.rect(screen, (80, 200, 120), (pad_x - 50, pad_y, 100, 10))
    pygame.draw.line(screen, (40, 120, 70), (pad_x, pad_y), (pad_x, pad_y - 16), 2)

    # drone body (a tilted bar with two rotors)
    bx, by = 40 * math.cos(tilt), 40 * math.sin(tilt)
    left = (x - bx, y - by)
    right = (x + bx, y + by)
    pygame.draw.line(screen, (220, 220, 240), left, right, 6)
    pygame.draw.circle(screen, (240, 240, 80), (int(left[0]), int(left[1])), 7)
    pygame.draw.circle(screen, (240, 240, 80), (int(right[0]), int(right[1])), 7)

    # HUD
    msg = "LANDED softly!" if landed else f"vy {vy:+.1f}  tilt {tilt:+.2f}  err_x {pad_x-x:+.0f}"
    col = (120, 240, 150) if landed else (220, 220, 220)
    screen.blit(font.render(msg, True, col), (16, 16))
    screen.blit(font.render("drag to move the landing pad", True, (140, 150, 170)), (16, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
