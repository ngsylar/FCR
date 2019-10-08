# grid_map
================
# Gabriel Rocha Fontenele
# 15/0126760

# UNB - FCR A 2018/2
================

Entrada
-------
Pelo teclado atrav�s do terminal

Saida
-----
Instru��es e dados atrav�s do terminal
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

Dependencias pr�prias
---------------------
import pacotinho.map
import pacotinho.grid

Algoritmo
---------
O algoritmo principal implementado n�o foi retirado de nenhuma refer�ncia, foi criado e desenvolvido pelo autor
As fun��es que possuem refer�ncia foram apresentadas e descritas no relat�rio

Funcao Principal:
	Enquanto rob�_est�_ligado:
		ponto_inicial = ponto_ao_ligar_robo()
		ponto_final = <input>
		caminho = dijkstra(ponto_inicial, ponto_final)
		Para i de 0 at� tamanho(caminho):
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


Descri��o dos arquivos
----------------------

src/
    |--> pacotinho/
        |--> __init__.py: arquivo de inicializacao da biblioteca pacotinho
        |--> map.py: c�digo contendo a estrutura do grafo com o mapa topologico
        |--> grid.py: c�digo contendo estruturas de matriz para grade de ocupa��o
    |--> tmp/
        |--> grid.txt: *arquivo salvo da grade de ocupa��o geral
        |--> grid_[i]: *arquivo salvo da grade particular do no i
    |--> grid_map.py: source code
Entrega_2.pdf: Roteiro deste trabalho
example.mkv: v�deo de exemplo com uma execu��o do c�digo
readme.txt: este arquivo
relatorio.pdf: relat�rio do trabalho, contendo descri��o do c�digo, das estruturas e das fun��es
stage_sp.png: imagem com a representa��o do grafo com o mapa topol�gico sobre o ambiente de simula��o STAGE

*arquivos a serem criados durante a execucao do source code

