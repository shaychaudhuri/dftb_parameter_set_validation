from fpdf import FPDF

parameter_set = ''

pdf = FPDF()
pdf.add_page()

pdf.set_font('Arial', style='BU', size=15)
pdf.cell(200, 10, txt=f'{parameter_set} Parameter Set Report', ln=1, align='C')

E_ads = ['Eads_Au10.png', 'Eads_Au18.png', 'Eads_Au34.png', 'Eads_Au111.png']
RMSD = 'RMSD.png'

pdf.set_font('Arial', style='BU', size=10)
pdf.text(10, 25, txt='Adsorption Energies')
pdf.image(E_ads[0], x=5, y=30, w=100)
pdf.image(E_ads[1], x=108, y=30, w=100)
pdf.image(E_ads[2], x=5, y=108, w=100)
pdf.image(E_ads[3], x=108, y=108, w=100)

pdf.text(10, 195, txt='Root-Mean-Square Deviation (RMSD)')
pdf.image(RMSD, x=56.5, y=200, w=100)

pdf.output(f'{parameter_set}.pdf')
