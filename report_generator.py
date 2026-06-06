import json
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

REPORTS_DIR = "reports"


def ensure_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def create_json_report(repo, scores, issues, recommendations, ai_summary=None):
    ensure_reports_dir()

    safe_name = repo.get("full_name", "report").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_name}_{timestamp}.json"
    filepath = os.path.join(REPORTS_DIR, filename)

    report_data = {
        "repository": repo,
        "scores": scores,
        "issues": [
            {
                "title": item[0],
                "level": item[1],
                "type": item[2]
            }
            for item in issues
        ],
        "recommendations": recommendations,
        "ai_summary": ai_summary,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4, ensure_ascii=False)

    return filename


def draw_wrapped_text(pdf, text, x, y, max_chars=88, line_height=15):
    words = str(text).split()
    line = ""

    for word in words:
        if len(line + " " + word) <= max_chars:
            line += " " + word
        else:
            pdf.drawString(x, y, line.strip())
            y -= line_height
            line = word

    if line:
        pdf.drawString(x, y, line.strip())
        y -= line_height

    return y


def create_pdf_report(repo, scores, issues, recommendations, ai_summary=None):
    ensure_reports_dir()

    safe_name = repo.get("full_name", "report").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_name}_{timestamp}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    pdf = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(40, y, "AI GitHub Project Reviewer Report")

    y -= 35
    pdf.setFont("Helvetica", 11)
    y = draw_wrapped_text(pdf, f"Repository: {repo.get('full_name', 'Unknown')}", 40, y)
    y = draw_wrapped_text(pdf, f"URL: {repo.get('html_url', '')}", 40, y)
    y = draw_wrapped_text(pdf, f"Language: {repo.get('language', 'Unknown')}", 40, y)
    y = draw_wrapped_text(pdf, f"License: {repo.get('license', 'Unknown')}", 40, y)
    y = draw_wrapped_text(pdf, f"Default Branch: {repo.get('default_branch', 'Unknown')}", 40, y)
    y = draw_wrapped_text(pdf, f"Created: {repo.get('created_at', 'Unknown')}", 40, y)
    y = draw_wrapped_text(pdf, f"Last Commit: {repo.get('last_commit', 'Unknown')}", 40, y)

    y -= 20
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "GitHub Metrics")

    pdf.setFont("Helvetica", 11)
    metrics = [
        f"Stars: {repo.get('stars', 0)}",
        f"Forks: {repo.get('forks', 0)}",
        f"Watchers: {repo.get('watchers', 0)}",
        f"Open Issues: {repo.get('open_issues', 0)}",
        f"Open Pull Requests: {repo.get('open_pull_requests', 0)}",
        f"Contributors: {repo.get('contributors', 0)}",
        f"Releases: {repo.get('releases', 0)}",
    ]

    for metric in metrics:
        y -= 18
        pdf.drawString(60, y, metric)

    y -= 25
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Scores")

    pdf.setFont("Helvetica", 11)
    for key, value in scores.items():
        y -= 18
        pdf.drawString(60, y, f"{key.replace('_', ' ').title()}: {value}/100")

    if ai_summary:
        y -= 25
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, y, "AI Summary")

        y -= 20
        pdf.setFont("Helvetica", 11)
        y = draw_wrapped_text(pdf, ai_summary.get("summary", ""), 60, y, max_chars=80)

        y -= 12
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(60, y, "Strengths")
        pdf.setFont("Helvetica", 11)

        for item in ai_summary.get("strengths", []):
            y -= 18
            y = draw_wrapped_text(pdf, f"- {item}", 75, y, max_chars=75)

        y -= 10
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(60, y, "Weaknesses")
        pdf.setFont("Helvetica", 11)

        for item in ai_summary.get("weaknesses", []):
            y -= 18
            y = draw_wrapped_text(pdf, f"- {item}", 75, y, max_chars=75)

    if y < 170:
        pdf.showPage()
        y = height - 50

    y -= 25
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Issues Found")

    pdf.setFont("Helvetica", 11)
    for issue in issues:
        y -= 18

        if y < 70:
            pdf.showPage()
            y = height - 50

        pdf.drawString(60, y, f"- {issue[0]} ({issue[1]})")

    y -= 25

    if y < 100:
        pdf.showPage()
        y = height - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Recommendations")

    pdf.setFont("Helvetica", 11)
    for rec in recommendations:
        y -= 18

        if y < 70:
            pdf.showPage()
            y = height - 50

        y = draw_wrapped_text(pdf, f"- {rec}", 60, y, max_chars=82)

    pdf.save()

    return filename