class Map:
    center = None
    near = None
    area = None
    value = None
    prev = None
    read = None

graph = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
graph[0] = Map()
graph[0].center = ()
graph[0].near = []
graph[0].area = []
graph[0].value = 999999999.0
graph[0].prev = 0
graph[0].read = 0

graph[1] = Map()
graph[1].center = (0.0, 0.0)
graph[1].near = [2, 38]
graph[1].area = [(-9.27, 4.46), (-1.25, 8.17), (4.40, -6.76), (-1.39, -10.11)]
graph[1].value = 999999999.0
graph[1].prev = 0
graph[1].read = 0

graph[2] = Map()
graph[2].center = (2.94, -11.84)
graph[2].near = [1, 3, 4]
graph[2].area = [(-7.51, -13.35), (5.48, -6.29), (7.82, -13.35), (-4.45, -20.11)]
graph[2].value = 999999999.0
graph[2].prev = 0
graph[2].read = 0

graph[3] = Map()
graph[3].center = (-7.71, -17.38)
graph[3].near = [2]
graph[3].area = [(-7.36, -13.99), (-2.87, -24.21), (-6.61, -26.33), (-10.64, -15.76)]
graph[3].value = 999999999.0
graph[3].prev = 0
graph[3].read = 0

graph[4] = Map()
graph[4].center = (15.23, -4.29)
graph[4].near = [2, 5]
graph[4].area = [(4.87, -6.62), (18.21, 0.94), (22.82, -9.60), (9.36, -17.16)]
graph[4].value = 999999999.0
graph[4].prev = 0
graph[4].read = 0

graph[5] = Map()
graph[5].center = (26.47, 1.56)
graph[5].near = [4, 6, 41]
graph[5].area = [(18.79, 1.19), (31.59, 7.34), (33.97, 1.30), (21.41, -5.79)]
graph[5].value = 999999999.0
graph[5].prev = 0
graph[5].read = 0

graph[6] = Map()
graph[6].center = (23.29, 16.97)
graph[6].near = [5, 9]
graph[6].area = [(10.92, 16.26), (19.67, 20.85), (27.82, 15.63), (28.65, 14.88), (29.40, 13.53), (29.80, 11.67), (29.48, 9.54), (29.00, 8.74), (29.80, 6.73), (17.45, 0.63)]
graph[6].value = 999999999.0
graph[6].prev = 0
graph[6].read = 0

####################################################################################

graph[7] = Map()	# 30 esquerdo
graph[7].center = (20.62, 83.31)
graph[7].near = [31, 30]
graph[7].area = [(14.77, 83.66), (16.92, 77.8), (25.78, 82.55), (22.83, 87.88)]
graph[7].value = 999999999.0
graph[7].prev = 0
graph[7].read = 0

graph[8] = Map()	# 30 direito
graph[8].center = (32.38, 89.51)
graph[8].near = [30, 29]
graph[8].area = [(28.16, 90.95), (29.43, 84.7), (38.35, 89.51), (35.98, 95.3)]
graph[8].value = 999999999.0
graph[8].prev = 0
graph[8].read = 0

####################################################################################

graph[9] = Map()
graph[9].center = (15.00, 20.45)
graph[9].near = [6, 39]
graph[9].area = [(13.69, 17.96), (19.15, 21.29), (14.92, 24.41), (12.03, 22.08)]
graph[9].value = 999999999.0
graph[9].prev = 0
graph[9].read = 0

####################################################################################

graph[10] = Map()
graph[10].center = (93.44, 35.97)
graph[10].near = [40, 11]
graph[10].area = [(82.35, 34.06), (86.94, 24.44), (106.29, 33.12), (101.5, 43.92)]
graph[10].value = 999999999.0
graph[10].prev = 0
graph[10].read = 0

graph[11] = Map()
graph[11].center = (107.00, 43.51)
graph[11].near = [10, 12, 15]
graph[11].area = [(100.97, 45.84), (108.75, 49.79), (112.02, 41.52), (104.37, 37.56)]
graph[11].value = 999999999.0
graph[11].prev = 0
graph[11].read = 0

graph[12] = Map()
graph[12].center = (103.76, 52.02)
graph[12].near = [11, 13]
graph[12].area = [(96.26, 53.19), (109.24, 59.64), (112.25, 52.08), (100.97, 45.9)]
graph[12].value = 999999999.0
graph[12].prev = 0
graph[12].read = 0

graph[13] = Map()
graph[13].center = (97.79, 69.29)
graph[13].near = [12, 14]
graph[13].area = [(97.97, 54.64), (96.07, 54.57), (93.52, 60.61), (95.28, 61.83), (91.22, 72.91), (107.22, 80.79), (116.11, 63.23)]
graph[13].value = 999999999.0
graph[13].prev = 0
graph[13].read = 0

