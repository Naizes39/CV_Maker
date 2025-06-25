from .models.cv import PersonalInfo, CV
from .models.section import *
from .services.strategy_pdf import LaTeXStrategy
from .services.section_factory import SectionFactory, SectionError
from .cv_exceptions import GenerationError, ValidationError
from typing import Optional

def ask_for_input(prompt: str, optional: bool = False) -> Optional[str]:
    prefix = "(opcjonalne) " if optional else ""
    value = input(f"{prefix}{prompt}: ").strip()
    return value if value else None

def get_personal_info() -> PersonalInfo:
    print("\n--- Krok 1: Dane Osobowe ---")
    first_name = ask_for_input("Imię")
    last_name = ask_for_input("Nazwisko")
    email = ask_for_input("Email")
    phone = ask_for_input("Telefon")
    profession = ask_for_input("Zawód / Stanowisko")
    
    links = []
    print("Podaj linki (np. do LinkedIn, GitHub). Wciśnij Enter przy pustym polu, aby zakończyć.")
    while True:
        link = ask_for_input("Link")
        if link:
            links.append(link)
        else:
            break
            
    return PersonalInfo(
        first_name=first_name, last_name=last_name, email=email,
        phone=phone, profession=profession, links=links
    )

def get_summary_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Podsumowanie'? (t/n)").lower() != 't':
        return None
    
    print("\n-- Wpisz swoje podsumowanie zawodowe --")
    summary_text = ask_for_input("Podsumowanie")
    if summary_text:
        return {"title": "Summary", "summary_text": summary_text}
    return None

