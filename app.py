import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_babel import Babel
from datetime import datetime

app = Flask(__name__)
babel = Babel(app)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'cv')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

LANGUAGES = {
    'en': 'English',
    'uk': 'Українська'
}

SKILLS_DICT = {
    "Programming Languages/Technologies": ["Java EE/Servlets/JPA/REST", "Java/JDBC/Maven/Gradle",
                                           "Software Architecture Design/Design Patterns",
                                           "Swing", "XML/JSON", "HTML/CSS/Bootstrap", "SQL", "Python", "JavaScript",
                                           "LabView"],
    "Frameworks/Libraries": ["Spring", "Hibernate", "Lombok", "Google GRPC", "Junit", "Mockito", "Selenium (Automation)", "Robot Framework (Automation)",
                             "Flask (Python Web)"],
    "RDBMS": ["MySQL", "PostgreSQL", "C-tree"],
    "CI/CD/Version Control": ["TeamCity", "Bitbucket", "Artifactory", "GitHub"],
    "Testing Tools": ["Postman", "SoapUI", "BloomRPC"],
    "Virtualization Tools": ["Docker"],
    "Methodologies": ["Agile, Scrum"],
    "Operating Systems": ["Microsoft Windows", "Linux"],
    "Application/Web Servers": ["Tomcat"],
    "Cloud": ["Microsoft Azure", "AWS"],
    "Development Tools": ["IntelliJ IDEA", "Eclipse", "PyCharm"]
}


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(),
            'work_experience': datetime.utcnow().year - 2016}


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/switch_lang/<lang>', methods=['GET', 'POST'])
def switch_lang(lang):
    return redirect(url_for('home', lang=lang))


@app.route('/')
@app.route('/<lang>/home')
def home(lang=app.config['BABEL_DEFAULT_LOCALE']):
    sorted_skills = dict(sorted(SKILLS_DICT.items(), key=lambda x: len(x[1]), reverse=True))
    if lang == 'en':
        return render_template(template_name_or_list="index_en.html", skills=sorted_skills, lang=lang)
    else:
        return render_template(template_name_or_list="index_uk.html", skills=sorted_skills, lang=lang)


@app.route('/<lang>/certificates')
def certificates(lang=app.config['BABEL_DEFAULT_LOCALE']):
    if lang == 'en':
        return render_template(template_name_or_list="certificates_en.html", lang=lang)
    else:
        return render_template(template_name_or_list="certificates_uk.html", lang=lang)


@app.route('/<lang>/contact', methods=['GET', 'POST'])
def contact(lang=app.config['BABEL_DEFAULT_LOCALE']):
    if request.method == 'GET':
        if lang == "en":
            return render_template(template_name_or_list="contacts_en.html", lang=lang)
        else:
            return render_template(template_name_or_list="contacts_uk.html", lang=lang)


@app.route('/uploads/<name>', methods=['GET', 'POST'])
def download(name):
    file_base_path = os.path.join('static', 'cv')
    return send_from_directory(file_base_path, name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
