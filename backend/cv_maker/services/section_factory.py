from typing import Dict, Any
from ..models.section import (
    Section,
    SummarySection,
    EducationSection, EducationEntry,
    ExperienceSection, ExperienceEntry,
    SkillsSection, SkillEntry,
    ProjectsSection, ProjectEntry,
    CertificatesSection, CertificateEntry,
    LanguagesSection, LanguageEntry,
    AwardsSection, AwardEntry,
    PublicationsSection, PublicationEntry,
)
from ..cv_exceptions import SectionError


class SectionFactory:
    def __init__(self):
        self._registry = {
            "education": (EducationSection, EducationEntry, 'add_education'),
            "experience": (ExperienceSection, ExperienceEntry, 'add_experience'),
            "skills": (SkillsSection, SkillEntry, 'add_skill'),
            "projects": (ProjectsSection, ProjectEntry, 'add_project'),
            "certificates": (CertificatesSection, CertificateEntry, 'add_certificate'),
            "languages": (LanguagesSection, LanguageEntry, 'add_language'),
            "awards": (AwardsSection, AwardEntry, 'add_award'),
            "publications": (PublicationsSection, PublicationEntry, 'add_publication'),
        }

    def create_section(self, section_type: str, data: Dict[str, Any]) -> Section:
        if section_type == "summary":
            section_obj = SummarySection(title=data.get("title", "Summary"))
            section_obj.summary = data.get("summary_text", "")
            return section_obj

        if section_type not in self._registry:
            raise SectionError(f"Unknown section type: '{section_type}'")

        ContainerClass, EntryClass, add_method_name = self._registry[section_type]

        section_obj = ContainerClass(title=data.get("title", section_type.capitalize()))

        add_method = getattr(section_obj, add_method_name)

        for entry_data in data.get("entries", []):
            entry_obj = EntryClass.from_dict(entry_data)
            add_method(entry_obj)
        return section_obj