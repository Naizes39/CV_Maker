import copy
from typing import List, Type
from models.cv import CV
from models.section import Section, ExperienceSection

class CVBuilder:
    def __init__(self, base_cv: CV):
        self.base_cv = base_cv
        self.final_sections: List[Section] = copy.deepcopy(base_cv.sections)

    def remove_section(self, section_title: str) -> 'CVBuilder':
        self.final_sections = [
            section for section in self.final_sections if section.title != section_title
        ]
        return self

    def keep_last_n_experiences(self, n: int) -> 'CVBuilder':
        for section in self.final_sections:
            if isinstance(section, ExperienceSection):
                break
        return self
    def build(self) -> List[Section]:
        return self.final_sections