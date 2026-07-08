#!/usr/bin/env python3

import math


def inverse_kinematics(vx, vy, omega):

    radius = 0.14

    wl = (vx - 0.68*omega)/radius

    wr = ((-vx/2)-((math.sqrt(3)/2)*vy)-(0.68*omega))/radius

    wb = ((-vx/2)+((math.sqrt(3)/2)*vy)-(0.68*omega))/radius


    return wl, wr, wb

def main():

    vx = float(input("vx (m/s): "))
    vy = float(input("vy (m/s): "))
    omega = float(input("omega (rad/s): "))

    wl, wr, wb = inverse_kinematics(vx, vy, omega)

    print(f"\nLeft wheel  : {wl:.3f} rad/s")
    print(f"Right wheel : {wr:.3f} rad/s")
    print(f"Rear wheel  : {wb:.3f} rad/s")


if __name__ == "__main__":
    main()