def get_experience_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Doświadczenie'? (t/n)").lower() != 't':
        return None

    section_data = {"title": "Experience", "entries": []}
    while True:
        print("\n-- Nowy wpis: Doświadczenie --")
        job_title = ask_for_input("Stanowisko")
        company_name = ask_for_input("Nazwa firmy")
        start_date = ask_for_input("Data rozpoczęcia")
        end_date = ask_for_input("Data zakończenia", optional=True)
        
        responsibilities = []
        print("Podaj obowiązki (jeden na raz). Wciśnij Enter przy pustym polu, aby zakończyć.")
        while True:
            resp = ask_for_input("Obowiązek")
            if resp:
                responsibilities.append(resp)
            else:
                break
        
        if job_title and company_name and start_date:
            entry_data = {
                "job_title": job_title, "company_name": company_name,
                "start_date": start_date, "end_date": end_date, "responsibilities": responsibilities
            }
            section_data["entries"].append(entry_data)
        else:
            print("Stanowisko, nazwa firmy i data rozpoczęcia są wymagane.")
        
        if ask_for_input("Dodać kolejne doświadczenie? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def get_education_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Edukacja'? (t/n)").lower() != 't':
        return None
    section_data = {"title": "Education", "entries": []}
    while True:
        print("\n-- Nowy wpis: Edukacja --")
        university_name = ask_for_input("Nazwa uczelni")
        city = ask_for_input("Miasto")
        country = ask_for_input("Kraj")
        degree = ask_for_input("Tytuł / Poziom")
        field_of_study = ask_for_input("Kierunek studiów")
        specialization = ask_for_input("Specjalizacja", optional=True)
        start_date = ask_for_input("Data rozpoczęcia", optional=True)
        end_date = ask_for_input("Data ukończenia", optional=True)
        
        if university_name and city and country and degree and field_of_study:
            entry_data = {
                "university_name": university_name, "city": city, "country": country,
                "degree": degree, "field_of_study": field_of_study,
                "specialization": specialization, "start_date": start_date, "end_date": end_date
            }
            section_data["entries"].append(entry_data)
        else:
            print("Nazwa uczelni, miasto, kraj, tytuł i kierunek są wymagane.")

        if ask_for_input("Dodać kolejną uczelnię? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def get_skills_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Umiejętności'? (t/n)").lower() != 't':
        return None

    section_data = {"title": "Technical Skills", "entries": []}
    while True:
        print("\n-- Nowy wpis: Umiejętność --")
        category = ask_for_input("Kategoria (np. Języki programowania)")
        name = ask_for_input("Nazwa umiejętności (np. Python)")
        
        if name and category:
            entry_data = {"name": name, "level": category}
            section_data["entries"].append(entry_data)
        else:
            print("Kategoria i nazwa umiejętności są wymagane.")

        if ask_for_input("Dodać kolejną umiejętność? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def get_projects_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Projekty'? (t/n)").lower() != 't':
        return None

    section_data = {"title": "Projects", "entries": []}
    while True:
        print("\n-- Nowy wpis: Projekt --")
        name = ask_for_input("Nazwa projektu")
        end_date = ask_for_input("Data ukończenia", optional=True)
        
        technologies = []
        print("Podaj technologie (jedna na raz). Wciśnij Enter przy pustym polu, aby zakończyć.")
        while True:
            tech = ask_for_input("Technologia")
            if tech:
                technologies.append(tech)
            else:
                break

        responsibilities = []
        print("Podaj punkty opisu projektu (jeden na raz). Wciśnij Enter przy pustym polu, aby zakończyć.")
        while True:
            resp = ask_for_input("Opis")
            if resp:
                responsibilities.append(resp)
            else:
                break
        
        if name:
            entry_data = {
                "name": name, "end_date": end_date,
                "technologies": technologies, "responsibilities": responsibilities
            }
            section_data["entries"].append(entry_data)
        else:
            print("Nazwa projektu jest wymagana.")

        if ask_for_input("Dodać kolejny projekt? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def get_certificates_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Certyfikaty'? (t/n)").lower() != 't':
        return None

    section_data = {"title": "Certifications", "entries": []}
    while True:
        print("\n-- Nowy wpis: Certyfikat --")
        name = ask_for_input("Nazwa certyfikatu")
        org = ask_for_input("Organizacja wydająca")
        date = ask_for_input("Data wydania")

        if not (name and org and date):
            print("Nazwa, organizacja i data są wymagane.")
            continue
        
        entry_data = {"name": name, "issuing_organization": org, "issue_date": date}
        section_data["entries"].append(entry_data)

        if ask_for_input("Dodać kolejny certyfikat? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def get_languages_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Języki'? (t/n)").lower() != 't':
        return None

    section_data = {"title": "Languages", "entries": []}
    while True:
        print("\n-- Nowy wpis: Język --")
        lang = ask_for_input("Język")
        prof = ask_for_input("Poziom (np. Native, Fluent, C1)")

        if not (lang and prof):
            print("Język i poziom są wymagane.")
            continue
        
        entry_data = {"language": lang, "proficiency": prof}
        section_data["entries"].append(entry_data)

        if ask_for_input("Dodać kolejny język? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def get_awards_data() -> Optional[dict]:
    if ask_for_input("Czy chcesz dodać sekcję 'Nagrody'? (t/n)").lower() != 't':
        return None

    section_data = {"title": "Awards", "entries": []}
    while True:
        print("\n-- Nowy wpis: Nagroda --")
        name = ask_for_input("Nazwa nagrody")
        awarded_by = ask_for_input("Przyznana przez")
        date = ask_for_input("Data")
        description = ask_for_input("Opis", optional=True)

        if not (name and awarded_by and date):
            print("Nazwa, organizacja przyznająca i data są wymagane.")
            continue
        
        entry_data = {"name": name, "awarded_by": awarded_by, "date": date, "description": description}
        section_data["entries"].append(entry_data)

        if ask_for_input("Dodać kolejną nagrodę? (t/n)").lower() != 't':
            break
    return section_data if section_data["entries"] else None

def run_cv_creator():
    personal_info = get_personal_info()
    main_cv = CV(personal_info=personal_info)
    
    print("\n--- Krok 2: Dodawanie Sekcji ---")
    sections_to_create = {}

    section_getters = {
        "summary": get_summary_data,
        "experience": get_experience_data,
        "education": get_education_data,
        "skills": get_skills_data,
        "projects": get_projects_data,
        "certificates": get_certificates_data,
        "languages": get_languages_data,
        "awards": get_awards_data,
    }

    for section_type, getter_func in section_getters.items():
        if section_data := getter_func():
            sections_to_create[section_type] = section_data

    section_factory = SectionFactory()
    for section_type, section_data in sections_to_create.items():
        try:
            if not section_data: continue
            section = section_factory.create_section(section_type, section_data)
            main_cv.add_section(section)
        except (SectionError, ValidationError) as e:
            print(f"Błąd podczas tworzenia sekcji '{section_type}': {e}")
    
    print("\n--- Krok 3: Generowanie PDF ---")
    if not main_cv.sections:
        print("Nie dodano żadnych sekcji. Anulowano generowanie PDF.")
        return

    output_filename = ask_for_input("Podaj nazwę pliku wyjściowego (np. moje_cv.pdf)")
    if not output_filename:
        output_filename = "cv.pdf"
    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"

    strategy = LaTeXStrategy()
    try:
        strategy.generate(
            personal_info=main_cv.personal_info, 
            sections=main_cv.sections, 
            output_path=output_filename
        )
        print(f"\nCV zostało pomyślnie wygenerowane do pliku: {output_filename}")
    except (GenerationError, FileNotFoundError) as e:
        print(f"\nNiestety, wystąpił krytyczny błąd podczas generowania PDF: {e}")
        print("Upewnij się, że masz zainstalowanego LaTeX-a i wszystkie zależności.")
    except Exception as e:
        print(f"\nNiestety, wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    run_cv_creator()