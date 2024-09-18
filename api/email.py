from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from api.v1.serializers import AssignmentSerializer


def send_report_email(username, recipient_email, report_data, score, remark):
    mail_subject = "Your Report"

    context = {
        "report": report_data,
        "user": username,
        "score": score,
        "remark": remark
    }

    html_message = render_to_string(f"email.html", context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=mail_subject,
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    message.attach_alternative(html_message, "text/html")

    if message.send(fail_silently=False):
        return True
    else:
        return False


def format_questions(json_data):
    formatted_output = ""
    for question in json_data['questions']:
        q_text = question['question']['text']
        a_text = question['correct']
        user_text = question['text'] or "blank"

        formatted_output += f"""
        <div style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #e1e1e1;">
            <div style="font-weight: bold; color: #2c3e50; margin-bottom: 10px;">Qn: {q_text}</div>
            <div style="color: #34495e; margin-bottom: 10px;">Ans: {user_text}</div>
            <div style="color: #27ae60; font-style: italic; margin-bottom: 10px;">Correct_answer: {a_text}</div>
            <div style="color: #e74c3c;">Score: {question['score']}</div>
        </div>
        """

    return formatted_output.strip()


def send_mark_sheet(assignment, email=None, username="user"):
    serializer = AssignmentSerializer(assignment)
    results = serializer.data

    score = round(results['performance'] * 100, 0)
    if score >= 80:
        remark = "Das ist eine hervorragende Punktzahl"
    elif score >= 60:
        remark = "Du hast gut abgeschnitten, aber es gibt noch viel Raum für Verbesserungen"
    elif score >= 40:
        remark = "Faire Punktzahl. Entspann dich nicht, lies weiter, und mit Frag Abi gibt es immer Raum, sich zu verbessern"
    else:
        remark = "Das war eine unterdurchschnittliche Punktzahl, du musst dich mehr anstrengen."

    if email is None:
        return False

    return send_report_email(username, email, format_questions(results), score, remark)
