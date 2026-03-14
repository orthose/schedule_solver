import os
from flask import Flask, request, render_template

from schedule_solver import ScheduleSolver


START_HOUR = int(os.getenv("START_HOUR", 13))
STOP_HOUR = int(os.getenv("STOP_HOUR", 19))
START_AT_30 = bool(os.getenv("START_AT_30", 0))


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    objective_value = 0
    affected_slots = set()
    
    if request.method == "POST":
        free_slots = [
            tuple(int(i) for i in k.split("_")[1:]) for k in request.form.keys()
        ]
        print(free_slots)
        ss = ScheduleSolver(free_slots)
        ss.solve()
        print(ss.status)
        objective_value = ss.objective.value()
        affected_slots = {
            k for k, v in ss.variables_swim_slot.items() if v.roundedValue() == 1
        }

    slots_hours = [sl for j in range(START_HOUR, STOP_HOUR) for sl in [f"{j}h00", f"{j}h30"]]
    if START_AT_30:
        slots_hours = slots_hours[1:-1]

    return render_template(
        "index.html",
        slots_hours=slots_hours,
        objective_value=objective_value,
        affected_slots=affected_slots,
    )
