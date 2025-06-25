import copy
from typing import List
from datetime import datetime
from ..models.cv import CV
from ..models.section import Section, ExperienceSection

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
        experience_section = next((s for s in self.final_sections if isinstance(s, ExperienceSection)), None)

        if experience_section and n > 0:
            def get_sort_key(entry):
                if entry.end_date and entry.end_date.lower() == 'present':
                    return datetime.max
                
                date_str = entry.end_date or entry.start_date
                if date_str:
                    try:
                        return datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        return datetime.min 
                return datetime.min

            sorted_entries = sorted(experience_section.entries, key=get_sort_key, reverse=True)
            experience_section._entries = sorted_entries[:n]
        return self

    def build(self) -> List[Section]:
        return self.final_sections