import subprocess
import os
import jinja2
from abc import ABC, abstractmethod
from typing import List
from collections import defaultdict
from ..models.cv import PersonalInfo
from ..models.section import (
    Section,
    SkillsSection,
    ExperienceEntry,
    EducationEntry,
    CertificateEntry,
    LanguageEntry,
    ProjectEntry,
    AwardEntry,
    PublicationEntry,
    SkillEntry,
)
from ..cv_exceptions import GenerationError


class OutputStrategy(ABC):
    @abstractmethod
    def generate(self, personal_info: PersonalInfo, sections: List[Section], output_path: str):
        pass


def latex_escape(value):
    s = str(value)
    s = s.replace('\\', '\\textbackslash{}')
    s = s.replace('{', '\\{')
    s = s.replace('}', '\\}')
    s = s.replace('&', '\\&')
    s = s.replace('#', '\\#')
    s = s.replace('%', '\\%')
    s = s.replace('_', '\\_')
    s = s.replace('$', '\\$')
    s = s.replace('^', '\\textasciicircum{}')
    s = s.replace('~', '\\textasciitilde{}')
    return s

class LaTeXStrategy(OutputStrategy):
    def _prepare_skills_data(self, sections: List[Section]):
        for section in sections:
            if isinstance(section, SkillsSection):
                skills_by_category = defaultdict(list)
                for entry in section.entries:
                    if entry.level:
                        skills_by_category[entry.level].append(entry.name)
                section.skills_by_category = skills_by_category

    def generate(self, personal_info: PersonalInfo, sections: List[Section], output_path: str):
        print(f"Rozpoczynam generowanie PDF przez LaTeX do pliku: {output_path}")
        self._prepare_skills_data(sections)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.dirname(script_dir)

        latex_jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            block_start_string='\\BLOCK{',
            block_end_string='}',
            variable_start_string='\\VAR{',
            variable_end_string='}',
            comment_start_string='\\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
        )
        latex_jinja_env.filters['latex_escape'] = latex_escape
        template = latex_jinja_env.get_template('cv_template.tex')
        rendered_latex = template.render(info=personal_info, sections=sections)
        temp_tex_filename = "temp_cv.tex"
        with open(temp_tex_filename, 'w', encoding='utf-8') as f:
            f.write(rendered_latex)
        print("Uruchamiam kompilator pdflatex...")
        for i in range(2):
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-format=pdf', f'-jobname={output_path.replace(".pdf", "")}', temp_tex_filename],
                capture_output=True, text=True, encoding='utf-8'
            )
        if process.returncode == 0:
            print(f"Plik PDF '{output_path}' został pomyślnie wygenerowany!")
        else:
            log_file = f"{output_path.replace('.pdf', '')}.log"
            error_message = (
                f"Błąd kompilacji LaTeX. Sprawdź plik '{log_file}' po szczegóły.\n"
                f"--- Log kompilatora LaTeX: ---\n{process.stdout}"
            )
            raise GenerationError(error_message)

        temp_files = [
            f"{output_path.replace('.pdf', '')}.aux",
            f"{output_path.replace('.pdf', '')}.log",
            f"{output_path.replace('.pdf', '')}.out",
            temp_tex_filename
        ]
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)