import math
from timeit import default_timer as timer
import numpy as np
from scipy.optimize import fsolve


class Locator:
    coords = []

    TM1 = -100
    TM2 = -100
    TM3 = -100

    ZTM4 = -100

    start_time = timer()

    TM1coord = [0, 0, 0]
    TM2coord = [500, 0, 0]
    TM3coord = [0, 500, 0]
    ZTM4coord = [500, 0, 0]

    def updateValue(self, dic):
        if dic['id'] == 'TM1':
            self.TM1 = int(dic['distance'])
        elif dic['id'] == 'TM2':
            self.TM2 = int(dic['distance'])
        elif dic['id'] == 'TM3':
            self.TM3 = int(dic['distance'])
        elif dic['id'] == 'ZTM4':
            self.ZTM4 = int(dic['distance'])

    @staticmethod
    def formula(x1, y1, x2, y2, r1, r2):

        d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        if d > r1 + r2:
            r1 += d - (r1 + r2) + 1
        if d < abs(r1 - r2):
            r1 += d - abs(r1 - r2) + 1
        # if abs(d - (r1 + r2)) < 0.0001:
        # # Если в одной точке
        #     x3 = (x1 + x2) / 2
        #     y3 = (y1 + y2) / 2
        #     return [x3, -1000], [y3, 1000]
        # else:
        b = (r2 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        a = d - b
        h = math.sqrt(r2 ** 2 - b ** 2)
        x = x1 + (x2 - x1) / (d / a)
        y = y1 + (y2 - y1) / (d / a)
        x3 = x - (y - y2) * h / b
        y3 = y + (x - x2) * h / b
        x4 = x + (y - y2) * h / b
        y4 = y - (x - x2) * h / b

        resX = [x3, x4]
        resY = [y3, y4]
        # if 0 <= x3 <= 500:
        #     resX.append(x3)
        # if 0 <= x4 <= 500:
        #     resX.append(x4)
        # if 0 <= y3 <= 500:
        #     resY.append(y3)
        # if 0 <= y4 <= 500:
        #     resY.append(y4)
        return resX, resY

    def getCoordXY(self):

        X = []
        Y = []
        if self.TM1 > 0 and self.TM2 > 0:
            # if abs(self.TM2[1] - self.TM1[1]) < 0.003:
            _Y, _X = self.formula(self.TM1coord[0],
                                  self.TM1coord[1],
                                  self.TM2coord[0],
                                  self.TM2coord[1],
                                  self.TM1,
                                  self.TM2)
            X.extend(_X)
            Y.extend(_Y)
        if self.TM1 > 0 and self.TM3 > 0:
            _Y, _X = self.formula(self.TM1coord[0],
                                  self.TM1coord[1],
                                  self.TM3coord[0],
                                  self.TM3coord[1],
                                  self.TM1,
                                  self.TM3)
            X.extend(_X)
            Y.extend(_Y)
        if self.TM2 > 0 and self.TM3 > 0:
            _Y, _X = self.formula(self.TM2coord[0],
                                  self.TM2coord[1],
                                  self.TM3coord[0],
                                  self.TM3coord[1],
                                  self.TM2,
                                  self.TM3)
            X.extend(_X)
            Y.extend(_Y)

        if X:
            for i in range(0, int(len(X) / 2)):
                max_tmp = max(X)
                min_tmp = min(X)
                mean_tmp = sum(X) / len(X)

                if abs(mean_tmp - max_tmp) > abs(mean_tmp - min_tmp):
                    X.remove(max_tmp)
                else:
                    X.remove(min_tmp)

            for i in range(0, int(len(Y) / 2)):
                max_tmp = max(Y)
                min_tmp = min(Y)
                mean_tmp = sum(Y) / len(Y)

                if abs(mean_tmp - max_tmp) > abs(mean_tmp - min_tmp):
                    Y.remove(max_tmp)
                else:
                    Y.remove(min_tmp)
            # trueX = []
            # X.sort()
            # print('X = ' + str(X))
            # flag = False
            #
            # prev = X[0]
            # for i in range(1, len(X)):
            #     if abs(X[i] - prev) < 1:
            #         flag = True
            #         trueX.append(X[i])
            #     else:
            #         if flag:
            #             trueX.append(prev)
            #             break
            #         prev = X[i]
            #
            # trueY = []
            # Y.sort()
            # flag = False
            #
            # prev = Y[0]
            # for i in range(1, len(Y)):
            #     if abs(Y[i] - prev) < 1:
            #         flag = True
            #         trueY.append(Y[i])
            #     else:
            #         if flag:
            #             trueY.append(prev)
            #             break
            #         prev = Y[i]

            # if trueY and trueX:
            return sum(X) / len(X), sum(Y) / len(Y)

        return -1, -1

    def getCoordXZ(self):

        X = []
        Z = []
        if self.TM1 > 0 and self.TM2 > 0:
            # if abs(self.TM2[1] - self.TM1[1]) < 0.003:
            _Z, _X = self.formula(self.TM1coord[0],
                                  self.TM1coord[1],
                                  self.TM2coord[0],
                                  self.TM2coord[1],
                                  self.TM1,
                                  self.TM2)
            X.extend(_X)
            Z.extend(_Z)
        if self.TM1 > 0 and self.ZTM4 > 0:
            _Z, _X = self.formula(self.TM1coord[0],
                                  self.TM1coord[1],
                                  self.ZTM4coord[0],
                                  self.ZTM4coord[1],
                                  self.TM1,
                                  self.ZTM4)
            X.extend(_X)
            Z.extend(_Z)
        if self.TM2 > 0 and self.ZTM4 > 0:
            _Z, _X = self.formula(self.TM2coord[0],
                                  self.TM2coord[1],
                                  self.ZTM4coord[0],
                                  self.ZTM4coord[1],
                                  self.TM2,
                                  self.ZTM4)
            X.extend(_X)
            Z.extend(_Z)

        if X:
            for i in range(0, int(len(X) / 2)):
                max_tmp = max(X)
                min_tmp = min(X)
                mean_tmp = sum(X) / len(X)

                if abs(mean_tmp - max_tmp) > abs(mean_tmp - min_tmp):
                    X.remove(max_tmp)
                else:
                    X.remove(min_tmp)

            for i in range(0, int(len(Z) / 2)):
                max_tmp = max(Z)
                min_tmp = min(Z)
                mean_tmp = sum(Z) / len(Z)

                if abs(mean_tmp - max_tmp) > abs(mean_tmp - min_tmp):
                    Z.remove(max_tmp)
                else:
                    Z.remove(min_tmp)

            return sum(X) / len(X), sum(Z) / len(Z)

        return -1, -1

    def planB(self):
        if self.TM1 > 0 and self.TM2 > 0 and self.TM3 > 0:
            a1 = np.array(self.TM3coord)
            r1 = self.TM3
            a2 = np.array(self.TM2coord)
            r2 = self.TM2
            a3 = np.array(self.TM1coord)
            r3 = self.TM1

            def position(a, r, u, v):
                return a + r * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v)])

            def f(args):
                u1, v1, u2, v2, u3, v3, _, _, _ = args
                pos1 = position(a1, r1, u1, v1)
                pos2 = position(a2, r2, u2, v2)
                pos3 = position(a3, r3, u3, v3)
                return np.array([pos1 - pos2, pos1 - pos3, pos2 - pos3]).flatten()

            guess = np.array([np.pi / 4, np.pi / 4, np.pi / 4, np.pi / 4, np.pi / 4, np.pi / 4, 0, 0, 0])

            x0 = fsolve(f, guess)
            u1, v1, u2, v2, u3, v3, _, _, _ = x0

            xyz1 = position(a1, r1, u1, v1)
            xyz2 = position(a2, r2, u2, v2)
            xyz3 = position(a3, r3, u3, v3)

            if xyz1 == [] or xyz2 == [] or xyz3 == []:
                return -1, -1, -1

            X = (xyz1[0] + xyz2[0] + xyz3[0]) / 3
            Y = (xyz1[1] + xyz2[1] + xyz3[1]) / 3
            Z = (xyz1[2] + xyz2[2] + xyz3[2]) / 3

            return int(X), int(Y), int(Z)

        return -1, -1, -1
