import math
import sys


try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except:
    print('usage', sys.argv[0], 'infile outfile')
    sys.exit(1)

infile = open(input_file, 'r')
outfile = open(output_file, 'w')

def rotate(x, y, a):
    c, s = math.cos(a), math.sin(a)
    return (x * c + y * s, -x * s + y * c)

def initSpher(a, f):             # расчет характеристик эллипсоида
    b = a * (1. - f)
    c = a / (1. - f)
    e2 = f * (2. - f)
    e12 = e2 / (1. - e2)
    return (b, c, e2, e12)

def cartToSpher(x, y, z):     # перевод из топографической в сферичесую систему координат
    p, azi = math.hypot(x, y), math.atan2(y, x)
    return azi, math.atan2(z, p), math.hypot(p, z)

def toTopo(lat0, lon0, h0, x, y, z, a, f):     # перевод в топографическую систему координат
    b, c, e2, e12 = initSpher(a, f)
    sin_lat = math.sin(lat0)
    n = a / math.sqrt(1. - e2 * sin_lat ** 2)
    z = z + e2 * n * sin_lat
    x, y = rotate(x, y, lon0)
    z, x = rotate(z, x, math.pi / 2. - lat0)
    z = z - (n + h0)
    x = -x
    return cartToSpher(x, y, z) 

A, F = 6378136, 1/298.25784     # характеристики земного эллипсоида по пз-90
lat_0, lon_0, h_0 = math.radians(60.0460), math.radians(27.0515), 27   # координаты точки стояния
t = -1    # дамми-переменная для времени от начала сеанса

for line in infile:
    parameters = line.split()
    if len(parameters) > 2:
        t += 1
        x, y, z = float(parameters[0]), float(parameters[1]), float(parameters[2])
        az, el, dst = toTopo(lat_0, lon_0, h_0, x, y, z, A, F)
        az, el = math.degrees(az), math.degrees(el)
        if az <0:
            az += 360
        outfile.write('%d    %5.2f    %5.2f\n' % (t, az, el))
    else:
        pass

infile.close()
outfile.close()
