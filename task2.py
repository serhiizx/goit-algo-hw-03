import sys
import turtle
import argparse

def koch_curve(t, level, size):
    if level == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, level - 1, size / 3)
            t.left(angle)


def koch_snowflake(t, level, size):
    for _ in range(3):
        koch_curve(t, level, size)
        t.right(120)


def draw_koch_snowflake(level, size=300):
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.pensize(2)
    t.speed(0)
    t.color("blue")
    
    t.penup()
    t.goto(-size / 2, 0)
    t.pendown()

    koch_snowflake(t, level, size)
    
    t.hideturtle() 
    window.mainloop()

def parse_args():
    parser = argparse.ArgumentParser(description="Draw Koch snowflake fractal.")
    parser.add_argument("level", type=int, nargs="?", default=3, help="Recursion level (default: 3)")
    parser.add_argument('-s', "--size", type=int, default=300, help="Snowflake size (default: 300)")

    args = parser.parse_args()

    if args.level < 0:
        parser.error("Level must not be nagative")

    return args

if __name__ == '__main__':
    try:
        args = parse_args()
        draw_koch_snowflake(args.level, args.size)
    except Exception as e:
        print(e)
        sys.exit(1)