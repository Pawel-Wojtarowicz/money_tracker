from deta import Deta 


DETA_KEY = "a0mat9mq_vr6od5N9ap9h8VvnQqYMBJwgu4LtKpfh"

#initialize with deta_key
deta = Deta(DETA_KEY)

#create connection to db
db = deta.Base("monthly_reports")

def insert_periods(period, incomes, expenses, comment):
    return db.put({"key":period, "incomes":incomes, "expenses":expenses, "comment":comment})

def fetch_all_periods():
    #return to dict all periods 
    res = db.fetch()
    return res.items

def get_periods(period):
    return db.get(period)