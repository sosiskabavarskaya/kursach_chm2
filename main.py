from math import sin

# Константы и НУ для диффура и расчетов
a = 0
b = 10
h = 0.005
# h /= 2
# h /= 2
# h /= 2
# h /= 2
# L0 = 2.3
y_0 = 3.1
dy_0 = 0
COUNT = int((b - a) / h)
L = 10
A = 0.5
g = 386
w = 5.3



def write_to_file(x, y, dy, ddy, count, filename, mode):
    # Запись в файл
    f = open(f'{filename}.txt', mode)
    f1 = open(f'{filename}-1.txt', mode)
    f2 = open(f'{filename}-2.txt', mode)
    f.write("{")
    f1.write("{")
    f2.write("{")
    for i in range(count):
        if i > 0:
            f.write(", ")
            f1.write(", ")
            f2.write(", ")
        f.write('{' + str(x[i]) + ', ' + str(y[i]) + '}')
        f1.write('{' + str(x[i]) + ', ' + str(dy[i]) + '}')
        f2.write('{' + str(x[i]) + ', ' + str(ddy[i]) + '}')
    f.write('}\n')
    f1.write('}\n')
    f2.write('}\n')

    f.close()
    f1.close()
    f2.close()


def f_ddy(x, y):
    # Начальный дифур
    return (3 / (2 * L)) * (g - A * w * sin(w * x)) * sin(y)

def Eiler():
    # Метод Эйлера - на сетке Х находит решение диффура в 
    x = [0 for _ in range(COUNT)]
    y = [0 for _ in range(COUNT)]
    dy = [0 for _ in range(COUNT)]
    ddy = [0 for _ in range(COUNT)]

    x[0] = a
    y[0] = y_0
    dy[0] = dy_0
    for i in range(COUNT - 1):
        # Поиск решений dy, y. ddy мы знаем, тк изначально задан дифур второго порядка, но все равно считаем для поиска решений
        x[i + 1] = x[i] + h
        ddy[i] = f_ddy(x[i], y[i])
        dy[i + 1] = dy[i] + h * ddy[i]
        y[i + 1] = y[i] + h * dy[i]
    write_to_file(x, y, dy, ddy, COUNT,'eiler_output', 'w')

def f1(x, u1, u2):
    return u2

def f2(x, u1, u2):
    return (3 / (2 * L))* (g - A * w * sin(w * x))* sin(u1)

#  1 порядок \/

def K1_f1_1(x, u1, u2):
    return f1(x, u1, u2)

def K1_f2_1(x, u1, u2):
    return f2(x, u1, u2) 

# 2 порядок \/

def K1_f1_2(x, u1, u2):
    return f1(x, u1, u2)

def K1_f2_2(x, u1, u2):
    return f2(x, u1, u2)

def K2_f1_2(x, u1, u2):
    return f1(x + h, u1 + h * K1_f1_2(x, u1, u2), u2 + h * K1_f2_2(x, u1, u2))

def K2_f2_2(x, u1, u2):
    return f2(x + h, u1 + h * K1_f1_2(x, u1, u2), u2 + h * K1_f2_2(x, u1, u2))

# 3 порядок \/

def K1_f1_3(x, u1, u2):
    return f1(x, u1, u2)

def K1_f2_3(x, u1, u2):
    return f2(x, u1, u2)

def K2_f1_3(x, u1, u2):
    return f1(x + (h / 2), u1 + h * K1_f1_3(x, u1, u2) / 2, u2 + h * K1_f2_3(x, u1, u2) / 2)

def K2_f2_3(x, u1, u2):
    return f2(x + (h / 2), u1 + h * K1_f1_3(x, u1, u2) / 2, u2 + h * K1_f2_3(x, u1, u2) / 2)

def K3_f1_3(x, u1, u2):
    return f1(x + h, u1 - h * K1_f1_3(x, u1, u2) + 2 * h * K2_f1_3(x, u1, u2), u1 - h * K1_f2_3(x, u1, u2) + 2 * h * K2_f2_3(x, u1, u2))

def K3_f2_3(x, u1, u2):
    return f2(x + h, u1 - h * K1_f1_3(x, u1, u2) + 2 * h * K2_f1_3(x, u1, u2), u1 - h * K1_f2_3(x, u1, u2) + 2 * h * K2_f2_3(x, u1, u2))
# 4 порядок \/

def K1_f1(x, u1, u2):
    return f1(x, u1, u2)

