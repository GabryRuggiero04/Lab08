import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # TO FILL
        self._view._txtOut.controls.clear()
        nerc=self._view._ddNerc.value
        maxY=self._view._txtYears.value
        maxH=self._view._txtHours.value
        if nerc is None:
            self._view.create_alert("Attenzione!! Selezionare un nerc")
            return
        if maxY is "":
            self._view.create_alert("Attenzione!! Selezionare per quanti anni")
            return
        if maxH is "":
            self._view.create_alert("Attenzione!! Selezionare numero massimo di ore")
            return
        oggettoNerc = self._idMap[nerc]
        listaEventi=self._model.worstCase(oggettoNerc, maxY, maxH)
        sommaOre=0
        totPeople=0
        for e in listaEventi:
            sommaOre+=((e.date_event_finished - e.date_event_began).total_seconds() / 3600)
            totPeople+=e.customers_affected
        self._view._txtOut.controls.append(
            ft.Text(f"Tot people affected: {totPeople}"))
        self._view._txtOut.controls.append(
            ft.Text(f"Tot hours of outage: {sommaOre}"))
        listaEventi.sort(key=lambda x: x.id, reverse=True)
        for e in listaEventi:
            self._view._txtOut.controls.append(
                ft.Text(e))
        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

