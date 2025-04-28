from typing import List, Dict, Optional

# Each scenario is a dictionary with a clear structure
basic_scenarios: List[Dict] = [
    {
        "id": 1,
        "name": "Scenario 1",
        "description": "Balise p",
        "full_description": "Injection dans une balise <p> classique.",
        "category": "HTML Injection",
        "template_block": "p_block"
    },
    {
        "id": 2,
        "name": "Scenario 2",
        "description": "Attribut onmouseover",
        "full_description": "Injection dans un attribut HTML comme onmouseover.",
        "category": "Attribute Injection",
        "template_block": "onmouseover_block"
    },
    {
        "id": 3,
        "name": "Scenario 3",
        "description": "Script inline",
        "full_description": "Injection directe dans une balise <script>.",
        "category": "Script Injection",
        "template_block": "script_inline_block"
    },
    {
        "id": 4,
        "name": "Scenario 4",
        "description": "Input hidden",
        "full_description": "Injection dans un champ <input type='hidden'>.",
        "category": "Form Injection",
        "template_block": "input_hidden_block"
    },
    {
        "id": 5,
        "name": "Scenario 5",
        "description": "URL image",
        "full_description": "Injection dans le chemin de l'attribut src d'une image.",
        "category": "Attribute Injection",
        "template_block": "img_src_block"
    },
    {
        "id": 6,
        "name": "Scenario 6",
        "description": "Attribut href",
        "full_description": "Injection dans un lien <a href='...'>.",
        "category": "Attribute Injection",
        "template_block": "href_block"
    },
    {
        "id": 7,
        "name": "Scenario 7",
        "description": "Attribut src de script",
        "full_description": "Injection dans un <script src='...'>.",
        "category": "Script Injection",
        "template_block": "script_src_block"
    },
    {
        "id": 8,
        "name": "Scenario 8",
        "description": "JavaScript dans un onclick",
        "full_description": "Injection dans un attribut onclick.",
        "category": "Event Handler Injection",
        "template_block": "onclick_block"
    },
    {
        "id": 9,
        "name": "Scenario 9",
        "description": "Valeur de textarea",
        "full_description": "Injection dans le contenu d'un <textarea>.",
        "category": "Form Injection",
        "template_block": "textarea_block"
    },
    {
        "id": 10,
        "name": "Scenario 10",
        "description": "Commentaire HTML",
        "full_description": "Injection dans un <!-- commentaire -->.",
        "category": "HTML Injection",
        "template_block": "comment_block"
    },
    {
        "id": 11,
        "name": "Scenario 11",
        "description": "JSON dans script",
        "full_description": "Injection dans un objet JSON inline dans un script.",
        "category": "Script Injection",
        "template_block": "json_script_block"
    },
    {
        "id": 12,
        "name": "Scenario 12",
        "description": "Valeur de select/option",
        "full_description": "Injection dans une valeur d'option dans un <select>.",
        "category": "Form Injection",
        "template_block": "select_option_block"
    },
    {
        "id": 13,
        "name": "Scenario 13",
        "description": "Attribut style",
        "full_description": "Injection dans un attribut style (CSS inline).",
        "category": "CSS Injection",
        "template_block": "style_block"
    },
    {
        "id": 14,
        "name": "Scenario 14",
        "description": "Meta refresh",
        "full_description": "Injection dans une balise <meta http-equiv='refresh'>.",
        "category": "HTML Injection",
        "template_block": "meta_refresh_block"
    },
    {
        "id": 15,
        "name": "Scenario 15",
        "description": "Title de page",
        "full_description": "Injection dans le <title> de la page.",
        "category": "HTML Injection",
        "template_block": "title_block"
    },
    {
        "id": 16,
        "name": "Scenario 16",
        "description": "Donnée insérée en JS string",
        "full_description": "Injection dans une chaîne de caractères JS.",
        "category": "Script Injection",
        "template_block": "js_string_block"
    },
    {
        "id": 17,
        "name": "Scenario 17",
        "description": "Dataset HTML5",
        "full_description": "Injection dans un attribut data-* d'un élément.",
        "category": "Attribute Injection",
        "template_block": "dataset_block"
    },
    {
        "id": 18,
        "name": "Scenario 18",
        "description": "Table HTML",
        "full_description": "Injection dans une cellule d'un tableau HTML.",
        "category": "HTML Injection",
        "template_block": "table_cell_block"
    },
    {
        "id": 19,
        "name": "Scenario 19",
        "description": "Placeholder d'un input",
        "full_description": "Injection dans l'attribut placeholder.",
        "category": "Attribute Injection",
        "template_block": "placeholder_block"
    },
    {
        "id": 20,
        "name": "Scenario 20",
        "description": "Balise iframe",
        "full_description": "Injection dans l'attribut src d'une balise iframe.",
        "category": "HTML Injection",
        "template_block": "iframe_block"
    }
]

# Helper functions for working with scenarios
def get_scenario_by_id(scenario_id: int) -> Optional[Dict]:
    """
    Get a scenario by its ID
    
    Args:
        scenario_id: The ID of the scenario to retrieve
        
    Returns:
        The scenario dictionary or None if not found
    """
    for scenario in basic_scenarios:
        if scenario["id"] == scenario_id:
            return scenario
    return None

def get_scenarios_by_category(category: str) -> List[Dict]:
    """
    Get all scenarios in a specific category
    
    Args:
        category: The category to filter by
        
    Returns:
        A list of scenarios in the specified category
    """
    return [scenario for scenario in basic_scenarios if scenario["category"] == category]
