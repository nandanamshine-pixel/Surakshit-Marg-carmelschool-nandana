import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from flask import Flask, render_template, request


@dataclass(frozen=True)
class RiskFactor:
    penalty: int
    focus: str
    precautions: Tuple[str, ...]
    label: str


TEXT_RISK_FACTORS: Dict[str, RiskFactor] = {
    "speeding": RiskFactor(
        penalty=35,
        focus="Speed of the vehicle and attention of driver",
        precautions=(
            "Slow down and follow speed limits",
            "Keep a safe distance from vehicles infront and behind you.",
        ),
        label="Speeding / high vehicle speed",
    ),
    "phone": RiskFactor(
        penalty=24,
        focus="Driver or pedestrian distracted",
        precautions=(
            "Avoid use of phone while walking near or on roads.",
            "Do not use phone while driving. Connect to blutooth if call is urgent",
            "Stop in a safe place before checking a device (Do not stop at turns).",
        ),
        label="Mobile phone distraction",
    ),
    "rain": RiskFactor(
        penalty=12,
        focus="Road and weather conditions",
        precautions=(
            "Reduce speed during rain.",
            "Use lights.",
            "Try not to take sharp turns",
        ),
        label="Rain / wet road",
    ),
    "fog": RiskFactor(
        penalty=13,
        focus="Road and weather conditions",
        precautions=(
            "Use low-beam lights in fog.",
            "Use headlights and drive more carefully.",
        ),
        label="Fog / low visibility",
    ),
    "night": RiskFactor(
        penalty=12,
        focus="Visibility of road users",
        precautions=(
            "Wear reflective or bright clothing at night.",
            "Use proper headlights and road-side lighting.",
        ),
        label="Night / poor lighting",
    ),
    "dark": RiskFactor(
        penalty=12,
        focus="Visibility of road users",
        precautions=(
            "Use light or headlight.",
            "Wear reflective shoes or neon outfits",
            "Slow down and look out for blind spots.",
        ),
        label="Low light conditions",
    ),
    "child": RiskFactor(
        penalty=10,
        focus="Protection of children near roads",
        precautions=(
            "Use extra caution where children are present.",
            "Reduce speed near schools and play areas.",
            "Guardians should always accompany children outside",
        ),
        label="Child near road",
    ),
    "children": RiskFactor(
        penalty=10,
        focus="Protection of children near roads",
        precautions=(
            "Be extra cautious where children are present.",
            "Reduce speed near schools and play areas.",
            "Guardians should always accompany children outside",
        ),
        label="Children near road",
    ),
    "crossing": RiskFactor(
        penalty=9,
        focus="Pedestrian crossing behavior",
        precautions=(
            "Cross only at safe points.",
            "Look both ways and confirm vehicles have stopped or slowed down or at a safe distance",
            "Look first right, then left, then again right, and then cross",
            "Look for pelican crossing i.e., pedestrian crossing sign in traffic lights",
        ),
        label="Active road crossing",
    ),
    "obstruction": RiskFactor(
        penalty=14,
        focus="Visibility of road users",
        precautions=(
            "Move to a point with clear sight before crossing.",
            "Avoid stepping out from behind parked vehicles.",
        ),
        label="Obstruction blocking view",
    ),
    "helmet": RiskFactor(
        penalty=-8,
        focus="Rider protection",
        precautions=("Well done!! Continue wearing a properly fitted helmet.",),
        label="Helmet in use",
    ),
    "seatbelt": RiskFactor(
        penalty=-8,
        focus="Passenger protection",
        precautions=("Ensure all passengers use seatbelts.",),
        label="Seatbelt in use",
    ),
}


