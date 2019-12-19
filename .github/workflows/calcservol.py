import argparse
import os
import sys

class lists:
    def __init__(self):
        self.listvol=[]
        self.listfnd=[]
        self.listrg=[]
        self.listsid=[]
    def listoct(self, texto, varoct):
        fnd = texto.find(varoct)
        textoi = ''
        while fnd != -1:
            for i in range(8):
                textoi = textoi + texto[fnd + len(varoct) + i]
            self.listvol.append(textoi)
            textoi = ''
            self.listfnd.append(fnd)
            fnd = texto.find(varoct, fnd + 1)
        for i in range(len(self.listvol)):
            self.listvol[i] = self.listvol[i].rstrip('\n ')
        return self.listvol
    def listrgf(self, texto):
        textoj = ''
        for j in self.listfnd:
            fnd1 = texto.find('AVP: Rating-Group(432) l=12 f=-M- val=',j)
            for k in range(5):
                textoj = textoj + texto[fnd1 + len('AVP: Rating-Group(432) l=12 f=-M- val=')+k]
            self.listrg.append(textoj)
            textoj = ''
        for i in range(len(self.listrg)):
            self.listrg[i] = self.listrg[i].rstrip('\n ')
        return self.listrg
    def listsidf(self, texto):
        textoj = ''
        for j in self.listfnd:
            fnd1 = texto.find('AVP: Service-Identifier(439) l=12 f=-M- val=',j)
            for k in range(5):
                textoj = textoj + texto[fnd1 + len('AVP: Service-Identifier(439) l=12 f=-M- val=')+k]
            self.listsid.append(textoj)
            textoj = ''
        for i in range(len(self.listsid)):
            self.listsid[i] = self.listsid[i].rstrip('\n ')
        return self.listsid

def desplegar_programa(file_name):
    print('Calculando consumo del usuario por servicio en el archivo {}...'.format(file_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculador de Consumo de usuario por Servicio')
    parser.add_argument('--txt', metavar='<nombre del archivo>',
                        help='Archivo Trace en formato text', required=True)
    args = parser.parse_args()

    file_name = args.txt
    if not os.path.isfile(file_name):
        print('"{}" does not exist'.format(file_name), file=sys.stderr)
        sys.exit(-1)

    desplegar_programa(file_name)

    stream = open(file_name, "rt", encoding = "utf-8")
    texto = stream.read()
    listout = lists()
    listinp = lists()
    downl = listout.listoct(texto, "CC-Output-Octets: ")
    upl = listinp.listoct(texto, "CC-Input-Octets: ")
    rgs = listout.listrgf(texto)
    sid = listout.listsidf(texto)
    totalvollist = []
    services = []
    for i in range(len(downl)):
        totalvollist.append(int(downl[i])+int(upl[i]))
    for i in range(len(rgs)):
        if rgs[i] + sid[i] == '210850':
            services.append('VIVA-CHAT')
        elif rgs[i] + sid[i] == '2300100':
            services.append('BOLSA-MEGAS')
        elif rgs[i] + sid[i] == '210070':
            services.append('DNS')
        elif rgs[i] + sid[i] == '280010':
            services.append('FACEBOOK-ILIM')
        elif rgs[i] + sid[i] == '210450':
            services.append('VIVA-APP')
        else:
            continue
    dictservol = {}
    for i in services:
        dictservol[i]=0

    for key, val in dictservol.items():
        sumvol = 0
        for i in range(len(totalvollist)):
            if key == services[i]:
                dictservol[key] = sumvol + totalvollist[i]
                sumvol = sumvol + totalvollist[i]
    print('    SERVICIO   ','  |  ','   CONSUMO  ')
    print('------------------------------------')
    for servicio, consumo in dictservol.items():
        print(' ',servicio,(13-len(servicio))*' ',' | ', consumo/1000000 if consumo > 1000000 else consumo/1000 if consumo > 1000 else consumo, end = ' ')
        if consumo < 1000:
            print(' Bytes ')
        elif consumo < 1000000:
            print('KBytes')
        elif consumo < 100000000:
            print('MBytes')
    sys.exit(0)