graph[14] = Map()
graph[14].center = (87.77, 94.20)
graph[14].near = [13, 27]
graph[14].area = [(91.11, 72.88), (98.88, 76.94), (84.6, 114.41), (76.8, 110.13)]
graph[14].value = 999999999.0
graph[14].prev = 0
graph[14].read = 0

graph[15] = Map()
graph[15].center = (126.35, 53.12)
graph[15].near = [11, 16]
graph[15].area = [(109.41, 48.14), (112.54, 40.08), (143.59, 54.68), (139.19, 64.01)]
graph[15].value = 999999999.0
graph[15].prev = 0
graph[15].read = 0

graph[16] = Map()
graph[16].center = (143.56, 62.57)
graph[16].near = [15, 17]
graph[16].area = [(139.31, 64.01), (146.32, 67.49), (148.98, 61.06), (142.14, 57.46)]
graph[16].value = 999999999.0
graph[16].prev = 0
graph[16].read = 0

graph[17] = Map()
graph[17].center = (136.72, 81.92)
graph[17].near = [16, 18]
graph[17].area = [(138.96, 64.01), (146.49, 67.43), (134.32, 98.66), (127.08, 95.29)]
graph[17].value = 999999999.0
graph[17].prev = 0
graph[17].read = 0

graph[18] = Map()
graph[18].center = (129.54, 100.17)
graph[18].near = [17, 19, 20]
graph[18].area = [(126.68, 95.93), (134.32, 98.77), (132.7, 103.41), (125.23, 100.39)]
graph[18].value = 999999999.0
graph[18].prev = 0
graph[18].read = 0

graph[19] = Map()
graph[19].center = (141.88, 104.68)
graph[19].near = [18]
graph[19].area = [(129.8, 110.36), (146.55, 119.68), (153.79, 100.05), (137.1, 91.07)]
graph[19].value = 999999999.0
graph[19].prev = 0
graph[19].read = 0

graph[20] = Map()
graph[20].center = (126.06, 110.59)
graph[20].near = [18, 21]
graph[20].area = [(132.64, 103.29), (125.4, 100.45), (119.26, 116.96), (126.21, 120.61)]
graph[20].value = 999999999.0
graph[20].prev = 0
graph[20].read = 0

graph[21] = Map()
graph[21].center = (121.72, 120.09)
graph[21].near = [20, 22, 23]
graph[21].area = [(125.98, 120.79), (119.2, 117.08), (117.23, 122.0), (124.3, 125.42)]
graph[21].value = 999999999.0
graph[21].prev = 0
graph[21].read = 0

graph[22] = Map()
graph[22].center = (111.75, 115.75)
graph[22].near = [21]
graph[22].area = [(113.76, 130.75), (97.25, 121.65), (105.13, 101.67), (121.69, 110.36)]
graph[22].value = 999999999.0
graph[22].prev = 0
graph[22].read = 0

graph[23] = Map()
graph[23].center = (118.99, 127.97)
graph[23].near = [21, 24]
graph[23].area = [(117.31, 122.0), (124.31, 125.88), (120.24, 135.25), (113.51, 132.01)]
graph[23].value = 999999999.0
graph[23].prev = 0
graph[23].read = 0

graph[24] = Map()
graph[24].center = (115.75, 135.79)
graph[24].near = [23, 25, 26]
graph[24].area = [(113.51, 132.01), (111.53, 136.88), (118.38, 139.69), (120.24, 135.37)]
graph[24].value = 999999999.0
graph[24].prev = 0
graph[24].read = 0

graph[25] = Map()
graph[25].center = (112.68, 144.72)
graph[25].near = [24]
graph[25].area = [(118.38, 139.81), (111.57, 136.72), (102.63, 160.46), (109.79, 161.29)]
graph[25].value = 999999999.0
graph[25].prev = 0
graph[25].read = 0

graph[26] = Map()
graph[26].center = (95.30, 124.85)
graph[26].near = [24, 27]
graph[26].area = [(81.22, 130.12), (108.27, 144.87), (113.87, 130.94), (87.58, 116.29)]
graph[26].value = 999999999.0
graph[26].prev = 0
graph[26].read = 0

graph[27] = Map()
graph[27].center = (79.66, 115.34)
graph[27].near = [14, 26, 28]
graph[27].area = [(87.58, 116.29), (76.76, 110.25), (71.69, 123.52), (81.17, 129.93)]
graph[27].value = 999999999.0
graph[27].prev = 0
graph[27].read = 0

graph[28] = Map()
graph[28].center = (62.86, 106.13)
graph[28].near = [27, 29]
graph[28].area = [(76.67, 110.3), (48.95, 95.08), (46.46, 101.4), (74.22, 116.48)]
graph[28].value = 999999999.0
graph[28].prev = 0
graph[28].read = 0