CHECKBOX_RISK_FACTORS: Dict[str, RiskFactor] = {
    "pedestrian_present": RiskFactor(
        penalty=10,
        focus="Pedestrian protection",
        precautions=(
            "Drivers should slow down or prepare to stop for pedestrians.",
            "Cross only at safe points.",
            "Look both ways and confirm vehicles have stopped or slowed down or at a safe distance",
            "Look first right, then left, then again right, and then cross",
            "Look for pelican crossing i.e., pedestrian crossing sign in traffic lights",
        ),
        label="Pedestrian present",
    ),
    "night_poor_lighting": RiskFactor(
        penalty=14,
        focus="Visibility of road users",
        precautions=(
            "Use light or headlight.",
            "Wear reflective shoes or neon outfits",
            "Slow down and look out for blind spots.",
        ),
        label="Night / poor lighting",
    ),
    "obstruction_blocking_view": RiskFactor(
        penalty=13,
        focus="Visibility of road users",
        precautions=(
            "Choose to cross at places with clear visibility.",
            "Avoid crossing between parked or stopped vehicles.",
        ),
        label="Obstruction blocking view",
    ),
    "distracted_driver": RiskFactor(
        penalty=21,
        focus="Driver attention and behavior",
        precautions=(
            "Have full attention on road, pedestrians and signals.",
            "Do not use phone while driving. Connect to blutooth if call is urgent",
            "Stop in a safe place before checking a device (Do not stop at turns).",
        ),
        label="Distracted driver",
    ),
    "speeding_high_vehicle_speed": RiskFactor(
        penalty=35,
        focus="Vehicle speed and stopping distance",
        precautions=(
            "Slow down and follow speed limits",
            "Keep a safe distance from vehicles infront and behind you.",
        ),
        label="Speeding / high vehicle speed",
    ),
}


RISK_MESSAGES: Dict[str, str] = {
    "No risk": "No risk - Well donee!!! Continue that pace you can do it!!",
    "Low risk": "Low risk - It's ok, take precautions and stay alert.",
    "Medium risk": "Medium risk - Slow downnn! Apply the necessary precautions NOW!.",
    "High risk": "High risk - Immediately stop. Now, follow 'STOP' - Scan, Think, Observe, Proceed.",
}


def classify_risk(score: int) -> str:
    if score >= 85:
        return "No risk"
    if score >= 65:
        return "Low risk"
    if score >= 40:
        return "Medium risk"
    return "High risk"


def default_result() -> dict:
    category = "No risk"
    return {
        "score": 100,
        "category": category,
        "primary_focus": "None",
        "top_factor": "None",
        "message": RISK_MESSAGES[category],
        "precautions": ["Keep following signs and safe crossing rules."],
    }


def evaluate_scenario(text: str, selected_checks: List[str]) -> dict:
    text_lower = text.lower()
    score = 100
    focus_scores = defaultdict(int)
    precautions_scores = defaultdict(int)
    factor_scores = defaultdict(int)

    for keyword, factor in TEXT_RISK_FACTORS.items():
        if keyword in text_lower:
            score -= factor.penalty
            impact = abs(factor.penalty)
            focus_scores[factor.focus] += impact
            factor_scores[factor.label] += impact
            for item in factor.precautions:
                precautions_scores[item] += impact

    for key in selected_checks:
        factor = CHECKBOX_RISK_FACTORS.get(key)
        if factor is None:
            continue

        score -= factor.penalty
        impact = abs(factor.penalty)
        focus_scores[factor.focus] += impact
        factor_scores[factor.label] += impact
        for item in factor.precautions:
            precautions_scores[item] += impact

    score = max(0, min(100, score))
    category = classify_risk(score)

    if focus_scores:
        primary_focus = max(focus_scores.items(), key=lambda x: x[1])[0]
    else:
        primary_focus = "General road awareness"

    if factor_scores:
        top_factor = max(factor_scores.items(), key=lambda x: x[1])[0]
    else:
        top_factor = "None"

    sorted_precautions = sorted(
        precautions_scores.items(), key=lambda x: x[1], reverse=True
    )
    precautions = [item for item, _ in sorted_precautions[:5]]

    if not precautions:
        precautions = [
            "Stay alert to traffic from all directions.",
            "Use marked crossings and obey traffic signals.",
        ]

    return {
        "score": score,
        "category": category,
        "primary_focus": primary_focus,
        "top_factor": top_factor,
        "message": RISK_MESSAGES[category],
        "precautions": precautions,
    }


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        result = default_result()
        scenario_text = ""
        selected_checks: List[str] = []

        if request.method == "POST":
            scenario_text = request.form.get("scenario", "").strip()
            selected_checks = request.form.getlist("checks")
            result = evaluate_scenario(scenario_text, selected_checks)

        return render_template(
            "index.html",
            result=result,
            scenario_text=scenario_text,
            selected_checks=selected_checks,
        )

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
