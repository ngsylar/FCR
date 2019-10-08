# grid_map
================
# Gabriel Rocha Fontenele
# 15/0126760

# UNB - FCR A 2018/2
================

Entrada
-------
Pelo teclado através do terminal

Saida
-----
Instruções e dados através do terminal
Arquivos de texto contendo desenhos feitos por caracteres

Dependencias do ROS
-------------------
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

Dependencias fora do ROS
------------------------
import tf
import math
import time
import sys
import os

Dependencias próprias
---------------------
import pacotinho.map
import pacotinho.grid

Algoritmo
---------
O algoritmo principal implementado não foi retirado de nenhuma referência, foi criado e desenvolvido pelo autor
As funções que possuem referância foram apresentadas e descritas no relatório

Funcao Principal:
	Enquanto robô_está_ligado:
		ponto_inicial = ponto_ao_ligar_robo()
		ponto_final = <input>
		caminho = dijkstra(ponto_inicial, ponto_final)
		Para i de 0 até tamanho(caminho):
			ajustar_angulo()
			navegar_ate(caminho[i])
			grade = desenhar_grade(caminho[i])
		coordenada_x = <input>
		coordenada_y = <input>
		procurar_coordenadas(grade)
		ir_a_pontos(coordenada_x, coordenada_y)
	Fim enquanto
Fim Principal

Funcao ir_a_pontos(coordenada_x, coordenada_y):
	Enquanto x_atual != coordenada_x e y_atual != coordenada_y:
		mostrar_grade()
		ajustar_angulo()
		acelerar()
		Se detectar_obstaculo():
			desviar()
		Fim se
	Fim enquanto
Fim ir_a_pontos


Descrição dos arquivos
----------------------

src/
    |--> pacotinho/
        |--> __init__.py: arquivo de inicializacao da biblioteca pacotinho
        |--> map.py: código contendo a estrutura do grafo com o mapa topologico
        |--> grid.py: código contendo estruturas de matriz para grade de ocupação
    |--> tmp/
        |--> grid.txt: *arquivo salvo da grade de ocupação geral
        |--> grid_[i]: *arquivo salvo da grade particular do no i
    |--> grid_map.py: source code
Entrega_2.pdf: Roteiro deste trabalho
example.mkv: vídeo de exemplo com uma execução do código
readme.txt: este arquivo
relatorio.pdf: relatório do trabalho, contendo descrição do código, das estruturas e das funções
stage_sp.png: imagem com a representação do grafo com o mapa topológico sobre o ambiente de simulação STAGE

*arquivos a serem criados durante a execucao do source code