graph[29] = Map()
graph[29].center = (42.46, 95.13)
graph[29].near = [28, 8]
graph[29].area = [(46.44, 101.22), (52.3, 85.61), (41.8, 79.78), (36.19, 95.46)]
graph[29].value = 999999999.0
graph[29].prev = 0
graph[29].read = 0

####################################################################################

graph[30] = Map()
graph[30].center = (26.01, 85.74)
graph[30].near = [7, 8]
graph[30].area = [(22.83, 87.88), (25.72, 82.61), (29.43, 84.64), (28.16, 90.95)]
graph[30].value = 999999999.0
graph[30].prev = 0
graph[30].read = 0

####################################################################################

graph[31] = Map()
graph[31].center = (10.83, 77.51)
graph[31].near = [7, 32]
graph[31].area = [(14.82, 83.7), (20.5, 68.27), (10.21, 62.69), (4.21, 78.27)]
graph[31].value = 999999999.0
graph[31].prev = 0
graph[31].read = 0

graph[32] = Map()
graph[32].center = (-1.56, 71.26)
graph[32].near = [31, 33]
graph[32].area = [(4.1, 78.16), (-8.96, 71.25), (-6.76, 65.1), (6.4, 72.04)]
graph[32].value = 999999999.0
graph[32].prev = 0
graph[32].read = 0

graph[33] = Map()
graph[33].center = (-9.44, 67.14)
graph[33].near = [32, 34]
graph[33].area = [(-8.99, 71.43), (-12.92, 69.53), (-10.5, 63.19), (-6.87, 64.99)]
graph[33].value = 999999999.0
graph[33].prev = 0
graph[33].read = 0

graph[34] = Map()
graph[34].center = (-16.57, 63.61)
graph[34].near = [33, 35]
graph[34].area = [(-10.58, 63.12), (-20.68, 57.98), (-23.42, 63.91), (-12.92, 69.35)]
graph[34].value = 999999999.0
graph[34].prev = 0
graph[34].read = 0

graph[35] = Map()
graph[35].center = (-24.39, 59.38)
graph[35].near = [34, 36, 37]
graph[35].area = [(-23.45, 63.77), (-28.31, 61.32), (-26.15, 54.99), (-20.72, 57.94)]
graph[35].value = 999999999.0
graph[35].prev = 0
graph[35].read = 0

graph[36] = Map()
graph[36].center = (-32.33, 55.44)
graph[36].near = [35]
graph[36].area = [(-28.42, 61.11), (-39.46, 55.6), (-37.12, 49.27), (-26.22, 54.92)]
graph[36].value = 999999999.0
graph[36].prev = 0
graph[36].read = 0

graph[37] = Map()
graph[37].center = (-16.40, 38.06)
graph[37].near = [35, 38]
graph[37].area = [(-12.27, 17.56), (-7.06, 20.69), (-11.19, 32.02), (-10.58, 32.31), (-12.13, 36.59), (-12.74, 36.33), (-20.76, 57.85), (-26.52, 54.75)]
graph[37].value = 999999999.0
graph[37].prev = 0
graph[37].read = 0

graph[38] = Map()
graph[38].center = (-6.31, 9.91)
graph[38].near = [1, 37, 39]
graph[38].area = [(-13.78, 16.59), (-6.48, 20.90), (-4.90, 16.66), (-5.51, 16.30), (-4.25, 13.20), (-3.53, 13.42), (-1.27, 8.13), (-9.29, 4.46)]
graph[38].value = 999999999.0
graph[38].prev = 0
graph[38].read = 0

graph[39] = Map()
graph[39].center = (5.56, 15.64)
graph[39].near = [9, 38]
graph[39].area = [(-1.58, 9.34), (-3.35, 13.46), (12.06, 21.89), (13.69, 17.9)]
graph[39].value = 999999999.0
graph[39].prev = 0
graph[39].read = 0

####################################################################################

graph[40] = Map()
graph[40].center = (71.2, 23.8)
graph[40].near = [41, 10]
graph[40].area = [(60.75, 10.42), (56.99, 21.0), (82.35, 34.06), (86.94, 24.44)]
graph[40].value = 999999999.0
graph[40].prev = 0
graph[40].read = 0

graph[41] = Map()
graph[41].center = (45.0, 11.31)
graph[41].near = [5, 40]
graph[41].area = [(31.65, 7.45), (35.48, -2.37), (60.75, 10.42), (56.99, 21.0)]
graph[41].value = 999999999.0
graph[41].prev = 0
graph[41].read = 0

####################################################################################

def define_graph():
    return graph
