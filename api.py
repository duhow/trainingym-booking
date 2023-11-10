import requests
import json
from datetime import datetime, timedelta

class Dias:
    lunes = 0
    martes = 1
    miercoles = 2
    jueves = 3
    viernes = 4
    sabado = 5
    domingo = 6

class Trainingym:
    base_url = "https://www.trainingymapp.com/webtouch/"
    headers = dict()
    gym = dict()
    session = requests.Session()

    @property
    def person_fullname(self):
        return " ".join([self.gym["nombreSocio"], self.gym["apellidoSocio"]]).title()

    def login(self, email, password):
        data = {
            "user": email,
            "pass": password,
            "tokenKiosko": ""
        }

        req = self.query("/api/indexs/login", json=data, method="POST")

        login = req.json()

        assert login["Result"] == 0, "failed to login?"
        assert json.loads(login.get("d")).get("baja", True) == False, "user not active?"
        centros = json.loads(login.get("d")).get("Centros", {})
        assert len(centros) >= 1, "no centers found"

        #print(centros)
        self.gym = centros[0]
        # NOTE: We are using the connect.sid cookie, not the Token.
        #self.headers["Authorization"] = "Bearer " + self.gym.get("accessToken")

    def query(self, path, json=None, data=None, method="GET", headers=dict()):
        url = self.base_url + path.lstrip("/")
        headers = {**self.headers, **headers}

        req = self.session.request(method, url,
            headers=headers,
            data=data, json=json
        )

        return req

    def query_user(self, path, referer):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": f"{self.base_url}/{referer}"
        }
        req = self.query(path, headers=headers)
        req.raise_for_status()

        return req.json()

    def parse_date(self, date):
        return datetime.strptime(date, "%Y-%m-%d")

    def parse_hour(self, hour, date=None):
        hour_parsed = datetime.strptime(hour, "%H:%M")
        if not date:
            return hour_parsed
        return date.replace(hour=hour_parsed.hour, minute=hour_parsed.minute)

    def myBookings(self):
        # aaData[], new to old, 100 entries
        return self.query_user("/api/usuarios/reservas/myBookings?noCache=0", referer="actividades")

    def getActivityGroups(self, lang: int = 6):
        return self.query_user("/api/usuarios/reservas/getActivityGroups?idLanguage={lang}&noCache=0", referer="actividades")

    def getSchedulesApp(self, start_date: str = None):
        end_days = 5
        if start_date is not None:
            raise NotImplementedError("Setting a start date is not implemented yet")

        today = datetime.now().date()

        start_date = str(today)
        end_date = str(today + timedelta(days=end_days))

        url = f"/api/usuarios/reservas/getSchedulesApp/?startDateTime={start_date}&endDateTime={end_date}&noCache=0"
        # calendar[*] dateProgram,schedules[*]
        return self.query_user(url, referer="actividades")

    def next_activities(self):
        """ Return a list of upcoming activities. Include completed today """
        today = datetime.now()
        bookings = self.myBookings()
        activities = list()

        for booking_day in bookings["aaData"]:
            day = self.parse_date(booking_day["dateProgram"])
            if day.date() < today.date():
                continue
            for data in booking_day["schedules"]:
                fulldate = self.parse_hour(data["timeStart"], day)
                activity = {
                    "id": data["id"],
                    "name": data["activity"]["name"],
                    "date": fulldate
                }
                activities.append(activity)

        return activities



# https://www.trainingymapp.com/webtouch/api/viewss/menu/usuario
# 
# https://www.trainingymapp.com/webtouch/api/ejercicios/sessionActual
# 
# https://www.trainingymapp.com/webtouch/actividades
# https://www.trainingymapp.com/webtouch/api/usuarios/reservas/getActivityGroups?idLanguage=6&noCache=0.24304466395171853
# https://www.trainingymapp.com/webtouch/api/viewss/reservas/reservashorario
# https://www.trainingymapp.com/webtouch/api/usuarios/reservas/myBookings
# https://www.trainingymapp.com/webtouch/api/usuarios/reservas/getSchedulesApp/?startDateTime=2023-11-06&endDateTime=2023-11-11&noCache=0.9027295201678431
# 
# 
# POST https://www.trainingymapp.com/webtouch/api/usuarios/reservas/bookTouch/60383865?noCache=0.55294557303735
# {"connectionClientId":""}
# POST https://www.trainingymapp.com/webtouch/api/usuarios/reservas/cancelBook/60383865?noCache=0.9921674306812154
