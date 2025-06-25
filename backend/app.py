from flask import Flask, jsonify, send_file, request
from cv_maker.models.cv import PersonalInfo, CV
from cv_maker.models.section import *
from cv_maker.services.strategy_pdf import LaTeXStrategy
from cv_maker.services.builder_cv import CVBuilder
from cv_maker.cv_exceptions import CVException, GenerationError
from cv_maker.services.section_factory import SectionFactory, SectionError


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
        personal_info_data = data.get('personal_info', {})
        if not personal_info_data:
            return jsonify({"error": "Missing 'personal_info' in request"}), 400

        links = []
        if linkedin_url := personal_info_data.pop('linkedin', None):
            if linkedin_url.strip(): links.append(linkedin_url.strip())
        if github_url := personal_info_data.pop('github', None):
            if github_url.strip(): links.append(github_url.strip())

        personal_info = PersonalInfo(**personal_info_data, links=links)
        main_cv = CV(personal_info=personal_info)

        section_factory = SectionFactory()

        sections_to_create = data.get('sections', {})

        for section_type, section_data in sections_to_create.items():
            try:
                section = section_factory.create_section(section_type, section_data)
                main_cv.add_section(section)
            except SectionError as e:
                app.logger.warning(f"Skipping unknown or invalid section type: {e}")

        builder_config = data.get('builder_config', {})
        if builder_config:
            builder = CVBuilder(base_cv=main_cv)
            if 'keep_last_n_experiences' in builder_config:
                n = builder_config['keep_last_n_experiences']
                if isinstance(n, int) and n > 0:
                    builder.keep_last_n_experiences(n)
            
            if 'remove_sections' in builder_config:
                titles_to_remove = builder_config['remove_sections']
                if isinstance(titles_to_remove, list):
                    for title in titles_to_remove:
                        builder.remove_section(title)
            final_sections = builder.build()
        else:
            final_sections = main_cv.sections

        output_filename = "generated_cv.pdf"
        strategy = LaTeXStrategy()
        strategy.generate(
            personal_info=main_cv.personal_info,
            sections=final_sections,
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