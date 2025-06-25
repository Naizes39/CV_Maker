import copy
import uuid
from typing import List, Optional
from . import section
from ..cv_exceptions import ValidationError, TypeValidationError

class PersonalInfo:
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 email: str,
                 profession: str,
                 second_name: Optional[str] = None,
                 age: Optional[int] = None,
                 city: Optional[str] = None,
                 country: Optional[str] = None,
                 links: Optional[List[str]] = None,
                 phone: Optional[str] = None,
                 profession_level: Optional[str] = None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.profession = profession
        self.second_name = second_name
        self.age = age
        self.city = city
        self.country = country
        self.links = links if links is not None else []
        self.profession_level = profession_level

    @property
    def first_name(self) -> str:
        return self._first_name
    @first_name.setter
    def first_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("First name cannot be empty.")
        self._first_name = value.strip()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Last name cannot be empty.")
        self._last_name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str) or "@" not in value or "." not in value:
            raise ValidationError("A valid email address is required.")
        self._email = value.strip()

    @property
    def phone(self) -> Optional[str]:
        return self._phone

    @phone.setter
    def phone(self, value: Optional[str]):
        if value is not None:
            if not isinstance(value, str):
                raise TypeValidationError("Phone number must be a string or None.")
            cleaned_value = value.replace("+", "").replace("-", "").replace(" ", "")
            if not cleaned_value.isdigit():
                raise ValidationError("Phone number can only contain digits, spaces, hyphens and an optional '+' sign.")
        self._phone = value
    def __repr__(self) -> str:
        return f"PersonalInfo(name='{self.first_name} {self.last_name}', email='{self.email}')"

class CV:
    def __init__(self,
                 personal_info: PersonalInfo,
                 sections: Optional[List[section.Section]] = None):
        if not isinstance(personal_info, PersonalInfo):
            raise TypeValidationError("personal_info must be an instance of PersonalInfo class.")

        self.id = uuid.uuid4()
        self.personal_info = personal_info
        self.sections = sections if sections is not None else []
        self.dedicated_cvs: List['DedicatedCV'] = []

    def add_section(self, section_obj: section.Section):
        if not isinstance(section_obj, section.Section):
            raise TypeValidationError("Only objects inheriting from Section can be added.")
        self.sections.append(section_obj)

    def get_section_by_title(self, title: str) -> Optional[section.Section]:
        for sec in self.sections:
            if sec.title == title:
                return sec
        return None

    def remove_section_by_title(self, title: str) -> bool:
        initial_count = len(self.sections)
        self.sections = [sec for sec in self.sections if sec.title != title]
        return len(self.sections) < initial_count

    def create_dedicated_cv(self, company_name: str, job_link: str) -> 'DedicatedCV':
        dedicated = DedicatedCV(base_cv=self, company_name=company_name, job_link=job_link)
        self.dedicated_cvs.append(dedicated)
        return dedicated

    def __repr__(self) -> str:
        return (f"CV(name='{self.personal_info.first_name} {self.personal_info.last_name}', "
                f"sections={len(self.sections)})")

class DedicatedCV(CV):
    def __init__(self,
                 base_cv: CV,
                 company_name: str,
                 job_link: str):
        super().__init__(
            personal_info=copy.deepcopy(base_cv.personal_info),
            sections=copy.deepcopy(base_cv.sections)
        )

        if not company_name or not company_name.strip():
            raise ValidationError("Company name cannot be empty.")
        self.company_name = company_name
        self.job_link = job_link

    def __repr__(self) -> str:
        return (f"DedicatedCV(name='{self.personal_info.first_name}', "
                f"for='{self.company_name}', sections={len(self.sections)})")