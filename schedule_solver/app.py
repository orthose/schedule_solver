from schedule_solver import ScheduleSolver
from flask import Flask, request, render_template

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
    slots_hours = [sl for j in range(13, 19) for sl in [f"{j}h00", f"{j}h30"]]
    return render_template(
        "index.html",
        slots_hours=slots_hours,
        objective_value=objective_value,
        affected_slots=affected_slots,
    )
