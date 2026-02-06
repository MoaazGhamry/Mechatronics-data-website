def get_subject_icon(subject_name):
    """Returns a FontAwesome icon class string based on keywords in the subject name"""
    name = subject_name.lower()
    
    # Mapping of keywords to Font Awesome icon classes
    mapping = {
        'electronics': 'fas fa-microchip',
        'circuit': 'fas fa-bolt',
        'digital': 'fas fa-binary',
        'fluid': 'fas fa-water',
        'mechanics': 'fas fa-cogs',
        'machine': 'fas fa-tools',
        'manufacturing': 'fas fa-industry',
        'workshop': 'fas fa-hammer',
        'math': 'fas fa-calculator',
        'calculus': 'fas fa-square-root-alt',
        'physics': 'fas fa-atom',
        'heat': 'fas fa-fire-alt',
        'drawing': 'fas fa-drafting-compass',
        'graphic': 'fas fa-palette',
        'programming': 'fas fa-code',
        'coding': 'fas fa-terminal',
        'logic': 'fas fa-project-diagram',
        'electric': 'fas fa-plug',
        'power': 'fas fa-charging-station',
        'control': 'fas fa-sliders-h',
        'robot': 'fas fa-robot',
        'automation': 'fas fa-cog',
        'english': 'fas fa-language',
        'material': 'fas fa-cubes',
        'management': 'fas fa-tasks',
        'dynamic': 'fas fa-running',
        'static': 'fas fa-anchor',
        'thermal': 'fas fa-thermometer-half',
        'chemistry': 'fas fa-flask',
        'economy': 'fas fa-chart-line',
        'report': 'fas fa-file-signature',
    }

    for keyword, icon in mapping.items():
        if keyword in name:
            return icon
            
    # Default icons for general engineering
    return 'fas fa-graduation-cap'
