from flask import Flask, render_template, request, send_from_directory, redirect, url_for

from database import get_recent_reviews, init_db, save_review

from github_analyzer import (
    calculate_ai_readiness,
    calculate_scores,
    detect_technologies,
    generate_ai_summary,
    generate_file_distribution,
    generate_issues,
    generate_recommendations,
    generate_risk_analysis,
    get_repo_data,
)

from report_generator import create_json_report, create_pdf_report

app = Flask(__name__)
init_db()

latest_json_report = None
latest_pdf_report = None


@app.route("/", methods=["GET", "POST"])
def home():
    global latest_json_report, latest_pdf_report

    repo = None
    scores = None
    issues = None
    recommendations = None
    ai_summary = None
    technologies = None
    ai_readiness = None
    risk_analysis = None
    activity_data = None
    file_labels = None
    file_values = None
    error = None

    if request.method == "POST":
        repo_url = request.form.get("repo_url", "").strip()

        try:
            repo = get_repo_data(repo_url)
            scores = calculate_scores(repo)
            issues = generate_issues(repo)
            recommendations = generate_recommendations(repo)
            ai_summary = generate_ai_summary(repo, scores, issues, recommendations)
            technologies = detect_technologies(repo)
            ai_readiness = calculate_ai_readiness(repo, scores, technologies)
            risk_analysis = generate_risk_analysis(repo, issues)
            activity_data = repo.get("activity_data")

            file_labels, file_values = generate_file_distribution(repo)

            save_review(repo, scores)

            latest_json_report = create_json_report(
                repo,
                scores,
                issues,
                recommendations,
                ai_summary
            )

            latest_pdf_report = create_pdf_report(
                repo,
                scores,
                issues,
                recommendations,
                ai_summary
            )

        except Exception as e:
            error = str(e)

    recent_reviews = get_recent_reviews()

    return render_template(
        "index.html",
        repo=repo,
        scores=scores,
        issues=issues,
        recommendations=recommendations,
        ai_summary=ai_summary,
        technologies=technologies,
        ai_readiness=ai_readiness,
        risk_analysis=risk_analysis,
        activity_data=activity_data,
        file_labels=file_labels,
        file_values=file_values,
        recent_reviews=recent_reviews,
        latest_json_report=latest_json_report,
        latest_pdf_report=latest_pdf_report,
        token_available=bool(__import__("os").getenv("GITHUB_TOKEN")),
        error=error,
    )


@app.route("/new-review")
def new_review():
    return redirect(url_for("home"))


@app.route("/download-json/<filename>")
def download_json(filename):
    return send_from_directory("reports", filename, as_attachment=True)


@app.route("/download-pdf/<filename>")
def download_pdf(filename):
    return send_from_directory("reports", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)