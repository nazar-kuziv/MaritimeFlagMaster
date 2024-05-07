import svgutils.transform as st


def merge_svg_files(input_file1, input_file2, output_file):
    svg1 = st.fromfile('graphics/flags/letters/' + input_file1)
    svg2 = st.fromfile('graphics/flags/letters/' + input_file2)
    new = st.SVGFigure(1220, 600)
    new2 = st.SVGFigure(1220, 600)
    new.append(svg1)
    new2.append(svg2)
    new2 = new2.getroot()
    new2.moveto(620, 0)
    new.append(new2)
    new.save('graphics/flags/multiple/' + output_file)


def merge_svg_files_3(input_file1, input_file2, input_file3, output_file):
    svg1 = st.fromfile('graphics/flags/letters/' + input_file1)
    svg2 = st.fromfile('graphics/flags/letters/' + input_file2)
    # svg3 = st.fromfile('graphics/flags/letters/' + input_file3)
    svg3 = st.fromfile('graphics/flags/digits/' + input_file3)
    new = st.SVGFigure(1840, 600)
    new2 = st.SVGFigure(1220, 600)
    new3 = st.SVGFigure(1840, 600)
    new.append(svg1)
    new2.append(svg2)
    new2 = new2.getroot()
    new2.moveto(620, 0)
    new3.append(svg3)
    new3 = new3.getroot()
    new3.moveto(1240, 150)
    # new3.moveto(1240, 0)
    new.append(new2)
    new.append(new3)
    new.save('graphics/flags/multiple/' + output_file)


merge_svg_files('Delta.svg', 'X-ray.svg', 'DX.svg')
# merge_svg_files_3('Uniform.svg', 'Sierra.svg', '4.svg', 'US4.svg')
