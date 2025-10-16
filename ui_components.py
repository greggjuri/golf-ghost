"""
UI Components - Reusable UI elements
"""
import tkinter as tk


def create_header(root, theme):
    """Create the application header"""
    header = tk.Frame(root, bg=theme.colors['accent_blue'], height=80)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    # Title area
    title_frame = tk.Frame(header, bg=theme.colors['accent_blue'])
    title_frame.pack(expand=True)
    
    # Icon/Logo
    icon_label = tk.Label(
        title_frame, text="🤖", font=('Arial', 32),
        bg=theme.colors['accent_blue'], fg='white'
    )
    icon_label.pack(side='left', padx=(0, 15))
    
    # Title and subtitle
    text_frame = tk.Frame(title_frame, bg=theme.colors['accent_blue'])
    text_frame.pack(side='left')
    
    title = tk.Label(
        text_frame, text="GOLF GHOST ANALYTICS",
        font=('Arial', 24, 'bold'),
        bg=theme.colors['accent_blue'], fg='white'
    )
    title.pack(anchor='w')
    
    subtitle = tk.Label(
        text_frame, text="AI-Powered Score Generation System",
        font=('Arial', 10),
        bg=theme.colors['accent_blue'], fg='#e0e7ff'
    )
    subtitle.pack(anchor='w')
    
    return header


def create_stat_card(parent, label, value, color, theme):
    """Create a statistics display card"""
    card = tk.Frame(
        parent, bg=theme.colors['bg_card'],
        highlightbackground=theme.colors['border'],
        highlightthickness=1
    )
    card.pack(side='left', fill='both', expand=True, padx=8)
    
    value_label = tk.Label(
        card, text=str(value),
        font=('Arial', 28, 'bold'),
        bg=theme.colors['bg_card'],
        fg=color
    )
    value_label.pack(pady=(15, 5))
    
    label_label = tk.Label(
        card, text=label,
        font=('Arial', 9),
        bg=theme.colors['bg_card'],
        fg=theme.colors['text_muted']
    )
    label_label.pack(pady=(0, 15))
    
    return card


def create_button(parent, text, command, theme, style='primary'):
    """Create a styled button"""
    styles = {
        'primary': {
            'bg': theme.colors['accent_green'],
            'active_bg': '#059669'
        },
        'secondary': {
            'bg': theme.colors['bg_secondary'],
            'active_bg': theme.colors['border']
        },
        'danger': {
            'bg': theme.colors['danger'],
            'active_bg': '#dc2626'
        }
    }
    
    style_config = styles.get(style, styles['primary'])
    fg_color = 'white' if style != 'secondary' else theme.colors['text_secondary']
    
    button = tk.Button(
        parent, text=text, command=command,
        font=('Arial', 11, 'bold'),
        bg=style_config['bg'],
        fg=fg_color,
        activebackground=style_config['active_bg'],
        activeforeground='white' if style != 'secondary' else theme.colors['text_primary'],
        relief='flat',
        padx=25, pady=12,
        cursor='hand2',
        borderwidth=0
    )
    
    return button


def create_input_field(parent, label_text, var, theme):
    """Create a labeled input field"""
    container = tk.Frame(parent, bg=theme.colors['bg_card'])
    
    label = tk.Label(
        container, text=label_text,
        font=('Arial', 9, 'bold'),
        bg=theme.colors['bg_card'],
        fg=theme.colors['text_muted']
    )
    label.pack(anchor='w', pady=(0, 5))
    
    entry = tk.Entry(
        container, textvariable=var,
        font=('Arial', 10),
        bg=theme.colors['bg_secondary'],
        fg=theme.colors['text_primary'],
        insertbackground=theme.colors['text_primary'],
        relief='flat',
        borderwidth=0
    )
    entry.pack(fill='x', ipady=8, ipadx=12)
    
    return container, entry


def create_tab_button(parent, text, command, theme, is_active=False):
    """Create a tab navigation button"""
    bg_color = theme.colors['accent_blue'] if is_active else theme.colors['bg_secondary']
    fg_color = 'white' if is_active else theme.colors['text_secondary']
    
    button = tk.Button(
        parent, text=text, command=command,
        font=('Arial', 11, 'bold'),
        bg=bg_color,
        fg=fg_color,
        activebackground=theme.colors['accent_cyan'],
        activeforeground='white',
        relief='flat',
        padx=30, pady=12,
        cursor='hand2',
        borderwidth=0
    )
    
    return button


def create_card_frame(parent, theme):
    """Create a card container"""
    card = tk.Frame(
        parent, bg=theme.colors['bg_card'],
        highlightbackground=theme.colors['border'],
        highlightthickness=1
    )
    return card


def create_section_header(parent, text, theme):
    """Create a section header label"""
    header = tk.Label(
        parent, text=text,
        font=('Arial', 12, 'bold'),
        bg=theme.colors['bg_card'],
        fg=theme.colors['text_primary']
    )
    return header
