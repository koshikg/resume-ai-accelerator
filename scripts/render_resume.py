import argparse
import os
import re
from datetime import datetime

LATEX_SPECIALS = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}',
}

def escape_latex(text: str) -> str:
    return ''.join(LATEX_SPECIALS.get(c, c) for c in text)

SECTION_HEADERS = {
    'PROFESSIONAL SUMMARY': 'summary',
    'CERTIFICATIONS': 'certifications',
    'TECHNICAL SKILLS': 'skills',
    'EXPERIENCE': 'experience',
    'EARLIER ROLES': 'earlier_roles',
    'EDUCATION': 'education',
}

def parse_data_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]

    data = {
        'headers': {},
        'summary': [],
        'certifications': [],
        'skills': {},
        'experience_roles': [],  # list of dicts: {title, company, start, end, bullets}
        'earlier_roles': [],     # list of dicts: {company, years, titles:[..]}
        'education_lines': [],
    }

    # Parse header key=value until blank line
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            break
        if line.startswith('#'):
            i += 1
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            data['headers'][k.strip()] = v.strip()
        i += 1

    current_section = None

    def start_section(name):
        return SECTION_HEADERS.get(name.strip().upper())

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line.startswith('#'):
            i += 1
            continue
        upper = line.upper()
        section_name = start_section(upper)
        if section_name:
            current_section = section_name
            i += 1
            continue

        if current_section == 'summary':
            if not line.startswith('-'):
                data['summary'].append(line)
        elif current_section == 'certifications':
            if line.startswith('- '):
                data['certifications'].append(line[2:].strip())
        elif current_section == 'skills':
            if ':' in line:
                k, v = line.split(':', 1)
                data['skills'][k.strip().upper()] = [s.strip() for s in v.split(',') if s.strip()]
        elif current_section == 'experience':
            if line.startswith('ROLE:'):
                # finalize previous role implicitly
                role_line = line[5:].strip()
                # Format: Title | Company | Start -- End
                parts = [p.strip() for p in role_line.split('|')]
                title = parts[0] if len(parts) > 0 else ''
                company = parts[1] if len(parts) > 1 else ''
                date_part = parts[2] if len(parts) > 2 else ''
                if '--' in date_part:
                    start, end = [p.strip() for p in date_part.split('--', 1)]
                else:
                    start, end = date_part, ''
                data['experience_roles'].append({'title': title, 'company': company, 'start': start, 'end': end, 'bullets': []})
            elif line.startswith('- '):
                if data['experience_roles']:
                    data['experience_roles'][-1]['bullets'].append(line[2:].strip())
        elif current_section == 'earlier_roles':
            # Company header pattern: Company Name: (YYYY--YYYY)
            m = re.match(r'^([^:]+):\s*\(([^)]+)\)', line)
            if m:
                company = m.group(1).strip()
                years = m.group(2).strip()
                data['earlier_roles'].append({'company': company, 'years': years, 'titles': []})
            elif line.startswith('- '):
                if data['earlier_roles']:
                    data['earlier_roles'][-1]['titles'].append(line[2:].strip())
        elif current_section == 'education':
            data['education_lines'].append(line)
        i += 1

    return data


