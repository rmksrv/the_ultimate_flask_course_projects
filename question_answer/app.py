import os

import flask
import werkzeug.security

import models
import repos
import services.users
import utils.session

SECRET_KEY_LENGTH = 24

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(SECRET_KEY_LENGTH)


@app.route("/404")
def not_found() -> str | flask.Response:
    logged_in_user = utils.session.logged_in_user(flask.session)
    return flask.render_template(
        "not_found.html",
        title="404",
        logged_in_user=logged_in_user,
    )


@app.route("/answer/<int:question_id>", methods=["GET", "POST"])
def answer(question_id: int) -> str | flask.Response:
    required_policies = [models.UserPolicies.ANSWERING_QUESTIONS]
    logged_in_user = utils.session.logged_in_user(flask.session)
    if not utils.session.is_action_allowed_for_user(logged_in_user, required_policies):
        return flask.redirect(flask.url_for("not_found"))

    answering_question = repos.question.one_of(id=question_id)
    if flask.request.method == "POST":
        answer_text = flask.request.form.get("answer-text")
        repos.question.change({"answer": answer_text}, question=answering_question)
        return flask.redirect(flask.url_for("unanswered"))

    return flask.render_template(
        "answer.html",
        title="Answer",
        logged_in_user=logged_in_user,
        question=answering_question,
    )


@app.route("/ask", methods=["GET", "POST"])
def ask() -> str | flask.Response:
    required_policies = [models.UserPolicies.ASKING_QUESTION]
    logged_in_user = utils.session.logged_in_user(flask.session)
    if not utils.session.is_action_allowed_for_user(logged_in_user, required_policies):
        return flask.redirect(flask.url_for("not_found"))

    if flask.request.method == "POST":
        question_text = flask.request.form.get("input-question-text")
        expert_id = flask.request.form.get("input-expert")
        repos.question.new(
            question=question_text,
            asking_user_id=logged_in_user.id,
            expert_id=expert_id,
        )
        return flask.redirect("/")

    experts = repos.user.all_of(role=models.UserRole.EXPERT)
    return flask.render_template(
        "ask.html",
        title="Ask",
        logged_in_user=logged_in_user,
        experts=experts,
    )


@app.route("/")
def home() -> str | flask.Response:
    answered_questions = [
        (
            answered_question,
            repos.user.one_of(id=answered_question.asking_user_id),
            repos.user.one_of(id=answered_question.expert_id)
        ) for answered_question in repos.question.all_answered_questions()
    ]

    return flask.render_template(
        "home.html",
        title="Home",
        logged_in_user=utils.session.logged_in_user(flask.session),
        answered_questions=answered_questions,
    )


@app.route("/login", methods=["GET", "POST"])
def login() -> str | flask.Response:
    if flask.request.method == "POST":
        input_name = flask.request.form.get("input-name")
        usr = repos.user.one_of(name=input_name)
        if not usr:
            return flask.render_template(
                "login.html",
                info_message=f"No such user {input_name}",
            )

        input_password = flask.request.form.get("input-password")
        if not werkzeug.security.check_password_hash(usr.password, input_password):
            return flask.render_template(
                "login.html",
                info_message=f"Wrong password",
            )

        flask.session["logged_in_user"] = usr
        return flask.redirect("/")

    return flask.render_template(
        "login.html",
        title="Log in",
        logged_in_user=utils.session.logged_in_user(flask.session),
    )


@app.route("/logout")
def logout() -> str | flask.Response:
    del flask.session["logged_in_user"]
    return flask.redirect(
        flask.url_for(
            "home",
            logged_in_user=utils.session.logged_in_user(flask.session),
        )
    )


@app.route("/question/<int:question_id>")
def question(question_id: int) -> str | flask.Response:
    current_question = repos.question.one_of(id=question_id)
    asked_by = repos.user.one_of(id=current_question.asking_user_id)
    answered_by = repos.user.one_of(id=current_question.expert_id)
    return flask.render_template(
        "question.html",
        title="Question",
        logged_in_user=utils.session.logged_in_user(flask.session),
        question=current_question,
        asked_by=asked_by,
        answered_by=answered_by,
    )


@app.route("/promote/<int:user_id>")
def promote(user_id: int) -> str | flask.Response:
    required_policies = [models.UserPolicies.PROMOTING_TO_EXPERT]
    logged_in_user = utils.session.logged_in_user(flask.session)
    if not utils.session.is_action_allowed_for_user(logged_in_user, required_policies):
        return flask.redirect(flask.url_for("not_found"))

    user_to_promote = repos.user.one_of(id=user_id)
    services.admin.promote_user_to_expert(user_to_promote)
    return flask.redirect(
        flask.url_for(
            "users",
            logged_in_user=logged_in_user,
        )
    )


@app.route("/register", methods=["GET", "POST"])
def register() -> str | flask.Response:
    if flask.request.method == "POST":
        name = flask.request.form.get("input-name")
        if services.users.is_user_with_nickname_exists(name):
            return flask.render_template(
                "register.html",
                info_message=f"Sorry, name '{name}' is already taken",
            )

        hashed_pass = werkzeug.security.generate_password_hash(
            flask.request.form.get("input-password"), method="sha256"
        )
        repos.user.new(name, hashed_pass, models.UserRole.BASIC)
        return flask.redirect(flask.url_for("home",))

    return flask.render_template(
        "register.html",
        title="Register",
        logged_in_user=utils.session.logged_in_user(flask.session),
    )


@app.route("/unanswered")
def unanswered() -> str | flask.Response:
    required_policies = [models.UserPolicies.ANSWERING_QUESTIONS]
    logged_in_user = utils.session.logged_in_user(flask.session)
    if not utils.session.is_action_allowed_for_user(logged_in_user, required_policies):
        return flask.redirect(flask.url_for("not_found"))

    unanswered_questions = []
    for unanswered_question in repos.question.all_unanswered_questions(logged_in_user.id):
        asked_by = repos.user.one_of(id=unanswered_question.asking_user_id)
        unanswered_questions.append((unanswered_question, asked_by))

    return flask.render_template(
        "unanswered.html",
        title="Unanswered",
        logged_in_user=logged_in_user,
        unanswered_questions=unanswered_questions,
    )


@app.route("/users")
def users() -> str | flask.Response:
    required_policies = [models.UserPolicies.PROMOTING_TO_EXPERT]
    logged_in_user = utils.session.logged_in_user(flask.session)
    if not utils.session.is_action_allowed_for_user(logged_in_user, required_policies):
        return flask.redirect(flask.url_for("not_found"))

    return flask.render_template(
        "users.html",
        title="Users",
        logged_in_user=logged_in_user,
        all_users=repos.user.all_of(),
    )


if __name__ == '__main__':
    app.run(debug=True)
