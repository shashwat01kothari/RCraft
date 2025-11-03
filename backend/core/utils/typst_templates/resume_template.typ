#import "@preview/tablex:0.0.8": tablex, hlinex, vlinex

// A simple, elegant resume template for Typst.

#let heading(body) = {
  set text(1.1em, weight: "bold")
  set uppercase(true)
  set letter-spacing(0.05em)
  pad(top: 1.5em, bottom: 0.5em, body)
  line(length: 100%, stroke: 0.5pt)
}

#show heading: it => pad(bottom: 0.5em, it)

// --- Resume Content (populated by Jinja2) ---

#align(center)[
  #text(2.5em, weight: "medium")[{{ name }}]
  #v(0.5em)
  #text(0.9em)[
    {{ phone }} \
    #link("mailto:{{ email }}") \
    #link("{{ linkedin_url }}") \
    #link("{{ github_url }}")
  ]
]

// --- Sections ---

{% if summary %}
#heading("Professional Summary")
{{ summary }}
{% endif %}

{% if experience %}
#heading("Experience")
{{ experience | safe }}
{% endif %}

{% if projects %}
#heading("Projects")
{{ projects | safe }}
{% endif %}

{% if skills %}
#heading("Skills")
{{ skills }}
{% endif %}

{% if education %}
#heading("Education")
{{ education | safe }}
{% endif %}