def build_blocks(parsed: dict) -> dict:
    blocks = {}

    # Summary block (single \item)
    if parsed['summary']:
        summary_text = ' '.join(parsed['summary'])
        blocks['PROFESSIONAL_SUMMARY'] = f"\\item{{{escape_latex(summary_text)}}}"
    else:
        blocks['PROFESSIONAL_SUMMARY'] = '\\item{ }'

    # Certifications block (simple items for potential multi-column layout)
    cert_lines = []
    for cert in parsed['certifications']:
        cert_lines.append(f"\\item {{{escape_latex(cert)}}}")
    blocks['CERTIFICATIONS_BLOCK'] = '\n'.join(cert_lines) if cert_lines else '% No certifications'

    # Skills mapping
    def join_list(key):
            vals = parsed['skills'].get(key, [])
            if not vals:
                return ''
            return ', '.join(escape_latex(v) for v in vals)

    blocks['SKILLS_LANGUAGES'] = join_list('LANGUAGES')
    blocks['SKILLS_FRAMEWORKS'] = join_list('FRAMEWORKS')
    blocks['SKILLS_DEVOPS'] = join_list('DEVOPS TOOLS') or join_list('DEVOPS TOOLS')
    blocks['SKILLS_CLOUD_SECURITY'] = join_list('CLOUD AND SECURITY TOOLS')
    blocks['SKILLS_OTHERS'] = join_list('OTHERS')

    # Experience block
    exp_lines = []
    for role in parsed['experience_roles']:
        title = escape_latex(role['title'])
        company = escape_latex(role['company'])
        date_range = escape_latex(f"{role['start']} -- {role['end']}".strip())
        # Use compact experience-specific macros
        exp_lines.append(f"\\expProjectHeading{{\\titleItem{{{title}}} $|$ \\emph{{{company}}}}}{{{date_range}}}")
        if role['bullets']:
            exp_lines.append('\\expItemListStart')
            for b in role['bullets']:
                exp_lines.append(f"\\expItem{{{escape_latex(b)}}}")
            exp_lines.append('\\expItemListEnd')
    blocks['EXPERIENCE_BLOCK'] = '\n'.join(exp_lines) if exp_lines else '% No experience roles parsed'

    # Earlier roles block (single compact multi-line item like Technical Skills)
    if parsed['earlier_roles']:
        line_parts = []
        for employer in parsed['earlier_roles']:
            header = f"{employer['company']} ({employer['years']})" if employer['years'] else employer['company']
            roles_inline = '; '.join(employer['titles']) if employer['titles'] else ''
            if roles_inline:
                line_parts.append(f"\\titleItem{{{escape_latex(header)}}}{{: {escape_latex(roles_inline)}}}")
            else:
                line_parts.append(f"\\titleItem{{{escape_latex(header)}}}")
        # Join with line breaks; wrap in a single \item
        # Use a LaTeX line break with a small negative vertical space
        earlier_roles_compact = " \\\\[-2pt]\n        ".join(line_parts)
        blocks['EARLIER_ROLES_BLOCK'] = f"\\item{{{earlier_roles_compact}}}"
    else:
        blocks['EARLIER_ROLES_BLOCK'] = '% No earlier roles'

    # Education block
    edu_lines = []
    for line in parsed['education_lines']:
        if not line.strip():
            continue
        edu_lines.append(f"\\resumeProjectHeading{{\\titleItem{{{escape_latex(line.strip())}}}}}{{}}")
    blocks['EDUCATION_BLOCK'] = '\n'.join(edu_lines) if edu_lines else '% No education entries'

    return blocks


def apply_template(template_text: str, mapping: dict) -> str:
    out = template_text
    for k, v in mapping.items():
        out = out.replace(f"{{{{{k}}}}}", v)
    return out


def main():
    parser = argparse.ArgumentParser(description='Render LaTeX resume from template and data file.')
    parser.add_argument('--template', default='cv.tex.template', help='Path to template .tex file (default cv.tex.template)')
    parser.add_argument('--data', required=True, help='Path to structured data file ( *_data.txt )')
    parser.add_argument('--output', default='cv.tex', help='Output .tex file to generate/overwrite (default cv.tex)')
    args = parser.parse_args()

    # Resolve absolute paths
    template_path = os.path.abspath(args.template)
    data_path = os.path.abspath(args.data)
    output_path = os.path.abspath(args.output)

    if not os.path.exists(template_path):
        # fallback to legacy name
        legacy = template_path.replace('cv.tex.template', 'cv.template.tex')
        if os.path.exists(legacy):
            template_path = legacy
        else:
            raise FileNotFoundError(f'Template not found: {template_path}')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f'Data file not found: {data_path}')

    parsed = parse_data_file(data_path)
    blocks = build_blocks(parsed)

    # Header placeholder mapping
    headers = parsed['headers']
    placeholder_map = {
        'NAME': escape_latex(headers.get('NAME', '')),
        'LOCATION': escape_latex(headers.get('LOCATION', '')),
        'PHONE': escape_latex(headers.get('PHONE', '')),
        'EMAIL': escape_latex(headers.get('EMAIL', '')),
        'WEBSITE_URL': headers.get('WEBSITE', '#') or '#',
        'LINKEDIN_URL': headers.get('LINKEDIN', '#') or '#',
        'GITHUB_URL': headers.get('GITHUB', '#') or '#',
    }

    placeholder_map.update(blocks)

    with open(template_path, 'r', encoding='utf-8') as f:
        template_text = f.read()

    rendered = apply_template(template_text, placeholder_map)

    # Backup existing output if present
    if os.path.exists(output_path):
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        backup_path = output_path + f'.bak_{timestamp}'
        try:
            os.replace(output_path, backup_path)
            print(f'Backed up existing {output_path} -> {backup_path}')
        except OSError:
            print('Warning: could not backup existing output file.')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    print(f'Generated LaTeX resume: {output_path}')

if __name__ == '__main__':
    main()
