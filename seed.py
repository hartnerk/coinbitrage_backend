from coinbitrage_api.models import Alert, User

u1 = User(
    password = 'pbkdf2_sha256$260000$47gTWWDstRHN63CasbFrod$+GICg8uVLyhkpsujWemBjGwor4RaiB84eelqX00ftQM=',
    username = 'kyle',
    is_superuser =  't',
    is_active =  't',
    first_name =  '',
    last_name = '',
    email = '',
    is_staff =  't',
    date_joined =  '2021-04-14 19:13:56.339152-07'
)
u1.save()

a1 = Alert(
    user = u1,
    alert_name ="MY Frst Alert.",
    coin =  "BTC",
    threshold =  10,
    enabled = True
)
a1.save()