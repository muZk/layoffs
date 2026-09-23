"""Shared title and author treatment for report charts and their exports."""
import textwrap
AUTHOR = 'By Nicolás Gómez from trabajoremoto.cl'
TITLES = {
 'mechanisms':'Reasons attributed to layoffs',
 'all-reasons':'Reasons attributed to layoffs',
 'overlap':'How AI and other explanations overlap',
 'matrix':'Which explanations appear together?',
 'ai-mechanisms':'How sources link layoffs to AI',
 'evidence-gaps':'Announcements without a classifiable explanation',
 'hiring-distribution':'Workforce growth before the layoffs',
 'hiring-distribution-mobile':'Workforce growth before the layoffs',
 'hiring-business':'Workforce and business growth, 2019–2022',
}
def stamp(fig, name):
    # Place text outside the existing content, including legends and source notes.
    fig.canvas.draw()
    bounds = fig.get_tightbbox(fig.canvas.get_renderer())
    width, height = fig.get_size_inches()
    title = textwrap.fill(TITLES[name], width=max(26,int(width*7)))
    fig.text(bounds.x0/width, (bounds.y1+.22)/height, title,
             ha='left', va='bottom', fontsize=17 if width>6 else 15,
             fontweight='semibold', color='#252333', linespacing=1.25)
    fig.text(bounds.x0/width, (bounds.y0-.25)/height, AUTHOR,
             ha='left', va='top', fontsize=11 if width>6 else 9,
             color='#645d70')
