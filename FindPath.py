import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import sys
sys.setrecursionlimit(10000)

class Romania():
    def __init__(self, cityF):
        self.city = ["Oradea", "Zerind", "Arad", "Timisoara", "Lugoj", "Mehadia", "Drobeta", "Sibiu", "Rimnicu_vilcea",\
                     "Craiova", "Fagaras", "Pitesti", "Bucharest", "Giurgiu", "Urzicenimneamt", "Iasi", "Vaslui",\
                     "Hirsova", "Eforie", "Neamt"]
        self.pos = []
        self.dist = [[0,71,-1,-1,-1,-1,-1,151,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [71,0,75,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,75,0,118,-1,-1,-1,140,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,118,0,111,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,111,0,70,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,70,0,75,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,75,0,-1,-1,120,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [151,-1,140,-1,-1,-1,-1,0,80,-1,99,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,80,0,146,-1,97,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,120,-1,146,0,-1,138,-1,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,99,-1,-1,0,-1,211,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,97,138,-1,0,101,-1,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,211,101,0,90,85,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,90,0,-1,-1,-1,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,85,-1,0,-1,142,98,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,92,-1,-1,87],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,142,92,0,-1,-1,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,98,-1,-1,0,86,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,86,0,-1],
                     [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,87,-1,-1,-1,0]]
        self.LineDist = [380, 374, 366, 329, 244, 241, 242, 253, 193, 160, 178, 98, 0, 77, 80, 226, 199, 151, 161, 234]
        self.gn = [0] * 20
        self.prev = [cityF] * 20  # 前驱结点初始化为从Arad出发

        self.path = []
        self.cityFrom = cityF
        self.cityTo = 12

        self.open = [cityF]  # 生成第一个可能的解
        self.closed = []
        # 初始化图形
        self.g = nx.Graph()
        # 添加边
        edges = []
        for i in range(20):
            for j in range(20):
                if self.dist[i][j] != -1:
                    edges.append((self.city[i], self.city[j], self.dist[i][j]))
        self.g.add_weighted_edges_from(edges, color='black')
        # 绘制图
        plt.ion()
        self.pos = nx.spring_layout(self.g)
        nx.draw(self.g, pos=self.pos, with_labels=True)
        nx.draw_networkx(self.g, pos=self.pos, nodelist=[self.city[self.cityFrom]], node_color="green")
        # nx.draw_networkx_edges(self.g, pos=self.pos, edgelist=[("Arad", "Sibiu")], edge_color='green', width=5)

    def printPath(self):
        """
        打印路径
        :return:
        """
        n = self.cityTo
        while self.prev[n] != self.cityFrom:
            nx.draw_networkx_edges(self.g, pos=self.pos, edgelist=[(self.city[self.prev[n]], self.city[n])],\
                                   edge_color="green", width=5)
            plt.pause(0.3)
            n = self.prev[n]
        nx.draw_networkx_edges(self.g, pos=self.pos, edgelist=[(self.city[self.prev[n]], self.city[n])],\
                               edge_color="green", width=5)

    def BestFirst(self, begin):
        """
        best-first search
        :param cityTo:
        :return:
        """
        # 若是目标则停止，显示结果
        if begin == self.cityTo:
            self.printPath()
            return
        # 否则从该可能的解出发，生成新的可能解集
        new_solution = []
        for i in range(20):
            if self.dist[begin][i] != -1 and begin != i and i not in self.open:  # 如果结点可以扩展
                self.prev[i] = begin
                new_solution.append(i)
        # 用测试函数测试新的可能解集中的元素
        for s in new_solution:
            # 若是解，则停止
            if s == self.cityTo:
                nx.draw_networkx(self.g, pos=self.pos, nodelist=[self.city[s]], node_color="green")
                self.printPath()
                return
            else:
                self.open.append(s)
                nx.draw_networkx(self.g, pos=self.pos, nodelist=[self.city[s]], node_color="yellow")
                plt.pause(0.6)
        # 从解集中挑选最好的元素作为起点，调用BestFirst
        tmp_list = [self.LineDist[n] for n in self.open]
        tmp_list.sort()
        for t in tmp_list:
            min_idx = self.LineDist.index(t)
            if min_idx not in self.closed:
                break
        nx.draw_networkx(self.g, pos=self.pos, nodelist=[self.city[min_idx]], node_color="green")
        self.closed.append(min_idx)
        plt.pause(0.6)
        self.BestFirst(min_idx)

    def A_star(self):
        """
        A*算法
        :param cityTo:
        :return:
        """
        # 如果open={},失败退出
        if len(self.open) == 0:
            return
        # 在open表中取出f(n)值最小的结点n
        minFn = self.LineDist[self.open[0]] + self.gn[self.open[0]]
        minIndex = self.open[0]
        for i in self.open:
            fn = self.LineDist[i] + self.gn[i]
            if fn < minFn:
                minFn = fn
                minIndex = i
        self.open.remove(minIndex)
        self.closed.append(minIndex)
        nx.draw_networkx(self.g, pos=self.pos, nodelist=[self.city[minIndex]], node_color="green")
        # 如果是出口，则成功退出
        if minIndex == self.cityTo:
            self.printPath()
            return
        # 产生n的一切后继，将后继中不是n的前驱结点的集合作为M
        M = []
        for i in range(20):
            if self.dist[minIndex][i] != -1 and i != self.prev[minIndex] and minIndex != i:
                M.append(i)
        # 对M中的元素P,作两类处理
        for m in M:
            if m not in self.open and m not in self.closed:
                nx.draw_networkx(self.g, pos=self.pos, nodelist=[self.city[m]], node_color="yellow")
                plt.pause(1)
                self.open.append(m)
                self.prev[m] = minIndex
                nx.draw_networkx_edges(self.g, pos=self.pos, edgelist=[(self.city[minIndex], self.city[m])], \
                                       edge_color="yellow", width=3)
                self.gn[m] = self.gn[minIndex] + self.dist[minIndex][m]
            else:  # 更改P的子节点n的指针和费用
                if self.gn[m] > self.gn[minIndex] + self.dist[minIndex][m]:
                    nx.draw_networkx_edges(self.g, pos=self.pos, edgelist=[(self.city[self.prev[m]], self.city[m])], \
                                           edge_color="black", width=3)
                    self.prev[m] = minIndex
                    nx.draw_networkx_edges(self.g, pos=self.pos, edgelist=[(self.city[self.prev[m]], self.city[m])], \
                                           edge_color="yellow", width=3)
                    plt.pause(1)
                    self.gn[m] = self.gn[minIndex] + self.dist[minIndex][m]

                    if m in self.closed:
                        self.closed.remove(m)
                        self.open.append(m)
        self.A_star()

city = ["Oradea", "Zerind", "Arad", "Timisoara", "Lugoj", "Mehadia", "Drobeta", "Sibiu", "Rimnicu_vilcea",\
                     "Craiova", "Fagaras", "Pitesti", "Bucharest", "Giurgiu", "Urzicenimneamt", "Iasi", "Vaslui",\
                     "Hirsova", "Eforie", "Neamt"]

top = Tk()  # 父容器
top.geometry('500x300+500+200')  # 宽x高+偏移量
top.title('Romania Problems')


def BestFirst():
    r = Romania(city.index(cmb.get()))
    r.BestFirst(r.cityFrom)

def A_star():
    r = Romania(city.index(cmb.get()))
    r.A_star()

L1 = Label(top, text="选择起始城市").place(x=30, y=30)
cmb = ttk.Combobox(top)
cmb['value'] = tuple(city)
cmb.current(2)
cmb.place(x=150, y=30)

BBestFirst = Button(top, text="最佳优先搜索", command=BestFirst).place(x=30, y=100)
BAstar = Button(top, text="A*算法", command=A_star).place(x=30,y=150)

top.mainloop()

plt.ioff()
plt.show()









                

        

        



