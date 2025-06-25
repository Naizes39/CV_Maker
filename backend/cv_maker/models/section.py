
from typing import Optional
from ..cv_exceptions import ValidationError, TypeValidationError, MissingDataError
import uuid

class Section:
    def __init__(self, title: str):
        self.title = title 
        self._id = uuid.uuid4()
        self._entries = []

    @property
    def id(self) -> uuid.UUID:
        return self._id
    @property
    def entries(self):
        return self._entries
    def __repr__(self) -> str:
        return f"Section(title='{self.title}', entries={len(self.entries)})"
    def add_entry(self, entry):
        self.entries.append(entry)
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, new_title: str):
        if not isinstance(new_title, str) or not new_title.strip():
            raise ValidationError("Title cannot be empty and must be a string.")
        self._title = new_title.strip()
        
        
class SummarySection(Section):
    def __init__(self, title: str = "Summary"):
        super().__init__(title)
        self.summary = ""
    def __repr__(self) -> str:
        return f"SummarySection(title='{self.title}', summary='{self.summary[:50]}...')"
    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, new_summary: str):
        if not isinstance(new_summary, str):
            raise TypeValidationError("Summary must be a string.")
        self._summary = new_summary.strip()

class EducationEntry:
    def __init__(self,
                 university_name: str,
                 city: str,
                 country: str,
                 degree: str,
                 field_of_study: str,
                 specialization: Optional[str],
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 gpa: Optional[float] = None):
        self.university_name = university_name
        self.city = city
        self.country = country
        self.degree = degree
        self.field_of_study = field_of_study
        self.specialization = specialization
        self.start_date = start_date
        self.end_date = end_date
        self.gpa = gpa
    @property
    def university_name(self) -> str:
        return self._university_name

    @university_name.setter
    def university_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("University name cannot be empty and must be a string.")
        self._university_name = value.strip()
    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("City cannot be empty and must be a string.")
        self._city = value.strip()
    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Country cannot be empty and must be a string.")
        self._country = value.strip()
    @property
    def degree(self) -> str:
        return self._degree

    @degree.setter
    def degree(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Degree cannot be empty and must be a string.")
        self._degree = value.strip()
    @property
    def field_of_study(self) -> str:
        return self._field_of_study

    @field_of_study.setter
    def field_of_study(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Field of study cannot be empty and must be a string.")
        self._field_of_study = value.strip()
    @property
    def specialization(self) -> Optional[str]:
        return self._specialization
    @specialization.setter
    def specialization(self, value: Optional[str]):
        if value is None:
            self._specialization = None
        elif not isinstance(value, str) or not value.strip():
            raise ValidationError("Specialization must be a non-empty string if provided, or None.")
        else:
            self._specialization = value.strip()


    @property
    def start_date(self) -> Optional[str]:
        return self._start_date

    @start_date.setter
    def start_date(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Start date must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("Start date, if provided, cannot be an empty string.")
            self._start_date = stripped_value
        else:
            self._start_date = None
    @property
    def end_date(self) -> Optional[str]:
        return self._end_date

    @end_date.setter
    def end_date(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("End date must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("End date, if provided, cannot be an empty string.")
            self._end_date = stripped_value
        else:
            self._end_date = None
    @property
    def gpa(self) -> Optional[float]:
        return self._gpa

    @gpa.setter
    def gpa(self, value: Optional[float]):
        if value is not None:
            if not isinstance(value, (float, int)):
                raise TypeValidationError("GPA must be a number or None.")
            if not (0.0 <= float(value) <= 5.0):
                raise ValidationError("GPA must be within a valid range (e.g., 0.0-5.0) or None.")
        self._gpa = float(value) if value is not None else None

    def __repr__(self) -> str:
        return f"EducationEntry(university='{self.university_name}', field='{self.field_of_study}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'EducationEntry':
        required_keys = ["university_name", "city", "country", "degree", "field_of_study"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for EducationEntry: {key}")
        return cls(
            university_name=data["university_name"],
            city=data["city"],
            country=data["country"],
            degree=data["degree"],
            field_of_study=data["field_of_study"],
            specialization=data.get("specialization"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            gpa=data.get("gpa")
        )

class EducationSection(Section):
    def __init__(self, title: str = "Education"):
        super().__init__(title)
    def add_education(self, entry: EducationEntry):
        if not isinstance(entry, EducationEntry):
            raise TypeValidationError("Only EducationEntry objects can be added to EducationSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"EducationSection(title='{self.title}', entries_count={len(self.entries)})"    

class ExperienceEntry:
    def __init__(self,
                 job_title: str,
                 company_name: str,
                 start_date: str,
                 end_date: Optional[str] = None,
                 city: Optional[str] = None,
                 country: Optional[str] = None,
                 responsibilities: Optional[list[str]] = None):
        self.job_title = job_title
        self.company_name = company_name
        self.start_date = start_date
        self.end_date = end_date
        self.city = city
        self.country = country
        self.responsibilities = responsibilities
    @property
    def job_title(self) -> str:
        return self._job_title

    @job_title.setter
    def job_title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Job title cannot be empty and must be a string.")
        self._job_title = value.strip()
    @property
    def company_name(self) -> str:
        return self._company_name

    @company_name.setter
    def company_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Company name cannot be empty and must be a string.")
        self._company_name = value.strip()
    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Start date cannot be empty and must be a string.")
        self._start_date = value.strip()
    @property
    def end_date(self) -> Optional[str]:
        return self._end_date

    @end_date.setter
    def end_date(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("End date must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("End date, if provided, cannot be an empty string.")
            self._end_date = stripped_value
        else:
            self._end_date = None
    @property
    def city(self) -> Optional[str]:
        return self._city

    @city.setter
    def city(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("City must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("City, if provided, cannot be an empty string.")
            self._city = stripped_value
        else:
            self._city = None
    @property
    def country(self) -> Optional[str]:
        return self._country

    @country.setter
    def country(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Country must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("Country, if provided, cannot be an empty string.")
            self._country = stripped_value
        else:
            self._country = None
    @property
    def responsibilities(self) -> list[str]:
        return self._responsibilities

    @responsibilities.setter
    def responsibilities(self, value: Optional[list[str]]):
        if value is None:
            self._responsibilities = []
        elif isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
            self._responsibilities = [item.strip() for item in value]
        elif isinstance(value, list) and not all(isinstance(item, str) and item.strip() for item in value):
            raise ValidationError("All responsibilities must be non-empty strings.")
        else:
            raise TypeValidationError("Responsibilities must be a list of strings or None.")
    def __repr__(self) -> str:
        return f"ExperienceEntry(job_title='{self.job_title}', company='{self.company_name}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'ExperienceEntry':
        required_keys = ["job_title", "company_name", "start_date"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for ExperienceEntry: {key}")
        return cls(
            job_title=data["job_title"],
            company_name=data["company_name"],
            start_date=data["start_date"],
            end_date=data.get("end_date"),
            city=data.get("city"),
            country=data.get("country"),
            responsibilities=data.get("responsibilities")
        )

class ExperienceSection(Section):
    def __init__(self, title: str = "Experience"):
        super().__init__(title)

    def add_experience(self, entry: ExperienceEntry):
        if not isinstance(entry, ExperienceEntry):
            raise TypeValidationError("Only ExperienceEntry objects can be added to ExperienceSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"ExperienceSection(title='{self.title}', entries_count={len(self.entries)})"

class SkillEntry:
    def __init__(self, name: str, level: Optional[str] = None):
        self.name = name
        self.level = level
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Skill name cannot be empty and must be a string.")
        self._name = value.strip()
    @property
    def level(self) -> Optional[str]:
        return self._level

    @level.setter
    def level(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Skill level must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("Skill level, if provided, cannot be an empty string.")
            self._level = stripped_value
        else:
            self._level = None
    def __repr__(self) -> str:
        return f"SkillEntry(name='{self.name}', level='{self.level}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'SkillEntry':
        if "name" not in data:
            raise MissingDataError("Missing required key in data for SkillEntry: name")
        return cls(name=data["name"], level=data.get("level"))

class SkillsSection(Section):
    def __init__(self, title: str = "Skills"):
        super().__init__(title)

    def add_skill(self, entry: SkillEntry):
        if not isinstance(entry, SkillEntry):
            raise TypeValidationError("Only SkillEntry objects can be added to SkillsSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"SkillsSection(title='{self.title}', entries_count={len(self.entries)})"

class CertificateEntry:
    def __init__(self,
                 name: str,
                 issuing_organization: str,
                 issue_date: str,
                 expiration_date: Optional[str] = None,
                 credential_id: Optional[str] = None,
                 credential_url: Optional[str] = None):
        self.name = name
        self.issuing_organization = issuing_organization
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.credential_id = credential_id
        self.credential_url = credential_url
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Certificate name cannot be empty and must be a string.")
        self._name = value.strip()
    @property
    def issuing_organization(self) -> str:
        return self._issuing_organization

    @issuing_organization.setter
    def issuing_organization(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Issuing organization cannot be empty and must be a string.")
        self._issuing_organization = value.strip()
    @property
    def issue_date(self) -> str:
        return self._issue_date

    @issue_date.setter
    def issue_date(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Issue date cannot be empty and must be a string.")
        self._issue_date = value.strip()
    @property
    def expiration_date(self) -> Optional[str]:
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Expiration date must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("Expiration date, if provided, cannot be an empty string.")
            self._expiration_date = stripped_value
        else:
            self._expiration_date = None
    @property
    def credential_id(self) -> Optional[str]:
        return self._credential_id

    @credential_id.setter
    def credential_id(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Credential ID must be a string or None.")
            stripped_value = value.strip()
            self._credential_id = stripped_value
        else:
            self._credential_id = None
    @property
    def credential_url(self) -> Optional[str]:
        return self._credential_url

    @credential_url.setter
    def credential_url(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Credential URL must be a string or None.")
            self._credential_url = value.strip()
        else:
            self._credential_url = None
    def __repr__(self) -> str:
        return f"CertificateEntry(name='{self.name}', organization='{self.issuing_organization}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'CertificateEntry':
        required_keys = ["name", "issuing_organization", "issue_date"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for CertificateEntry: {key}")
        return cls(
            name=data["name"],
            issuing_organization=data["issuing_organization"],
            issue_date=data["issue_date"],
            expiration_date=data.get("expiration_date"),
            credential_id=data.get("credential_id"),
            credential_url=data.get("credential_url")
        )

class CertificatesSection(Section):
    def __init__(self, title: str = "Certificates"):
        super().__init__(title)

    def add_certificate(self, entry: CertificateEntry):
        if not isinstance(entry, CertificateEntry):
            raise TypeValidationError("Only CertificateEntry objects can be added to CertificatesSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"CertificatesSection(title='{self.title}', entries_count={len(self.entries)})"

class LanguageEntry:
    def __init__(self, language: str, proficiency: str):
        self.language = language
        self.proficiency = proficiency
    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Language cannot be empty and must be a string.")
        self._language = value.strip()
    @property
    def proficiency(self) -> str:
        return self._proficiency

    @proficiency.setter
    def proficiency(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Proficiency cannot be empty and must be a string.")
        self._proficiency = value.strip()
    def __repr__(self) -> str:
        return f"LanguageEntry(language='{self.language}', proficiency='{self.proficiency}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'LanguageEntry':
        required_keys = ["language", "proficiency"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for LanguageEntry: {key}")
        return cls(language=data["language"], proficiency=data["proficiency"])

class LanguagesSection(Section):
    def __init__(self, title: str = "Languages"):
        super().__init__(title)

    def add_language(self, entry: LanguageEntry):
        if not isinstance(entry, LanguageEntry):
            raise TypeValidationError("Only LanguageEntry objects can be added to LanguagesSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"LanguagesSection(title='{self.title}', entries_count={len(self.entries)})"

class ProjectEntry:
    def __init__(self,
                 name: str,
                 responsibilities: Optional[list[str]] = None,
                 technologies: Optional[list[str]] = None,
                 url: Optional[str] = None,
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None):
        self.name = name
        self.responsibilities = responsibilities
        self.technologies = technologies
        self.url = url
        self.start_date = start_date
        self.end_date = end_date
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Project name cannot be empty and must be a string.")
        self._name = value.strip()

    @property
    def responsibilities(self) -> list[str]:
        return self._responsibilities

    @responsibilities.setter
    def responsibilities(self, value: Optional[list[str]]):
        if value is None:
            self._responsibilities = []
        elif isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
            self._responsibilities = [item.strip() for item in value]
        elif isinstance(value, list) and not all(isinstance(item, str) and item.strip() for item in value):
            raise ValidationError("All responsibilities must be non-empty strings.")
        else:
            raise TypeValidationError("Responsibilities must be a list of strings or None.")

    @property
    def technologies(self) -> list[str]:
        return self._technologies

    @technologies.setter
    def technologies(self, value: Optional[list[str]]):
        if value is None:
            self._technologies = []
        elif isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
            self._technologies = [item.strip() for item in value]
        elif isinstance(value, list) and not all(isinstance(item, str) and item.strip() for item in value):
            raise ValidationError("All technologies must be non-empty strings.")
        else:
            raise TypeValidationError("Technologies must be a list of strings or None.")
    @property
    def url(self) -> Optional[str]:
        return self._url
    @url.setter
    def url(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("URL must be a string or None.")
            self._url = value.strip()
        else:
            self._url = None
    @property
    def start_date(self) -> Optional[str]:
        return self._start_date

    @start_date.setter
    def start_date(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Start date must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("Start date, if provided, cannot be an empty string.")
            self._start_date = stripped_value
        else:
            self._start_date = None
    @property
    def end_date(self) -> Optional[str]:
        return self._end_date

    @end_date.setter
    def end_date(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("End date must be a string or None.")
            stripped_value = value.strip()
            if not stripped_value:
                raise ValidationError("End date, if provided, cannot be an empty string.")
            self._end_date = stripped_value
        else:
            self._end_date = None
    def __repr__(self) -> str:
        return f"ProjectEntry(name='{self.name}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectEntry':
        required_keys = ["name"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for ProjectEntry: {key}")
        return cls(
            name=data["name"],
            responsibilities=data.get("responsibilities"),
            technologies=data.get("technologies"),
            url=data.get("url"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date")
        )

class ProjectsSection(Section):
    def __init__(self, title: str = "Projects"):
        super().__init__(title)

    def add_project(self, entry: ProjectEntry):
        if not isinstance(entry, ProjectEntry):
            raise TypeValidationError("Only ProjectEntry objects can be added to ProjectsSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"ProjectsSection(title='{self.title}', entries_count={len(self.entries)})"

class AwardEntry:
    def __init__(self,
                 name: str,
                 awarded_by: str,
                 date: str,
                 description: Optional[str] = None):
        self.name = name
        self.awarded_by = awarded_by
        self.date = date
        self.description = description
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Award name cannot be empty and must be a string.")
        self._name = value.strip()
    @property
    def awarded_by(self) -> str:
        return self._awarded_by

    @awarded_by.setter
    def awarded_by(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Awarded by cannot be empty and must be a string.")
        self._awarded_by = value.strip()
    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Date cannot be empty and must be a string.")
        self._date = value.strip()
    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Description must be a string or None.")
            self._description = value.strip()
        else:
            self._description = None
    def __repr__(self) -> str:
        return f"AwardEntry(name='{self.name}', awarded_by='{self.awarded_by}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'AwardEntry':
        required_keys = ["name", "awarded_by", "date"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for AwardEntry: {key}")
        return cls(
            name=data["name"],
            awarded_by=data["awarded_by"],
            date=data["date"],
            description=data.get("description")
        )

class AwardsSection(Section):
    def __init__(self, title: str = "Awards"):
        super().__init__(title)

    def add_award(self, entry: AwardEntry):
        if not isinstance(entry, AwardEntry):
            raise TypeValidationError("Only AwardEntry objects can be added to AwardsSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"AwardsSection(title='{self.title}', entries_count={len(self.entries)})"

class PublicationEntry:
    def __init__(self,
                 title: str,
                 authors: list[str],
                 venue: str,
                 date: str,
                 doi_or_url: Optional[str] = None,
                 summary: Optional[str] = None):
        self.title = title
        self.authors = authors
        self.venue = venue
        self.date = date
        self.doi_or_url = doi_or_url
        self.summary = summary
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Publication title cannot be empty and must be a string.")
        self._title = value.strip()
    @property
    def authors(self) -> list[str]:
        return self._authors

    @authors.setter
    def authors(self, value: list[str]):
        if not isinstance(value, list) or not all(isinstance(author, str) and author.strip() for author in value):
            raise TypeValidationError("Authors must be a list of non-empty strings.")
        if not value:
            raise ValidationError("Authors list cannot be empty.")
        self._authors = [author.strip() for author in value]
    @property
    def venue(self) -> str:
        return self._venue

    @venue.setter
    def venue(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Venue cannot be empty and must be a string.")
        self._venue = value.strip()
    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Date cannot be empty and must be a string.")
        self._date = value.strip()
    @property
    def doi_or_url(self) -> Optional[str]:
        return self._doi_or_url

    @doi_or_url.setter
    def doi_or_url(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("DOI or URL must be a string or None.")
            self._doi_or_url = value.strip()
        else:
            self._doi_or_url = None
    @property
    def summary(self) -> Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Summary must be a string or None.")
            self._summary = value.strip()
        else:
            self._summary = None
    def __repr__(self) -> str:
        return f"PublicationEntry(title='{self.title[:30]}...', venue='{self.venue}')"
    @classmethod
    def from_dict(cls, data: dict) -> 'PublicationEntry':
        required_keys = ["title", "authors", "venue", "date"]
        for key in required_keys:
            if key not in data:
                raise MissingDataError(f"Missing required key in data for PublicationEntry: {key}")
        return cls(
            title=data["title"],
            authors=data["authors"],
            venue=data["venue"],
            date=data["date"],
            doi_or_url=data.get("doi_or_url"),
            summary=data.get("summary")
        )

class PublicationsSection(Section):
    def __init__(self, title: str = "Publications"):
        super().__init__(title)

    def add_publication(self, entry: PublicationEntry):
        if not isinstance(entry, PublicationEntry):
            raise TypeValidationError("Only PublicationEntry objects can be added to PublicationsSection.")
        self.add_entry(entry)
    def __repr__(self) -> str:
        return f"PublicationsSection(title='{self.title}', entries_count={len(self.entries)})"

class CustomSection(Section):
    def __init__(self, title: str):
        super().__init__(title)
    def __repr__(self) -> str:
        return f"CustomSection(title='{self.title}', entries_count={len(self.entries)})"