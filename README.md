# Trainingym Booking

Never miss your classes again and be the first one to join!

# Setup

Create a file `config.yaml`:

```yaml
telegram: userid to message
telegram_bot: "botid:token"
email: trainingym@email.com
password: password-to-login
```

Create a file `clases.yaml`:

```yaml
lunes:
  desde: 6pm
  clases:
  - gac
  - bodypump
martes: {}
miercoles: {}
jueves: {}
viernes: {}
```

Setup a cronjob or similar suitable to your needs.

```
0 21 * * 0,1,4,5 sleep 0.6; cd /home/user/trainingym-booking; (./main.py | ./send.py)
```
