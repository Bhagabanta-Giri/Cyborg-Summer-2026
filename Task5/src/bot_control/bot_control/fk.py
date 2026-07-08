#!/usr/bin/env python3

import math

def forward_kinematics(omega_left, omega_right, omega_rear):

    radius = 0.14

    vx = (radius / 3) * (2 * omega_left - omega_right - omega_rear)
    vy = (radius / math.sqrt(3)) * (omega_rear - omega_right)
    omega = -(radius / 2.04) * (omega_left + omega_right + omega_rear)

    return vx, vy, omega

def main():

    wl = float(input("Left wheel (rad/s): "))
    wr = float(input("Right wheel (rad/s): "))
    wb = float(input("Rear wheel (rad/s): "))

    vx, vy, omega = forward_kinematics(
        wl,
        wr,
        wb
    )

    print(f"\nvx     : {vx:.3f} m/s")
    print(f"vy     : {vy:.3f} m/s")
    print(f"omega  : {omega:.3f} rad/s")


if __name__ == "__main__":
    main()