def K1_f2(x, u1, u2):
    return f2(x, u1, u2)

def K2_f1(x, u1, u2):
    return f1(x + (h / 2), u1 + (h / 2) * K1_f1(x, u1, u2), u2 + (h / 2) * K1_f2(x, u1, u2))

def K2_f2(x, u1, u2):
	return f2(x + (h / 2), u1 + (h / 2) * K1_f1(x, u1, u2), u2 + (h / 2) * K1_f2(x, u1, u2))

def K3_f1(x, u1, u2):
    return f1(x + (h / 2), u1 + (h / 2) * K2_f1(x, u1, u2), u2 + (h / 2) * K2_f2(x, u1, u2))

def K3_f2(x, u1, u2):
	return f2(x + (h / 2), u1 + (h / 2) * K2_f1(x, u1, u2), u2 + (h / 2) * K2_f2(x, u1, u2))

def K4_f1(x, u1, u2):
    return f1(x + (h / 2), u1 + (h / 2) * K3_f1(x, u1, u2), u2 + (h / 2) * K3_f2(x, u1, u2))

def K4_f2(x, u1, u2):
	return f2(x + (h / 2), u1 + (h / 2) * K3_f1(x, u1, u2), u2 + (h / 2) * K3_f2(x, u1, u2))


def function_for_convergence(order):
    global h
    global COUNT
    for i in range(5):
        Runge_Kutte(order, write_mode='a')
        h = h / 2
        COUNT = int((b - a) / h)

def Runge_Kutte(order=4, write_mode='w'):
    # Метод Рунге Кутта 
    x = [0 for _ in range(COUNT)]
    y = [0 for _ in range(COUNT)]
    dy = [0 for _ in range(COUNT)]
    ddy = [0 for _ in range(COUNT)]

    x[0] = a
    y[0] = y_0
    dy[0] = dy_0
    
    if (order == 4):
        for i in range(COUNT - 1):
            x[i + 1] = x[i] + h
            ddy[i] = (K1_f2(x[i], y[i], dy[i]) + 2 * K2_f2(x[i], y[i], dy[i]) + 2 * K3_f2(x[i], y[i], dy[i]) + K4_f2(x[i], y[i], dy[i])) / 6
            # ddy[i] = (K1_f1)
            dy[i + 1] = dy[i] + h * ddy[i]
            y[i + 1] = y[i] + h * (K1_f1(x[i], y[i], dy[i]) + 2 * K2_f1(x[i], y[i], dy[i]) + 2 * K3_f1(x[i], y[i], dy[i]) + K4_f1(x[i], y[i], dy[i])) / 6
    elif (order == 3):
        for i in range(COUNT - 1):
            x[i + 1] = x[i] + h
            ddy[i] = (K1_f2_3(x[i], y[i], dy[i]) + 4 * K2_f2_3(x[i], y[i], dy[i]) + K3_f2_3(x[i], y[i], dy[i])) / 6
            dy[i + 1] = dy[i] + h * ddy[i]
            y[i + 1] = y[i] + h * (K1_f1_3(x[i], y[i], dy[i]) + 4*K2_f1_3(x[i], y[i], dy[i]) + K3_f1_3(x[i], y[i], dy[i])) / 6
    elif (order == 2):
        for i in range(COUNT - 1):
            x[i + 1] = x[i] + h
            ddy[i] = K2_f2_2(x[i], y[i], dy[i])
            dy[i + 1] = dy[i] + h * ddy[i]
            y[i + 1] = y[i] + h * K2_f1_2(x[i], y[i], dy[i])
    elif (order == 1):
        for i in range(COUNT - 1):
            x[i + 1] = x[i] + h
            ddy[i] = f2(x[i], y[i], dy[i])
            dy[i + 1] = dy[i] + h * ddy[i]
            y[i + 1] = y[i] + h * f1(x[i], y[i], dy[i])
    if write_mode == 'a':
        write_to_file(x, y, dy, ddy, COUNT, f'all-runge-order{order}', write_mode)
    else:
        write_to_file(x, y, dy, ddy, COUNT, f'runge-order{order}', write_mode)


if __name__ == "__main__":
    order = input('Order???\n> ')
    order = int(order)
    mode = input('ALL MODE OR NOT ALL??? (1 or 2)\n> ')
    mode = int(mode)
    if mode == 1:
        function_for_convergence(order=order)
    else:
        Runge_Kutte(order=order)
