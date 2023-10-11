import csv

def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


rooms = read_csv('data/Public Bump - Rooms.csv')
bumpers = read_csv('data/Public Bump - Bumpers.csv')
t = read_csv('data/Public Bump - Time slots.csv')


d_gender = { "M": 1, "F": 2}
c = {"SUITE": 2, "SINGLE": 1, "DOUBLE":2, "TRIPLE": 3, "QUAD": 4}


# AJUSTAR LA PUNTAUCION DE LAS HABITACIONES A LA IDEAL
d_p = {"SUITE": 49, "SINGLE": 50, "DOUBLE": 22, "TRIPLE": 10, "QUAD": 1}

class Room:
    
    id = 0
    tipo = ''
    genero = 0  # 1 (Male), 2 (Female), 3 (Mixed)
    inquilinos = []
    capacidad = 0
    preferencias = []
    p = 0

    def __init__(self, id, tipo, capacidad):
        self.inquilinos = list()
        self.id = id
        self.tipo = tipo
        self.capacidad = capacidad
        self.p = d_p[tipo]
    
    def lleno(self):
        return self.capacidad == len(self.inquilinos)
    
    def espacio(self):
        return self.capacidad - len(self.inquilinos)
    
    def add_inquilino(self, inquilino):
        if self.lleno():
            return False
        self.inquilinos.append(inquilino)
        self.p = self.p/2
        if(self.lleno()):
            self.p = 0
        return True
    
    def set_genero(self, genero):
        g = d_gender[genero]
        if self.genero == 0:
            self.genero = g
        elif self.genero != g:
            self.genero = 3

    def toString(self):
        return f'[POINTS: {self.p}] Room {self.id} - {self.tipo} - {self.genero} - {self.espacio()} / {self.capacidad} '
    
    def __lt__(self, other):
        return self.p > other.p
    

    
class Bumper:
    id = 0
    seniority = 0

    def __init__(self, id, s):
        self.id = id
        self.seniority = s



estado = { "AVAILABLE": True, "TAKEN": False }
all_rooms = dict()

for room in rooms:
    id = room['Room']
    tipo = room['Room Type']
    gender = room['Gender']
    dn = room['Deposit Number']
    capacity = c[tipo]

    if(id in all_rooms):
        if dn == "":
            continue
        dn = int(dn)
        all_rooms[id].add_inquilino(dn)
        all_rooms[id].set_genero(gender)

    else:
        all_rooms[id] = Room(id, tipo, capacity)
        if dn != "":
            dn = int(dn)
            all_rooms[id].add_inquilino(dn)
            all_rooms[id].set_genero(gender)


coopers = list()
for bumper in bumpers:
    id = bumper['Deposit Number']
    s = bumper['Seniority']
    if s == "":
        s = 0
    s = int(s)
    coopers.append(Bumper(id, s))

d_times = dict()
for time in t:
    d_times[time['Deposit Number/Group Number']] = time['Time']


from queue import PriorityQueue

priority_queue = PriorityQueue()

for room in all_rooms.values():
    priority_queue.put((-room.p, room))


results = dict()


s = ""
for cooper in coopers:
    a_room = priority_queue.get()[1]
    s += a_room.toString() + "\n"
    a_room.add_inquilino(cooper.id)
    priority_queue.put((-a_room.p, a_room))
    results[cooper.id] = a_room



DEPOSIT_NUMBER = "27565" #CHANGE THIS VALUE

print("--------------------------------------------------------------------------")
print("PREDICTION LAUNCHED FOR " + str(DEPOSIT_NUMBER) + " DEPOSIT NUMBER")
print("--------------------------------------------------------------------------")
print(f'ROOM TYPE: {results[DEPOSIT_NUMBER].tipo} - WITH {results[DEPOSIT_NUMBER].espacio()} OF {results[DEPOSIT_NUMBER].capacidad} SPACES AVAILABLES')
print("--------------------------------------------------------------------------")
print("BUMP TIME: " + d_times[DEPOSIT_NUMBER])
print("--------------------------------------------------------------------------\n")
