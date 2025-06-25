from flask import Flask, jsonify, send_file, request
from cv_maker.models.cv import PersonalInfo, CV
from cv_maker.models.section import *
from cv_maker.services.strategy_pdf import LaTeXStrategy
from cv_maker.cv_exceptions import CVException, GenerationError


app = Flask(__name__)

@app.route('/')
def home():
    return "Backend is running."

@app.route('/api/message')
def get_message():
    return jsonify({'message': 'Hello from the backend! The connection is successful.'})

@app.route('/api/generate_cv', methods=['POST'])
def generate_cv():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    try:
        personal_info_data = data.get('personal_info')
        if not personal_info_data:
            return jsonify({"error": "Missing 'personal_info' in request"}), 400

        personal_info = PersonalInfo(
            first_name=personal_info_data.get('first_name', ''),
            last_name=personal_info_data.get('last_name', ''),
            email=personal_info_data.get('email', ''),
            phone=personal_info_data.get('phone', ''),
            profession=personal_info_data.get('profession', ''),
            city=personal_info_data.get('city', ''),
            country=personal_info_data.get('country', ''),
            links=[
                link for link in [
                    personal_info_data.get('linkedin', '').strip(),
                    personal_info_data.get('github', '').strip()
                ] if link
            ]
        )
        main_cv = CV(personal_info=personal_info)

        if 'summary' in data and data['summary']:
            section = SummarySection(title="Summary")
            section.summary = data['summary']
            main_cv.add_section(section)

        if 'experience' in data:
            section = ExperienceSection(title="Experience")
            for entry_data in data.get('experience', []):
                entry = ExperienceEntry(**entry_data)
                section.add_experience(entry)
            if section.entries:
                main_cv.add_section(section)

        if 'education' in data:
            section = EducationSection(title="Education")
            for entry_data in data.get('education', []):
                entry = EducationEntry(**entry_data)
                section.add_education(entry)
            if section.entries:
                main_cv.add_section(section)

        if 'skills' in data:
            section = SkillsSection(title="Skills")
            for cat in data['skills']:
                category = cat.get('category')
                skills = cat.get('skills', [])
                for skill in skills:
                    entry = SkillEntry(name=skill, level=category)
                    section.add_skill(entry)
            if section.entries:
                main_cv.add_section(section)

        if 'projects' in data:
            section = ProjectsSection(title="Projects")
            for entry_data in data.get('projects', []):
                entry = ProjectEntry(**entry_data)
                section.add_project(entry)
            if section.entries:
                main_cv.add_section(section)

        if 'certificates' in data:
            section = CertificatesSection(title="Certifications")
            for entry_data in data.get('certificates', []):
                entry = CertificateEntry(**entry_data)
                section.add_certificate(entry)
            if section.entries:
                main_cv.add_section(section)

        if 'languages' in data:
            section = LanguagesSection(title="Languages")
            for entry_data in data.get('languages', []):
                entry = LanguageEntry(**entry_data)
                section.add_language(entry)
            if section.entries:
                main_cv.add_section(section)

        if 'awards' in data:
            section = AwardsSection(title="Awards")
            for entry_data in data.get('awards', []):
                entry = AwardEntry(**entry_data)
                section.add_award(entry)
            if section.entries:
                main_cv.add_section(section)

        output_filename = "generated_cv.pdf"
        strategy = LaTeXStrategy()
        strategy.generate(
            personal_info=main_cv.personal_info,
            sections=main_cv.sections,
            output_path=output_filename
        )

        return send_file(output_filename, as_attachment=True, download_name='cv.pdf', mimetype='application/pdf')
    
    except TypeError as e:
        return jsonify({"error": f"Invalid data structure or missing key in JSON payload: {e}"}), 400
    except GenerationError as e:
        app.logger.error(f"LaTeX Generation Error: {e}")
        return jsonify({"error": f"Failed to generate PDF. Ensure LaTeX is installed. Details: {e}"}), 500
    except CVException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')