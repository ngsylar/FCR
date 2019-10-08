#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import pacotinho.map
import pacotinho.grid
import tf
import math
import time
import sys
import os

# sensores e odometria
laser = ()
sonarf = ()
x = 0.0
y = 0.0
z = 0.0

# correcao da odometria (precisa ser modificado com as coordenadas do ponto 1 no stage)
corx = -55.0
cory = -60.0

# modo de execucao (rapido ou preciso)
mode = 0

# ------------------------------------------------------------------------------
# funcoes do sistema

dl = 0
dr = 0

tmex = 0        # tempo execucao
loading = 1     # carregamento
def progressBar(value, endvalue, bar_length):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

# ------------------------------------------------------------------------------
# funcoes de dados ROSPY

def odom_call(data):
    global x, y, z, corx, cory, loading, tmex

    x = data.pose.pose.position.x - corx
    y = data.pose.pose.position.y - cory
    quaternion = (
        data.pose.pose.orientation.x,
        data.pose.pose.orientation.y,
        data.pose.pose.orientation.z,
        data.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    z = yaw
    # if loading == 0:
    #     print ' '
    #     print 'instant {0}'.format(tmex)
    #     print 'x: {0}'.format(x)
    #     print 'y: {0}'.format(y)
    #     print 'z: {0}'.format(z)
    #     tmex = tmex + 1

def laser_call(data):           # comeca pelo lado direito
    global laser
    laser = data.ranges
    # if loading == 0:
    #     print(len(laser))
    #     for i in range(0, 270):
    #         print '{0}: {1}'.format(i, laser[i])

def sonarf_call(data):         # recebe dados do sonar
    global sonarf
    sonarf = data.ranges       # salva dados em sonarf
    # if loading == 0:
    #     print(len(sonarf))
    #     for i in range(0, 10):
    #         print '{0}: {1}'.format(i, sonarf[i])

# ------------------------------------------------------------------------------
# funcoes de posicionamento

def inside_polygon(x, y, points):
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def placenode(x, y, graph):
    i = 1
    points = graph[i].area
    while (i != len(graph)) and (not inside_polygon(x, y, points)):
        i = i + 1
        if i != len(graph):
            points = graph[i].area
        else:
            print ' '
            print 'Local inexistente!'
    return i

def placegrid(posx, posy, drawn, graph):
    i = 0
    j = drawn[i]
    points = graph[j].area
    while (i != len(drawn)) and (not inside_polygon(posx, posy, points)):
        i = i + 1
        if i != len(drawn):
            j = drawn[i]
            points = graph[j].area
        else:
            print ' '
            print 'Local inexistente!'

    place = []
    place.append(j)
    place.append(i)
    return place

def pos_quad(z):

    if z == 0:
        quad = 0
    elif (math.pi)/2 >= z and z > 0:
        quad = 1
    elif math.pi >= z and z > (math.pi)/2:
        quad = 2
    elif 0 > z and z > -(math.pi)/2:
        quad = 4
    else:
        quad = 3

    return quad

def pos_diag():
    global z

    if -3*(math.pi)/4 <= z and z < -(math.pi)/4:
        diag = 4
    elif -(math.pi)/4 <= z and z < (math.pi)/4:
        diag = 1
    elif (math.pi)/4 <= z and z < 3*(math.pi)/4:
        diag = 2
    else:
        diag = 3

    return diag

def calc_ang(posx, posy):
    global x, y

    tanx = posx - x
    tany = posy - y
    angz = math.atan2(tany, tanx)
    # print 'tanx: {0}'.format(tanx)
    # print 'tany: {0}'.format(tany)
    # print 'angz: {0}'.format(angz)
    return angz

# ------------------------------------------------------------------------------
# funcoes angulares

def adjust_angle_right(vel, vel_msg, angz):
    global z

    while ((angz + 0.003) < z or z < (angz - 0.003)):
        vel_msg.angular.z = -abs(angz - z)
        vel.publish(vel_msg)
    vel_msg.angular.z = 0
    vel.publish(vel_msg)

def adjust_angle_left(vel, vel_msg, angz):
    global z

    while ((angz + 0.003) < z or z < (angz - 0.003)):
        vel_msg.angular.z = abs(angz - z)
        vel.publish(vel_msg)
    vel_msg.angular.z = 0
    vel.publish(vel_msg)

def adjust_angle(vel, vel_msg, posx, posy):
    global z

    quad = pos_quad(z)
    angz = calc_ang(posx, posy)

    if angz == 0:
        if quad == 1 or quad == 2:
            adjust_angle_right(vel, vel_msg, angz)
        else:
            adjust_angle_left(vel, vel_msg, angz)
    elif angz > 0:
        if quad == 0:
            adjust_angle_left(vel, vel_msg, angz)
        elif quad == 1 or quad == 2:
            if z > angz:
                adjust_angle_right(vel, vel_msg, angz)
            else:
                adjust_angle_left(vel, vel_msg, angz)
        else:
            case1 = angz + abs(z)
            case2 = 2*(math.pi) - case1
            if case1 < case2:
                adjust_angle_left(vel, vel_msg, angz)
            else:
                adjust_angle_right(vel, vel_msg, angz)
    else:
        if quad == 0:
            adjust_angle_right(vel, vel_msg, angz)
        elif quad == 3 or quad == 4:
            if z < angz:
                adjust_angle_left(vel, vel_msg, angz)
            else:
                adjust_angle_right(vel, vel_msg, angz)
        else:
            case1 = z + abs(angz)
            case2 = 2*(math.pi) - case1
            if case1 < case2:
                adjust_angle_right(vel, vel_msg, angz)
            else:
                adjust_angle_left(vel, vel_msg, angz)

def adjust_dl(vel, vel_msg):
    global dl, dr

    while sonarf[3] < 1.3 or sonarf[4] < 1.3 or sonarf[5] < 1.3:
        #print('dl_in1')
        vel_msg.angular.z = 1
        vel.publish(vel_msg)
    while sonarf[0] > 1.3 and sonarf[1] > 1.3:
        #print('dl_in2')
        vel_msg.angular.z = 1
        vel.publish(vel_msg)
    vel_msg.angular.z = 0
    vel.publish(vel_msg)

    dl = 1
    dr = 0

def adjust_dr(vel, vel_msg):
    global dl, dr

    while sonarf[4] < 1.3 or sonarf[5] < 1.3 or sonarf[6] < 1.3:
        #print('dr_in1')
        vel_msg.angular.z = -1
        vel.publish(vel_msg)
    while sonarf[9] > 1.3 and sonarf[8] > 1.3:
        #print('dr_in2')
        vel_msg.angular.z = -1
        vel.publish(vel_msg)
    vel_msg.angular.z = 0
    vel.publish(vel_msg)

    dl = 0
    dr = 1

# ------------------------------------------------------------------------------
# funcoes de navegacao e mapeamento

def showme(matrix, matsize, thegrid, thesize, graph):
    global x, y

    clear()
    place = placenode(x, y, graph)
    gx = int(((matsize/2) + (corx*2) + (x*2)) - 1)
    gy = int(((matsize/2) + (cory*2) + (y*2)) - 1)
    print '\nPonto atual no mapa topologico: {0}'.format(place)
    print 'Posicao na grade de ocupacao: [{0}][{1}]'.format(gx, gy)

    gx_s = gx - (thesize/2)
    gy_s = gy - (thesize/2)
    gx_f = gx + (thesize/2)-1
    gy_f = gy + (thesize/2)-1
    # print 'gx_s {0} gx_f {1}'.format(gx_s, gx_f)
    # print 'gy_s {0} gy_f {1}'.format(gy_s, gy_f)

    i = 0
    ig = gx_s
    while ig <= gx_f:
        j = 0
        jg = gy_s
        while jg <= gy_f:
            # print 'i {0} j {1}'.format(i, j)
            # print 'ig {0} jg {1}'.format(ig, jg)
            if (0 <= ig and ig < matsize) and (0 <= jg and jg < matsize):
                thegrid[i][j] = matrix[ig][jg]
            jg = jg + 1
            j = j + 1
        ig = ig + 1
        i = i + 1
    thegrid[(thesize/2)-1][(thesize/2)-1] = -1

    j = thesize - 1
    while j >= 0:
        for i in range (0, thesize):
            if thegrid[i][j] == -1:
                sys.stdout.write('P ')
            elif thegrid[i][j] == 5:
                sys.stdout.write('. ')
            elif thegrid[i][j] >= 10:
                sys.stdout.write('# ')
            elif thegrid[i][j] == 0:
                sys.stdout.write('  ')
            else:
                sys.stdout.write('{0} '.format(thegrid[i][j]))
            sys.stdout.flush()
        sys.stdout.write('\n')
        sys.stdout.flush()
        j = j - 1

def runner(vel, vel_msg, posx, posy, matrix, matsize, sector, secsize, graph):
    global x, y, z, dl, dr

    stopped = 0
    adjust_angle(vel, vel_msg, posx, posy)
    while ((posx + 2) < x or x < (posx - 2)) or ((posy + 2) < y or y < (posy - 2)):
        showme(matrix, matsize, sector, secsize, graph)
        vel_msg.linear.x = 1
        vel_msg.angular.z = 0
        vel.publish(vel_msg)

        if sonarf[4] < 1.3 or sonarf[5] < 1.3:
            vel_msg.linear.x = 0
            vel.publish(vel_msg)
            diag = pos_diag()
            angz = calc_ang(posx, posy)

            if diag == 4:
                #print('case4')
                if -(math.pi)/2 <= angz and angz < (math.pi)/2:
                    adjust_dl(vel, vel_msg)
                else:
                    adjust_dr(vel, vel_msg)
            elif diag == 1:
                #print('case1')
                if 0 <= angz and angz < math.pi:
                    adjust_dl(vel, vel_msg)
                else:
                    adjust_dr(vel, vel_msg)
            elif diag == 2:
                #print('case2')
                if -(math.pi)/2 <= angz and angz < (math.pi)/2:
                    adjust_dr(vel, vel_msg)
                else:
                    adjust_dl(vel, vel_msg)
            else:
                #print('case3')
                if 0 <= angz and angz < math.pi:
                    adjust_dr(vel, vel_msg)
                else:
                    adjust_dl(vel, vel_msg)

        adjusted = 0
        while dl == 1 and sonarf[4] >= 1.3 and sonarf[5] >= 1.3 and stopped == 0:
            showme(matrix, matsize, sector, secsize, graph)
            vel_msg.linear.x = 1
            vel_msg.angular.z = 0
            vel.publish(vel_msg)

            if sonarf[3] < 1.3:
                vel_msg.linear.x = 0
                vel.publish(vel_msg)
                #print('dl_ex')
                adjust_dl(vel, vel_msg)
                adjusted = 0

            if sonarf[0] > 1.3 and sonarf[1] > 1.3 and sonarf[2] > 1.3:
                vel_msg.linear.x = 0.2
                vel.publish(vel_msg)
                if adjusted == 0:
                    #print('dl_adj')
                    adjust_angle(vel, vel_msg, posx, posy)
                    adjusted = 1

            if not ((posx+2 < x or x < posx-2) or (posy+2 < y or y < posy-2)):
                stopped = 1

        adjusted = 0
        while dr == 1 and sonarf[4] >= 1.3 and sonarf[5] >= 1.3 and stopped == 0:
            showme(matrix, matsize, sector, secsize, graph)
            vel_msg.linear.x = 1
            vel_msg.angular.z = 0
            vel.publish(vel_msg)

            if sonarf[6] < 1.3:
                vel_msg.linear.x = 0
                vel.publish(vel_msg)
                #print('dr_ex')
                adjust_dr(vel, vel_msg)
                adjusted = 0

            if sonarf[9] > 1.3 and sonarf[8] > 1.3 and sonarf[7] > 1.3:
                vel_msg.linear.x = 0.2
                vel.publish(vel_msg)
                if adjusted == 0:
                    #print('dr_adj')
                    adjust_angle(vel, vel_msg, posx, posy)
                    adjusted = 1

            if not ((posx+2 < x or x < posx-2) or (posy+2 < y or y < posy-2)):
                stopped = 1

    vel_msg.linear.x = 0
    vel.publish(vel_msg)

def walker(vel, vel_msg, posx, posy, matrix, matsize, sector, secsize, graph):
    global x, y

    while ((posx + 0.3) < x or x < (posx - 0.3)) or ((posy + 0.3) < y or y < (posy - 0.3)):
        showme(matrix, matsize, sector, secsize, graph)
        square = (posx - x)**2 + (posy - y)**2
        dist = square**0.5
        vel_msg.linear.x = dist
        vel.publish(vel_msg)
    vel_msg.linear.x = 0.1
    vel.publish(vel_msg)

def walk(vel, vel_msg, posx, posy):
    global x, y

    while ((posx + 0.3) < x or x < (posx - 0.3)) or ((posy + 0.3) < y or y < (posy - 0.3)):
        square = (posx - x)**2 + (posy - y)**2
        dist = square**0.5
        vel_msg.linear.x = dist
        vel.publish(vel_msg)
    vel_msg.linear.x = 0
    vel.publish(vel_msg)

def dijkstra(graph, start, end):
    graph[start].value = 0.0
    analyze = []

    analyze.append(start)
    while len(analyze) > 0:
        s = analyze.pop(0)
        while (graph[s].read == 1) and (len(analyze) > 0):
            s = analyze.pop(0)
        for i in range (0, len(graph[s].near)):
            v = graph[s].near[i]
            square = (graph[v].center[0] - graph[s].center[0])**2 + (graph[v].center[1] - graph[s].center[1])**2
            dist = square**0.5
            value = graph[s].value + dist
            if (graph[v].read == 0) and (value < graph[v].value):
                graph[v].value = value
                graph[v].prev = s
                if len(analyze) == 0:
                    analyze.append(v)
                else:
                    j = 0
                    flag = 0
                    while flag == 0:
                        act = analyze[j]
                        if graph[v].value < graph[act].value:
                            analyze.insert(j, v)
                            flag = 1
                        elif j == (len(analyze)-1):
                            analyze.append(v)
                            flag = 1
                        j = j + 1
        graph[s].read = 1

    # cria uma lista do caminho de nos a serem percorridos
    way = []
    way.append(end)
    while way[0] != start:
        way.insert(0, graph[end].prev)
        end = graph[end].prev

    # redefine o grafo para um novo calculo de caminho
    for i in range (1, len(graph)):
        graph[i].value = 999999999.0
        graph[i].prev = 0
        graph[i].read = 0

    return way

# ------------------------------------------------------------------------------
# funcoes para grade de ocupacao

def drawtxt(thegrid, thesize, path, type):
    arq = open(path, type)
    j = thesize-1
    while j >= 0:
        for i in range (0, thesize):
            if thegrid[i][j] == -1:
                arq.write('P ')
            elif thegrid[i][j] == 5:
                arq.write('. ')
            elif thegrid[i][j] >= 10:
                arq.write('# ')
            elif thegrid[i][j] == 0:
                arq.write('  ')
            else:
                arq.write('{0} '.format(thegrid[i][j]))
        arq.write('\n')
        j = j - 1
    arq.close()

def drawsec(matrix, matsize, thegrid, thesize, path):
    global x, y

    gx = int(((matsize/2) + (corx*2) + (x*2)) - 1)
    gy = int(((matsize/2) + (cory*2) + (y*2)) - 1)
    gx_s = gx - (thesize/2)
    gy_s = gy - (thesize/2)
    gx_f = gx + (thesize/2)-1
    gy_f = gy + (thesize/2)-1
    # print 'gx_s {0} gx_f {1}'.format(gx_s, gx_f)
    # print 'gy_s {0} gy_f {1}'.format(gy_s, gy_f)

    i = 0
    ig = gx_s
    while ig <= gx_f:
        j = 0
        jg = gy_s
        while jg <= gy_f:
            # print 'i {0} j {1}'.format(i, j)
            # print 'ig {0} jg {1}'.format(ig, jg)
            if (0 <= ig and ig < matsize) and (0 <= jg and jg < matsize):
                thegrid[i][j] = matrix[ig][jg]
            jg = jg + 1
            j = j + 1
        ig = ig + 1
        i = i + 1
    thegrid[(thesize/2)-1][(thesize/2)-1] = -1
    drawtxt(thegrid, thesize, path, 'w')

def eraser(matrix, teta, dist, gx, gy):

    if dist >= 0.5:
        dy = math.sin(teta) * dist
        dx = math.cos(teta) * dist
        posx = int(gx + dx*2)
        posy = int(gy + dy*2)
        matsize = len(matrix)
        if (0 <= posx and posx < matsize) and (0 <= posy and posy < matsize):
            if 0 < matrix[posx][posy] and matrix[posx][posy] < 300:
                matrix[posx][posy] = matrix[posx][posy] - 1
        eraser(matrix, teta, (dist-0.5), gx, gy)

def maker(matrix, gx, gy):
    global z, laser

    start = z
    dist = list(laser)

    for i in range (0, len(dist)):
        if i < 134.5:
            teta = start - math.radians(134.5) + math.radians(i)
        else:
            teta = start + math.radians(i-134.5)

        if dist[i] > 15:
            dist[i] = 15
            eraser(matrix, teta, (dist[i]-0.5), gx, gy)

        else:
            dy = math.sin(teta) * dist[i]
            dx = math.cos(teta) * dist[i]
            posx = int(gx + dx*2)
            posy = int(gy + dy*2)
            matsize = len(matrix)
            if (0 <= posx and posx < matsize) and (0 <= posy and posy < matsize):
                if matrix[posx][posy] < 300:
                    matrix[posx][posy] = matrix[posx][posy] + 1
            eraser(matrix, teta, (dist[i]-0.5), gx, gy)

def gridmaker(vel, vel_msg, matrix, gx, gy):
    global z, mode

    if mode == 0:
        speed = 0.1
    else:
        speed = math.pi

    start = z
    if z <= 0:
        while z <= 0:
            maker(matrix, gx, gy)
            vel_msg.angular.z = speed
            vel.publish(vel_msg)
    else:
        while z > 0:
            maker(matrix, gx, gy)
            vel_msg.angular.z = speed
            vel.publish(vel_msg)
    vel_msg.angular.z = 0
    vel.publish(vel_msg)

    if mode == 0:
        while ((start + 0.009) < z or z < (start - 0.009)):
            maker(matrix, gx, gy)
            vel_msg.angular.z = speed
            vel.publish(vel_msg)
    else:
        while ((start + 0.003) < z or z < (start - 0.003)):
            maker(matrix, gx, gy)
            vel_msg.angular.z = abs(start - z)
            vel.publish(vel_msg)
    vel_msg.angular.z = 0
    vel.publish(vel_msg)

    # print start
    # print z

# ------------------------------------------------------------------------------
# funcoes do programa

def treat_node(vel, vel_msg, dest, drawn, matrix, matsize, gridno, gridsize):
    # verifica a existencia de grade neste ponto
    i = 0
    j = 0
    while i != len(drawn) and j == 0:
        if drawn[i] == dest:
            j = dest
        i = i + 1

    # monta grade neste ponto
    if j != dest:
        sys.stdout.write("Montando grade em {0}     \r".format(dest))
        sys.stdout.flush()
        gx = int(((matsize/2) + (corx*2) + (x*2)) - 1)
        gy = int(((matsize/2) + (cory*2) + (y*2)) - 1)
        gridmaker(vel, vel_msg, matrix, gx, gy)
        drawsec(matrix, matsize, gridno, gridsize, 'tmp/grid_{0}.txt'.format(dest))
        drawn.append(dest)

def run():
    rospy.init_node('percepcao', anonymous=True)
    global mode

    # define variaveis de publicacao do ROS
    vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    odom_callback = rospy.Subscriber('/pose', Odometry, odom_call)
    global x, y, z
    laser_callback = rospy.Subscriber('/hokuyo_scan', LaserScan, laser_call)
    global laser
    sonarf_callback = rospy.Subscriber('/sonar_front', LaserScan, sonarf_call)
    global sonarf

    # carregamento de dados
    global loading
    for i in range(0, 101):
        progressBar(i, 100, 20)
        time.sleep(0.0125)
    print(' ')
    loading = 0

    # inicio do programa
    print 'Escolha um modo de execucao:'
    print '0 Precisao'
    print '1 Velocidade'
    mode = input('Digite: ')
    if mode > 1:
        mode = 1
    elif mode < 0:
        mode = 0

    # sistema de mapeamento
    graph = pacotinho.map.define_graph()        # grafo do mapa stage
    error = 0
    matrix = pacotinho.grid.define_grid()       # matriz da grade completa
    matsize = len(matrix)
    sector = pacotinho.grid.define_sector()     # grade da interface de usuario
    secsize = len(sector)
    gridno = pacotinho.grid.define_gridno()     # grade de um no do stage
    gridsize = len(gridno)
    drawn = []                                  # listas de grades desenhadas

    # cria um arquivo txt com a grade de ocupacao inicial
    arq = open('tmp/grid.txt', 'w')
    for j in range (0, matsize):
        for i in range (0, matsize):
            arq.write('5 ')
        arq.write('\n')
    arq.close()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        # interface de usuario
        place = placenode(x, y, graph)
        if place == len(graph):
            print 'Modifique o ponto inicial do pioneer'
            sys.exit()
        if error == 0:
            print(' ')
            size = len(graph) - 1
            print 'O Pioneer esta no ponto {0} de {1}'.format(place, size)
            dest = input('A qual ponto deseja move-lo? ')
        else:
            print(' ')
            print 'O ponto inserido nao existe!'
            dest = input('Insira um novo ponto: ')
        if dest == 0:
            print 'Programa encerrado'
            sys.exit()
        if dest < 0 or dest >= len(graph):
            error = 1

        else:
            # calculo do menor caminho
            error = 0
            place = placenode(x, y, graph)
            way = dijkstra(graph, place, dest)
            print way
            dest = way.pop(0)

            # desenha grade de ocupacao do no inicial
            treat_node(vel, vel_msg, dest, drawn, matrix, matsize, gridno, gridsize)
            sys.stdout.write("Saiu do ponto {0}         \r".format(dest))
            sys.stdout.flush()

            # ajusta o angulo e vai ate o ponto definido
            while len(way) > 0:
                dest = way.pop(0)
                adjust_angle(vel, vel_msg, graph[dest].center[0], graph[dest].center[1])
                walk(vel, vel_msg, graph[dest].center[0], graph[dest].center[1])

                # desenha grade de ocupacao do no atual
                treat_node(vel, vel_msg, dest, drawn, matrix, matsize, gridno, gridsize)
                sys.stdout.write("Passou pelo ponto {0}     \r".format(dest))
                sys.stdout.flush()

            # desenha a grade de ocupacao do caminho percorrido no mapa geral
            drawtxt(matrix, matsize, 'tmp/grid.txt', 'r+')
            sys.stdout.write("Grade de ocupacao desenhada\n".format(dest))
            sys.stdout.flush()

            # interface de usuario (subjanela simbolica)
            print '\nExplore um ponto interno (x;y)'
            explorer = [0,0]
            explorer[1] = len(drawn)
            while explorer[1] == len(drawn):
                posx = input('Coordenada X: ')
                posy = input('Coordenada Y: ')
                explorer = placegrid(posx, posy, drawn, graph)

            # vai ate o ponto fornecido
            place = dest
            dest = explorer[0]
            way = dijkstra(graph, place, dest)
            uma_gambiarra = len(way) - 1
            way.pop(uma_gambiarra)
            while len(way) > 0:
                dest = way.pop(0)
                adjust_angle(vel, vel_msg, graph[dest].center[0], graph[dest].center[1])
                walker(vel, vel_msg, graph[dest].center[0], graph[dest].center[1], matrix, matsize, sector, secsize, graph)
            runner(vel, vel_msg, posx, posy, matrix, matsize, sector, secsize, graph)

        rate.sleep()

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass
