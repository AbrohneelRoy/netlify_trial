import turtle as t

List = ["red", "yellow", "green", "white", "cyan", "orange"]

t.bgcolor("black")
t.speed(0)
for i in range(300):
    t.color(List[i % 6])
    t.forward(i)
    t.left(59)



t.done()
