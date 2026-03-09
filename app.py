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
        focus="Vehicle speed and driver attention",
        precautions=(
            "Slow down and follow posted speed limits.",
            "Keep a safe stopping distance from vehicles.",
        ),
        label="Speeding / high vehicle speed",
    ),
    "phone": RiskFactor(
        penalty=24,
        focus="Driver or pedestrian distraction",
        precautions=(
            "Avoid phone use while walking or driving near roads.",
            "Pause in a safe place before checking a device.",
        ),
        label="Mobile phone distraction",
    ),
    "rain": RiskFactor(
        penalty=12,
        focus="Road and weather conditions",
        precautions=(
            "Reduce speed during rain.",
            "Use lights and improve following distance.",
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
            "Use lighting and reflective materials.",
            "Slow down and scan blind spots.",
        ),
        label="Low light conditions",
    ),
    "child": RiskFactor(
        penalty=10,
        focus="Protection of children near roads",
        precautions=(
            "Use extra caution where children are present.",
            "Reduce speed near schools and play areas.",
        ),
        label="Children near road",
    ),
    "children": RiskFactor(
        penalty=10,
        focus="Protection of children near roads",
        precautions=(
            "Use extra caution where children are present.",
            "Reduce speed near schools and play areas.",
        ),
        label="Children near road",
    ),
    "crossing": RiskFactor(
        penalty=9,
        focus="Pedestrian crossing behavior",
        precautions=(
            "Cross only at safe, marked, or signalized points.",
            "Look both ways and confirm vehicles have stopped.",
        ),
        label="Active road crossing",
    ),
    "obstruction": RiskFactor(
        penalty=14,
        focus="Visibility of road users",
        precautions=(
            "Move to a point with clear sight lines before crossing.",
            "Avoid stepping out from behind parked vehicles.",
        ),
        label="Obstruction blocking view",
    ),
    "helmet": RiskFactor(
        penalty=-8,
        focus="Rider protection",
        precautions=("Continue wearing a properly fitted helmet.",),
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
            "Drivers should slow down and prepare to stop for pedestrians.",
            "Pedestrians should cross only when vehicles are controlled.",
        ),
        label="Pedestrian present",
    ),
    "night_poor_lighting": RiskFactor(
        penalty=14,
        focus="Visibility of road users",
        precautions=(
            "Improve visibility using lighting or reflective items.",
            "Reduce speed and increase scanning range.",
        ),
        label="Night / poor lighting",
    ),
    "obstruction_blocking_view": RiskFactor(
        penalty=13,
        focus="Visibility of road users",
        precautions=(
            "Choose crossing points with clear visibility.",
            "Avoid crossing between parked or stopped vehicles.",
        ),
        label="Obstruction blocking view",
    ),
    "distracted_driver": RiskFactor(
        penalty=21,
        focus="Driver attention and behavior",
        precautions=(
            "Eliminate distractions while driving.",
            "Keep full attention on road users and signals.",
        ),
        label="Distracted driver",
    ),
    "speeding_high_vehicle_speed": RiskFactor(
        penalty=35,
        focus="Vehicle speed and stopping distance",
        precautions=(
            "Reduce speed immediately.",
            "Leave enough distance to stop safely.",
        ),
        label="Speeding / high vehicle speed",
    ),
}


RISK_MESSAGES: Dict[str, str] = {
    "No risk": "No risk - Continue that pace. Well done.",
    "Low risk": "Low risk - Stay alert and maintain safe behavior.",
    "Medium risk": "Medium risk - Slow down and apply precautions now.",
    "High risk": "High risk - Immediate control actions are required.",
}


def classify_risk(score: int) -> str:
    if score >= 85:
        return "High risk"
    if score >= 65:
        return "Medium risk"
    if score >= 40:
        return "Low risk"
    return "No risk"


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
