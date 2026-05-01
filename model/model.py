from datetime import datetime

from database.DAO import DAO


class Model:
    def __init__(self):
        self._totPersone = None
        self._bestSequenza = None
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self._listEvents=DAO.getAllEvents(nerc)
        self._bestSequenza=[]
        self._totPersone=0
        self.ricorsione([], maxY, maxH, 0, 0)
        return self._bestSequenza

    def ricorsione(self, parziale, maxY, maxH, pos, parzPersone):
        # TO FILL
        if pos==len(self._listEvents):
            if parzPersone>self._totPersone:
                self._totPersone = parzPersone
                self._bestSequenza = list(parziale)

        else:
            for e in range(pos,len(self._listEvents)):
                #filtri
                if self.controlloAnno(self._listEvents[e], parziale, maxY):
                    if self.controlloOre(self._listEvents[e], parziale, maxH):
                        nuovoParzPersone=parzPersone+self._listEvents[e].customers_affected
                        parziale.append(self._listEvents[e])
                        self.ricorsione(parziale, maxY, maxH, e+1, nuovoParzPersone)
                        #backtracking
                        parziale.pop()

    def controlloOre(self, eventoCorrente, parziale, maxH):
        somma=0
        for e in parziale:
            somma+=((e.date_event_finished - e.date_event_began).total_seconds() / 3600)
        somma+=((eventoCorrente.date_event_finished-eventoCorrente.date_event_began).total_seconds() / 3600)
        if somma>int(maxH):
            return False
        return True

    def controlloAnno(self,eventoCorrente, parziale, maxY):
        listaDate=[]
        for e in parziale:
            listaDate.append(e.date_event_began.year)
            listaDate.append(e.date_event_finished.year)
        listaDate.append(eventoCorrente.date_event_began.year)
        listaDate.append(eventoCorrente.date_event_finished.year)
        if max(listaDate)-min(listaDate)>int(maxY):
            return False
        return True

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc