def f():
    for i in range(1, 10):
        file = open(f'ZOV{i}.txt', '+w')
        file.write('GOIDA')
        file.close()